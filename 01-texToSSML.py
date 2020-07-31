#!/usr/local/bin/python3 

import subprocess
import time
from os import system
import re
import os
import numpy as np
import pickle
import simplejson as json 
import pickle


filename='00-creds.json'
file = open(filename,'rb')
data=json.load(file)
file.close() 
completePath=os.path.abspath(data['path']) 
fullPath=completePath

def addTitle(lab):
	if lab=="esl":
		texData="""
		<mark name='mark2'/> Welcome to <mark name='mark1'/> the <mark name='mark1'/> Economic Science <mark name='mark1'/> Laboratory. 
		Please carefully watch these video instructions and follow along on the paper copy at your desk. <break strength="x-strong"/> 
		"""
	# elif lab=="vseel":
	# 	print "PURDUE LABBBBB"
	# 	texData="""
	# 	[[2]] Welcome to [[1]] the Vernon Smith [[1]] Experimental Economics [[1]] Laboratory. [[slnc 250]]  Please carefully watch these video instructions and follow along on the paper copy at your desk.  [[slnc 500]]

	# 	%s
	# 	"""%(texData)
	return texData



def findNext(string,substrings,index):
	locations=[]
	for substring in substrings:
		thisIndex=string.find(substring,index)
		if thisIndex>-1:
			locations.append([thisIndex,substring])
	locations.sort()
	return locations

def getNestedString(string,start,ps,pe,startIndex):
	i1=string.find(start,startIndex)
	i2=i1-1
	count=0
	while True:
		o1=string.find(ps,i2+1) 
		o2=string.find(pe,i2+1)
		print(count,o1,o2) 
		if o1!=-1 and o1<o2:
			count+=1
			i2=o1
		elif o1>o2 or (o1==-1 and o2>-1): 
			count-=1
			i2=o2
		if count==0:
			break
	return string[i1:i2+len(pe)]



texFile=fullPath+"instructions.tex"
file = open(texFile,'r')
fileData=file.read()
file.close() 




#deleteComments
lines = re.findall(r"\\*%.*",fileData)
for line in lines:
	if line[0]!="\\":#ensure not a latex %
		fileData=fileData.replace(line,"")

# get main text
fileData = re.findall(r"\\begin{document}(.*)\\end{document}",fileData,re.DOTALL)[0] 

#replace front header
addEverypageHook=getNestedString(fileData,"\\AddEverypageHook{","{","}",0)
fileData=fileData.replace(addEverypageHook,"")

#replace defs
defs = re.findall(r"(\\def(\\.*?){(.*?)})",fileData,re.DOTALL)
for k in defs:
	fileData=fileData.replace(k[0],"")
	fileData=fileData.replace(k[1]+" ",k[2]+" ")


#replace $D$
lines = re.findall(r"\$.{1,10}\$",fileData)
for line in lines:
	fileData=fileData.replace(line,line[1:-1])


#replace quotes
fileData=fileData.replace("``",'<break strength="weak"/>')
fileData=fileData.replace("''",'<break strength="weak"/>')




fileData=fileData.replace("\\%","%")#replace latex %
fileData=fileData.replace("\\$","$")#replace latex $
fileData=fileData.replace("\\#","#")#replace latex #
fileData=fileData.replace("\\\\","\n")#replace latex #

r=r"\$\s*?\\\{[,\s0-9]+\\ldots[,\s0-9]+\\\}\s*?\$"
firstMatch = re.findall(r,fileData,re.DOTALL)
for k in firstMatch:
	new="from "+k.replace(" ","")[3:-3].replace("\\ldots","up to").replace(",",", ")
	fileData=fileData.replace(k,new)

#replace begin{center}
while True:
	sectionOuter=getNestedString(fileData,"\\begin{center}","\\begin{center}","\\end{center}",0)
	if sectionOuter!="":
		new=sectionOuter[14:-12]
		if new[-1]!="\n":
			new+="\n"
		if new[0]!="\n":
			new="\n"+new
		fileData=fileData.replace(sectionOuter,new)
	else:
		break

#replace sections
# \section*{\dblbkt{3} Welcome} 
for sectionTitle in ["section","subsection","subsubsection"]:
	while True:
		sectionOuter=getNestedString(fileData,"\\"+sectionTitle,"{","}",0)
		if sectionOuter!="":
			sectionInner = re.findall(r".*?{(.*)",sectionOuter,re.DOTALL)[0][:-1]
			fileData=fileData.replace(sectionOuter,sectionInner+'.<break strength="x-strong"/>')
		else:
			break

#replace 
while True:
	sectionOuter=getNestedString(fileData,"{\\bf ","{","}",0)
	if sectionOuter!="":
		new='<prosody volume="loud" rate="slow">%s</prosody>'%(sectionOuter[4:-1])
		fileData=fileData.replace(sectionOuter,new)
	else:
		break


#replace items
index=0
current=[]
enumerateIndex=0
enumerateStrings=[[],["1","2","3","4","5","6","7","8","9","10"],["a","b","c","d","e","f","g","h","i","j","k"],["i","ii","iii","iv","v","vi","vii","viii","ix","x"]]
enumerateCounts=[0,0,0,0]
itemsToBeReplaced=[]
while True:
	this=findNext(fileData,["\\item ","\\begin{itemize}","\\end{itemize}","\\begin{enumerate}","\\end{enumerate}"],index)	
	if this!=[]:
		this=this[0]
		thisString=""
		index=this[0]+1
		if this[1].find("\\begin")>-1:
			current.append(this[1])
			if this[1].find("enumerate")>-1:
				enumerateIndex+=1
		elif this[1].find("\\end")>-1:
			current=current[:-1]
			if this[1].find("enumerate")>-1:
				enumerateCounts[enumerateIndex]=0
				enumerateIndex-=1
		elif this[1]=="\\item ":
			if current[-1].find("enumerate")>-1:
				thisString=enumerateStrings[enumerateIndex][enumerateCounts[enumerateIndex]]
				enumerateCounts[enumerateIndex]+=1
			else:
				thisString="*"
			itemsToBeReplaced.append([thisString,len(current)])
	elif this==[]:
		break


firstMatch = re.findall(r"\s*\\item",fileData,re.DOTALL)
index=0
for k in firstMatch:
	this=itemsToBeReplaced[index]
	if this[0]=="*":
		thisString="\n"+"\t"*this[1]
	else:
		thisString="\n"+"\t"*this[1]+this[0]+"."
	fileData=fileData.replace(k,thisString,1)
	index+=1
fileData=fileData.replace("\\begin{enumerate}","")
fileData=fileData.replace("\\end{enumerate}","")
fileData=fileData.replace("\\begin{itemize}","")
fileData=fileData.replace("\\end{itemize}","")



fileData=fileData.replace("\\dblbkt{1}","<mark name='mark1'/>")
fileData=fileData.replace("\\dblbkt{2}","<mark name='mark2'/>")
fileData=fileData.replace("\\dblbkt{3}","<mark name='mark3'/>")
fileData=fileData.replace("\\dblbkt{4}","<mark name='mark4'/>")
fileData=fileData.replace("\\dblbkt{5}","<mark name='mark5'/>")
fileData=fileData.replace("\\dblbkt{6}","<mark name='mark6'/>")


firstMatch = re.findall(r"(\\dblbkt{.*?slnc.*?([0-9]+).*?})",fileData,re.DOTALL)
for k in firstMatch:
	fileData=fileData.replace(k[0],'<break time="%sms"/>'%(k[1]))

for k in range(100):
	fileData=fileData.replace("  "," ")





fileData=addTitle("esl")+fileData

fileData="<speak>%s</speak>"%(fileData)


filename=fullPath+"generatedFiles/01-ssml.txt"
file = open(filename,'w')
file.writelines(fileData)
file.close() 
