import simplejson as json 

filename='00-setPath.py'
file = open(filename,'r')
fileData=file.read()
file.close() 
exec(fileData)

filename=fullPath+"generatedFiles/output.marks"
file = open(filename,'r')
fileData=file.read()
file.close() 

filename=fullPath+"generatedFiles/tasks.json"
file = open(filename,'rb')
tasks=json.load(file)
file.close()  


this=[json.loads(x) for x in fileData.split("\n") if len(x)>3]
times=[]
tasksOut=[]
forSorting=[]
counter=-1
resyncTime=0
for k in this:
	if k['type']=="ssml":
		thisNumber=int(k['value'].replace("mark",""))
		for j in range(thisNumber):
			counter+=1
			if counter<len(tasks):
				# tasksOut.append(tasks[counter])
				print(tasks[counter]) 
				forSorting.append([float(k['time'])/1000,counter,tasks[counter]])
			else:
				print("TOO MANY MARKERS, NOT ENOUGH TASKS",counter,len(tasks)) 
			# times.append(float(k['time'])/1000)
	elif k['type']=="sentence":
		thisTime=float(k['time'])/1000#-.2
		if thisTime-resyncTime>10 and thisTime>0:
			resyncTime=thisTime
			forSorting.append([thisTime,counter,{'func': 'resyncAudio', 'args': {}}])
			# times.append(thisTime)#go back at end of sentence
			# tasksOut.append({'func': 'resyncAudio', 'args': {}})

forSorting.sort()
for k in forSorting:
	times.append(k[0])
	tasksOut.append(k[2])
filename=fullPath+"generatedFiles/taskTimes.json"
file = open(filename,'w')
json.dump(times,file)
file.close()  

filename=fullPath+"generatedFiles/tasksOut.json"
file = open(filename,'w')
json.dump(tasksOut,file)
file.close()  

# times=[]
# for k in this:
# 	if k['type']=="sentence":
# 		times.append(float(k['time'])/1000)

# filename=fullPath+"generatedFiles/sentences.json"
# file = open(filename,'w')
# json.dump(times,file)
# file.close()  

