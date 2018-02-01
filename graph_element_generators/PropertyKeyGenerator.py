import random

class PropertyKeyGenerator():
	property_key_dict = None
	property_key_type_dict = None

	@classmethod
	def __init__(cls, property_key_dict):
		cls.property_key_dict = property_key_dict
		cls.property_key_type_dict = {	"Text" : "toString()",
						"Int" : "toInteger()", 
						"Double" : "toDouble()", 
						"Float" : "toFloat()",
						"Timestamp" : "toInteger()"}	# need to figure something out for this

	def generate_property_key(self, property_key):
		property_key_type = self.property_key_dict[property_key]["type"]
		# NOTE: this is a stand-in
		value = random.sample((0,1000), 1)[0]
		# TO DO: handle more exotic types (e.g. Date)
		# handle multiple cardinality
		if self.property_key_dict[property_key]["cardinality"] == "multiple":
			value = [value]
		#  TO DO: need to handle metaproperties
		return value
