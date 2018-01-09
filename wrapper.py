import sys
relative_path = '../cta-gamma-ray-analysis'
sys.path.insert(0, relative_path)
from classes import Extractor
from matplotlib import pyplot as plt
from bs4 import BeautifulSoup

def extract_source(cubefile_name):
	xt = Extractor.Extractor(cubefile_name, relative_path+'/')
	return xt.perform_extraction()

def print_graphs(inp, ctl, det):
	input_xml = open(inp, 'r')
	ctlike_xml = open(ctl, 'r')
	hypotesis_xml = open(det, 'r')

	input = BeautifulSoup(input_xml, "html.parser")
	ctlike = BeautifulSoup(ctlike_xml, "html.parser")
	hypotesis = BeautifulSoup(hypotesis_xml, "html.parser")

	print("sorgenti in input = {0}".format(input.get_text().count("<source")))
	print("sorgenti in ctlike = {0}".format(ctlike.get_text().count("<source")))
	print("sorgenti in hypotesis = {0}".format(hypotesis.get_text().count("<source")))
	return

