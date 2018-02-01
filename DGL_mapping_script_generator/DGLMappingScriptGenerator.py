class DGLMappingScriptGenerator():
	out_directory = None
	mapping_script_file = None

	@classmethod
	def __init__(cls, out_directory="/home/automaton"):
		cls.out_directory = out_directory
		cls.mapping_script_file = open(cls.out_directory + "/mapping_script.groovy", "w")

	def write_to_file(self, groovy):
		self.mapping_script_file.write(groovy)

	def create_groovy_file_variable(self, label, file_path):
		groovy = "{l}_file = \"{f}\"\n".format(l=label, f=file_path)
		self.write_to_file(groovy)

	def create_groovy_vertex_mapper(self, vertex_label):
		groovy = vertex_label + "_V = {"
		groovy += "\n\tkey 'id'"
		groovy += "\n}\n"
		self.write_to_file(groovy)

	def create_groovy_edge_mapper(self, edge_name, out_label, in_label):
		"""
	outV 'out', {
		key 'id'
	}
	inV 'in', {
		key 'id'
	}
"""
		groovy = edge_name + "_E = {"
		groovy += "\n\toutV 'out', {"
		groovy += "\n\t\tlabel '{o}'".format(o=out_label)
		groovy += "\n\t\tkey 'id'"
		groovy += "\n\t}"
		groovy += "\n\tinV 'in', {"
		groovy += "\n\t\tlabel '{i}'".format(i=in_label)
		groovy += "\n\t\tkey 'id'"
		groovy += "\n\t}"
		groovy += "\n}\n"
		self.write_to_file(groovy)

	def create_groovy_vertex_loader(self, vertex_label):
		"""
		"""
		groovy = "{v}_data = File.json({v}_file)\n".format(v=vertex_label)
		groovy += "load({v}_data).asVertices({v}_V)\n\n".format(v=vertex_label)
		self.write_to_file(groovy)

	def create_groovy_edge_loader(self, edge_name):
		groovy = "{e}_data = File.json({e}_file)\n".format(e=edge_name)
		groovy += "load({e}_data).asEdges({e}_E)\n\n".format(e=edge_name)
		self.write_to_file(groovy)

	def generate_DGL_mapping_script(self, list_of_vertex_labels, list_of_edges, list_of_vertex_data_paths, list_of_edge_data_paths):
		for i in range(len(list_of_vertex_labels)):
			vertex_label = list_of_vertex_labels[i]
			self.create_groovy_file_variable(vertex_label, list_of_vertex_data_paths[i])
			self.create_groovy_vertex_mapper(vertex_label)
			self.create_groovy_vertex_loader(vertex_label)
		for i in range(len(list_of_edges)):
			edge = list_of_edges[i]
			# create edge_name; since same edgeLabel can be purposed between various in/out vertexLabel pairs, we need to be specific about that information as well

			[{u'distribution': {u'name': u'power', u'parameters': {u'decay_constant': 2}}, u'edge_label': u'reviewed', u'from': u'Item', u'to': u'Customer'}]

			edge_name = edge["edge_label"] + "_" + edge["from"] + "_" + edge["to"]
			self.create_groovy_file_variable(edge_name, list_of_edge_data_paths[i])
			self.create_groovy_edge_mapper(edge_name, edge["from"], edge["to"])
			self.create_groovy_edge_loader(edge_name)
		# close up mapping script file
		self.mapping_script_file.close()
