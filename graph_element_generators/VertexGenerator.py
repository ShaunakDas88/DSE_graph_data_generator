import os
import json

from PropertyKeyGenerator import PropertyKeyGenerator

class VertexGenerator():
	property_key_generator = None
	vertex_label_dict = None
	out_directory = None

	@classmethod
	def __init__(cls, vertex_label_dict, property_key_dict, out_directory=os.environ["HOME"]):
		cls.vertex_label_dict = vertex_label_dict
		cls.property_key_generator = PropertyKeyGenerator(property_key_dict)
		cls.out_directory = out_directory

	def generate_vertices(self, vertex_label, num_vertices):
		"""

		"""
		file_path = self.out_directory + "/" + vertex_label + "_v.json"
		vertex_file = open(file_path, "w")
		for i in range(num_vertices):
			curr_dict = {"label" : str(vertex_label), "id" : i}
			# generate propertyKeys
			if self.vertex_label_dict[vertex_label]["propertykeys"]:
				for property_key in self.vertex_label_dict[vertex_label]["propertykeys"]:
					curr_dict[property_key] = self.property_key_generator.generate_property_key(property_key)
			vertex_file.write(str(curr_dict)+"\n")
		# close up the data file we wrote
		vertex_file.close()
		return file_path
