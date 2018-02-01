from pprint import pprint
from collections import Counter

class InputValidator():
	vertexlabel_dict = None
	edgelabel_dict = None
	vertex_stats_list = None
	edge_stats_list = None
	# these arrays will store any vertexLabels and edgeLabels that do not belong in the schema
	invalid_vertex_labels = None
	invalid_edges = None
	# these arrays will store any edgeLabels which were given 
	no_distribution_edges = None
	no_distribution_name_edges = None
	no_distribution_param_edges = None
	invalid_distribution_param_edges = None

	@classmethod
	def __init__(cls, vertexlabel_dict, edgelabel_dict, vertex_stats_list, edge_stats_list):
		cls.vertexlabel_dict = vertexlabel_dict
		cls.edgelabel_dict = edgelabel_dict
		cls.vertex_stats_list = vertex_stats_list
		cls.edge_stats_list = edge_stats_list
		cls.invalid_vertex_labels = []
		cls.invalid_edges = []
		cls.no_distribution_edges = []
		cls.no_distribution_name_edges = []
		cls.no_distribution_param_edges = []
		cls.invalid_distribution_param_edges = []

	def validate_edge_distribution_input(self):
		"""	
		This method will validate whether the correct parameters were provided for a given 
		edge-degree distribution
	
		"""
		for edge_dict in self.edge_stats_list:
			edge_label = edge_dict["edge_label"]
			if "distribution" not in edge_dict:
				self.no_distribution_edges.append(edge_label)
			else:
				distribution_dict = edge_dict["distribution"]
				if "name" not in distribution_dict:
					no_distribution_name_edges.append(edge_label)
				# the case that no parameters are provided for the edge-degree distribution
				elif "parameters" not in edge_dict["distribution"]:
						no_distribution_params_edges.append(edge_label)
				# the case that parameters are provided for the edge-degree distribution
				else:
					distribution_parameters_dict = distribution_dict["parameters"]
					info_dict = {"edge_label" : edge_label, "distribution_name" : distribution_dict["name"], "error" : "invalid distribution parameters"}
					if distribution_dict["name"] is "uniform":
						if ["lower", "upper"] not in distribution_parameters_dict:
							invalid_parameters_edges.append(info_dict)
					elif distribution_dict["name"] is "power":
						if "decay constant" not in distribution_parameters_dict:
							invalid_parameters_edges.append(info_dict)
					elif distribution_dict["name"] is "gaussian":
						if "variance"  not in distribution_parameters_dict:
							invalid_parameters_edges.append(info_dict)

	def validate_vertices(self):
		schema_vertex_labels = [vertex_label for vertex_label in self.vertexlabel_dict]
		stats_vertex_labels = [vertex_dict["vertex_label"] for vertex_dict in self.vertex_stats_list]
		self.invalid_vertex_labels = list(Counter(stats_vertex_labels) - Counter(schema_vertex_labels))
		if len(self.invalid_vertex_labels) > 0:
			print "\nThe following vertexLabels were found in the provided stats file, but NOT in the provided schema file. Please make sure the data in the two files is compatible:"
			for vertex_label in self.invalid_vertex_labels:
				print vertex_label
			print "\n"
			exit()

	def validate_edges(self):
		schema_edges = [{"label" : edgelabel, "out" : self.edgelabel_dict[edgelabel]["from"], "in" : self.edgelabel_dict[edgelabel]["to"]} for edgelabel in self.edgelabel_dict]
		stats_edges = [{"label" : edge_dict["edge_label"], "out" : edge_dict["from"], "in" : edge_dict["to"]} for edge_dict in self.edge_stats_list]
		#pprint(schema_edges)
		#pprint(stats_edges)
		for edge in stats_edges:
			if edge not in schema_edges:
				self.invalid_edges.append(edge)
		if len(self.invalid_edges) > 0:
			print "\nThe following edges were found in the provided stats file, but NOT in the provided schema  file. Please make sure the data in the two files is compatible:"
			for edge in self.invalid_edges:
				print edge
			print "\n"
			exit()

	def validate_input(self):
		self.validate_vertices()
		self.validate_edges()
		self.validate_edge_distribution_input()
