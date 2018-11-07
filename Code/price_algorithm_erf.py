from matplotlib import cm
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D
import math
from scipy.special import erfinv


# euclidian distance between 2 points on the grid
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# returns the price for any arbitary combination of power production and consumption instead of just the values on the grid
def get_price(production, consumption, buy_price):
    length = len(buy_price) - 1
    # first we limit the coordinates of the request to one that is actually inside the precomputed grid (not sure how correct that is)
    while production > length or consumption > length:
        production /= 2.0
        consumption /= 2.0

    # then we find the nearest integers that will be actual entries in the precomputed grid
    low_x = int(math.floor(production))
    low_y = int(math.floor(consumption))

    high_x = int(math.ceil(production))
    high_y = int(math.ceil(consumption))

    # with these integers we can do a weighted average by using the nearest values in the grid
    # for each value we would like to add to the average we first check just in case it is out of bounds
    # finally we add a small value to the division (that 0.01) so that it cant result in an infinite
    sum = 0.0
    total_weight = 0.0
    if steps > low_x >= 0 and steps > low_y >= 0:
        sum += buy_price[low_x][low_y] * 1.0 / (0.01 + distance(low_x, low_y, production, consumption))
        total_weight += 1.0 / (0.01 + distance(low_x, low_y, production, consumption))
    if steps > high_x >= 0 and steps > low_y >= 0:
        sum += buy_price[high_x][low_y] * 1.0 / (0.01 + distance(high_x, low_y, production, consumption))
        total_weight += 1.0 / (0.01 + distance(high_x, low_y, production, consumption))
    if steps > low_x >= 0 and steps > high_y >= 0:
        sum += buy_price[low_x][high_y] * 1.0 / (0.01 + distance(low_x, high_y, production, consumption))
        total_weight += 1.0 / (0.01 + distance(low_x, high_y, production, consumption))
    if steps > high_x >= 0 and steps > high_y >= 0:
        sum += buy_price[high_x][high_y] * 1.0 / (0.01 + distance(high_x, high_y, production, consumption))
        total_weight += 1.0 / (0.01 + distance(high_x, high_y, production, consumption))
    return round(sum / total_weight, 2)


# the function that will be applied to the elements in the diagonal
def interpolation_function(value):
    return math.erf(value)


steps = 251
debug = False
if steps % 2 == 0:
    print('steps have to be odd')
    steps += 1

# instantiate the price values at 0 across the grid
internal_consumption = [0] * steps
internal_production = [0] * steps
buy_price = [[]] * steps
for diagonal_id in range(steps):
    buy_price[diagonal_id] = [0] * steps

deh_sells_electricity = 50
deh_buys_electricity = 30

middle_price = (deh_sells_electricity + deh_buys_electricity) / 2

# if consumption >> production the price is obviously at what we would buy it from deh
buy_price[0][steps - 1] = deh_sells_electricity
# if production >> consumption the price is the reverese
buy_price[steps - 1][0] = deh_buys_electricity

# we want the equations of the graph to revolve around 0 so we will use this offset to achieve that
# eg from [50 30] the values we will have to deal with will be [10 -10]
interpolation_offset = middle_price
interpolation_top = deh_sells_electricity - interpolation_offset
interpolation_bottom = deh_buys_electricity - interpolation_offset

print("maximum price after offset:" + str(interpolation_top))
print("minimum price after offset:" + str(interpolation_bottom))

# interpolation diagonally copy pasting the main diagonal and scaling it for the amount of tiles in the diagonal
for diagonal_id in range(0, steps, 1):
    # this is the size of the diagonal
    diagonal_size = diagonal_id + 1
    if debug:
        print("------ diagonal size:" + str(diagonal_size) + " ---------")
    if diagonal_size is 1:
        buy_price[0][0] = interpolation_offset
        continue

    # tiles apart from the middle one we will have to calculate in the diagonal
    distance_to_interpolation_edge = (diagonal_size - 1.0) / 2.0

    for diagonal_point in range(diagonal_size):

        # weird math that allows us to traverse the points of a diagonal in an array
        write_y = diagonal_id - diagonal_point
        write_x = diagonal_point
        if debug:
            print("trying to write to y:" + str(write_y) + " x:" + str(write_x))

        if write_y >= steps or write_y < 0 or write_x >= steps or write_x < 0:
            print("oob")
        else:
            to_write = round(
                interpolation_function((diagonal_point - (diagonal_size - 1) / 2.0) / distance_to_interpolation_edge)*interpolation_top
                + interpolation_offset, 2)
            buy_price[write_x][write_y] = to_write
            if debug:
                print("wrote :" + str(to_write))

for diagonal_id in range(steps - 2, -1, -1):
    diagonal_size = diagonal_id + 1
    if debug:
        print("------ diagonal size:" + str(diagonal_size) + " ---------")
    if diagonal_size is 1:
        buy_price[steps - 1][steps - 1] = interpolation_offset
        continue

    # tiles apart from the middle one we will have to calculate in the diagonal
    distance_to_interpolation_edge = (diagonal_size - 1) / 2.0
    for diagonal_point in range(diagonal_size):

        # weird math that allows us to traverse the points of a diagonal in an array
        write_y = steps - 1 - diagonal_point
        write_x = steps - 1 - (diagonal_id - diagonal_point)
        if debug:
            print("tried to write to y:" + str(write_y) + " x:" + str(write_x))

        if write_y >= steps or write_y < 0 or write_x >= steps or write_x < 0:

            print("oob")
        else:
            to_write = round(
                interpolation_function((diagonal_point - (diagonal_size - 1) / 2.0) / distance_to_interpolation_edge)*interpolation_top
                + interpolation_offset, 2)
            buy_price[write_x][write_y] = to_write
            if debug:
                print("wrote :" + str(to_write))

# visualization
matrix = np.matrix(buy_price)

X = np.arange(1, 1 + steps, 1)
Y = np.arange(1, 1 + steps, 1)
X, Y = np.meshgrid(X, Y)
fig = plt.figure()
ax = Axes3D(fig)

m = cm.ScalarMappable(cmap=cm.jet)
m.set_array(matrix)

surf = ax.plot_surface(X, Y, matrix, cmap=cm.coolwarm,
                       linewidth=0.5, antialiased=True)

line1z = np.array(buy_price[int((steps - 1) / 2)])
line1y = np.full(steps, int((steps - 1) / 2))
line1x = np.array(range(1, steps+1))

ax.plot3D(line1x, line1y, line1z, 'black')

line2z = np.array([i[int((steps - 1) / 2)] for i in buy_price])
line2x = np.full(steps, int((steps - 1) / 2))
line2y = np.array(range(1, steps+1))

ax.plot3D(line2x, line2y, line2z, 'black')

line2z = np.full(steps, middle_price)
line2x = np.array(range(1, steps+1))
line2y = np.array(range(1, steps+1))

ax.plot3D(line2x, line2y, line2z, 'black')

# Add a color bar which maps values to colors.
fig.colorbar(surf, shrink=0.5, aspect=5)

plt.show()
if False:
    scipy.io.savemat('c:/tmp/arrdata.mat', mdict={'matrix': matrix})

# example prices
# lots of production
print(str(get_price(10000, 1, buy_price)))
# lots of consumption
print(str(get_price(1, 10000, buy_price)))
# even
print(str(get_price(10, 10, buy_price)))
# weird numbers
print(str(get_price(412312.54, 125373.321, buy_price)))
