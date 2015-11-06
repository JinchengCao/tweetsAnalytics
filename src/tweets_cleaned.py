# example of program that calculates the number of tweets cleaned
import re
import sys
#ft = open('../tweet_output/ft1.txt', 'w')
#with open('../tweet_input/tweets.txt') as f:
ft = open(sys.argv[2], 'w')
with open(sys.argv[1]) as f:
    for line in f:
    	if not line.startswith('{"created_at"'):
    		continue
    	else:
			match = re.search(r'(?<="text":").*?(?=","source")',line) #extract text
			text = match.group(0)
			text = text.decode('unicode_escape').encode('ascii','ignore') #decode and encode to remove unicode
			text = ' '.join(text.split()) #replace whitespace with single space
			text = text.replace('\/','/').replace('\\\\','\\').replace('\"','"').replace("\'","'") #replace escape characters
			match = re.search(r'(?<="created_at":").*?(?=","id")',line)
			timestamp = match.group(0)
			afterExtraction = text + " (timestamp: " + timestamp + ")" #extract timestamp
			ft.write(afterExtraction + '\n')
			print afterExtraction
ft.close()   

if __name__ == '__main__':
	print "Tweets are cleaned."