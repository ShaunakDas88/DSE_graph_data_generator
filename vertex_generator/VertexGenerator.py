import json

class VertexGenerator():
			
	def generate_vertices(self, vertex_label, num_vertices):
		vertex_file = open(vertex_label + "_v.json", "w")
		for i in range(num_vertices):
			# TO DO: propertyKey generation
			curr_dict = {"id" : i, "label" : vertex_label}
			vertex_file.write(str(curr_dict)+"\n")
		vertex_file.close()
