# CV_Reversibility

This code was made with the help of Danny Chhin and Maddison Eisnor while I was employed in Prof. Janine Mauzeroll's lab as a postdoctoral researcher.

This code takes in separate potential and current columns of a CV, finds the peak heights of the peaks in the CV, and if there are two peak heights in the CV, returns a reversiblity value by dividing the first peak that comes up in the scan by the second peak. If there are any other numbers of peaks, the code returns the peak heights in the order they appeared during the CV.

![Picture3](https://github.com/user-attachments/assets/99c157af-2f1d-43d1-a1cd-fd2933fb6b21)

The code works by finding derivatives of the data and looking for inflections (colored yellow in below image). This depends on the noise of the data and the flatness of it. If the CV is incredibly resistive, this likely won't work and you will need to first subtract a baseline from it. This code has functionality for adding noise to CVs and smoothing CVs to reduce noise. Once a series of inflections are identified, these inflections are grouped by a minimum distance user variable. Play with this variable for datasets with differing data acquisition rates. 

Once zones are created, the zones are designated as 'short' or 'long' by a user variable. This variable takes the average of all zone lengths and sorts the zones by checking if each zone is above (long) or below (short) the product of the user input and the average zone length. Long and short are written on the trace.

![Picture2](https://github.com/user-attachments/assets/683061c7-bb3f-46fe-84bf-3e21ebea3188)

Once separated into zones, a user input is taken for the amount of data points to be used before the dot on the trace as a length. The data points in this length are averaged and fit with a line (red and orange below). These lines are checked for when it intersects with the maximum or minimum of the next short zone. The peak heights are found from the difference between the intercept and peak maximum(length of purple and green lines). Peak heights are reported to the user as described above.

![Picture1](https://github.com/user-attachments/assets/cf1cf1cf-e7c2-4895-8fb6-c7620c14c9f5)
