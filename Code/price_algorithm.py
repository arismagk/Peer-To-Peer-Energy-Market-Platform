from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import scipy.io
import matplotlib.pyplot as plt
import math 

steps=101


if (steps%2==0) :
    print('steps have to be odd')


internal_consumption=[0]*steps
internal_production=[0]*steps
buy_price=[[]]*steps
for i in range(steps):
    buy_price[i]=[0]*steps
    
deh_sells_electricity = 50
deh_buys_electricity = 30

middle_price=(deh_sells_electricity+deh_buys_electricity)/2

buy_price[0][steps-1]=deh_sells_electricity

buy_price[steps-1][0]=deh_buys_electricity


for i in range(steps):
    buy_price[i][i]=middle_price


interpolation_offset=middle_price
interpolation_top=deh_sells_electricity-interpolation_offset
interpolation_bottom=deh_buys_electricity-interpolation_offset

distance_to_interpolation_edge=(steps-1)/2

interpolation_factor_at_edge=interpolation_top**(1.0/3.0)
interpolation_factor=interpolation_factor_at_edge/distance_to_interpolation_edge

print("int factor"+str(interpolation_factor))



#interpolation using x^3
for i in range(steps):
    buy_price[steps-1-i][i]=round((interpolation_factor*(i-(steps-1)/2))**(3)+interpolation_offset,2)


#interpolation diagonally copy pasting the main diagonal
for i in range(0,steps*2-1,2) :
    diagonal_size=i+1
    print("------ diagonal size:"+str(diagonal_size)+" ---------")
    for k in range(diagonal_size):
        print("i:"+str(i)+"  k:"+str(k))

        write_y=i-k
        write_x=k

        read_y=(steps-1)/2+(diagonal_size-1)/2-k
        read_x=(steps-1)/2-(diagonal_size-1)/2+k

        print("trying to write to y:"+str(write_y)+" x:"+str(write_x)+" from y:"+str(read_y)+" x:"+str(read_x))

        if write_y>=steps or write_y<0 or write_x>=steps or write_x<0 or read_y>=steps or read_y<0 or read_x>=steps or read_x<0 :
            print("oob")
            
        else :
            
           
            buy_price[write_y][write_x]= buy_price[read_y][read_x]



for y in range(0,steps) :
    for x in range(0,steps) :
        if buy_price[y][x]==0 :

            sum=0
            existed=0
            above_read=[y-1,x]
            left_read=[y,x-1]
            below_read=[y+1,x]
            right_read=[y,x+1]

            if above_read[0]<steps and above_read[0]>=0 and above_read[1]<steps and above_read[1]>=0 :
                sum+=buy_price[above_read[0]][above_read[1]]
                existed+=1
            if left_read[0]<steps and left_read[0]>=0 and left_read[1]<steps and left_read[1]>=0 :
                sum+=buy_price[left_read[0]][left_read[1]]
                existed+=1
            if below_read[0]<steps and below_read[0]>=0 and below_read[1]<steps and below_read[1]>=0 :
                sum+=buy_price[below_read[0]][below_read[1]]
                existed+=1
            if right_read[0]<steps and right_read[0]>=0 and right_read[1]<steps and right_read[1]>=0 :
                sum+=buy_price[right_read[0]][right_read[1]]
                existed+=1

            buy_price[y][x]=round(sum*1.0/existed,2)


matrix=np.matrix(buy_price)

#print(matrix)

X = np.arange(1, 1+steps,1)
Y = np.arange(1, 1+steps,1)
X,Y=np.meshgrid(X,Y)
fig = plt.figure()
ax = fig.gca(projection='3d')

m = cm.ScalarMappable(cmap=cm.jet)
m.set_array(matrix)

surf =ax.plot_surface(X,Y,matrix, cmap=cm.coolwarm,
                       linewidth=0.1, antialiased=False)


# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()

scipy.io.savemat('c:/tmp/arrdata.mat', mdict={'matrix': matrix})
