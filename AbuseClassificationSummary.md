# Initial Email Classification Testing

## Summary

I featurized the JPL Abuse email data set into counts per email of the top 2000 words from the set and counts of some other email features like attachment extensions and number of email addresses. I then ran this data through five kfold splits for each of four classification methods (linear SVC, random forest, KNN, naive bayes) to classify into slightly modified JPL abuse categories. Precision and recall values were best for random forest and linear SVC (low- to mid-90s), with KNN and naive bayes resulting in lower accuracy. With tweaking of model parameters, improvement of the featurization and more data, we should be able to improve on this baseline model performance.

## Details

### Featurization

In addition to counts of the most frequent words in the Abuse data set, the features include:
 * Number of JPL email addresses present
 * Number of non-JPL email addresses present
 * Number of characters and words in the email subject
 * Number of attachments and count of each attachment extension present in the dataset in the email

### Model Results

Each model was run with the default scikit-learn settings. I dropped the "Unknown" category from the JPL Abuse set, and combined the "Spear Phishing" and "Phishing Training" categories into one Phishing category. Results below are typical/median results from the kfolds, not actual averages of the different runs.

#### Naive Bayes

Confusion matrix

| 49 | 28 |  6 |  0 |  8 |  3 | 23 |
| 11 | 463 |  24 |  8 | 23 | 30 | 26 |
| 1 | 44 | 969 |  0 | 15 | 30 | 29  |
| 0 |  4 |  0 | 46 |  3 |  1 |  2  |
| 0 |  9 |  1 |  0 | 22 |  1 |  1  |
| 0 | 28 |  5 |  1 | 11 | 190 |  9  |
| 0 | 10 |  2 |  0 |  3 |  5 | 273  |

Accuracy measures

category 	precision  recall  f1-score  support 

Not Spam  	0.80  0.42  0.55  117 
Malware  	0.79  0.79  0.79  585 
Phishing  	0.96  0.89  0.93  1088 
Propaganda	0.84  0.82  0.83  56 
Recon  		0.26  0.65  0.37  34 
Social Eng	0.73  0.78  0.75  244 
Spam  		0.75  0.93  0.83  293 

micro avg   0.83  0.83  0.83  2417
macro avg   0.73  0.75  0.72  2417
weighted avg   0.85  0.83  0.84  2417

#### K Nearest Neighbors

Confusion matrix

[[ 84   9   6   0   1   0   1]
 [  2 602   8   0   1  16   0]
 [  1  88 994   0   0   8   2]
 [  0   6   0  48   0   1   0]
 [  0  17   0   0  16   1   0]
 [  0 109  14   1   2 113   2]
 [  2  89  16   1   1  10 145]]

Accuracy measures

category  	precision  recall  f1-score  support 

Not Spam  	0.94  0.83  0.88  101 
Malware  	0.65  0.96  0.78  629 
Phishing  	0.96  0.91  0.93  1093 
Propaganda	0.96  0.87  0.91  55 
Recon  		0.76  0.47  0.58  34 
Social Eng	0.76  0.47  0.58  241 
Spam  		0.97  0.55  0.70  264 

micro avg   0.83  0.83  0.83  2417
macro avg   0.86  0.72  0.77  2417
weighted avg   0.86  0.83  0.82  2417

#### Linear SVC

Confusion matrix

| 92 | 5   | 2    | 0  | 1  | 1   | 3   |
| 8  | 547 | 4    | 2  | 7  | 22  | 6   |
| 3  | 6   | 1091 | 1  | 3  | 10  | 2   |
| 1  | 2   | 0    | 51 | 2  | 2   | 1   |
| 0  | 3   | 1    | 0  | 28 | 1   | 0   |
| 1  | 27  | 9    | 1  | 2  | 203 | 3   |
| 2  | 26  | 7    | 1  | 3  | 3   | 221 |

Accuracy measures

category  	precision  recall  f1-score  support 

Not Spam  	0.86  0.88  0.87  104 
Malware  	0.89  0.92  0.90  596 
Phishing  	0.98  0.98  0.98  1116 
Propaganda	0.91  0.86  0.89  59 
Recon  		0.61  0.85  0.71  33 
Social Eng	0.84  0.83  0.83  246 
Spam  		0.94  0.84  0.89  263 

micro avg   0.92  0.92  0.92  2417
macro avg   0.86  0.88  0.87  2417
weighted avg   0.93  0.92  0.92  2417

#### Random Forest

Confusion matrix

[[ 91    4    3   0   0    0    1]
 [  2  609   10   0   0    4    4]
 [  1   18 1073   0   0    6    7]
 [  0    7    0  41   0    0    2]
 [  0    8    0   0  23    1    0]
 [  1   37    7   1   0  204    6]
 [  0   14    7   0   0    2  223]]

Accuracy measures

category	precision  recall  f1-score  support 

Not Spam	0.96  0.92  0.94  99 
Malware		0.87  0.97  0.92  629 
Phishing	0.98  0.97  0.97  1105 
Propaganda	0.98  0.82  0.89  50 
Recon  		1.00  0.72  0.84  32 
Social Eng	0.94  0.80  0.86  256 
Spam  		0.92  0.91  0.91  246 

micro avg   0.94  0.94  0.94  2417
macro avg   0.95  0.87  0.90  2417
weighted avg   0.94  0.94  0.94  2417
