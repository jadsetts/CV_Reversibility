#This is data input for only one CV, but there's some code to bring in a few CVs.
#The CV must be one full sweep to work properly.
def plotSimulatedData(data, noiseValue=0.02,graphOption=0):

    nD=np.loadtxt(file)
    potential=nD[:,0]-4.2
    current=nD[:,1]
    
    noise=[]
    counter=0
    for i in range(round(len(potential)/2)):
        noise.append(random.uniform(-noiseValue,noiseValue)+counter)
        counter+=0.0
    
    current[:round(len(current)/2)]=current[:round(len(current)/2)]+noise
    noise.reverse()
    current[round(len(current)/2):]=current[round(len(current)/2):]+noise
    if int(graphOption) == 0:
        #Then we can plot the current (smoothY or arraypos3) vs. potential (arraypos5) data.
        fig = plt.figure()
        ax = plt.axes()
        plt.plot(potential,current,label='Simulated Data')
        plt.plot(potential[round(len(current)/2):],noise,label='Noise ('+str(noiseValue)+')')
        plt.legend()
        ax.set_xlabel('Potential (V)')
        ax.set_ylabel('Current (nA)')
    return potential,current

#Testing
# file=r'C:\Users\jadse\Desktop\Postdoc\Coding\CV_Fitting\SimulationData\fakeData.txt'
# noiseVal=0.02
# potential,current=plotSimulatedData(file,noiseVal,0)
# potential,current=plotSimulatedData(file)

#This is data input for only one CV, but there's some code to bring in a few CVs.
#The CV must be one full sweep to work properly.
#Smoothing is likely necessary and you need to do some form of smoothing.
#Consider your data density and play with the bin number.

def plotExperimentalData(data, smoothBinNumber=50,graph=1):
    nD=np.loadtxt(file)
    potential=nD[:,0]
    current=nD[:,1]
    #Lets smooth the current data. savgol_filter() has bin size in 2nd position, and polynomial order in the 3rd position.
    #Uncommenting the below line we can check how the smoothing worked.
    smoothY=ssi.savgol_filter(current,smoothBinNumber,3)
    current=smoothY
    
    #Then we can plot the current (smoothY or arraypos3) vs. potential (arraypos5) data.
    if graph == 0:
        fig = plt.figure()
        ax = plt.axes()
        plt.plot(potential,current,color='k')
        ax.set_xlabel('Potential (V)')
        ax.set_ylabel('Current (A)')
    elif graph != 0:
        graph=graph
    return potential,current

#Testing
# file=r'C:\Users\jadse\Desktop\Postdoc\Coding\CV_Fitting\SimulationData\LTO_SECCM-CV.txt'
# bins=50
# pot,cur = plotExperimentalData(file,bins,1)


#This set of code finds the inflection points, differentiates which one are peaks (described below), then fits the slopes of the CVs with lines.
#This is a refined code of Danny's
#This now separates sections into zones (listOfLists) and then performs actions on them.
#You can try experimenting with current, currentBGR, currentBGRS and dd_BGRLine as well

def findAndLabelZones(potential,current,separationValue,percentOfAverageLength):
    d_BGRLine=np.gradient(current)
    #Find the best way to perform peak identification
    peak_pos=(np.where((d_BGRLine[:-1]*d_BGRLine[1:])<0))[0] #for the first derivative, find when an inflection happens
    
    current=np.asarray(current)
    potential=np.asarray(potential)
    
    plt.figure()
    plt.plot(current)
    plt.scatter(peak_pos,current[peak_pos],color='yellow')
    
    listOfLists=[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],]
    
    #This is where separation value comes in. Zone identification ends here.
    listOfListsIndex=0
    counter=0
    for i in peak_pos:
        listOfLists[listOfListsIndex].append(i)
        if counter <= len(peak_pos)-2:
            if abs(peak_pos[counter]-peak_pos[counter+1]) > separationValue:
                listOfListsIndex+=1
        counter+=1
    
    #Trim empty []s in ListOfLists
    i=0
    while i in range(len(listOfLists)):
        if len(listOfLists[i]) == 0:
            listOfLists.pop(i)
        elif len(listOfLists[i]) > 0:
            i+=1
        else:
            i+=1
    
    #Identify which positions are 'long' or 'short' zones.
    #This section returns a boolean array of True=long, Short=False
    #It also creates the array called final_PeakPos which stores the last value for long zones, and min or max for short zones depending on scan direction.
    #Find average length of arrays:
    
    averageLengthList=[]
    for i in listOfLists:
        averageLengthList.append(len(i))
    averageLength=round(sum(averageLengthList)/len(averageLengthList))
    
    final_peakPos=[]
    booleanArray=[] #true is long zone, false is short zone
    for i in range(len(listOfLists)):
        if len(listOfLists[i]) > averageLength*percentOfAverageLength: #True is long!
            final_peakPos.append(listOfLists[i][-1])
            booleanArray.append(True)
        elif len(listOfLists[i]) < averageLength*percentOfAverageLength:
            #Still need to determine max or min!
            if current[listOfLists[i][0]] > sum(current)/len(current):
                final_peakPos.append(max(listOfLists[i]))
            elif current[listOfLists[i][0]] < sum(current)/len(current):
                final_peakPos.append(min(listOfLists[i]))
            booleanArray.append(False)
    
    plt.scatter(final_peakPos,current[final_peakPos],color='red')
    counter=0
    for i in booleanArray:
        if i == True: #True is long!
            plt.text(final_peakPos[counter],current[final_peakPos[counter]],'Long')
            counter+=1
        elif i == False:
            plt.text(final_peakPos[counter],current[final_peakPos[counter]],'Short')
            counter+=1
        else:
            counter+=1
    plt.legend(['Raw current','All inflection points','Filtered Zones'])
    return final_peakPos, booleanArray,listOfLists

#Testing
# file=r'C:\Users\jadse\Desktop\Postdoc\Coding\CV_Fitting\SimulationData\LTO_SECCM-CV.txt'
# bins=10
# potential,current = plotExperimentalData(file,bins,1)
# sepVal=90
# percentOfAverageLength=0.4
# final_peakPos,booleanArray,listOfLists = findAndLabelZones(potential,current,sepVal,percentOfAverageLength)



#Now comes the fitting part!
#This part fits the lines based on long,short,long zones. So if this identification didn't work, then this part fails
#Make sure fittingArray is set appropriately for the number of zones and for lengths.

def findReversibility(final_peakPos, booleanArray, listOfLists,fitting,fittingArrayOption=0): 
    #This creates pp_fits which stores best fit line data from fitting-final_peakPos[i]:final_peakPos[i] for building lines that will be used for backgrounds
    #ideally, fitting is more robust instead of just a user input. Maybe we could create a user fitting array for each peak at least
    pp_fits=[]
    i=0
    start=[]
    end=[]
    counter=0
    fitCounter=0
    location=[]
    while i < (len(final_peakPos)-1):
        if booleanArray[i] == True and booleanArray[i+1] == False: #long, then short! Then we create a line fit to the lead-up to this.
            if fittingArrayOption == 1:
                start.append(final_peakPos[i]-fitting)
                end.append((final_peakPos[i]))
                pp_fits.append(sst.linregress(potential[start[counter]:end[counter]],current[start[counter]:end[counter]]))
                location.append(final_peakPos[i])
                location.append(final_peakPos[i+1])
            elif fittingArrayOption == 0:
                start.append((final_peakPos[i])-fittingArray[fitCounter])
                end.append((final_peakPos[i]))
                pp_fits.append(sst.linregress(potential[start[counter]:end[counter]],current[start[counter]:end[counter]]))
                location.append(final_peakPos[i])
                location.append(final_peakPos[i+1])
                fitCounter+=1
            counter+=1
        elif booleanArray[i] == False:
            i=i
        i+=1

    #Now we make lines for a pretty picture and find the peak heights
    pp_fits_lines=[]
    peak_heights=[]
    iii=0
    while iii < (len(pp_fits)*2):
        quick_pot=[]
        if fittingArrayOption == 1:
            for j in potential[(location[iii])-fitting:location[iii+1]]:
                quick_pot.append(pp_fits[round(iii/2)].slope*j+pp_fits[round(iii/2)].intercept)
        elif fittingArrayOption == 0:
            for j in potential[(location[iii])-fittingArray[round(iii/2)]:location[iii+1]]:
                quick_pot.append(pp_fits[round(iii/2)].slope*j+pp_fits[round(iii/2)].intercept)
        pp_fits_lines.append(quick_pot)
        peak_heights.append(round(abs(current[location[iii+1]]-quick_pot[-1]),11))
        iii+=2
    
    #Now let's plot everything!
    #Peak heights are 2 points.
    linewidth=3
    fig = plt.figure()
    ax = plt.axes()
    plt.plot(potential,current,c='black')
    plt.plot(potential[final_peakPos],current[final_peakPos],linestyle='None',marker='o',markeredgecolor='Purple',markerfacecolor='Purple',markersize=10)
    iiii=0
    counter3=0
    while iiii < (len(pp_fits_lines)*2):
        if fittingArrayOption == 1:
            plt.plot(potential[(location[iiii])-fitting:location[iiii+1]],pp_fits_lines[counter3],lw=linewidth)
        elif fittingArrayOption == 0:
            plt.plot(potential[(location[iiii])-fittingArray[counter3]:location[iiii+1]],pp_fits_lines[counter3],lw=linewidth)
        plt.plot([potential[location[iiii+1]],potential[location[iiii+1]+1]],[current[location[iiii+1]],pp_fits_lines[counter3][-1]],lw=linewidth)
        iiii+=2
        counter3+=1
    ax.set_xlabel('Voltage (V)')
    ax.set_ylabel('Current (nA)')
    
    if len(peak_heights) == 2:
        string='Peak 1 reversibility calculated from first and second peaks are '+str(round(peak_heights[0]/peak_heights[1],2))+'.'
    elif len(peak_heights) != 2:
        string='This program cannot give you the exact reversibility, but will give you peak heights in order.\n Please divide the corresponding peak heights for reversibility. The peak heights are: '
        for i in peak_heights:
            string+=str(round(i,4))+', '
        string=string[-2]+'.'
        
    return string

#Testing
# fitting=40
# # fitting=[200,200,75,30]
# fittingArrayOption=0 #Set to 0 if you want to use 'fittingArray', 1 if you dont want to use 'fitting'. Check above 2 lines.
# findReversibility(final_peakPos, booleanArray, listOfLists,fitting,fittingArrayOption)
