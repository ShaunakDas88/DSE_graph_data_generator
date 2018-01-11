import json
from optparse import OptionParser

from schema_processor.SchemaProcessor import SchemaProcessor
from vertex_generator.VertexGenerator import VertexGenerator
from edge_generator.EdgeGenerator import EdgeGenerator

parser = OptionParser()
parser.add_option("--schema_file_path", dest="schema_file_path", help="Where the schema file is located")
parser.add_option("--edge_distribution", dest="edge_distribution", default="uniform", help="How we want the edge data to be distributed between different vertexLabels")
parser.add_option("--mapping_script_file_name", dest="mapping_script_file", default="mapping-script.groovy", help="Where to create DGL mapping script file")
parser.add_option("--path_to_graph_statistical_specs", dest="graph_stats_specs", help="location of the json file which specifies the number of vertices for each vertexLabel, edge-degree distribution for each edgeLabel, etc.")

(options, args) = parser.parse_args()

path_to_graph_stats_specs_file = options.graph_stats_specs
# null check
graph_stats_specs_dict = json.load(open(path_to_graph_stats_specs_file, "r"))

# process the provided schema first
# TO DO

# this dict will be keyed by vertexLabels, valued by their user-defined count
vertex_count_dict = {}
vertex_generator = VertexGenerator()
vertex_stats_specs_dict = graph_stats_specs_dict["vertex_stats"]
for vertex_dict in vertex_stats_specs_dict:
	vertex_generator.generate_vertices(vertex_dict["vertex_label"], vertex_dict["count"])
	vertex_count_dict[vertex_dict["vertex_label"]] = vertex_dict["count"]

# generate edge data
edge_generator = EdgeGenerator()
edge_stats_specs_dict = graph_stats_specs_dict["edge_stats"]
for edge_dict in edge_stats_specs_dict:
	edge_generator.generate_edges(edge_dict, vertex_count_dict)
