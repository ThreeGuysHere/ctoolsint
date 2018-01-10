from matplotlib import pyplot as plt, mlab
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
				curr.append(param.get('value'))
			lf.append(curr)
	return lf


def extract_source(cubefile_name):
	xt = Extractor.Extractor(cubefile_name, relative_path+'/')
	return xt.perform_extraction()


def print_graphs(inp, ctl, det):
	print('=================================')
	print('Graphs')
	print("Input_file: {0}\nDetected_file: {1}\nCTLike_file: {2}".format(inp, det, ctl))

	# Parse files
	input_res = parse_xml(inp)
	print(input_res)
	detection_res = parse_xml(det)
	print(detection_res)
	ctlike_res = parse_xml(ctl)
	print(ctlike_res)

	# Plot graphs
	plt.figure(num=1, figsize=(14, 6))

	# # Plot 1: number of spots found
	plt.subplot(121)

	plt.title("Number of spots found")
	plt.xlabel('files')
	plt.ylabel("n° detections")
	labels = ['input', 'detected', 'ctlike']
	counts = [len(input_res), len(detection_res), len(ctlike_res)]
	plt.bar(labels, counts, color=['r', 'g', 'b'])

	# # Plot 2: gaussian error
	plt.subplot(122)

	plt.title("Gaussian error")
	plt.xlabel('qualcosa')
	plt.ylabel("qualcos'altro")
	mu = 0
	variance = 1
	sigma = np.sqrt(variance)
	x = np.linspace(mu - 3*sigma, mu+3*sigma, 100)
	plt.plot(x, mlab.normpdf(x, mu, sigma))

	# # Display
	plt.show()

	return

