## Tasks

##### Completed
<li> Read propagation paths from database as a variable length sequence
<li> Transform propagation paths to fixed length sequences
<li> RNN-based propagation path representation, 
<li> CNN-based propagation path representation
<li> Propagation path classification


##### Todo
<li>Adjust data
<li>Train model with extracted timeline based features
<li>Write the paper



## Definitions

**UserVector** represts the characteristics of each user

**PropagationPath** is defined as a *variable length multivarient tim Te series* P(ai) = (...,(xj , t),...), in which each tuple (xj , t) denotes that user uj tweets/retweets the news story ai at time t. we set the time of a source tweet being posted to 0. Thus, t > 0 refers to the time of a retweet being posted.

**GroundTruth** Each news story ai is associatedwith a label L(ai) that reflects its truthfulness. Each label L(ai) ∈ {0, 1}r. When r = 1, L(ai)=0 denotes the news
story ai is *true*, and L(ai)=1 denotes ai is *fake*.

**PartialPropagationPath** of a given news story ai as
P(ai, T) = ((xj ,t < T)), where T is a *detection deadline* after which all the observed data cannot be used in detecting fake news.

## Database Object Structure

GET tweets.cascades

```json
{"_id":{"$oid":"611a751f136ce8c98ad4c242"},"node_sequence":[{"$numberLong":"1379138530841034752"},{"$numberLong":"3400400919"},{"$numberLong":"1353500664299663361"},{"$numberLong":"1308829799977086977"}],"ground_truth":false,"node_feature_sequence":[{"user_id":{"$numberLong":"1379138530841034752"},"emotional_frequency":{"fear":0,"anger":0,"anticipation":0.1294642857142857,"trust":0.25,"surprise":0,"positive":0.4,"negative":0.12708333333333333,"sadness":0,"disgust":0,"joy":0},"emotional_mean":{"fear":0,"anger":0,"anticipation":0.1294642857142857,"trust":0.25,"surprise":0,"positive":0.4,"negative":0.12708333333333333,"sadness":0,"disgust":0,"joy":0},"emotional_std":{"fear":0,"anger":0,"anticipation":0.1294642857142857,"trust":0.25,"surprise":0,"positive":0.4,"negative":0.12708333333333333,"sadness":0,"disgust":0,"joy":0},"emotional_q1":{"fear":0,"anger":0,"anticipation":0.1294642857142857,"trust":0.25,"surprise":0,"positive":0.4,"negative":0.12708333333333333,"sadness":0,"disgust":0,"joy":0},"emotional_q2":{"fear":0,"anger":0,"anticipation":0.1294642857142857,"trust":0.25,"surprise":0,"positive":0.4,"negative":0.12708333333333333,"sadness":0,"disgust":0,"joy":0},"emotional_q3":{"fear":0,"anger":0,"anticipation":0.1294642857142857,"trust":0.25,"surprise":0,"positive":0.4,"negative":0.12708333333333333,"sadness":0,"disgust":0,"joy":0},"followers_count":91137,"friends_count":0,"listed_count":186,"statuses_count":163,"created_at":"Mon Apr 05 18:27:20 +0000 2021"},{"user_id":{"$numberLong":"3400400919"},"emotional_frequency":{"fear":0.014705882352941176,"anger":0,"anticipation":0,"trust":0.2,"surprise":0,"positive":0.28787878787878785,"negative":0.25,"sadness":0,"disgust":0,"joy":0},"emotional_mean":{"fear":0.014705882352941176,"anger":0,"anticipation":0,"trust":0.2,"surprise":0,"positive":0.28787878787878785,"negative":0.25,"sadness":0,"disgust":0,"joy":0},"emotional_std":{"fear":0.014705882352941176,"anger":0,"anticipation":0,"trust":0.2,"surprise":0,"positive":0.28787878787878785,"negative":0.25,"sadness":0,"disgust":0,"joy":0},"emotional_q1":{"fear":0.014705882352941176,"anger":0,"anticipation":0,"trust":0.2,"surprise":0,"positive":0.28787878787878785,"negative":0.25,"sadness":0,"disgust":0,"joy":0},"emotional_q2":{"fear":0.014705882352941176,"anger":0,"anticipation":0,"trust":0.2,"surprise":0,"positive":0.28787878787878785,"negative":0.25,"sadness":0,"disgust":0,"joy":0},"emotional_q3":{"fear":0.014705882352941176,"anger":0,"anticipation":0,"trust":0.2,"surprise":0,"positive":0.28787878787878785,"negative":0.25,"sadness":0,"disgust":0,"joy":0},"followers_count":522,"friends_count":456,"listed_count":7,"statuses_count":9764,"created_at":"Sun Aug 02 19:41:48 +0000 2015"},{"user_id":{"$numberLong":"1353500664299663361"},"emotional_frequency":{"fear":0,"anger":0,"anticipation":0,"trust":0,"surprise":0,"positive":0.14464285714285713,"negative":0,"sadness":0,"disgust":0,"joy":0},"emotional_mean":{"fear":0,"anger":0,"anticipation":0,"trust":0,"surprise":0,"positive":0.14464285714285713,"negative":0,"sadness":0,"disgust":0,"joy":0},"emotional_std":{"fear":0,"anger":0,"anticipation":0,"trust":0,"surprise":0,"positive":0.14464285714285713,"negative":0,"sadness":0,"disgust":0,"joy":0},"emotional_q1":{"fear":0,"anger":0,"anticipation":0,"trust":0,"surprise":0,"positive":0.14464285714285713,"negative":0,"sadness":0,"disgust":0,"joy":0},"emotional_q2":{"fear":0,"anger":0,"anticipation":0,"trust":0,"surprise":0,"positive":0.14464285714285713,"negative":0,"sadness":0,"disgust":0,"joy":0},"emotional_q3":{"fear":0,"anger":0,"anticipation":0,"trust":0,"surprise":0,"positive":0.14464285714285713,"negative":0,"sadness":0,"disgust":0,"joy":0},"followers_count":49,"friends_count":444,"listed_count":0,"statuses_count":2663,"created_at":"Mon Jan 25 00:31:29 +0000 2021"},{"user_id":{"$numberLong":"1308829799977086977"},"emotional_frequency":{"fear":0.125,"anger":0,"anticipation":0,"trust":0.125,"surprise":0,"positive":0.28928571428571426,"negative":0.2,"sadness":0.020833333333333332,"disgust":0,"joy":0},"emotional_mean":{"fear":0.125,"anger":0,"anticipation":0,"trust":0.125,"surprise":0,"positive":0.28928571428571426,"negative":0.2,"sadness":0.020833333333333332,"disgust":0,"joy":0},"emotional_std":{"fear":0.125,"anger":0,"anticipation":0,"trust":0.125,"surprise":0,"positive":0.28928571428571426,"negative":0.2,"sadness":0.020833333333333332,"disgust":0,"joy":0},"emotional_q1":{"fear":0.125,"anger":0,"anticipation":0,"trust":0.125,"surprise":0,"positive":0.28928571428571426,"negative":0.2,"sadness":0.020833333333333332,"disgust":0,"joy":0},"emotional_q2":{"fear":0.125,"anger":0,"anticipation":0,"trust":0.125,"surprise":0,"positive":0.28928571428571426,"negative":0.2,"sadness":0.020833333333333332,"disgust":0,"joy":0},"emotional_q3":{"fear":0.125,"anger":0,"anticipation":0,"trust":0.125,"surprise":0,"positive":0.28928571428571426,"negative":0.2,"sadness":0.020833333333333332,"disgust":0,"joy":0},"followers_count":88,"friends_count":176,"listed_count":1,"statuses_count":3255,"created_at":"Wed Sep 23 18:05:23 +0000 2020"}]}
```


## Data Collection

Collect True and False cascades from different root users
Collect random 1% of the total cascade number and limit the cascade depth to 5