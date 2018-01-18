#This script is used to analyze tweet data
#Word frequencies for word clouds, tweet sentiment
#uses vectors "term_vec" and "term_vec_ep2" generated in Cleaning

from sentiment_module import sentiment
import numpy as np
from collections import Counter

term = 'happy'
sentiment.exist(term)
sentiment.sentiment(term)

#episode 1 frequencies
all_terms = np.concatenate(term_vec)

counts = Counter(all_terms)
print(counts)

#episode 2 frequencies
all_terms = np.concatenate(term_vec_ep2)
counts = Counter(all_terms)
print(counts)

#grabbing time stamps
tweets = open('ALL_TWEETS_SORTED.csv', 'r', encoding = "utf8")
reader = csv.reader(tweets)
header = reader.__next__()

tweets_time = []
#tweets_time_ep2 = tweets_time

for row in reader:
    tweet = row[1]
    tweets_time.append(tweet)

for i in range(len(tweets_time)):
    tweets_time[i] = tweets_time[i][11:16]

#new_time
new_time = [0]
for i in range(1, 22697):
    if tweets_time[i] != tweets_time[i-1]:
        #print(tweets_time[i])
        new_time.append(i)
new_time.append(len(tweets_time)-1)
     
#new_time_ep2
new_time_ep2 = [0]
for i in range(1, 16080):
    if tweets_time[i] != tweets_time[i-1]:
        #print(tweets_time[i])
        new_time_ep2.append(i)
new_time_ep2.append(len(tweets_time)-1)
        
#ep1 dictionaries
d = { }
for i in range(1, 83):
    d["all_tweets{0}".format(i)] = np.concatenate(term_vec[new_time[i-1]:new_time[i]-1])

d2 = {}
for i in d:
    d2[i] = Counter(d[i])
   # print(i)
   
#count instances of characters across time
character = 'randall'
char_count = []
for i in d2:
    char_count.append(d2[i][character])

#ep2
char_count_ep2 = []
for i in d2_ep2:
    char_count_ep2.append(d2_ep2[i][character])

#ep2 dictionaries
d_ep2 = { }
for i in range(1, 85):
    d_ep2["all_tweets{0}".format(i)] = np.concatenate(term_vec_ep2[new_time_ep2[i-1]:new_time_ep2[i]-1])

d2_ep2 = {}
for i in d_ep2:
    d2_ep2[i] = Counter(d_ep2[i])
   # print(i)
   
#ep2 counts
kate_ep2 = []
for i in d2_ep2:
    kate_ep2.append(d2_ep2[i]['kate'])
    
love_ep2 = []
for i in d2_ep2:
    love_ep2.append(d2_ep2[i]['love'])

#sentiment analysis

ep1_arousal = []
ep1_valence = []
for i in d:
    ep1_arousal.append(sentiment.sentiment(d[i].tolist())['arousal'])
    ep1_valence.append(sentiment.sentiment(d[i].tolist())['valence'])
    
#ep2 sentiment analysis
ep2_arousal = []
ep2_valence = []
for i in d_ep2:
    ep2_arousal.append(sentiment.sentiment(d_ep2[i].tolist())['arousal'])
    ep2_valence.append(sentiment.sentiment(d_ep2[i].tolist())['valence'])

#getting sentiment for subsets of the tweets
terms = ['randall']
#terms = ['jack', 'rebecca', 'randall', 'kate', 'kevin', 'beth',
#         'toby', 'william', 'miguel', 'sophie', 'Sterling K Brown', 
#         'Milo Ventimiglia', 'Mandy Moore', 'Chrissy Metz', 
#         'Justin Hartley', 'Susan Kelechi Watson', 'Chris Sullivan', 
#         'Ron Cephas Jones', 'justinhartley', 'sterlingkbrown', 
#         'chrissymetz', 'skelechiwatson', 'miloventimiglia', 
#         'themandymoore']

#any(i in term_list for i in ['test','love'])

#need to create new tweet vectors with and without term list
#also need to grab time stamp for those tweets for aggregation
term_vec_without_terms = []
term_vec_with_terms = []
without_terms_time = []
with_terms_time = []
for i in range(len(term_vec)):
    if any(j in term_vec[i] for j in terms):
        term_vec_with_terms.append(term_vec[i])
        with_terms_time.append(tweets_time[i])
        continue
    term_vec_without_terms.append(term_vec[i])
    without_terms_time.append(tweets_time[i])

#index of new time for term_vector with terms
with_terms_new_time = [0]
for i in range(1, len(with_terms_time)):
    if with_terms_time[i] != with_terms_time[i-1]:
        #print(tweets_time[i])
        with_terms_new_time.append(i)
if with_terms_time[-1] == with_terms_time[-2]:
    with_terms_new_time.append(len(with_terms_time)-1)

#acutal times for term_vector with terms (for graphing)
with_terms_actual_times= []
for i in with_terms_new_time:
    with_terms_actual_times.append(with_terms_time[i])

#index of new time for term_vector without terms
without_terms_new_time = [0]
for i in range(1, len(without_terms_time)):
    if without_terms_time[i] != without_terms_time[i-1]:
        #print(tweets_time[i])
        without_terms_new_time.append(i)
without_terms_new_time.append(len(without_terms_time)-1)
    
    
term_vec_ep2_without_terms = []
term_vec_ep2_with_terms = []
without_terms_time_ep2 = []
with_terms_time_ep2 = []
for i in range(len(term_vec_ep2)):
    if any(j in term_vec_ep2[i] for j in terms):
        term_vec_ep2_with_terms.append(term_vec_ep2[i])
        with_terms_time_ep2.append(tweets_time_ep2[i])
        continue
    term_vec_ep2_without_terms.append(term_vec_ep2[i])
without_terms_time_ep2.append(tweets_time_ep2[i])
    

####
#index of new time for ep2 term_vector with terms
with_terms_new_time_ep2 = [0]
for i in range(1, len(with_terms_time_ep2)):
    if with_terms_time_ep2[i] != with_terms_time_ep2[i-1]:
        #print(tweets_time[i])
        with_terms_new_time_ep2.append(i)
if with_terms_time_ep2[-1] == with_terms_time_ep2[-2]:
    with_terms_new_time_ep2.append(len(with_terms_time_ep2)-1)

#acutal times for ep2 term_vector with terms (for graphing)
with_terms_actual_times_ep2= []
for i in with_terms_new_time_ep2:
    with_terms_actual_times_ep2.append(with_terms_time_ep2[i])

####
without_terms_new_time_ep2 = [0]
for i in range(1, len(without_terms_time_ep2)):
    if without_terms_time_ep2[i] != without_terms_time_ep2[i-1]:
        #print(tweets_time[i])
        without_terms_new_time_ep2.append(i)
without_terms_new_time_ep2.append(len(without_terms_time_ep2)-1)

#building time dictionaries for ep1 and ep2 tweets with terms

d_with = { }
for i in range(1, len(with_terms_new_time)):
#    if i != 73:
        d_with["all_tweets{0}".format(i)] = np.concatenate(term_vec_with_terms[with_terms_new_time[i-1]:with_terms_new_time[i]])

ep1_with_arousal = []
ep1_with_valence = []
for i in d_with:
    ep1_with_arousal.append(sentiment.sentiment(d_with[i].tolist())['arousal'])
    ep1_with_valence.append(sentiment.sentiment(d_with[i].tolist())['valence'])

d_ep2_with = {}
for i in range(1, len(with_terms_new_time_ep2)):
    d_ep2_with["all_tweets{0}".format(i)] = np.concatenate(term_vec_ep2_with_terms[with_terms_new_time_ep2[i-1]:with_terms_new_time_ep2[i]])

ep2_with_arousal = []
ep2_with_valence = []
for i in d_ep2_with:
    ep2_with_arousal.append(sentiment.sentiment(d_ep2_with[i].tolist())['arousal'])
    ep2_with_valence.append(sentiment.sentiment(d_ep2_with[i].tolist())['valence'])
#building time dictionaries for ep1 and ep2 tweets without terms

d_without = { }
for i in range(1, len(without_terms_new_time)):
    d_without["all_tweets{0}".format(i)] = np.concatenate(term_vec_without_terms[without_terms_new_time[i-1]:without_terms_new_time[i]-1])

ep1_without_arousal = []
ep1_without_valence = []
for i in d_without:
    ep1_without_arousal.append(sentiment.sentiment(d_without[i].tolist())['arousal'])
    ep1_without_valence.append(sentiment.sentiment(d_without[i].tolist())['valence'])

sentiment.sentiment(np.concatenate(term_vec_without_terms).tolist())
sentiment.sentiment(np.concatenate(term_vec_with_terms).tolist())
sentiment.sentiment(np.concatenate(term_vec).tolist())
