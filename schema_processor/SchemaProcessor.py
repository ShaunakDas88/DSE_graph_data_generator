class SchemaProcessor():
	schema_file_path = None
	propertykey_map = None
	vertex_label_map = None
	edge_label_map = None
	propertykey_schema_lines = None
	vertex_schema_lines = None
	edge_schema_lines = None

	@classmethod
	def __init__(cls, schema_file_path):
		cls.schema_file_path = schema_file_path
		cls.propertykey_map = {}
		cls.vertexlabel_map = {}
		cls.edgelabel_map = {}
		cls.propertykey_schema_lines = []
		cls.vertex_schema_lines = []
		cls.edge_schema_lines = []

	def build_propertykey_map(self):
		# example: schema.propertyKey('reviewText').Text().single().create()
		for line in self.propertykey_schema_lines:
			pieces = line.split(".")
			curr_key = pieces[1].split("(")[1].split(")")[0].strip().strip("\"").strip("'").strip()
                        # get rid of unnecessary elements of this array. Eventually, need to determine the type for a
			pieces.pop(1)
                        pieces.pop(0)	# this should be string 'schema'
                        pieces.pop(-1) 		# this should be string 'create()' or 'add()'
			self.propertykey_map[curr_key] = {}
			# determine cardinality of the current vertexLabel
			if "multiple()" in pieces:
				self.propertykey_map[curr_key]["cardinality"] = "multiple"
				pieces.remove("multiple()")
			else:
				self.propertykey_map[curr_key]["cardinality"] = "single"
				pieces.remove("single()")
			# determine if this property has meta-properties
			self.propertykey_map[curr_key]["metaproperties"] = None
			for piece in pieces:
				if piece.startswith("properties("):
					self.propertykey_map[curr_key]["metaproperties"] = [k.strip().strip("\"").strip("'").strip() for k in piece.split("(")[1].split(")")[0].split(",")]
					pieces.remove(piece)
					# no need to iterate through remaining pieces
					break
			# at this point, we should be left with only the type for our propertyKey
			if len(pieces) == 1:
				self.propertykey_map[curr_key]["type"] = pieces[0].split("(")[0].strip()
			else:
				print "We have not fully processed the entirety of line, in order to now infer element type: {l}."
				exit()
#		from pprint import pprint
#		pprint(self.propertykey_map)

	def build_vertexlabel_and_edgelabel_maps(self):
		# example: 
		for line in self.vertex_schema_lines:
			pieces = line.split(".")
			curr_label = pieces[1].split("(")[1].split(")")[0].strip().strip("\"").strip("'").strip()
			self.vertexlabel_map[curr_label] = {"custom_id_key": None, "propertykeys": None, "out": None, "in": None}
			# time to fill up our vertex dict
			for piece in pieces:
				# dealing with a custom id key
				if piece.startswith("partitionKey("):
					self.vertexlabel_map[curr_label]["custom_id_key"] = piece.split("(")[1].split(")")[0].strip().strip("\"").strip("'").strip()
				# dealing with propertykeys
				if piece.startswith("properties("):
					self.vertexlabel_map[curr_label]["propertykeys"] = [k.strip().strip("\"").strip("'").strip() for k in piece.split("(")[1].split(")")[0].split(",")]

		# example: 				
		for line in self.edge_schema_lines:
			pieces = line.split(".")
			curr_label = pieces[1].split("(")[1].split(")")[0].strip("\"").strip("'")
			self.edgelabel_map[curr_label] = {"custom_id_key": None, "propertykeys": None, "from": None, "to": None}
			# time to fill up our edge dict
			for piece in pieces:
				# dealing with custom id
				if piece.startswith("partition("):
					# QUESTION: worry about other keys for custom ids
					self.edgelabel_map[curr_label]["custom_id_key"] = piece.split("(")[1].split(")")[0].strip().strip("\"").strip("'").strip()
				# dealing with propertykeys
				if piece.startswith("properties("):
					self.edgelabel_map[curr_label]["propertykeys"] = [k.strip().strip("\"").strip("'").strip() for k in piece.split("(")[1].split(")")[0].split(",")]
				# dealing with connection information
				if piece.startswith("connection("):
					from_to_list = [k.strip().strip("\"").strip("'").strip() for k in piece.split("(")[1].split(")")[0].split(",")]
					self.edgelabel_map[curr_label]["from"] = from_to_list[0]
					self.edgelabel_map[curr_label]["to"] = from_to_list[1]
					# need to fill in these fields for our vertex dict
					if not self.vertexlabel_map[from_to_list[0]]["out"]:
						self.vertexlabel_map[from_to_list[0]]["out"] = []
					self.vertexlabel_map[from_to_list[0]]["out"].append({"edgelabel": curr_label, "vertexlabel": from_to_list[1]})
					if not self.vertexlabel_map[from_to_list[1]]["in"]:
						self.vertexlabel_map[from_to_list[1]]["in"] = []
                                        self.vertexlabel_map[from_to_list[1]]["in"].append({"edgelabel": curr_label, "vertexlabel": from_to_list[0]})

	def separate_schema_lines(self):
		schema_file = open(self.schema_file_path, "r")
		for line in schema_file:
			pieces = line.split(".")
			if len(pieces) > 1:
				if pieces[1].startswith("propertyKey("):
					self.propertykey_schema_lines.append(line)
				# want to ignore any lines that define indexes, since we are only interested in data generation			
				if pieces[1].startswith("vertexLabel(") and "index" not in line:
					self.vertex_schema_lines.append(line)
				if pieces[1].startswith("edgeLabel(") and "index" not in line:
					self.edge_schema_lines.append(line)
		schema_file.close()

	def build_schema_maps(self):
		self.separate_schema_lines()
		self.build_propertykey_map()
		self.build_vertexlabel_and_edgelabel_maps()
		return self.propertykey_map, self.vertexlabel_map, self.edgelabel_map
