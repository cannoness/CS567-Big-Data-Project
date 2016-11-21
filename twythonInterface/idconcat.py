ids = {}

lineCount = long(0)
uniqueCount = long(0)

bigIDFile = 'output/trump.output'
smallIDFile = 'output/trumpIDShort.txt'

with open(bigIDFile, 'r') as fp:
    for line in fp:
        lineCount += 1
        lineArr = line.split()
        if len(lineArr) == 1:
            print "Singleton"
        userName = lineArr[0]
        tweetID = long(lineArr[1])
        if userName in ids:
            oldID = ids[userName]
            if oldID < tweetID: #keep the most recent one we find
                ids[userName] = tweetID

        else:
            ids[userName] = tweetID
            uniqueCount += 1

print lineCount, " lines."
print uniqueCount, " unique."

fileOut = open(smallIDFile, 'w')
for idStr in ids:
    fileOut.write(idStr)
    fileOut.write(' ')
    fileOut.write(str(ids[idStr]))
    fileOut.write('\n')
