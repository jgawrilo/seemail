from flask import Flask, request, send_from_directory,redirect, url_for

import redis
import json

# set the project root directory as the static folder, you can set others.
app = Flask(__name__, static_url_path='')


@app.route('/html/<path:path>')
def send_js(path):
    return send_from_directory('html', path)

@app.route('/add', methods=['POST']) 
def foo():
    server = request.form.get('server')
    user = request.form.get('user')
    password = request.form.get('password')
    print(password)
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    thing = json.dumps({"server":server,"user":user,"password":password})
    r.set(thing,1)
    return redirect('localhost:8000/html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)