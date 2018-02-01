import os
import random
import math

from PropertyKeyGenerator import PropertyKeyGenerator

class EdgeGenerator():
	edge_label_dict = None
	property_key_generator = None
	out_directory = None

	def __init__(cls, edge_label_dict, property_key_dict, out_directory=os.environ["HOME"]):
		cls.edge_label_dict = edge_label_dict
		cls.property_key_generator = PropertyKeyGenerator(property_key_dict)
		cls.out_directory = out_directory

	def write_dict_to_file(self, edge_dict, edge_file):
		edge_file.write(str(edge_dict) + "\n")

	def sample_edges_and_write(self, out_vertex, out_label, in_label, in_count, num_neighbors, edge_label, data_file):
		curr_in_vertices = random.sample(range(0, in_count), num_neighbors)
		for in_vertex in curr_in_vertices:
			curr_dict = {"out" : {"label" : str(out_label), "id" : str(out_vertex)} , "in" : {"label" : str(in_label), "id" : str(in_vertex)}, "label": str(edge_label)}
			# generate propertyKeys
			if self.edge_label_dict[edge_label]["propertykeys"]:
				for property_key in self.edge_label_dict[edge_label]["propertykeys"]:
        	                        curr_dict[property_key] = self.property_key_generator.generate_property_key(property_key)
			# write the edge data to file
			self.write_dict_to_file(curr_dict, data_file)

	def generate_edges(self, edge_label, edge_stats_dict, vertex_count_dict):
		"""

		"""
		file_path = self.out_directory + "/" + edge_label + "_e.json"
		edge_file = open(file_path, "w")
		out_vertex_label = edge_stats_dict["from"]
		out_count = vertex_count_dict[edge_stats_dict["from"]]
		in_vertex_label = edge_stats_dict["to"]
		in_count = vertex_count_dict[edge_stats_dict["to"]]
		distribution_dict = edge_stats_dict["distribution"]
		distribution = distribution_dict["name"]
		# determine which distribution we want to create edges along
		if distribution == "uniform":
			# get distribution parameters
			lower = distribution_dict["parameters"]["lower"]
	 		upper = distribution_dict["parameters"]["upper"]
			# generate edges
			self.generate_uniform_distribution(edge_label, out_vertex_label, out_count, in_vertex_label, in_count, lower, upper, edge_file)
		if distribution == "power":
			# get distribution parameter
			decay_constant = distribution_dict["parameters"]["decay_constant"]
			# generate edges
			self.generate_power_law_distribution(edge_label, out_vertex_label, out_count, in_vertex_label, in_count, decay_constant, edge_file)
		if distribution == "gaussian":
			# get distribution parameter
			variance = distribution_dict["parameters"]["variance"]
			# generate edges
			self.generate_gaussian_distribution(edge_label, out_vertex_label, out_count, in_vertex_label, in_count, variance, edge_file)
		return file_path

	def generate_uniform_distribution(self, edge_label, out_label, out_count, in_label, in_count, a, b, edge_file):
		# counter for keeping track of which index we left off on, for the out-vertex set
		prev_out_vertex = 0
		# iterate over all admissable out-degree values
		for k in range(a, b+1):
			# the number of out-vertices with degree k
			curr_num_out_vertices = int(float(1)/float(b-a+1)*out_count)
			if prev_out_vertex < out_count:
				#print "ray"
				for curr_out_vertex in range(prev_out_vertex, min(prev_out_vertex + curr_num_out_vertices, out_count)):
					# select neighbors, generate appropriate dicts, write to file
					self.sample_edges_and_write(curr_out_vertex, out_label, in_label, in_count, k, edge_label, edge_file)
			else:
				break
			# update this counter
			prev_out_vertex += curr_num_out_vertices
		# close up our data file
		edge_file.close()

	def generate_power_law_distribution(self, edge_label, out_label, out_count, in_label, in_count, decay_constant, edge_file):
		# compute leading coefficient
		sum_of_fractions = float(0)
		# iterate over all possible out-degree values
		for k in range(1, in_count+1):
			sum_of_fractions += float(1)/float(k**decay_constant)
		coefficient = float(1/sum_of_fractions)
		# counter for keeping track of which index we left off on, for the out-vertex set
		prev_out_vertex = 0
		for k in range(1, in_count):
			# determine the number of out vertices with degree k
			curr_ratio = float(coefficient)/float(k**decay_constant)
			curr_num_out_vertices = int(curr_ratio * out_count)
			# NOTE: since power-law is monotonically decreasing, once we hit zero frequency for an outgoing edge degree, we can stop
			if curr_num_out_vertices == 0 or prev_out_vertex < out_count:
				for curr_out_vertex in range(prev_out_vertex, min(prev_out_vertex + curr_num_out_vertices, out_count)):
					# select neighbors, generate dicts, write them to file
					self.sample_edges_and_write(curr_out_vertex, out_label, in_label, in_count, k, edge_label, edge_file)
			# in this case, we either add no edges, or we have exhausted all vertices in our outgoing set
			else:
				break
			# update this counter
			prev_out_vertex += curr_num_out_vertices
		# close up our data file
		edge_file.close()

	def generate_gaussian_distribution(self, edge_label, out_label, out_count, in_label, in_count, variance, edge_file):
		# compute constants for density function
		mean = in_count/2
		coefficient = float(1)/float(2*math.pi*variance)**(0.5)
		# counter for keeping track of which index we left off on, for the out-vertex set
		prev_out_vertex = 0 
		# iterate over all possible out-degree values
		sum = 0
		for k in range(0, in_count+1):
			# determine the number of out vertices with degree k
			curr_exponent = -(float(k - mean)**2)/float(2*variance)
			curr_ratio = float(coefficient)*float(math.e**(curr_exponent))
			#print "k = {c} : ".format(c=k) + str(curr_ratio)
			curr_num_out_vertices = int(curr_ratio * out_count)
			if curr_num_out_vertices > 0:
				sum = sum + curr_num_out_vertices
			if prev_out_vertex < out_count:
				for curr_out_vertex in range(prev_out_vertex, min(prev_out_vertex + curr_num_out_vertices, out_count)):
					# select neighbors, generate dicts,  write them to file
					self.sample_edges_and_write(curr_out_vertex, out_label, in_label, in_count, k, edge_label, edge_file)
			# in this case, we either add no edges, or we have exhausted all vertices in our outgoing set
			else:
				break
			# update this counter
			prev_out_vertex += curr_num_out_vertices
		# close up our data file
		edge_file.close()
