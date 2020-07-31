import simplejson as json 
import re


#load files
filename='00-setPath.py'
file = open(filename,'r')
fileData=file.read()
file.close() 
exec(fileData)

filename=fullPath+"generatedFiles/01-ssml.txt"
file = open(filename,'r')
fileData=file.read()
file.close() 

filename=fullPath+"generatedFiles/output.marks"
file = open(filename,'r')
marks=file.read()
file.close() 
marks=[json.loads(x) for x in marks.split("\n") if len(x)>3]
marks=[x for x in marks if x['type']=='word']

#replace all tags
tags = re.findall(r"<.*?>",fileData,re.DOTALL) 
for t in tags:
	fileData=fileData.replace(t,"")

#cleanr up data
for k in range(100):
	fileData=fileData.replace(" .",".")
	fileData=fileData.replace("..",".")
	fileData=fileData.replace("\n"," ")
	fileData=fileData.replace("\t"," ")
	fileData=fileData.replace("  "," ")

def simp(string):
	return string.replace(".","").replace(",","").replace(")","").replace("(","").replace(":","").lower()


#get words and times for each word 
captions=[]
words=fileData.split(" ")
wi=0
mi=0
wordData=[]
while True:
	actualWord=words[wi]
	thisWord=simp(actualWord)
	thisMark=marks[mi]
	thisMarkWord=simp(thisMark['value'])
	print(thisMarkWord) 
	if thisWord=="":
		wi+=1
	elif thisMarkWord.find("<")>-1 and thisMarkWord.find(">")>-1:
		mi+=1
	else:
		nextWord=simp(words[wi+1])
		print(nextWord,mi,len(marks)) 
		try:
			nextMark=marks[mi+1]
			nextMarkWord=simp(nextMark['value'])
		except:
			nextMarkWord=""
		if thisWord==thisMarkWord:
			wordData.append([actualWord,thisMark['time']])
			wi+=1
			mi+=1
		elif thisWord==thisMarkWord+nextMarkWord:
			wordData.append([actualWord,thisMark['time']])
			wi+=1
			mi+=2
		else:
			print(thisWord)
			print(nextWord)
			print(thisMarkWord)
			print(nextMarkWord)
			input() 

	if mi>len(marks)-1 or wi>len(words)-1:
		break


#get captions and times based on threshold which is number of characters.  
this=[0,'']
threshold=100
for w in wordData:
	if this[1]=="":
		this[0]=w[1]
	this[1]+=w[0]+" "
	if len(this[1])>threshold:
		captions.append(this)
		this=[0,'']
captions.append(this)
captions.append([wordData[-1][1]+5000,"End of Instructions."])



#create output [words,duration for this caption, end time]
out=[]
for (i,c) in enumerate(captions[:-1]):
	n=captions[i+1]
	duration=n[0]-c[0]
	this=[c[1],float(duration)/1000,float(n[0])/1000]
	out.append(this)

filename=fullPath+"generatedFiles/captions.json"
file = open(filename,'w')
json.dump(out,file)
file.close()  


