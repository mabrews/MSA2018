#this script is used to preprocess twitter data for NLP

import nltk
#nltk.download('punkt')
#nltk.download('stopwords')
import csv
import re
import string
import os

os.chdir('C:\\Users\mabre\Google Drive\Fall 2 Homework (Team 10)\Text Analytics Project\Data')

#Let's start out slow, shall we?

#tweets = open('tweet_00001.csv', 'r', encoding = "utf8")

#LEH GOOOOOOOOOOO
tweets = open('ALL_TWEETS_SORTED.csv', 'r', encoding = "utf8")
reader = csv.reader(tweets)
header = reader.__next__()

tweets_body = []

for row in reader:
    tweet = row[5]
    tweets_body.append(tweet)

#remove punctuation    
punc = re.compile( '[%s]' % re.escape( string.punctuation ) )
term_vec = [ ]

for j in tweets_body:
    j = j.lower()
    j = punc.sub( '', j )
    term_vec.append( nltk.word_tokenize( j ) )

#remove stop words

stop_words = nltk.corpus.stopwords.words( 'english' )
stop_words.append('thisisus')
stop_words.append('rt')
stop_words.append('nbcthisisus')

for i in range( 0 , len(term_vec) ):
    term_list = [ ]

    for term in term_vec[ i ]:
        if term not in stop_words:
            term_list.append( term )

    term_vec[ i ] = term_list

#porter stem remaining terms

porter = nltk.stem.porter.PorterStemmer()

for i in range( 0, len( term_vec ) ):
    for j in range( 0, len( term_vec[ i ] ) ):
        term_vec[ i ][ j ] = porter.stem( term_vec[ i ][ j ] )

#save the cleaned tweets to a csv
out = open( 'ALL_TWEETS_2_CLEANED_NO_PORTER_SORTED_UTF8.csv', 'w' , newline = '',encoding = "utf8")
writer = csv.writer( out )
for j in range(len(term_vec)):
    writer.writerow(term_vec[j])
out.close()

#repeating cleaning for episode 2 tweets
tweets = open('ALL_TWEETS_2_SORTED.csv', 'r', encoding = "utf8")
reader = csv.reader(tweets)
header = reader.__next__()

tweets_body = []

for row in reader:
    tweet = row[5]
    tweets_body.append(tweet)

#remove punctuation    
punc = re.compile( '[%s]' % re.escape( string.punctuation ) )
term_vec_ep2 = [ ]

for j in tweets_body:
    j = j.lower()
    j = punc.sub( '', j )
    term_vec_ep2.append( nltk.word_tokenize( j ) )

#remove stop words

stop_words = nltk.corpus.stopwords.words( 'english' )
stop_words.append('thisisus')
stop_words.append('rt')
stop_words.append('nbcthisisus')

for i in range( 0 , len(term_vec_ep2) ):
    term_list = [ ]

    for term in term_vec_ep2[ i ]:
        if term not in stop_words:
            term_list.append( term )

    term_vec_ep2[ i ] = term_list