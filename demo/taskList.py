import simplejson as json 

def addToDict(baseDict,dictToAdd):
	for x in dictToAdd:
		baseDict[x]=dictToAdd[x]
	return baseDict

def makeSlideAutomatic(slideInfo):
	taskListOut=[]
	baseColor=slideInfo[0]
	backgroundColor="rgba(%s,%s,%s,.1)"%tuple(baseColor)
	titleColor="rgba(%s,%s,%s,1)"%tuple([int(float(x)/2) for x in baseColor])
	taskListOut.append({"func":"runJavascriptFunction","args":{"functionName":"clearAllInstructions"}})	
	taskListOut.append({"func":"changeBackgroundColor","args":{"color":backgroundColor}})
	#title
	titleDict={"text":slideInfo[1][0],"divID":"instructionsSlideTitle","top":50,"color":titleColor,"fontSize":60,"fadeTime":1}
	if len(slideInfo[1])>1:
		titleDict=addToDict(titleDict,slideInfo[1][1])
	taskListOut.append(getPlaceText(**titleDict))
	print(titleDict) 

	totalEntries=len(slideInfo)-2
	if totalEntries==4:
		entryTops=[200,350,500,650]
	elif totalEntries==5:
		entryTops=[200,325,450,575,700]
	elif totalEntries==6:
		entryTops=[175,275,375,475,575,675]
		entryTops=[175,300,425,550,675,800]
		entryTops=[150,275,400,525,650,775]
	elif totalEntries==7:
		entryTops=[150,250,350,450,550,650,750]
	elif totalEntries==8:
		entryTops=[125+x*float(775-125)/7 for x in range(8)]
		print(entryTops)
		input()  
	for k in range(1,len(slideInfo)-1):
		entryDict={"text":slideInfo[k+1][0],"divID":"instructionsSlideEntry%s"%(k),"top":entryTops[k-1]}
		if len(slideInfo[k+1])>1:
			entryDict=addToDict(entryDict,slideInfo[k+1][1])
		taskListOut.append(getPlaceText(**entryDict))
		print(entryDict) 
	return taskListOut

def getPlaceText(text,divID,top,left=0,color="rgba(0,0,0,1)",fontSize=45,fadeTime=2,textAlign="center"):
	argsDict={}
	argsDict['text']=text
	argsDict['divID']=divID
	argsDict['top']="%spx"%(top)
	argsDict['left']=left
	argsDict['color']=color
	argsDict['fontSize']="%spx"%(fontSize)
	argsDict['fadeTime']=fadeTime
	argsDict['textAlign']=textAlign
	return {"func":"placeText","args":argsDict}

def mouseSequence(sequence):
	this={"func":"mouseSequence","runOnRefresh":False,"args":{"sequence":sequence}}
	print(this)
	return this

tasks=[]


tasks+=[
#Intro Slide
{"func":"changeBackgroundColor","args":{
	"color":"rgba(0,0,255,.1)"}},
{"func":"placeText","args":{
	"text":"Welcome To",
	"top":"150px",
	"left":0,
	"color":"rgba(0,0,0,1)",
	"textAlign":"center",
	"divID":"automatic",
	"fontSize":"45px",
	"fadeTime":2,
	"textAlign":"center"}},
{"func":"placeText","args":{
	"text":"The Economic Science",
	"top":"625px",
	"left":0,
	"color":"rgba(0,0,0,1)",
	"textAlign":"center",
	"divID":"automatic2",
	"fontSize":"45px",
	"fadeTime":2,
	"textAlign":"center"}},
{"func":"placeText","args":{
	"text":"Laboratory",
	"top":"700px",
	"left":0,
	"color":"rgba(0,0,0,1)",
	"textAlign":"center",
	"divID":"automatic3",
	"fontSize":"45px",
	"fadeTime":2,
	"textAlign":"center"}},
{"func":"runJavascriptFunction","args":{
	"functionName":"drawLogoESL"}}]


#Welcome Slide
tasks+=makeSlideAutomatic([[0,255,0],["Welcome"],
	["Economics Experiment."],
	["Will get paid in cash at the end of the experiment."],
	["Please remain silent."],
	["Please raise your hand for help."]
	])

#Welcome Slide 2
tasks+=makeSlideAutomatic([[255,0,0],["Welcome"],
	["Do not talk, laugh or exclaim out loud."],
	["Keep your eyes on your screen only."],
	["Turn off electronic devices and put them away."],
	["We appreciate your cooperation."]
	])


#Agenda
thisStyle={"textAlign":"left","left":"200px"}
tasks+=makeSlideAutomatic([[0,0,255],["Agenda"],
	["1. Instructions",thisStyle],
	["2. Quiz",thisStyle],
	["3. Experiment",thisStyle],
	["4. Survey",thisStyle],
	["5. Payment",thisStyle]
	])


#Experiment overview
tasks+=makeSlideAutomatic([[255,0,0],["Overview of the Experiment"],
	["Matched in pairs."],
	["Your choice affects your payoff."],
	["Your choice affects their payoff."],
	["Their choice affects your payoff."]
	])


thisStyle={"textAlign":"left","left":"200px"}
#Experiment details
tasks+=makeSlideAutomatic([[0,255,0],["Details of the Experiment"],
	["Exchange Rate: 70 Francs = $1",thisStyle],
	["3 Matches (may have different # of periods)",thisStyle],
	["At beginning of each match, randomly matched with another subject",thisStyle],
	["Your identity is anonymous",thisStyle],
	["Matched with same subject for entire match",thisStyle],
	["Randomly matched with another subject in the next match",thisStyle]
	])

#Experimental Interface
tasks+=[
	{"func":"runJavascriptFunction","args":{"functionName":"clearAllInstructions"}},
	{"func":"setInstructionParameters","args":{}},
	{"func":"instructionsSetState","args":{}},
	{"func":"runJavascriptFunction","args":{"functionName":"drawCaptionOverlay"}},
	{"func":"runJavascriptFunction","args":{"functionName":"drawCursorOverlay"}},
	{"func":"placeCursor","args":{"x":500,"y":500}},
]

#Game Table
tasks+=[
	{"func":"runJavascriptFunction","args":{"functionName":"toggleOverlay"}},
	{"func":"highlightDiv","args":{"divName":"gameDiv"}},
	mouseSequence([["toDiv",{"divName":"gameDiv"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableRowLabel_1"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableRowLabel_2"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableColLabel_1"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableColLabel_2"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableRowLabel_2"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableColLabel_1"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableEntry_2_1"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableEntry_2_1"}]]),
	{"func":"unHighlightDiv","args":{"divName":"gameDiv"}}
]


#Show Payoff Summary
tasks+=[
	{"func":"highlightDiv","args":{"divName":"questionsDiv"}},
	mouseSequence([["toDiv",{"divName":"periodSummaryLabel"}]]),
	mouseSequence([["toDiv",{"divName":"summaryLabel"}]]),
	{"func":"unHighlightDiv","args":{"divName":"questionsDiv"}}
]



#Show History
tasks+=[
	{"func":"highlightDiv","args":{"divName":"historyDiv"}},
	{"func":"highlightDiv","args":{"divName":"historyLabels"}},
	mouseSequence([["toDiv",{"divName":"historyLabels"}]]),
	{"func":"unHighlightDiv","args":{"divName":"historyDiv"}},
	{"func":"unHighlightDiv","args":{"divName":"historyLabels"}},
]


#Show StatusBar:status#1
tasks+=[
	{"func":"highlightDiv","args":{"divName":"statusBar"}},
	mouseSequence([["toDiv",{"divName":"statusBar"}]]),
	{"func":"unHighlightDiv","args":{"divName":"statusBar"}},
	{"func":"runJavascriptFunction","args":{"functionName":"toggleOverlay"}},
]

# //Make Row choice
tasks+=[
	mouseSequence([["toDiv",{"divName":"gameTableRowLabel_1"}],["clickDiv",{"divName":"gameTableRowLabel_1","func":"instructionsSelectRow","args":{"row":"1"}}]]),
	mouseSequence([["toDiv",{"divName":"summaryMyChoiceEntry"}]]),
]

# //Make Col choice
tasks+=[
	mouseSequence([["toDiv",{"divName":"gameTableColLabel_2"}],["clickDiv",{"divName":"gameTableColLabel_2","func":"instructionsSelectCol","args":{"col":"2"}}]]),
	mouseSequence([["toDiv",{"divName":"summaryOthersChoiceEntryGuess"}]]),
]

# //Status #2
tasks+=[
	mouseSequence([["toDiv",{"divName":"statusBar"}]]),
]
# //Status #3
tasks+=[
	{"func":"instructionsFinishPeriod","args":{}},
	mouseSequence([["toDiv",{"divName":"selectedColumnDiv2","anchor":"south"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableEntry_1_1"}]]),
	mouseSequence([["toDiv",{"divName":"summaryOthersChoiceEntryActual"}]]),
	mouseSequence([["toDiv",{"divName":"summaryPayoffs"}]]),
	mouseSequence([["toDiv",{"divName":"historyEntry_20_0"}]]),
	mouseSequence([["toDiv",{"divName":"summaryLabel"}]]),
	mouseSequence([["toDiv",{"divName":"totalPayoffMineLabel"}]]),
	mouseSequence([["toDiv",{"divName":"correctGuessesLabel"}]]),
	mouseSequence([["toDiv",{"divName":"gameTableEntry_1_1"}]]),
	mouseSequence([["clickDiv",{"divName":"gameTableEntry_1_1","func":"instructionsMovetoNextPeriod","args":{}}]]),
]

tasks+=[{"func":"runJavascriptFunction","args":{"functionName":"deleteCursorOverlay"}}]


thisStyle={"textAlign":"left","left":"100px"}
thisStyle2={"textAlign":"center"}
thisStyle3={"textAlign":"left","left":"200px"}
#Number of Periods Per Match
tasks+=makeSlideAutomatic([[0,255,0],["Number of Periods Per Match"],
	["Each period one number drawn from set",thisStyle],
	["{1, 2, 3,..., 98, 99, 100} (and replaced).",thisStyle2],
	["- If the number is 1 - The match ends.",thisStyle3],
	["- If the number is not 1 - The match will continue.",thisStyle3],
	["In every period:",thisStyle],
	["- 1% chance that match end.",thisStyle3],
	["- 99% chance that match has another period.",thisStyle3],
	["This procedure has been performed on the computer, before the experiment.",thisStyle],
	])


#Payoffs
thisStyle={"textAlign":"left","left":"200px"}
thisStyle2={"textAlign":"left","left":"300px"}
thisStyle3={"textAlign":"left","left":"400px"}

tasks+=makeSlideAutomatic([[255,0,0],["Payoffs"],
	["Your payment will contain the following:",thisStyle],
	["1. $5 Show up fee.",thisStyle2],
	["2. Payment for all Francs earned in all periods.",thisStyle2],
	["- Exchange Rate: 70 Francs = $1.",thisStyle3],
	["3. Bonus payment for raffle tickets.",thisStyle2],
	["Paid in cash, in private.",thisStyle]
	])



filename='generatedFiles/tasks.json'
file = open(filename,'w')
json.dump(tasks,file)
file.close()  


