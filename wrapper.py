import sys
relative_path = '../cta-gamma-ray-analysis'
sys.path.insert(0, relative_path)
from classes import Extractor
from matplotlib import pyplot as plt
import numpy as np
from bs4 import BeautifulSoup


def extract_source(cubefile_name):
	xt = Extractor.Extractor(cubefile_name, relative_path+'/')
	return xt.perform_extraction()

def print_graphs(inp, ctl, det):
	print('=================================')
	print('Graphs')
	print("Input_file: {0}\nDetected_file: {1}\nCTLike_file: {2}".format(inp, det, ctl))

	# Open files
	input_xml = open(inp, 'r')
	ctlike_xml = open(ctl, 'r')
	detected_xml = open(det, 'r')

	# Read files
	input = input_xml.read()
	ctlike = ctlike_xml.read()
	detected = detected_xml.read()

	# Plot graphs
	plt.figure(num=1, figsize=(14, 6))

	# # Plot 1: number of spots found
	plt.subplot(121)

	plt.title("Number of spots found")
	plt.xlabel('files')
	plt.ylabel("n° detections")
	labels = ['input', 'detected', 'ctlike']
	counts = [str(input).count("RA"), str(detected).count("RA"), str(ctlike).count("RA")]
	plt.bar(labels, counts, color=['r', 'g', 'b'])

	# # Plot 2: gaussian error
	plt.subplot(122)

	plt.title("Gaussian error")
	plt.xlabel('qualcosa')
	plt.ylabel("qualcos'altro")
	plt.plot([1, 2, 3, 4])

	# # Display
	plt.show()

	# Close files
	input_xml.close()
	ctlike_xml.close()
	detected_xml.close()

	return

