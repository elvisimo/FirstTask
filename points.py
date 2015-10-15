__author__ = 'silend'
import math
import itertools
"""
This script allow you to find the shortest distance between any numbers of points.
It can read source data ( coords of points ) from user input / file.
It uses divide and conquer algorithm, which allows it to run faster on big numbers of points.
Default value to use bruteforce is 3, if you will use it, test different values to reach higher speed
"""

def get_points_coord_manual():  # Get coords from standard input
	points_list = []
	print("Enter coords of points to check or type RUN to finish:")
	while True:
		point = input("\n>>")
		if point == "RUN":
			break
		else:
			try:
				point = tuple(int(x.strip()) for x in point.split(","))
				points_list.append(point)
			except:
				print("Correct format is X, Y where X and Y are coords of point")
				continue
	return points_list


def get_points_coord_file():  # Get coords from file
	print("Enter filename:")
	points_list = []
	while True:
		filename = input("\n>>")
		try:
			with open(filename) as input_file:
				for row in input_file:
					try:
						point = tuple(int(x.strip()) for x in row.split(","))
						points_list.append(point)
					except:
						print("Correct format is X, Y where X and Y are coords of point")
						continue
				break
		except:
			print("Enter a valid filename")
	return points_list


def greeting():  # Enter point into a program - choice how to enter data
	print("Hello! Please choise how you would like to enter points coords:"
			"\nType 1 for manual typing"
			"\nType 2 for uploading via file")
	while True:
		choice = input("\n>>")
		if choice == "1":
			points_list = get_points_coord_manual()
			break
		elif choice == "2":
			points_list = get_points_coord_file()
			break
		else:
			print("Please enter correct value!")
	return points_list


def sort_x(points_list):
	return sorted(points_list, key=lambda tup:tup[0])


def sort_y(points_list):
	return sorted(points_list, key=lambda tup:tup[1])

def dist(tup_1, tup_2):
	return math.sqrt((tup_1[0]-tup_2[0])**2 +(tup_1[1]-tup_2[1])**2)

def bruteforse(points_list):  # find min dist for small lists using O(n**2)
	if len(points_list) < 2:  # we need at least 2 points
		return None, None
	return min((p1, p2)
				for p1, p2 in itertools.combinations(points_list, r=2))


def shortest_dist_split(p_x, p_y, delta, best_pair): # <- a parameter
    ln_x = len(p_x)
    mx_x = p_x[ln_x // 2][0]
    s_y = [x for x in p_y if mx_x - delta <= x[0] <= mx_x + delta]
    best = delta
    for i in range(len(s_y) - 1):
        for j in range(1, min(i + 7, (len(s_y) - i))):
            p, q = s_y[i], s_y[i + j]
            dst = dist(p, q)
            if dst < best:
                best_pair = p, q
                best = dst
    return best_pair


def shortest_dist(x_sort_list, y_sort_list):
	if len(x_sort_list) <= 3:
		return bruteforse(x_sort_list)

	mid = len(x_sort_list) // 2
	left, right = x_sort_list[:mid], x_sort_list[mid:]
	left_x = sort_x(left)
	left_y = sort_y(left)
	right_x = sort_x(right)
	right_y = sort_y(right)
	(p1, q1) = shortest_dist(left_x, left_y)
	(p2, q2) = shortest_dist(right_x, right_y)
	d = min(dist(p1, p2), dist(p2, q2))
	mn = min((p1, q1), (p2, q2), key=lambda x: dist(x[0], x[1]))
	(p3, q3) = shortest_dist_split(x_sort_list, y_sort_list, d, mn)
	return min(mn, (p3, q3), key=lambda x: dist(x[0], x[1]))

def script_body():
	points_list = greeting()
	points_by_x = sort_x(points_list)
	points_by_y = sort_y(points_list)
	point_1, point_2 = shortest_dist(points_by_x, points_by_y)
	#  print("Min dist is between points {} and {}, equals to {}".format(point_1, point_2, dist(point_1, point_2)))
	print(dist(point_1, point_2))




script_body()
