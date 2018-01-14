import matplotlib.pyplot as plt
import numpy as np
import xml.etree.ElementTree as ET
import matplotlib.mlab as mlab
from scipy.stats import norm

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


######################################################

all_xml = ["examples/batches/1s/a.xml", "examples/batches/1s/b.xml", "examples/batches/1s/c.xml",
			   "examples/batches/1s/d.xml", "examples/batches/2s/a.xml", "examples/batches/2s/b.xml",
			   "examples/batches/2s/c.xml", "examples/batches/2s/d.xml", "examples/batches/3s/a.xml",
			   "examples/batches/3s/b.xml", "examples/batches/3s/c.xml", "examples/batches/3s/d.xml"]
num_input = 0
num_dec = 0
matches = []

for i in range(1, 13):
	# Parse files
	inp = all_xml[i-1]
	#print("Input_file: {0}".format(inp))
	input_res = parse_xml(inp)
	#print(input_res)

	det = "out/out"+str(i)+".xml"
	#print("Detected_file: {0}".format(det))
	detection_res = parse_xml(det)
	#print(detection_res)

	num_input += len(input_res)
	num_dec += len(detection_res)

	##################################################################################
	# Find matches
	# # Input vs Detected
	#print("Matches: input vs detected")
	matches.append(match_sources(input_res, detection_res))


fig = plt.figure(num=1, figsize=(20, 5))
fig.canvas.set_window_title('Graphs')
fig.suptitle("Gamma-ray analysis")

# # Plot 1: number of spots found
plt.subplot(131)

plt.title("Number of spots found")
plt.xlabel('files')
plt.ylabel("n° detections")
plt.yticks(range(0, np.max([num_dec, num_input]) + 1))

labels = ['input', 'detected']
counts = [num_input, num_dec]
plt.bar(labels, counts, color=['r', 'g'])

#################################
# # Plot 2: Detections
plt.subplot(132)

plt.title("Matches")
plt.xlabel('RA')
plt.ylabel("Dec")
# plt.autoscale = False
# plt.xlim(80,86)
# plt.ylim(21, 23)


print(matches)

for images in matches:
	for match in images:
		plt.plot(match[1][1], match[1][2], 'r+')  # input
		plt.plot(match[0][1], match[0][2], 'g^')  # detected

##########################################
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

for images in matches:
	for match in images:
		x_coord = match[0][1] - match[1][1]
		y_coord = match[0][2] - match[1][2]
		plt.plot(x_coord, y_coord, 'r+')
		#plt.text(x_coord, y_coord, match[0][0])
###############################################
# # Plot 4: binned histogram with fitting gaussian
plt.figure(4)

distances = []
for images in matches:
	for match in images:
		dist = euclidean_distance([match[0][1], match[0][2]], [match[1][1], match[1][2]])
		distances.append(dist)

hist_bins = np.arange(-0.05, 0.06, 0.01)
gauss_bins = np.arange(-0.05, 0.06, 0.001)

(mu, sigma) = norm.fit(distances)
y = mlab.normpdf(gauss_bins, mu, sigma)

plt.plot(np.arange(-0.05, 0.06, 0.001), y, 'r--', linewidth=2)
plt.hist(distances, bins=hist_bins, normed=1, facecolor='green', alpha=0.75)

plt.xlabel('Bins')
plt.ylabel('Hist. probabilities')
plt.title(r'$\mathrm{Fitting\ gaussian:}\ \mu=%.3f,\ \sigma=%.3f$' % (mu, sigma))
plt.grid(True)

##############################################
# # Display
plt.show()