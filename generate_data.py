import os
import json
from optparse import OptionParser

from schema_processor.SchemaProcessor import SchemaProcessor
from input_validator.InputValidator import InputValidator
from graph_element_generators.VertexGenerator import VertexGenerator
from graph_element_generators.EdgeGenerator import EdgeGenerator
from DGL_mapping_script_generator.DGLMappingScriptGenerator import DGLMappingScriptGenerator

parser = OptionParser()
parser.add_option("--schema_file_path", dest="schema_file_path", help="Where the schema file is located")
parser.add_option("--graph_stats_path", dest="graph_stats_path", help="location of the json file which specifies the number of vertices for each vertexLabel, edge-degree distribution for each edgeLabel, etc.")
parser.add_option("--output_directory", dest="output_directory", default=os.environ["HOME"], help="directory where to write files to")
(options, args) = parser.parse_args()

# process the provided schema first
if options.schema_file_path:
	schema_file_path = options.schema_file_path
	schema_processor = SchemaProcessor(schema_file_path)
	property_key_dict, vertex_label_dict, edge_label_dict = schema_processor.build_schema_element_dicts()
else:
	print "\nPlease provide path for --schema_file_path flag.\n"
	exit()

# get the dict corresponding to statistics user wants to define for their graph
if options.graph_stats_path:
        path_to_graph_stats_file = options.graph_stats_path
        graph_stats_dict = json.load(open(path_to_graph_stats_file, "r"))
	vertex_stats_list = graph_stats_dict["vertex_stats"]
	edge_stats_list = graph_stats_dict["edge_stats"]
else:
        print "\nPlease provide path for --graph_stats_path\n"
        exit()

# Sanity check that schema and provided stats json are compatible
input_validator = InputValidator(vertex_label_dict, edge_label_dict, vertex_stats_list, edge_stats_list)
input_validator.validate_input()

# make directory for output files
if not os.path.exists(options.output_directory):
	os.makedirs(options.output_directory)

# generate vertex data
vertex_count_dict = {}
list_of_vertex_data_paths = []
vertex_generator = VertexGenerator(vertex_label_dict, property_key_dict, options.output_directory)
for vertex_stats_dict in vertex_stats_list:
	vertex_label = vertex_stats_dict["vertex_label"]
	list_of_vertex_data_paths.append(vertex_generator.generate_vertices(vertex_label, vertex_stats_dict["count"]))
	vertex_count_dict[vertex_stats_dict["vertex_label"]] = vertex_stats_dict["count"]

# generate edge data
list_of_edge_data_paths = []
edge_generator = EdgeGenerator(edge_label_dict, property_key_dict, options.output_directory)
for edge_stats_dict in edge_stats_list:
	edge_label = edge_stats_dict["edge_label"]
	list_of_edge_data_paths.append(edge_generator.generate_edges(edge_label, edge_stats_dict, vertex_count_dict))

# generate the DGL mapping script for this data
dgl_mapping_script_generator = DGLMappingScriptGenerator(options.output_directory)
dgl_mapping_script_generator.generate_DGL_mapping_script(vertex_count_dict.keys(), edge_stats_list, list_of_vertex_data_paths, list_of_edge_data_paths)
