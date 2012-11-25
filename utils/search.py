#!/usr/bin/env python

from database.dbModels import *
from collections import Counter
import re, time

#BookScore = namedTuple('BookScore',['book','score'])
#Search book from ebenta library

#search books whose keywords match with the query
def searchBooks(query):
    start = time.time()
    #splits the query into words
    words = re.split('\W+',query)
    dbInstance = {}
    found = []
    ret = []
    # searches for individual match for every word in words
    # and appends every found result (even if it is already there)
    # to found and stores the respective dbModel instace to results
    for word in words:
        r = Library.all().filter('searchKeys', word).fetch(20)
        updateFound(found,dbInstance,r)
    
    score = Counter(found)

    sorted_score = mergeSort(invert(score))
    
    for score in sorted_score:
        ret.append(dbInstance[score[1]])
    end = time.time()
    return ret, end-start
    
#loops to all found keys and appends their id to found
def updateFound(found,dbInstance,result):
    for book in result:
        bid = book.key().id()
        found.append(bid)
        if bid not in dbInstance:
            dbInstance[bid] = book

#inverts a dictionary and returns a list
# sample input {'a': 1, 'b': 2}
#       output [[1,'a'],[2,'b']]
def invert(scores):
    ret = []
    for s in scores:
        ret.append([scores[s],s])
    return ret

# Mergesort descending
# src: http://errorsandexceptions.wordpress.com/2011/05/16/quicksort-and-mergesort-in-python/
def mergeSort(toSort):
	if len(toSort) <= 1:
		return toSort

	mIndex = len(toSort) / 2
	left = mergeSort(toSort[:mIndex])
	right = mergeSort(toSort[mIndex:])

	result = []
	while len(left) > 0 and len(right) > 0:
		if left[0][0] < right[0][0]:	
			result.append(right.pop(0))
		else:
			result.append(left.pop(0))

	if len(left) > 0:
		result.extend(mergeSort(left))
	else:
		result.extend(mergeSort(right))
	return result