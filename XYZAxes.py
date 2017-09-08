import urllib
import matplotlib.pyplot as plt
import csv
import sys
from math import *
from matplotlib import *
import numpy as np
from scipy import *
import scipy.signal as signal
import scipy.ndimage as ndimage

get_ipython().magic(u'matplotlib inline')


# File path for the data you want to graph
action = 'Untrimmed Accelerometer Data/S5/acc_S5pushup1_0'
file_name = action + '.csv'
csv_reader = csv.reader(open(file_name))

# Array of arrays of data in the csv file
verts = []

for row in csv_reader:
    verts.append(row)

time = []
x = []
y = []
z = []

# Get data from each row in the verts array and put it in the corresponding array
for vert in verts:
    time.append(float(vert[0])-float(verts[0][0]))
    x.append(float(vert[1]))
    y.append(float(vert[2]))
    z.append(float(vert[3]))
    
# File path to save the data
directory = "C:/Users/Student.121-GMASTER/Box Sync/Junior/SIR/Figures"
savepath = os.path.join(directory, "Untrimmed 3 Axis Graph.svg")

# Graph the data
ax = plt.subplot(111)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
plt.tick_params(axis='both', which='major', labelsize=14)
plt.tick_params(axis='both', which='minor', labelsize=14)
plt.plot(time, x, color="green")
plt.plot(time, y, color="red")
plt.plot(time, z, color="blue")
plt.legend(['X', 'Y', 'Z'])
plt.xlabel('time (s)', size = 14)
plt.ylabel('acceleration (m/$s^2$)', size = 14)
plt.title("Accelerometer Axes")
plt.savefig(savepath)
plt.show()