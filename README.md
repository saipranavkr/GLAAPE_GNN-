# GLAAPE_GNN-
The project aims at developing a neural network that will predict the output of EDA flow at a very early stage using GCNs, by converting RTL netlist file of a design into a graph object where nodes represent the gates and edges representing wires. 

Please copy the required .netlist, .v and .saif files from the NetlistFiles folder according to the training and testing complexity required. 

The RTL file is converted into a dictionary object (key, value pair where keys represent the gates and values represent the wires) before converting into a dgl graph object.

The root file is main_NN_concatenate_wires_name.py
Please run the code from this file.

model.py file contains the GCN model related code.
parse_saif file contains the functions to convert the saif file. Regular expressions are used for ID mapping of gates. The Ground Truths are also claculated in this file.
fixedPointAdder_TC_concatenate.py contains the parsing of all .netlist & .v files into a graph object.
