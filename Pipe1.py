import os
import gammalib
import ctools
import cscripts
import GammaPipe
import glob

# ============================= #
# Run binned in-memory pipeline #
# ============================= #
def pipeline_binned(model, outname, resname="result.xml"):
	print('Run binned pipeline')
	"""
	Run binned pipeline
	"""
	# Set usage string
	usage = 'Pipe1.py [-observation obsfilename] [-simmodel simmodelfilename] [-anamodel analysismodelfilename] [-confpipe configuration pipe][-seed seed]'

	# Set default options
	options = [{'option': '-observation', 'value': 'examples/obs_crab.xml'}, {'option': '-simmodel', 'value': ''}, {'option': '-anamodel', 'value': 'examples/crab.xml'}, {'option': '-runconf', 'value': ''}, {'option': '-eventfilename', 'value': ''}, {'option': '-seed', 'value': '0'}]

	# Get arguments and options from command line arguments
	args, options = cscripts.ioutils.get_args_options(options, usage)

	# Extract script parameters from options
	obsfilename = options[0]['value']
	simfilename = model
	analysisfilename = options[2]['value']
	runconffilename = options[3]['value']
	eventfilename = options[4]['value']
	in_seed = int(options[5]['value'])

	print(obsfilename)
	print(simfilename)
	print(analysisfilename)
	print(runconffilename)
	print(eventfilename)

	gp = GammaPipe.GammaPipe()
	
	gp.init(obsfilename, simfilename, analysisfilename, runconffilename, eventfilename)

	# Run analysis pipeline
	matches = gp.run_pipeline(seed=in_seed, outname=outname, resname=resname)

	# Return
	return


# ======================== #
# Main routine entry point #
# ======================== #
if __name__ == '__main__':

	# Run binned in-memory pipeline
	matches = []
	all_xml = ["examples/batches/1s/a.xml", "examples/batches/1s/b.xml", "examples/batches/1s/c.xml",
			   "examples/batches/1s/d.xml", "examples/batches/2s/a.xml", "examples/batches/2s/b.xml",
			   "examples/batches/2s/c.xml", "examples/batches/2s/d.xml", "examples/batches/3s/a.xml",
			   "examples/batches/3s/b.xml", "examples/batches/3s/c.xml", "examples/batches/3s/d.xml"]
	i = 1
	for model in all_xml:
		for j in range(100):
			pipeline_binned(model, "resultset/out"+str(i)+"_"+str(j)+".xml")
		i += 1

	print(matches)
