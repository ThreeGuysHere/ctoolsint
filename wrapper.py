import sys
sys.path.insert(0, '../cta-gamma-ray-analysis')
from classes import Extractor

def extract_source(cubefile_name):
	xt = Extractor.Extractor(cubefile_name)
	return xt.perform_extraction()


