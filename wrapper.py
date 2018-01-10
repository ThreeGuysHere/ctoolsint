import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import sys
relative_path = '../cta-gamma-ray-analysis'
sys.path.insert(0, relative_path)
from classes import Extractor


def parse_xml(filename):
	tree = ET.parse(filename)
	doc = tree.getroot()

	lf = []
	for source in doc.findall("source"):
		if source.get('type') == 'PointSource':
			curr = [source.get('name')]
			for param in source.findall("spatialModel/parameter"):
				curr.append(float(param.get('value')))
			lf.append(curr)
	return lf


def match_sources(input, other):
	listlist = []
	for found in other:
		current_dist = []
		for i in range(len(input)):
			dist = euclidean_distance(found[1:], input[i][1:])
			current_dist.append(dist)
		min_index = np.argmin(current_dist)
		# mapping found <-> input[min_index]
		listlist.append([found, input[min_index]])
	return listlist


def euclidean_distance(x, y):
	return np.sqrt(np.sum(np.square(np.subtract(x, y))))


def extract_source(cubefile_name):
	xt = Extractor.Extractor(cubefile_name, relative_path+'/')
	return xt.perform_extraction()


def print_graphs(inp, ctl, det):
	print('=================================')
	print('Graphs')

	# Parse files
	print("Input_file: {0}".format(inp))
	input_res = parse_xml(inp)
	print(input_res)

	print("Detected_file: {0}".format(det))
	detection_res = parse_xml(det)
	print(detection_res)

	# print("CTLike_file: {0}".format(ctl))
	# ctlike_res = parse_xml(ctl)
	# print(ctlike_res)

	# Find matches
	# # Input vs Detected
	print("Matches: input vs detected")
	matches = match_sources(input_res, detection_res)
	print(matches)

	# # # Input vs CTLike
	# matches2 = match_sources(input_res, ctlike_res)
	# print(matches2)

	# Plot graphs
	fig = plt.figure(num=1, figsize=(20, 5))
	fig.canvas.set_window_title('Graphs')
	fig.suptitle("Gamma-ray analysis")

	# # Plot 1: number of spots found
	plt.subplot(131)

	plt.title("Number of spots found")
	plt.xlabel('files')
	plt.ylabel("n° detections")
	plt.yticks(range(0, np.max([len(input_res), len(detection_res)])+1))

	labels = ['input', 'detected']
	counts = [len(input_res), len(detection_res)]
	plt.bar(labels, counts, color=['r', 'g'])

	# # Plot 2: Detections
	plt.subplot(132)

	plt.title("Matches")
	plt.xlabel('RA')
	plt.ylabel("Dec")
	# plt.autoscale = False
	# plt.xlim(80,86)
	# plt.ylim(21, 23)

	for match in matches:
		plt.plot(match[1][1], match[1][2], 'r+')  # input
		plt.plot(match[0][1], match[0][2], 'g^')  # detected

	# # Plot 3: euclidean distance
	plt.subplot(133)

	plt.title("Euclidean distance")
	plt.xlabel('RA')
	plt.ylabel("Dec")

	x = np.linspace(-0.2, 0.2, 100)
	x_data, y_data = np.meshgrid(x, x)
	z_data = np.sqrt(np.add(np.square(x_data), np.square(y_data)))
	cs = plt.contourf(x_data, y_data, z_data, levels=np.linspace(0, 1, 50))
	plt.colorbar(cs, format="%.2f")

	for match in matches:
		x_coord = match[0][1] - match[1][1]
		y_coord = match[0][2] - match[1][2]
		plt.plot(x_coord, y_coord, 'r+')
		plt.text(x_coord, y_coord, match[0][0])

	# # Display
	plt.show()

	return

