from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import scipy.io
import matplotlib.pyplot as plt


arrayGL = [[0,17283.98], [0, 18347], [0, 18247.83], [0, 20347], [0, 17317], [0, 6944],[760,7298.13],[4020,7763], [10470,7244.96], [20740,10475], [24980, 10682], [31870, 11828], [50040, 15051.6], [30900, 13489], [31690,13046.99], [30540,14619.5], [28780, 14548.53] 
,[24750,13849.38], [17600, 14992], [11690, 21168.699], [5120, 22752.388], [1600, 19340.79], [0, 19557], [0, 14100] ]
feed_in=12.31
feed_out=28.69
array_z=[27.4,
27.4,
27.4,
27.4,
27.4,
27.4,
26.7,
26.97,
18.45,
17.56,
16.19,
13.66,
15.84,
14.02,
13.71,
14.21,
15.03,
16.76,
19.74,
23.23,
25.65,
26.8,
27.4,
27.4,
27.4
]

for i in range(0,24,1):
   
   
   interior_price=array_z[i]
   
   
   
   if(arrayGL[i][0]>=arrayGL[i][1]):
		#print("Generation is biger: ",+arrayGL[i][0],"Load: ",+arrayGL[i][1], "And interior price is: ",+interior_price)
		generation_gain_tarrifs=arrayGL[i][0]*feed_in/4
		consumer_pay_tarrifs=arrayGL[i][1]*feed_out/4
		
		generation_gain = arrayGL[i][1]*interior_price/4.0 + (arrayGL[i][0]-arrayGL[i][1])*feed_in/4.0
		
		consumer_pay = arrayGL[i][1]*interior_price/4.0
		print("Z = ",+round(interior_price,3))
		print("With tariffs.....")
		print("Generation makes : ",+round(generation_gain_tarrifs,3),"Consumer pays: f",+round(consumer_pay_tarrifs,3))
		#print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		print("With fairness algorithm.....")
		print("Generation makes : f",+round(generation_gain,3),"Consumer pays: f",+round(consumer_pay,3))
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%")
   
   
   
   
   
   else:
		#print("Generation is : ",+arrayGL[i][0],"Load is bigger: ",+arrayGL[i][1], "And interior price is: ",+interior_price)
		generation_gain_tarrifs=arrayGL[i][0]*feed_in/4
		consumer_pay_tarrifs=arrayGL[i][1]*feed_out/4
		print("Z = ",+round(interior_price,3))
		print("With tariffs.....")
		print("Generation makes : ",+round(generation_gain_tarrifs,3),"Consumer pays: f",+round(consumer_pay_tarrifs,3))
		#print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
		
		generation_gain = arrayGL[i][0]*interior_price/4.0 
		
		consumer_pay = arrayGL[i][0]*interior_price/4.0 + (arrayGL[i][1]-arrayGL[i][0])*feed_out/4.0
		print("With fairness algorithm.....")
		
		print("Generation makes : ",+round(generation_gain,3),"Consumer pays: f",+round(consumer_pay,3))
		print("%%%%%%%%%%%%%%%%%%%%%%%%%%")
