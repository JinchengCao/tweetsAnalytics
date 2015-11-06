# example of program that calculates the average degree of hashtags
from datetime import datetime as dt
import re
import Queue
import sys
def uniqueTag(seq):
	seen = set()
	seen_add = seen.add
	return [ x for x in seq if not (x in seen or seen_add(x))]

def getDegree(graphList): #degree = 2 * (unique pairs numbers)/ (unique node numbers)
	nodeList = []
	pairList = []
	for tagList in graphList:
		nodeList = nodeList + tagList
		tagList2 = tagList[1: len(tagList)]
		tagList2.append(tagList[0]);
		pairs = zip(tagList,tagList2)
		if len(tagList) == 2:
			pairList = pairList + [(tagList[0],tagList[1])]
		else:
			pairList = pairList + pairs
	nodeSet = set(nodeList) # get unique node set
	pairSet = set(pairList) # get unique pair set e.g.[(a,b),(b,c),(c,a)]
	#print nodeSet
	#print pairSet
	#print len(nodeSet)
	#print len(pairSet)
	degree = float("{0:.2f}".format((2.0 * len(pairSet))/(1.0 * len(nodeSet))))
	return degree

timeQueue = Queue.Queue()
hashtagQueue = Queue.Queue() # use two queues to keep track of time and hashtag
graphList = []
ft = open(sys.argv[2], 'w')
with open(sys.argv[1]) as f:
	for line in f:
		text = line.split(" (timestamp:")[0].lower()
		if text == "":
			continue
		else:
			print text
			tag = re.findall(r'(?:(?<=\s)|^)#(\w*[A-Za-z_]+\w*)',text)
			tag = uniqueTag(tag)
			if tag and len(tag) > 1:
				graphList.append(tag) # only more than two hashtags in one tweet is meaningful for our calculation, it can be appended into graphList
			match = re.search(r'(?<=timestamp: ).*?(?=\))',line)
			time =  match.group(0)
			time = dt.strptime(time,'%a %b %d %H:%M:%S +0000 %Y')
			timeSecond = dt(time.year,time.month, time.day, time.hour, time.minute, time.second) #format time for second difference calculation
			while not timeQueue.empty() and (timeSecond - timeQueue.queue[0]).total_seconds() > 60: 
				timeQueue.get()
				tagPop = hashtagQueue.get() #FIFO queue, so the oldest one is kicked out of the queue
				if tagPop and len(tagPop) > 1:
					graphList.remove(tagPop) # only more than two hashtags in one tweet were appended, so we just need to find that on

			timeQueue.put(timeSecond)
			hashtagQueue.put(tag)
		print "degree"
		if not graphList: #graphList can be empty
			print 0
			ft.write(str(0) + '\n')
		else:
			d = getDegree(graphList)
			print d
			ft.write(str(d) + '\n')
		print "\n"

ft.close()  

if __name__ == '__main__':
	print "Average degree of hashtags is calculated."