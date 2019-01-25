import json

with open('C:\\Users\\daWigs\\Desktop\\Database\\Json\\gYYLbjXvHnP4dV4C - (From Mon Oct 29 06.41.55 +0000 2018 To Wed Apr 03 22.28.57 +0000 2013).json', 'r') as f: 
	data = json.load(f)

outfile = open('C:\\Users\\daWigs\\Desktop\\Database\\Json\\gYYLbjXvHnP4dV4C - (From Mon Oct 29 06.41.55 +0000 2018 To Wed Apr 03 22.28.57 +0000 2013)(2).json', 'w')	
	
mData = []	
print(0,round(len(data)/2))
for i in range(0,round(len(data)/2)):
	
	mData.extend([data[i]])
	
json.dump(mData, outfile)	
outfile.close()



outfile2 = open('C:\\Users\\daWigs\\Desktop\\Database\\Json\\gYYLbjXvHnP4dV4C - (From Mon Oct 29 06.41.55 +0000 2018 To Wed Apr 03 22.28.57 +0000 2013)(2).json', 'w')	
mData2 = []
print(i+1,(len(data)))
for m in range(i+1,(len(data))):
	
	mData2.extend([data[m]])
	
json.dump(mData2, outfile2)	
outfile.close()