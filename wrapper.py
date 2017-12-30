import sys
sys.path.insert(0, '../cta-gamma-ray-analisys/filters')
import Guyserz

def extract_source(cubefile_name):
	gz = Guyserz.Guyserz()
	return gz.perform_extraction(cubefile_name)


