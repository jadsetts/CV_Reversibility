#Summary of how to use all functions on a simulated dataset
import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.stats as sst

#Load simulated data
file=r'C:\Users\jadse\Desktop\Postdoc\Coding\CV_Fitting\SimulationData\fakeData.txt'
noiseVal=0.01
potential,current=addNoiseTo(file,noiseVal,1)

#Make specific zones
sepVal=20
percentOfAverageLength=1
final_peakPos,booleanArray,listOfLists = findAndLabelZones(potential,current,sepVal,percentOfAverageLength)

#Find reversibility from peak heights, using an array for fitting
# fittingArray=[20,40]
# fittingArrayOption=0 #Set to 0 if you want to use 'fittingArray', 1 if you dont want to use 'fitting'. Check above 2 lines.
# findReversibility(final_peakPos, booleanArray, listOfLists,fittingArray,fittingArrayOption)

#Find reversibility from peak heights, using a single value for fitting
fitting=20
fittingArrayOption=1 #Set to 0 if you want to use 'fittingArray', 1 if you dont want to use 'fitting'. Check above 2 lines.
findReversibility(final_peakPos, booleanArray, listOfLists,fitting,fittingArrayOption)


#Summary of how to use all functions on a real dataset
import numpy as np
import random
import matplotlib.pyplot as plt
import scipy.signal as ssi
import scipy

#Load data
file=r'C:\Users\jadse\Desktop\Postdoc\Coding\CV_Fitting\SimulationData\LTO_SECCM-CV.txt'
bins=10
potential,current = smoothData(file,bins,1)

#Make specific zones
sepVal=90
percentOfAverageLength=0.4
final_peakPos,booleanArray,listOfLists = findAndLabelZones(potential,current,sepVal,percentOfAverageLength)

# #Find reversibility from peak heights, using a single value for fitting
# fitting=40
# fittingArrayOption=1 #Set to 0 if you want to use 'fittingArray', 1 if you dont want to use 'fitting'. Check above 2 lines.
# findReversibility(final_peakPos, booleanArray, listOfLists,fitting,fittingArrayOption)

#Find reversibility from peak heights, using an array for fitting
fittingArray=[100,200]
fittingArrayOption=0 #Set to 0 if you want to use 'fittingArray', 1 if you dont want to use 'fitting'. Check above 2 lines.
findReversibility(final_peakPos, booleanArray, listOfLists,fittingArray,fittingArrayOption)

