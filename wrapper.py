import sys
sys.path.insert(0, '../cta-gamma-ray-analysis')
import Extractor

def extract_source(cubefile_name):
	xt = Extractor.Extractor()
	return xt.perform_extraction(cubefile_name)


