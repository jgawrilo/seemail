# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""The Python implementation of the gRPC route guide server."""

from concurrent.futures import ThreadPoolExecutor
from concurrent import futures
import time
import math

import grpc

import collector_pb2
import collector_pb2_grpc

import healthcheck_pb2_grpc
import healthcheck_pb2

import random
import time

import manager_pb2
import manager_pb2_grpc
import sys
from datetime import datetime, timedelta

from multiprocessing.pool import ThreadPool
from threading import Timer

import threading

import redis

import json
import requests

from rq import Queue

from requests.exceptions import ReadTimeout
import logging

sys.path.append('/root/mailinabox/management/')
sys.path.append('/home/rosteen/seemail/server_stub/swagger_server/controllers/')
import default_controller
#import server_code.default_controller as default_controller

# Important directories
mail_home = '/home/user-data/mail'
seemail_path = '/home/rosteen/seemail'


_ONE_YEAR_IN_SECONDS = 60 * 60 * 24 * 365


class Seemail_Collector(collector_pb2_grpc.CollectorServicer, healthcheck_pb2_grpc.HealthServicer):


  def __init__(self,conf,rerun):
    logging.info("Initializing Seemail Collection Server...")

    self.red = redis.StrictRedis(host=conf["redis_url"], port=conf["redis_port"], db=9)
    self.tokenred = redis.StrictRedis(host=conf["redis_url"], port=conf["redis_port"], db=10)
    jobred = redis.StrictRedis(host=conf["redis_url"], port=conf["redis_port"], db=11)
    self.q = Queue(connection=jobred)

    self.conf = conf


  def _validate_name(self, request):
    logging.info("_validate_name -> ")

    #TODO: ensure asked for email address is actually in system
    #TODO: return collector_pb2.TaskResponse(rule=request,error=collector_pb2.TaskResponse.INVALID_VALUE) if bad

    email_address = self._email_from_request(request)

    if email_address:
      all_users = default_controller.get_all_users()
      email_addresses = [user["email_address"] for user in all_users]
      if email_address not in email_addresses:
        logging.info(request.id + " -- " + request.entity.name + " is not valid")
        return collector_pb2.TaskResponse(rule=request,error=collector_pb2.TaskResponse.INVALID_VALUE)

      response = collector_pb2.TaskResponse(rule=request,
          error=collector_pb2.TaskResponse.NONE)

      logging.info(request.id + " -- " + request.entity.name + " is valid:")

      return collector_pb2.TaskResponse(rule=request,
                error=collector_pb2.TaskResponse.NONE)

    return collector_pb2.TaskResponse(rule=request,error=collector_pb2.TaskResponse.INVALID_VALUE)

  def _email_from_request(self, request):
    if type(request.entity.id) == str:
      if re.search("@", request.entity.id) is not None:
        return request.entity.id
    else:
      if re.search("@", request.entity.name) is not None:
        return request.entity.name
    logging.error("Request does not appear to contain an email address in id or name")
    return None

  def Check(self, request, context):
    logging.info("\n\nCheck -> ")
    return healthcheck_pb2.HealthCheckResponse(status=healthcheck_pb2.HealthCheckResponse.SERVING)

  def ValidateRule(self, request, context):
    logging.info("\n\nValidateRule -> ")
    logging.info(request)

    return self.validate_name(request)

    #TODO: Validate multiple rules

  def _start_rule(self,request):
    logging.info("_start_rule ->")
    logging.info(request)

    if self.red.get(request.id):
      logging.error("Request ID Already Made")
      return collector_pb2.TaskResponse(rule=request,
          error=collector_pb2.TaskResponse.NONE)

    # RGO - Change this to email address?
    # ENTITY REQUEST - name
    email_address = self._email_from_request(request)
    if email_address:
      logging.info("Firing Entity Info: " + request.id + " " + request.entity.name)

      # Check to see if user already being watched
      users_r = redis.StrictRedis(host='localhost', port=6379, db=1)
      user_found = False
      for key in users_r.scan_iter():
          if key == email_address.encode('utf-8'):
              user_found = True
              break

      # Get the user's email history if they were not already being watched
      if not user_found:
          # This sends the email throught he history kafka queue
          logging.info("Sending user email history to history queue")
          res = default_controller.request_mail_history_get([email_address],
                  request_key, 350000000)
          res = default_controller.monitor_users_get([email_address])

      # Otherwise return that we already were watching the user
      else:
          logging.info("User email was already being monitored")

      # self.q.enqueue(utils.process_entity,args=(
      #   self.access_tokens,
      #   request.id,
      #   request.entity.name,
      #   self.conf["kafka"],
      #   self.conf["kafka_topic"],
      #   None,
      #   self.conf["use_tor"],
      #   start
      #   ),
      #   timeout=_ONE_YEAR_IN_SECONDS,
      #   at_front = True
      # )
      return collector_pb2.TaskResponse(rule=request,
          error=collector_pb2.TaskResponse.NONE)


    logging.error("Collection type caused a fall through.")
    return collector_pb2.TaskResponse(rule=request,
      error=collector_pb2.TaskResponse.INVALID_VALUE)

  def StartRule(self, request, context):
    logging.info("\n\nStartRule -> ")
    return self._start_rule(request)

  def _stop_rule(self,request):
    logging.info("_stop_rule ->")
    logging.info(request)
    self.red.delete(request.id)

    email_address = self._email_from_request(request)
    # Remove user from list of email addresses to monitor
    if email_address:
      res = default_controller.unmonitor_users_get(email_address)
      return collector_pb2.TaskResponse(rule=request,
        error=collector_pb2.TaskResponse.NONE)

    # Return error if there was no email address in request
    return collector_pb2.TaskResponse(rule=request,
        error=collector_pb2.TaskResponse.INVALID_VALUE)

  def StopRule(self, request, context):
    logging.info("\n\nStopRule -> ")
    return self._stop_rule(request)


  def ValidateRules(self, request, context):
    logging.info("\n\nValidateRules -> ")
    logging.info(request)

    responses = [None] * len(request.rules)

    logging.info(responses)
    return collector_pb2.TaskResponses(responses=responses)

  def StartRules(self, request, context):
    logging.info("\n\nStartRules -> ")
    responses = [self._start_rule(x) for x in request.rules]
    logging.info(responses)
    return collector_pb2.TaskResponses(responses=responses)

  def StopRules(self, request, context):
    logging.info("\n\nStopRules -> ")
    responses = [self._stop_rule(x) for x in request.rules]
    return collector_pb2.TaskResponses(responses=responses)

def register_collector(conf, credentials):
  #channel = grpc.insecure_channel(conf["manager"])
  channel = grpc.secure_channel(conf["manager"], credentials)
  stub = manager_pb2_grpc.ManagerStub(channel)
  d = manager_pb2.RegistrationInfo(uri=conf["collector_url"],
      network=manager_pb2.VK,
      collection_types=[manager_pb2.ENTITY,manager_pb2.KEYWORD],
      collection_modes=[manager_pb2.POLLING]
    )
  resp = stub.Register(d)
  logging.info("Registered Collector.")
  time.sleep(60)

  resp = stub.Initialize(d)
  logging.info("Initialized Collector.")

def unregister_collector(conf):
  channel = grpc.insecure_channel(conf["manager"])
  stub = manager_pb2_grpc.ManagerStub(channel)
  d = manager_pb2.RegistrationInfo(uri=conf["collector_url"],
      network=manager_pb2.VK,
      collection_types=[manager_pb2.ENTITY,manager_pb2.KEYWORD],
      collection_modes=[manager_pb2.POLLING]
    )
  resp = stub.Unregister(d)
  logging.info("Unregistered Collector.")

def start_collector(conf, rerun):
  logging.basicConfig(filename=conf["log_file"],level=logging.INFO,format='%(asctime)s %(message)s')
  logging.info("Starting Collector.")

  # Retrieve SSL certificate
  with open('server.key', 'rb') as f:
    private_key = f.read()
  with open('server.crt', 'rb') as f:
    certificate_chain = f.read()
  server_credentials = grpc.ssl_server_credentials(((private_key, certificate_chain,),))

  server = grpc.server(futures.ThreadPoolExecutor(max_workers=3))

  my_collector = Seemail_Collector(conf,rerun)
  collector_pb2_grpc.add_CollectorServicer_to_server(my_collector, server)
  healthcheck_pb2_grpc.add_HealthServicer_to_server(my_collector, server)

  #server.add_insecure_port('[::]:50051')
  server.add_secure_port('[::]:50051', server_credentials)
  server.start()

  logging.info("Collector Started")

  # Just because
  time.sleep(2)

  try:
    channel_credentials = grpc.ssl_channel_credentials(root_certificates=certificate_chain)
    register_collector(conf, channel_credentials)
  except grpc._channel._Rendezvous:
    logging.error("Something wrong with endpoint?")
    sys.exit(1)
  
  try:
    while True:
      time.sleep(_ONE_YEAR_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  if len(sys.argv) < 3:
    print("Please specify config file and 'R' (register) or 'U' (unregister) on the command line")
    sys.exit(1)



  conf = json.load(open(sys.argv[1]))
  if sys.argv[2] == "R":
    start_collector(conf, sys.argv[3])
  elif sys.argv[2] == "U":
    unregister_collector(conf)

