# Import necessary libraries
import re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
# Global variable for info dictionary item which will be imported to parseVCD file
info = {}

# Global variables for storing core inputs and outputs
core_ips = []
core_ops = []

#Global variable to store edge information
edges = {}

attrs = {}

assign = {}

INVD0 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

INVD1 = [1.,0.,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

INVD2 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

INVD3 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

INVD6 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

CKND0 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

CKND1 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

CKND2 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

CKNXD0 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

CKNXD1 = [1.0,0.0,0.,0.,0.,0.,4.,4.,0.,0.,4.,4.,0.,0.,0.,0.,0.]

ND2D0 = [0.5,0.,0.,0.,0.,0.,4.,2.,2.,0.,2.,1.,1.,0.,2.,1.,1.]

ND2D1 = [0.5,0.,0.,0.,0.,0.,4.,2.,2.,0.,2.,1.,1.,0.,2.,1.,1.]

CKND2D0 = [0.5,0.,0.,0.,0.,0.,4.,2.,2.,0.,2.,1.,1.,0.,2.,1.,1.]

CKND2D1 = [0.5,0.,0.,0.,0.,0.,4.,2.,2.,0.,2.,1.,1.,0.,2.,1.,1.]

CKND2D2 = [0.5,0.,0.,0.,0.,0.,4.,2.,2.,0.,2.,1.,1.,0.,2.,1.,1.]

NR2D0 = [0.5,1.,1.,2.,0.,1.,1.,2.,0.,2.,2.,4.,0.,0.,0.,0.,0.]

NR2D1 = [0.5,1.,1.,2.,0.,1.,1.,2.,0.,2.,2.,4.,0.,0.,0.,0.,0.]

NR2D3 = [0.5,1.,1.,2.,0.,1.,1.,2.,0.,2.,2.,4.,0.,0.,0.,0.,0.]

NR2XD0 = [0.5,1.,1.,2.,0.,1.,1.,2.,0.,2.,2.,4.,0.,0.,0.,0.,0.]

NR2XD1 = [0.5,1.,1.,2.,0.,1.,1.,2.,0.,2.,2.,4.,0.,0.,0.,0.,0.]

AOI22D0 = [0.375,0.25,0.75,0.625,0.375,0.75,2.25,1.875,1.125,0.625,1.875,1.5625,0.9375,0.375,1.125,0.9375,0.5625]

AOI22D1 = [0.375,0.25,0.75,0.625,0.375,0.75,2.25,1.875,1.125,0.625,1.875,1.5625,0.9375,0.375,1.125,0.9375,0.5625]

AOI33D0 = [0.4375,0.0625,0.4375,0.171875,0.328125,0.4375,3.0625,1.203125,2.296875,0.171875,1.203125,0.47265625,0.90234375,0.328125,2.296875,0.90234375,1.72265625]

OAI33D0 = [0.4375,1.72265625,0.90234375,2.296875,0.328125,0.90234375,0.47265625,1.203125,0.171875,2.296875,1.203125,3.0625,0.4375,0.328125,0.171875,0.4375,0.0625]

OAI33D1 = [0.4375,1.72265625,0.90234375,2.296875,0.328125,0.90234375,0.47265625,1.203125,0.171875,2.296875,1.203125,3.0625,0.4375,0.328125,0.171875,0.4375,0.0625]

MUX4ND0 = [0.3125,0.5625,0.9375,0.9375,0.5625,0.9375,1.5625,1.5625,0.9375,0.9375,1.5625,1.5625,0.9375,0.5625,0.9375,0.9375,0.5625]

MUX3ND0 = [0.3125,0.5625,0.9375,0.9375,0.5625,0.9375,1.5625,1.5625,0.9375,0.9375,1.5625,1.5625,0.9375,0.5625,0.9375,0.9375,0.5625]

AN2D0 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

AN2XD1 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

CKAN2D0 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

CKAN2D1 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

CKAN2D2 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

CKAN2D4 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

CKAN2D8 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

IND2D0 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

IND2D1 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

IND2D2 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

INR2D0 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

INR2D1 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

AOI21D0 = [0.375,1.,1.,1.5,0.5,1.,1.,1.5,0.5,1.5,1.5,2.25,0.75,0.5,0.5,0.75,0.25]

AOI21D1 = [0.375,1.,1.,1.5,0.5,1.,1.,1.5,0.5,1.5,1.5,2.25,0.75,0.5,0.5,0.75,0.25]

OAI21D0 = [0.375,0.25,0.75,0.5,0.5,0.75,2.25,1.5,1.5,0.5,1.5,1.,1.,0.5,1.5,1.,1.]

MAOI22D0 = [0.375,0.25,0.75,0.625,0.375,0.75,2.25,1.875,1.125,0.625,1.875,1.5625,0.9375,0.375,1.125,0.9375,0.5625]

FCICOND1 = [0.375,0.25,0.75,0.75,0.25,0.75,2.25,2.25,0.75,0.75,2.25,2.25,0.75,0.25,0.75,0.75,0.25]

OAI31D0 = [0.3125,0.5625,0.9375,0.75,0.75,0.9375,1.5625,1.25,1.25,0.75,1.25,1.,1.,0.75,1.25,1.,1.]

OAI31D1 = [0.3125,0.5625,0.9375,0.75,0.75,0.9375,1.5625,1.25,1.25,0.75,1.25,1.,1.,0.75,1.25,1.,1.]

OAI31D2 = [0.3125,0.5625,0.9375,0.75,0.75,0.9375,1.5625,1.25,1.25,0.75,1.25,1.,1.,0.75,1.25,1.,1.]

OAI211D0 = [0.4375,0.0625,0.4375,0.125,0.375,0.4375,3.0625,0.875,2.625,0.125,0.875,0.25,0.75,0.375,2.625,0.75,2.25]

OAI211D1 = [0.4375,0.0625,0.4375,0.125,0.375,0.4375,3.0625,0.875,2.625,0.125,0.875,0.25,0.75,0.375,2.625,0.75,2.25]

ND3D0 = [0.5,0.,0.,0.,0.,0.,4.,1.,3.,0.,1.,0.25,0.75,0.,3.,0.75,2.25]

ND3D1 = [0.5,0.,0.,0.,0.,0.,4.,1.,3.,0.,1.,0.25,0.75,0.,3.,0.75,2.25]

OA22D0 = [0.375,1.5625,0.9375,0.625,1.875,0.9375,0.5625,0.375,1.125,0.625,0.375,0.25,0.75,1.875,1.125,0.75,2.25]

IOA22D1 = [0.375,2.25,0.75,1.125,1.875,0.75,0.25,0.375,0.625,1.125,0.375,0.5625,0.9375,1.875,0.625,0.9375,1.5625]

IOA22D2 = [0.375,2.25,0.75,1.125,1.875,0.75,0.25,0.375,0.625,1.125,0.375,0.5625,0.9375,1.875,0.625,0.9375,1.5625]

IAO22D1 = [0.375,1.5625	,0.9375,0.625,1.875,0.9375,0.5625,0.375,1.125,0.625,0.375,0.25,0.75,1.875,1.125,0.75,2.25]

BUFFD0 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

CKBD1 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

CKBXD1 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

CKBXD0 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

BUFFD1 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

BUFFD2 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

BUFFD3 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

AN3D0 = [0.5,4.,0.,3.,1.,0.,0.,0.,0.,3.,0.,2.25,0.75,1.,0.,0.75,0.25]

AN3D1 = [0.5,4.,0.,3.,1.,0.,0.,0.,0.,3.,0.,2.25,0.75,1.,0.,0.75,0.25]

AN3D2 = [0.5,4.,0.,3.,1.,0.,0.,0.,0.,3.,0.,2.25,0.75,1.,0.,0.75,0.25]

AOI211D0 = [0.4375,2.25,0.75,2.625,0.375,0.75,0.25,0.875,0.125,2.625,0.875,3.0625,0.4375,0.375,0.125,0.4375,0.0625]

AOI211D1 = [0.4375,2.25,0.75,2.625,0.375,0.75,0.25,0.875,0.125,2.625,0.875,3.0625,0.4375,0.375,0.125,0.4375,0.0625]

INR3D0 = [0.5,4.,0.,3.,1.,0.,0.,0.,0.,3.,0.,2.25,0.75,1.,0.,0.75,0.25]

INR4D0 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]

IINR4D0 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]

AOI31D0 = [0.3125,1.,1.,1.25,0.75,1.,1.,1.25,0.75,1.25,1.25,1.5625,0.9375,0.75,0.75,0.9375,0.5625]

AOI31D1 = [0.3125,1.,1.,1.25,0.75,1.,1.,1.25,0.75,1.25,1.25,1.5625,0.9375,0.75,0.75,0.9375,0.5625]

MOAI22D0 = [0.375,0.5625,0.9375,1.125,0.375,0.9375,1.5625,1.875,0.625,1.125,1.875,2.25,0.75,0.375,0.625,0.75,0.25]

AO33D1 = [0.4375,3.0625,0.4375,2.296875,1.203125,0.4375,0.0625,0.328125,0.171875,2.296875,0.328125,1.72265625,0.90234375,1.203125,0.171875,0.90234375,0.47265625]

AO33D0 = [0.4375,3.0625,0.4375,2.296875,1.203125,0.4375,0.0625,0.328125,0.171875,2.296875,0.328125,1.72265625,0.90234375,1.203125,0.171875,0.90234375,0.47265625]

OAI22D0 = [0.375,0.5625,0.9375,1.125,0.375,0.9375,1.5625,1.875,0.625,1.125,1.875,2.25,0.75,0.375,0.625,0.75,0.25]

OAI22D1 = [0.375,0.5625,0.9375,1.125,0.375,0.9375,1.5625,1.875,0.625,1.125,1.875,2.25,0.75,0.375,0.625,0.75,0.25]

ND4D0 = [0.5,0.,0.,0.,0.,0.,4.,0.5,3.5,0.,0.5,0.0625,0.4375,0.,3.5,0.4375,3.0625] 

ND4D1 = [0.5,0.,0.,0.,0.,0.,4.,0.5,3.5,0.,0.5,0.0625,0.4375,0.,3.5,0.4375,3.0625] 

NR4D0 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]

IIND4D1 = [0.5,0.0625,0.4375,0.,0.5,0.4375,3.0625,0.,3.5,0.,0.,0.,0.,0.5,3.5,0.,4.]

INR4D1 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]

IND3D0 = [0.5,0.25,0.75,0.,1.,0.75,2.25,0.,3.,0.,0.,0.,0.,1.,3.,0.,4.]

FA1D0_0 = [0.375,2.25,0.75,0.75,2.25,0.75,0.25,0.25,0.75,0.75,0.25,0.25,0.75,2.25,0.75,0.75,2.25] 

FA1D0_1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

FICIND1_0 = [0.375,2.25,0.75,0.75,2.25,0.75,0.25,0.25,0.75,0.75,0.25,0.25,0.75,2.25,0.75,0.75,2.25]

FICIND1_1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

FCICIND1 = [0.375,2.25,0.75,0.75,2.25,0.75,0.25,0.25,0.75,0.75,0.25,0.25,0.75,2.25,0.75,0.75,2.25]

OA222D0 = [0.3594,2.06640625,0.80859375,1.2578125,1.6171875,0.80859375,0.31640625,0.4921875,0.6328125,1.2578125,0.4921875,0.765625,0.984375,1.6171875,0.6328125,0.984375,1.265625]

AOI222D0 = [0.3594,0.765625,0.984375,1.2578125,0.4921875,0.984375,1.265625,1.6171875,0.6328125,1.2578125,1.6171875,2.06640625,0.80859375,0.4921875,0.6328125,0.80859375,0.31640625]

AOI222D1 = [0.3594,0.765625,0.984375,1.2578125,0.4921875,0.984375,1.265625,1.6171875,0.6328125,1.2578125,1.6171875,2.06640625,0.80859375,0.4921875,0.6328125,0.80859375,0.31640625]

OAI21D1 = [0.375,0.25,0.75,0.5,0.5,0.75,2.25,1.5,1.5,0.5,1.5,1.,1.,0.5,1.5,1.,1.]

IOA21D0 = [0.375,1.,1.,0.5,1.5,1.,1.,0.5,1.5,0.5,0.5,0.25,0.75,1.5,1.5,0.75,2.25]

IOA21D1 = [0.375,1.,1.,0.5,1.5,1.,1.,0.5,1.5,0.5,0.5,0.25,0.75,1.5,1.5,0.75,2.25]

IOA21D2 = [0.375,1.,1.,0.5,1.5,1.,1.,0.5,1.5,0.5,0.5,0.25,0.75,1.5,1.5,0.75,2.25]

OA31D0 = [0.3125,1.5625,0.9375,1.25,1.25,0.9375,0.5625,0.75,0.75,1.25,0.75,1.,1.,1.25,0.75,1.,1.]

OA31D1 = [0.3125,1.5625,0.9375,1.25,1.25,0.9375,0.5625,0.75,0.75,1.25,0.75,1.,1.,1.25,0.75,1.,1.]

NR3D0 = [0.5,2.25,0.75,3.,0.,0.75,0.25,1.,0.,3.,1.,4.,0.,0.,0.,0.,0.]

NR3D1 = [0.5,2.25,0.75,3.,0.,0.75,0.25,1.,0.,3.,1.,4.,0.,0.,0.,0.,0.]

XNR2D0 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

XNR2D1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

IAO21D0 = [0.375,2.25,0.75,1.5,1.5,0.75,0.25,0.5,0.5,1.5,0.5,1.,1.,1.5,0.5,1.,1.]

IAO21D1 = [0.375,2.25,0.75,1.5,1.5,0.75,0.25,0.5,0.5,1.5,0.5,1.,1.,1.5,0.5,1.,1.]

AO21D0 = [0.375,1.,1.,0.5,1.5,1.,1.,0.5,1.5,0.5,0.5,0.25,0.75,1.5,1.5,0.75,2.25]

OR2D0 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

OR2D1 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

OR2D2 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

OR2D4 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

OR2D8 = [0.5,1.,1.,0.,2.,1.,1.,0.,2.,0.,0.,0.,0.,2.,2.,0.,4.]

INR2XD0 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

INR2XD1 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

OAI222D0 = [0.3594,0.31640625,0.80859375,0.6328125,0.4921875,0.80859375,2.06640625,1.6171875,1.2578125,0.6328125,1.6171875,1.265625,0.984375,0.4921875,1.2578125,0.984375,0.765625]

OAI222D1 = [0.3594,0.31640625,0.80859375,0.6328125,0.4921875,0.80859375,2.06640625,1.6171875,1.2578125,0.6328125,1.6171875,1.265625,0.984375,0.4921875,1.2578125,0.984375,0.765625]

XOR2D0 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.] 

XOR2D1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.] 

CKXOR2D0 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

CKXOR2D1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

MUX2ND0 = [0.375,0.25,0.75,0.75,0.25,0.75,2.25,2.25,0.75,0.75,2.25,2.25,0.75,0.25,0.75,0.75,0.25]

MUX2D0 = [0.375,2.25,0.75,0.75,2.25,0.75,0.25,0.25,0.75,0.75,0.25,0.25,0.75,2.25,0.75,0.75,2.25]

AN4D0 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]

AN4D1 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]

AN4D2 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]

AO22D0 = [0.375,2.25,0.75,1.125,1.875,0.75,0.25,0.375,0.625,1.125,0.375,0.5625,0.9375,1.875,0.625,0.9375,1.5625]

AO31D0 = [0.3125,1.,1.,0.75,1.25,1.,1.,0.75,1.25,0.75,0.75,0.5625,0.9375,1.25,1.25,0.9375,1.5625]

AO31D1 = [0.3125,1.,1.,0.75,1.25,1.,1.,0.75,1.25,0.75,0.75,0.5625,0.9375,1.25,1.25,0.9375,1.5625]

AO31D2 = [0.3125,1.,1.,0.75,1.25,1.,1.,0.75,1.25,0.75,0.75,0.5625,0.9375,1.25,1.25,0.9375,1.5625]

AO32D0 = [0.375,2.25,0.75,1.6875,1.3125,0.75,0.25,0.5625,0.4375,1.6875,0.5625,1.265625,0.984375,1.3125,0.4375,0.984375,0.765625]

AOI32D0 = [0.375,0.25,0.75,0.4375,0.5625,0.75,2.25,1.3125,1.6875,0.4375,1.3125,0.765625,0.984375,0.5625,1.6875,0.984375,1.265625]

CMPE42D1_0 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

CMPE42D1_1 = [0.375,2.25,0.75,0.75,2.25,0.75,0.25,0.25,0.75,0.75,0.25,0.25,0.75,2.25,0.75,0.75,2.25]

CMPE42D1_2 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

XNR3D0 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

OAI221D0 = [0.40625,0.140625,0.609375,0.28125,0.46875,0.609375,2.640625,1.21875,2.03125,0.28125,1.21875,0.5625,0.9375,0.46875,2.03125,0.9375,1.5625]

OAI221D4 = [0.40625,0.140625,0.609375,0.28125,0.46875,0.609375,2.640625,1.21875,2.03125,0.28125,1.21875,0.5625,0.9375,0.46875,2.03125,0.9375,1.5625]

AOI221D0 = [0.40625,1.5625,0.9375,2.03125,0.46875,0.9375,0.5625,1.21875,0.28125,2.03125,1.21875,2.640625,0.609375,0.46875,0.28125,0.609375,0.140625]

AOI221D1 = [0.40625,1.5625,0.9375,2.03125,0.46875,0.9375,0.5625,1.21875,0.28125,2.03125,1.21875,2.640625,0.609375,0.46875,0.28125,0.609375,0.140625]

AOI221D4 = [0.40625,1.5625,0.9375,2.03125,0.46875,0.9375,0.5625,1.21875,0.28125,2.03125,1.21875,2.640625,0.609375,0.46875,0.28125,0.609375,0.140625]

AO221D0 = [0.40625,2.640625,0.609375,2.03125,1.21875,0.609375,0.140625,0.46875,0.28125,2.03125,0.46875,1.5625,0.9375,1.21875,0.28125,0.9375,0.5625]

OA221D0 = [0.40625,0.5625,0.9375,0.28125,1.21875,0.9375,1.5625,0.46875,2.03125,0.28125,0.46875,0.140625,0.609375,1.21875,2.03125,0.609375,2.640625]

OAI32D0 = [0.375,1.265625,0.984375,1.6875,0.5625,0.984375,0.765625,1.3125,0.4375,1.6875,1.3125,2.25,0.75,0.5625,0.4375,0.75,0.25]

OAI32D1 = [0.375,1.265625,0.984375,1.6875,0.5625,0.984375,0.765625,1.3125,0.4375,1.6875,1.3125,2.25,0.75,0.5625,0.4375,0.75,0.25]

OA32D0 = [0.375,0.765625,0.984375,0.4375,1.3125,0.984375,1.265625,0.5625,1.6875,0.4375,0.5625,0.25,0.75,1.3125,1.6875,0.75,2.25]

OA32D2 = [0.375,0.765625,0.984375,0.4375,1.3125,0.984375,1.265625,0.5625,1.6875,0.4375,0.5625,0.25,0.75,1.3125,1.6875,0.75,2.25]

OA211D0 = [0.4375,3.0625,0.4375,2.625,0.875,0.4375,0.0625,0.375,0.125,2.625,0.375,2.25,0.75,0.875,0.125,0.75,0.25]

OA211D2 = [0.4375,3.0625,0.4375,2.625,0.875,0.4375,0.0625,0.375,0.125,2.625,0.375,2.25,0.75,0.875,0.125,0.75,0.25]

AOI211XD0 = [0.4375,2.25,0.75,2.625,0.375,0.75,0.25,0.875,0.125,2.625,0.875,3.0625,0.4375,0.375,0.125,0.4375,0.0625]

IND4D1 = [0.5,0.0625,0.4375,0.,0.5,0.4375,3.0625,0.,3.5,0.,0.,0.,0.,0.5,3.5,0.,4.]

IND4D0 = [0.5,0.0625,0.4375,0.,0.5,0.4375,3.0625,0.,3.5,0.,0.,0.,0.,0.5,3.5,0.,4.]

OA21D0 = [0.375,2.25,0.75,1.5,1.5,0.75,0.25,0.5,0.5,1.5,0.5,1.,1.,1.5,0.5,1.,1.]

OA21D1 = [0.375,2.25,0.75,1.5,1.5,0.75,0.25,0.5,0.5,1.5,0.5,1.,1.,1.5,0.5,1.,1.]

AO211D0 = [0.4375,0.25,0.75,0.125,0.875,0.75,2.25,0.375,2.625,0.125,0.375,0.0625,0.4375,0.875,2.625,0.4375,3.0625]

AO211D2 = [0.4375,0.25,0.75,0.125,0.875,0.75,2.25,0.375,2.625,0.125,0.375,0.0625,0.4375,0.875,2.625,0.4375,3.0625]

AO222D0 = [0.3594,1.265625,0.984375,0.6328125,1.6171875,0.984375,0.765625,0.4921875,1.2578125,0.6328125,0.4921875,0.31640625,0.80859375,1.6171875,1.2578125,0.80859375,2.06640625]

OR3D0 = [0.5,0.25,0.75,0.,1.,0.75,2.25,0.,3.,0.,0.,0.,0.,1.,3.,0.,4.]

OR3D2 = [0.5,0.25,0.75,0.,1.,0.75,2.25,0.,3.,0.,0.,0.,0.,1.,3.,0.,4.]

OR4D1 = [0.5,0.0625,0.4375,0.,0.5,0.4375,3.0625,0.,3.5,0.,0.,0.,0.,0.5,3.5,0.,4.]

OR4D0 = [0.5,0.0625,0.4375,0.,0.5,0.4375,3.0625,0.,3.5,0.,0.,0.,0.,0.5,3.5,0.,4.]

MAOI222D0 = [0.375,0.25,0.75,0.75,0.25,0.75,2.25,2.25,0.75,0.75,2.25,2.25,0.75,0.25,0.75,0.75,0.25]

MAOI222D1 = [0.375,0.25,0.75,0.75,0.25,0.75,2.25,2.25,0.75,0.75,2.25,2.25,0.75,0.25,0.75,0.75,0.25]

DFQD1 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

DFQD2 = [0.5,4.,0.,2.,2.,0.,0.,0.,0.,2.,0.,1.,1.,2.,0.,1.,1.]

#DUMMY = [1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.]
DUMMY = [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]
#DUMMY0 =     np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],dtype=np.float32)
#DUMMY=np.array(np.reshape(DUMMY0,(1,17)))

LHQD1 = [1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

XOR4D0 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

XOR4D1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

XOR3D1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

XNR3D1 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

XNR4D0 = [0.25,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

EDFD1 = [1.,4.,0.,0.,4.,0.,0.,0.,0.,0.,0.,0.,0.,4.,0.,0.,4.]

NR4D1 = [0.5,4.,0.,3.5,0.5,0.,0.,0.,0.,3.5,0.,3.0625,0.4375,0.5,0.,0.4375,0.0625]


def getNE(line):
    if ((len(re.compile(r'\s*INVD0').findall(line))>0)
        or (len(re.compile(r'\s*INVD1').findall(line))>0)
        or (len(re.compile(r'\s*CKND0').findall(line))>0)
        or (len(re.compile(r'\s*CKND1').findall(line))>0)
        or (len(re.compile(r'\s*CKNXD0').findall(line))>0)
        or (len(re.compile(r'\s*CKNXD1').findall(line))>0)
        or ((len(re.compile(r'\s*CKND2').findall(line))>0) and (not (len(re.compile(r'\s*CKND2D0').findall(line))>0)) and (not (len(re.compile(r'\s*CKND2D1').findall(line))>0)) and (not (len(re.compile(r'\s*CKND2D2').findall(line))>0))) 
        or (len(re.compile(r'\s*INVD2').findall(line))>0)
        or (len(re.compile(r'\s*INVD3').findall(line))>0)
        or (len(re.compile(r'\s*INVD6').findall(line))>0)
        or (len(re.compile(r'\s*BUFFD0').findall(line))>0)
        or (len(re.compile(r'\s*CKBD1').findall(line))>0)
        or (len(re.compile(r'\s*BUFFD3').findall(line))>0)
        or (len(re.compile(r'\s*BUFFD1').findall(line))>0)
        or (len(re.compile(r'\s*BUFFD2').findall(line))>0)
#        or (len(re.compile(r'\s**DFQD1').findall(line))>0)
        or (len(re.compile(r'\s*LHQD1').findall(line))>0)
        or (len(re.compile(r'\s*CKBXD0').findall(line))>0)):
#         INVD0 U568 ( .I(n479), .ZN(n477) );
#         INVD1 U394 ( .I(n470), .ZN(n591) );
#         BUFFD0 U290 ( .I(n459), .Z(n470) );
        if len(re.compile(r'\s*INVD0').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*INVD0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'INVD0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*INVD1').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*INVD1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'INVD1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*CKND0').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*CKND0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'CKND0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*CKND1').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*CKND1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'CKND1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*CKNXD0').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*CKNXD0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'CKNXD0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*CKNXD1').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*CKNXD1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'CKNXD1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*CKND2').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*CKND2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'CKND2'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*INVD2').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*INVD2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'INVD2'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*INVD3').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*INVD3\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'INVD3'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*INVD6').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*INVD6\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'INVD6'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.250
            prob_t0 = 0.750
            inv=1
        elif len(re.compile(r'\s*BUFFD0').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*BUFFD0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'BUFFD0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*CKBD1').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*CKBD1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'CKBD1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*BUFFD3').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*BUFFD3\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'BUFFD3'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*BUFFD2').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*BUFFD2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'BUFFD2'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*BUFFD1').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*BUFFD1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'BUFFD1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
#        elif len(re.compile(r'\s*DFQD1').findall(line))>0:
#            pattern_1ip1op = re.compile(r'\s*DFQD1\s?([\a-zA-Z0-9_]+)\s\(.*?\((.*?)\).*?\((.*?)\)')
#            node = 'DFQD1'
        elif len(re.compile(r'\s*LHQD1').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*LHQD1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'LHQD1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*CKBXD0').findall(line))>0:
            pattern_1ip1op = re.compile(r'\s*CKBXD0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\)')
            node = 'CKBXD0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        matches_1ip1op = pattern_1ip1op.finditer(line)
        in_edge =[]
        instance =''
        out_edge =[]
        for match in matches_1ip1op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            out_edge.append(match.group(3))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    elif ((len(re.compile(r'\s*NR2D0').findall(line))>0)
        or (len(re.compile(r'\s*NR2D3').findall(line))>0)
        or (len(re.compile(r'\s*ND2D0').findall(line))>0)
        or (len(re.compile(r'\s*ND2D1').findall(line))>0)
        or (len(re.compile(r'\s*CKND2D0').findall(line))>0)
        or (len(re.compile(r'\s*CKND2D1').findall(line))>0)
        or (len(re.compile(r'\s*CKND2D2').findall(line))>0)
        or (len(re.compile(r'\s*NR2D1').findall(line))>0)
        or (len(re.compile(r'\s*AN2D0').findall(line))>0)
        or (len(re.compile(r'\s*AN2XD1').findall(line))>0)
        or (len(re.compile(r'\s*CKAN2D0').findall(line))>0)
        or (len(re.compile(r'\s*CKAN2D1').findall(line))>0)
        or (len(re.compile(r'\s*CKAN2D2').findall(line))>0)
        or (len(re.compile(r'\s*CKAN2D4').findall(line))>0)
        or (len(re.compile(r'\s*CKAN2D8').findall(line))>0)
        or (len(re.compile(r'\s*IND2D0').findall(line))>0)
        or (len(re.compile(r'\s*IND2D1').findall(line))>0)
        or (len(re.compile(r'\s*IND2D2').findall(line))>0)
        or (len(re.compile(r'\s*DFQD1').findall(line))>0)
        or (len(re.compile(r'\s*DFQD2').findall(line))>0)
        or (len(re.compile(r'\s*INR2D1').findall(line))>0)
        or (len(re.compile(r'\s*INR2XD1').findall(line))>0)
        or (len(re.compile(r'\s*NR2XD1').findall(line))>0)
        or (len(re.compile(r'\s*NR2XD0').findall(line))>0)
        or (len(re.compile(r'\s*XNR2D0').findall(line))>0)
        or (len(re.compile(r'\s*XNR2D1').findall(line))>0)
        or (len(re.compile(r'\s*OR2D0').findall(line))>0)
        or (len(re.compile(r'\s*OR2D2').findall(line))>0)
        or (len(re.compile(r'\s*OR2D4').findall(line))>0)
        or (len(re.compile(r'\s*OR2D8').findall(line))>0)
        or (len(re.compile(r'\s*OR2D1').findall(line))>0)
        or (len(re.compile(r'\s*INR2XD0').findall(line))>0)
        or (len(re.compile(r'\s*XOR2D0').findall(line))>0)
        or (len(re.compile(r'\s*XOR2D1').findall(line))>0)
        or (len(re.compile(r'\s*CKXOR2D0').findall(line))>0)
        or (len(re.compile(r'\s*CKXOR2D1').findall(line))>0)
        or (len(re.compile(r'\s*INR2D0').findall(line))>0)):
#         NR2D0 U43 ( .A1(n36), .A2(a[0]), .ZN(n45) );
#         ND2D0 U45 ( .A1(a[0]), .A2(n36), .ZN(n37) );
#         AN2D0 U50 ( .A1(a[0]), .A2(b[0]), .Z(n51) );
#         INR2D0 U52 ( .A1(b[1]), .B1(a[1]), .ZN(n46) );
        if len(re.compile(r'\s*NR2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*NR2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR2D0'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*NR2D3').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*NR2D3\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR2D3'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*ND2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*ND2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'ND2D0'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*ND2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*ND2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'ND2D1'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*CKND2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKND2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKND2D0'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*CKND2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKND2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKND2D1'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*CKND2D2').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKND2D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKND2D2'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*DFQD1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*DFQD1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'DFQD1'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*DFQD2').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*DFQD2\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'DFQD2'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*AN2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*AN2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN2D0'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*AN2XD1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*AN2XD1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN2XD1'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*CKAN2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKAN2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKAN2D0'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*CKAN2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKAN2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKAN2D1'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*CKAN2D2').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKAN2D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKAN2D2'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*CKAN2D4').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKAN2D4\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKAN2D4'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*CKAN2D8').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKAN2D8\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKAN2D8'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*NR2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*NR2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR2D1'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*IND2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*IND2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IND2D0'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*IND2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*IND2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IND2D1'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*IND2D2').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*IND2D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IND2D2'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*INR2XD0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*INR2XD0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'INR2XD0'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*INR2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*INR2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'INR2D0'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*OR2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*OR2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR2D0'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*OR2D2').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*OR2D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR2D2'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*OR2D4').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*OR2D4\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR2D4'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*OR2D8').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*OR2D8\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR2D8'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*OR2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*OR2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR2D1'
            prob_s0 = 0.25
            prob_s1 = 0.75
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=0
        elif len(re.compile(r'\s*XOR2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*XOR2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XOR2D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
        elif len(re.compile(r'\s*XOR2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*XOR2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XOR2D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*CKXOR2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKXOR2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKXOR2D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*CKXOR2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*CKXOR2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'CKXOR2D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*XNR2D0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*XNR2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XNR2D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=1
        elif len(re.compile(r'\s*XNR2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*XNR2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XNR2D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=1
        elif len(re.compile(r'\s*NR2XD1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*NR2XD1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR2XD1'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*NR2XD0').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*NR2XD0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR2XD0'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*INR2XD1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*INR2XD1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'INR2XD1'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        elif len(re.compile(r'\s*INR2D1').findall(line))>0:
            pattern_2ip1op = re.compile(r'\s*INR2D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'INR2D1'
            prob_s0 = 0.75
            prob_s1 = 0.25
            prob_t1 = 0.1875
            prob_t0 = 0.8125
            inv=1
        matches_2ip1op = pattern_2ip1op.finditer(line)
        in_edge=[]
        instance =''
        out_edge =[]
        for match in matches_2ip1op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            in_edge.append(match.group(3))
            out_edge.append(match.group(4))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    elif (len(re.compile(r'\s*AOI22D0').findall(line))>0
         or len(re.compile(r'\s*AOI22D1').findall(line))>0
         or len(re.compile(r'\s*OAI211D0').findall(line))>0
         or len(re.compile(r'\s*OAI211D1').findall(line))>0
         or len(re.compile(r'\s*INR4D0').findall(line))>0
         or len(re.compile(r'\s*IINR4D0').findall(line))>0
         or len(re.compile(r'\s*INR4D1').findall(line))>0
         or len(re.compile(r'\s*OAI31D0').findall(line))>0
         or len(re.compile(r'\s*OA22D0').findall(line))>0
         or len(re.compile(r'\s*IOA22D1').findall(line))>0
         or len(re.compile(r'\s*IOA22D2').findall(line))>0
         or len(re.compile(r'\s*IAO22D1').findall(line))>0
         or len(re.compile(r'\s*OA211D0').findall(line))>0
         or len(re.compile(r'\s*OA211D2').findall(line))>0
         or len(re.compile(r'\s*OAI22D0').findall(line))>0
         or len(re.compile(r'\s*OAI22D1').findall(line))>0
         or len(re.compile(r'\s*OAI31D1').findall(line))>0
         or len(re.compile(r'\s*AOI211D0').findall(line))>0
         or len(re.compile(r'\s*AOI211D1').findall(line))>0
         or len(re.compile(r'\s*AOI31D0').findall(line))>0
         or len(re.compile(r'\s*AOI31D1').findall(line))>0
         or len(re.compile(r'\s*AO211D0').findall(line))>0
         or len(re.compile(r'\s*AO211D2').findall(line))>0
         or len(re.compile(r'\s*NR4D0').findall(line))>0
         or len(re.compile(r'\s*IIND4D1').findall(line))>0
         or len(re.compile(r'\s*IND4D1').findall(line))>0
         or len(re.compile(r'\s*IND4D0').findall(line))>0
         or len(re.compile(r'\s*OAI31D2').findall(line))>0
         or len(re.compile(r'\s*OA31D0').findall(line))>0
         or len(re.compile(r'\s*OA31D1').findall(line))>0
         or len(re.compile(r'\s*AN4D0').findall(line))>0
         or len(re.compile(r'\s*AN4D2').findall(line))>0
         or len(re.compile(r'\s*OR4D0').findall(line))>0
         or len(re.compile(r'\s*OR4D1').findall(line))>0
         or len(re.compile(r'\s*AN4D1').findall(line))>0
         or len(re.compile(r'\s*ND4D0').findall(line))>0
         or len(re.compile(r'\s*ND4D1').findall(line))>0
         or len(re.compile(r'\s*AO22D0').findall(line))>0
         or len(re.compile(r'\s*AO31D0').findall(line))>0
         or len(re.compile(r'\s*AO31D1').findall(line))>0
         or len(re.compile(r'\s*AO31D2').findall(line))>0
         or len(re.compile(r'\s*AOI211XD0').findall(line))>0
         or len(re.compile(r'\s*MOAI22D0').findall(line))>0
         or len(re.compile(r'\s*XOR4D0').findall(line))>0
         or len(re.compile(r'\s*XOR4D1').findall(line))>0
         or len(re.compile(r'\s*XNR4D0').findall(line))>0
         or len(re.compile(r'\s*MAOI22D0').findall(line))>0
         or len(re.compile(r'\s*NR4D1').findall(line))>0):
#         AOI22D0 U49 ( .A1(b[3]), .A2(a[3]), .B1(n62), .B2(n63), .ZN(n52) );
#         MAOI22D0 U66 ( .A1(n49), .A2(n48), .B1(n47), .B2(n50), .ZN(n57) );
#         OAI31D0 U73 ( .A1(n60), .A2(n59), .A3(N36), .B(n64), .ZN(n61) );
        if len(re.compile(r'\s*AOI22D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AOI22D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI22D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2461
            prob_t0 = 0.7539
            inv=1
        elif len(re.compile(r'\s*AOI22D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AOI22D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI22D1'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2461
            prob_t0 = 0.7539
            inv=1
        elif len(re.compile(r'\s*OAI211D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OAI211D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI211D0'
            prob_s0 = 0.1875
            prob_s1 = 0.8125
            prob_t1 = 0.1523
            prob_t0 = 0.8476
            inv=1
        elif len(re.compile(r'\s*OAI211D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OAI211D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI211D1'
            prob_s0 = 0.1875
            prob_s1 = 0.8125
            prob_t1 = 0.1523
            prob_t0 = 0.8476
            inv=1
        elif len(re.compile(r'\s*INR4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*INR4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'INR4D0'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=1
        elif len(re.compile(r'\s*IINR4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*IINR4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IINR4D0'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=1
        elif len(re.compile(r'\s*INR4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*INR4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'INR4D1'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=1
        elif len(re.compile(r'\s*OA22D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OA22D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA22D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=0
        elif len(re.compile(r'\s*IOA22D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*IOA22D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IOA22D1'
            prob_s0 = 0.5625
            prob_s1 = 0.4375
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=1
        elif len(re.compile(r'\s*IOA22D2').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*IOA22D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IOA22D2'
            prob_s0 = 0.5625
            prob_s1 = 0.4375
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=1
        elif len(re.compile(r'\s*IAO22D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*IAO22D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IAO22D1'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=1
        elif len(re.compile(r'\s*XOR4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*XOR4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XOR4D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*XOR4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*XOR4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XOR4D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*XNR4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*XNR4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XNR4D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=1
        elif len(re.compile(r'\s*OA211D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OA211D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA211D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=0
        elif len(re.compile(r'\s*OA211D2').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OA211D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA211D2'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=0
        elif len(re.compile(r'\s*OAI22D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OAI22D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI22D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.7540
            prob_t0 = 0.2460
            inv=1
        elif len(re.compile(r'\s*OAI22D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OAI22D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI22D1'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.7540
            prob_t0 = 0.2460
            inv=1
        elif len(re.compile(r'\s*OAI31D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OAI31D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI31D1'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2461
            prob_t0 = 0.7539
            inv=1
        elif len(re.compile(r'\s*OAI31D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OAI31D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI31D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2461
            prob_t0 = 0.7539
            inv=1
        elif len(re.compile(r'\s*AOI211D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AOI211D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI211D0'
            prob_s0 = 0.8125
            prob_s1 = 0.1875
            prob_t1 = 0.1523
            prob_t0 = 0.8476
            inv=1
        elif len(re.compile(r'\s*AOI211D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AOI211D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI211D1'
            prob_s0 = 0.8125
            prob_s1 = 0.1875
            prob_t1 = 0.1523
            prob_t0 = 0.8476
            inv=1
        elif len(re.compile(r'\s*AOI211XD0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AOI211XD0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI211XD0'
            prob_s0 = 0.8125
            prob_s1 = 0.1875
            prob_t1 = 0.1523
            prob_t0 = 0.8476
            inv=1
        elif len(re.compile(r'\s*AOI31D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AOI31D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI31D0'
            prob_s0 = 0.5625
            prob_s1 = 0.4375
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=1
        elif len(re.compile(r'\s*AOI31D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AOI31D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI31D1'
            prob_s0 = 0.5625
            prob_s1 = 0.4375
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=1
        elif len(re.compile(r'\s*NR4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*NR4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR4D0'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=1
        elif len(re.compile(r'\s*IIND4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*IIND4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IIND4D1'
            prob_s0 = 0.0625
            prob_s1 = 0.9375
            prob_t1 = 0.0586
            prob_t0 = 0.9410
            inv=1
        elif len(re.compile(r'\s*IND4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*IND4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IND4D1'
            prob_s0 = 0.0625
            prob_s1 = 0.9375
            prob_t1 = 0.0586
            prob_t0 = 0.9410
            inv=1
        elif len(re.compile(r'\s*IND4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*IND4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IND4D0'
            prob_s0 = 0.0625
            prob_s1 = 0.9375
            prob_t1 = 0.0586
            prob_t0 = 0.9410
            inv=1
        elif len(re.compile(r'\s*OAI31D2').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OAI31D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI31D2'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=1
        elif len(re.compile(r'\s*OA31D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OA31D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA31D0'
            prob_s0 = 0.5625
            prob_s1 = 0.4375
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=0
        elif len(re.compile(r'\s*OA31D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OA31D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA31D1'
            prob_s0 = 0.5625
            prob_s1 = 0.4375
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=0
        elif len(re.compile(r'\s*AN4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AN4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN4D0'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=0
        elif len(re.compile(r'\s*AN4D2').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AN4D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN4D2'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=0
        elif len(re.compile(r'\s*OR4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OR4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR4D0'
            prob_s0 = 0.0625
            prob_s1 = 0.9375
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=0
        elif len(re.compile(r'\s*OR4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*OR4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR4D1'
            prob_s0 = 0.0625
            prob_s1 = 0.9375
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=0
        elif len(re.compile(r'\s*AN4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AN4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN4D1'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=0
        elif len(re.compile(r'\s*ND4D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*ND4D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'ND4D0'
            prob_s0 = 0.06255
            prob_s1 = 0.9375
            prob_t1 = 0.9414
            prob_t0 = 0.0586
            inv=1
        elif len(re.compile(r'\s*ND4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*ND4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'ND4D1'
            prob_s0 = 0.06255
            prob_s1 = 0.9375
            prob_t1 = 0.9414
            prob_t0 = 0.0586
            inv=1
        elif len(re.compile(r'\s*AO22D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AO22D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO22D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2460
            prob_t0 = 0.7540
            inv=0
        elif len(re.compile(r'\s*AO31D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AO31D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO31D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.7540
            prob_t0 = 0.2460
            inv=0
        elif len(re.compile(r'\s*AO31D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AO31D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO31D1'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.7540
            prob_t0 = 0.2460
            inv=0
        elif len(re.compile(r'\s*AO31D2').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AO31D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO31D2'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.7540
            prob_t0 = 0.2460
            inv=0
        elif len(re.compile(r'\s*AO211D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AO211D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO211D0'
            prob_s0 = 0.1875
            prob_s1 = 0.8125
            prob_t1 = 0.15234
            prob_t0 = 0.84765
            inv=0
        elif len(re.compile(r'\s*AO211D2').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*AO211D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO211D2'
            prob_s0 = 0.1875
            prob_s1 = 0.8125
            prob_t1 = 0.15234
            prob_t0 = 0.84765
            inv=0
        elif len(re.compile(r'\s*MAOI22D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*MAOI22D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MAOI22D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2461
            prob_t0 = 0.7539
            inv=1
        elif len(re.compile(r'\s*MOAI22D0').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*MOAI22D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MOAI22D0'
            prob_s0 = 0.4375
            prob_s1 = 0.5625
            prob_t1 = 0.2461
            prob_t0 = 0.7539
            inv=1
        elif len(re.compile(r'\s*NR4D1').findall(line))>0:
            pattern_4ip1op = re.compile(r'\s*NR4D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR4D1'
            prob_s0 = 0.9375
            prob_s1 = 0.0625
            prob_t1 = 0.0586
            prob_t0 = 0.9414
            inv=1
        matches_4ip1op = pattern_4ip1op.finditer(line)
        in_edge=[]
        instance =''
        out_edge =[]
        for match in matches_4ip1op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            in_edge.append(match.group(3))
            in_edge.append(match.group(4))
            in_edge.append(match.group(5))
            out_edge.append(match.group(6))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    elif (len(re.compile(r'\s*AOI21D0').findall(line))>0
         or len(re.compile(r'\s*AOI21D1').findall(line))>0
         or len(re.compile(r'\s*ND3D0').findall(line))>0
         or len(re.compile(r'\s*ND3D1').findall(line))>0
         or len(re.compile(r'\s*AN3D0').findall(line))>0
         or len(re.compile(r'\s*AN3D1').findall(line))>0
         or len(re.compile(r'\s*AN3D2').findall(line))>0
         or len(re.compile(r'\s*INR3D0').findall(line))>0
         or len(re.compile(r'\s*XOR3D1').findall(line))>0
         or len(re.compile(r'\s*XNR3D1').findall(line))>0
         or len(re.compile(r'\s*IND3D0').findall(line))>0
         or len(re.compile(r'\s*OAI21D1').findall(line))>0
         or len(re.compile(r'\s*OAI21D0').findall(line))>0
         or len(re.compile(r'\s*IOA21D0').findall(line))>0
         or len(re.compile(r'\s*IOA21D1').findall(line))>0
         or len(re.compile(r'\s*IOA21D2').findall(line))>0
         or len(re.compile(r'\s*OA21D0').findall(line))>0
         or len(re.compile(r'\s*OA21D1').findall(line))>0
         or len(re.compile(r'\s*OR3D0').findall(line))>0
         or len(re.compile(r'\s*OR3D2').findall(line))>0
         or len(re.compile(r'\s*NR3D0').findall(line))>0
         or len(re.compile(r'\s*NR3D1').findall(line))>0
         or len(re.compile(r'\s*IAO21D0').findall(line))>0
         or len(re.compile(r'\s*IAO21D1').findall(line))>0
         or len(re.compile(r'\s*AO21D0').findall(line))>0
         or len(re.compile(r'\s*MUX2D0').findall(line))>0
         or len(re.compile(r'\s*MUX2ND0').findall(line))>0
         or len(re.compile(r'\s*XNR3D0').findall(line))>0
         or len(re.compile(r'\s*FCICIND1').findall(line))>0
         or len(re.compile(r'\s*MAOI222D0').findall(line))>0
         or len(re.compile(r'\s*MAOI222D1').findall(line))>0
         or len(re.compile(r'\s*FCICOND1').findall(line))>0):
#         AOI21D0 U53 ( .A1(n44), .A2(n37), .B(n46), .ZN(n47) );
#         OAI21D0 U71 ( .A1(n57), .A2(n56), .B(n55), .ZN(N38) );
#         FCICOND1 U68 ( .A(a[1]), .B(b[1]), .CI(n51), .CON(n54) );
#        prob_t1=0
#        prob_t0=0
        if len(re.compile(r'\s*AOI21D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*AOI21D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI21D0'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*AOI21D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*AOI21D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI21D1'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*XOR3D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*XOR3D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XOR3D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*XNR3D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*XNR3D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XNR3D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=1
        elif len(re.compile(r'\s*ND3D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*ND3D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'ND3D0'
            prob_s0 = 0.125
            prob_s1 = 0.875
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*ND3D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*ND3D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'ND3D1'
            prob_s0 = 0.125
            prob_s1 = 0.875
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*IND3D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*IND3D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IND3D0'
            prob_s0 = 0.125
            prob_s1 = 0.875
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*OAI21D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*OAI21D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI21D0'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*OAI21D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*OAI21D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI21D1'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*OA21D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*OA21D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA21D0'
            prob_s0 = 0.625
            prob_s1 = 0.375
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=0
        elif len(re.compile(r'\s*OA21D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*OA21D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA21D1'
            prob_s0 = 0.625
            prob_s1 = 0.375
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=0
        elif len(re.compile(r'\s*IOA21D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*IOA21D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IOA21D0'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*IOA21D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*IOA21D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IOA21D1'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*IOA21D2').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*IOA21D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IOA21D2'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*NR3D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*NR3D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR3D0'
            prob_s0 = 0.875
            prob_s1 = 0.125
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*OR3D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*OR3D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR3D0'
            prob_s0 = 0.125
            prob_s1 = 0.875
            prob_t1 = 0.1093
            prob_t0 = 0.8906
            inv=0
        elif len(re.compile(r'\s*OR3D2').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*OR3D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OR3D2'
            prob_s0 = 0.125
            prob_s1 = 0.875
            prob_t1 = 0.1093
            prob_t0 = 0.8906
            inv=0
        elif len(re.compile(r'\s*NR3D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*NR3D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'NR3D1'
            prob_s0 = 0.875
            prob_s1 = 0.125
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*IAO21D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*IAO21D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IAO21D0'
            prob_s0 = 0.625
            prob_s1 = 0.375
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*IAO21D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*IAO21D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'IAO21D1'
            prob_s0 = 0.625
            prob_s1 = 0.375
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*AO21D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*AO21D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO21D0'
            prob_s0 = 0.375
            prob_s1 = 0.625
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=0
        elif len(re.compile(r'\s*MUX2D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*MUX2D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MUX2D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*MUX2ND0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*MUX2ND0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MUX2ND0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=0
        elif len(re.compile(r'\s*XNR3D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*XNR3D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'XNR3D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*FCICOND1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*FCICOND1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\)')
            node = 'FCICOND1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*FCICIND1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*FCICIND1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\)')
            node = 'FCICIND1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*MAOI222D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*MAOI222D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MAOI222D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=1
        elif len(re.compile(r'\s*MAOI222D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*MAOI222D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MAOI222D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=1
        elif len(re.compile(r'\s*INR3D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*INR3D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'INR3D0'
            prob_s0 = 0.875
            prob_s1 = 0.125
            prob_t1 = 0.9375
            prob_t0 = 0.0625
            inv=1
        elif len(re.compile(r'\s*AN3D0').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*AN3D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN3D0'
            prob_s0 = 0.875
            prob_s1 = 0.125
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*AN3D2').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*AN3D2\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN3D2'
            prob_s0 = 0.875
            prob_s1 = 0.125
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*AN3D1').findall(line))>0:
            pattern_3ip1op = re.compile(r'\s*AN3D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AN3D1'
            prob_s0 = 0.875
            prob_s1 = 0.125
            prob_t1 = 0.25
            prob_t0 = 0.75   
            inv=0
        matches_3ip1op = pattern_3ip1op.finditer(line)
        in_edge=[]
        instance =''
        out_edge =[]
        for match in matches_3ip1op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            in_edge.append(match.group(3))
            in_edge.append(match.group(4))
            out_edge.append(match.group(5))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    elif (len(re.compile(r'\s*CMPE42D1').findall(line))>0):
        if len(re.compile(r'\s*CMPE42D1').findall(line))>0:
            pattern_5ip3op = re.compile(r'\s*CMPE42D1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\)')
            node = 'CMPE42D1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        matches_5ip3op = pattern_5ip3op.finditer(line)
        in_edge=[]
        instance =''
        out_edge = []
        for match in matches_5ip3op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            in_edge.append(match.group(3))
            in_edge.append(match.group(4))
            in_edge.append(match.group(5))
            in_edge.append(match.group(6))
            out_edge.append(match.group(7))
            out_edge.append(match.group(8))
            out_edge.append(match.group(9))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    elif (len(re.compile(r'\s*AOI221D0').findall(line))>0
         or len(re.compile(r'\s*AOI221D1').findall(line))>0
         or len(re.compile(r'\s*AOI221D4').findall(line))>0
         or len(re.compile(r'\s*AO32D0').findall(line))>0
         or len(re.compile(r'\s*AO221D0').findall(line))>0
         or len(re.compile(r'\s*OA221D0').findall(line))>0
         or len(re.compile(r'\s*OAI221D0').findall(line))>0
         or len(re.compile(r'\s*OAI221D4').findall(line))>0
         or len(re.compile(r'\s*MUX3ND0').findall(line))>0
         or len(re.compile(r'\s*OAI32D0').findall(line))>0
         or len(re.compile(r'\s*OAI32D1').findall(line))>0
         or len(re.compile(r'\s*OA32D0').findall(line))>0
         or len(re.compile(r'\s*OA32D2').findall(line))>0
         or len(re.compile(r'\s*AOI32D0').findall(line))>0):
        if len(re.compile(r'\s*AOI221D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*AOI221D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI221D0'
            prob_s0 = 0.71875
            prob_s1 = 0.28125
            prob_t1 = 0.202148
            prob_t0 = 0.79785
            inv=1
        elif len(re.compile(r'\s*AOI221D1').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*AOI221D1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI221D1'
            prob_s0 = 0.71875
            prob_s1 = 0.28125
            prob_t1 = 0.202148
            prob_t0 = 0.79785
            inv=1
        elif len(re.compile(r'\s*MUX3ND0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*MUX3ND0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MUX3ND0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=1
        elif len(re.compile(r'\s*AOI221D4').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*AOI221D4\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI221D4'
            prob_s0 = 0.71875
            prob_s1 = 0.28125
            prob_t1 = 0.202148
            prob_t0 = 0.79785
            inv=1
        elif len(re.compile(r'\s*AO221D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*AO221D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO221D0'
            prob_s0 = 0.28125
            prob_s1 = 0.71875
            prob_t1 = 0.202148
            prob_t0 = 0.79785
            inv=0
        elif len(re.compile(r'\s*OA221D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*OA221D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA221D0'
            prob_s0 = 0.28125
            prob_s1 = 0.71875
            prob_t1 = 0.202148
            prob_t0 = 0.79785
            inv=0
        elif len(re.compile(r'\s*OAI221D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*OAI221D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI221D0'
            prob_s0 = 0.28125
            prob_s1 = 0.71875
            prob_t1 = 0.20343
            prob_t0 = 0.79657
            inv=1
        elif len(re.compile(r'\s*OAI221D4').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*OAI221D4\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI221D4'
            prob_s0 = 0.28125
            prob_s1 = 0.71875
            prob_t1 = 0.20343
            prob_t0 = 0.79657
            inv=1
        elif len(re.compile(r'\s*AO32D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*AO32D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO32D0'
            prob_s0 = 0.65625
            prob_s1 = 0.34375
            prob_t1 = 0.22558
            prob_t0 = 0.77441
            inv=0
        elif len(re.compile(r'\s*OAI32D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*OAI32D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI32D0'
            prob_s0 = 0.65625
            prob_s1 = 0.34375
            prob_t1 = 0.22558
            prob_t0 = 0.77441
            inv=1
        elif len(re.compile(r'\s*OAI32D1').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*OAI32D1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI32D1'
            prob_s0 = 0.65625
            prob_s1 = 0.34375
            prob_t1 = 0.22558
            prob_t0 = 0.77441
            inv=1
        elif len(re.compile(r'\s*OA32D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*OA32D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA32D0'
            prob_s0 = 0.34375
            prob_s1 = 0.65625
            prob_t1 = 0.22558
            prob_t0 = 0.77441
            inv=0
        elif len(re.compile(r'\s*OA32D2').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*OA32D2\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA32D2'
            prob_s0 = 0.34375
            prob_s1 = 0.65625
            prob_t1 = 0.22558
            prob_t0 = 0.77441
            inv=0
        elif len(re.compile(r'\s*AOI32D0').findall(line))>0:
            pattern_5ip1op = re.compile(r'\s*AOI32D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI32D0'
            prob_s0 = 0.34375
            prob_s1 = 0.65625
            prob_t1 = 0.22558
            prob_t0 = 0.77441
            inv=1
        matches_5ip1op = pattern_5ip1op.finditer(line)
        in_edge=[]
        instance =''
        out_edge = []
        for match in matches_5ip1op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            in_edge.append(match.group(3))
            in_edge.append(match.group(4))
            in_edge.append(match.group(5))
            in_edge.append(match.group(6))
            out_edge.append(match.group(7))
#            out_edge.append(match.group(8))
#            out_edge.append(match.group(9))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    elif (len(re.compile(r'\s*OA222D0').findall(line))>0
         or len(re.compile(r'\s*AOI222D1').findall(line))>0
         or len(re.compile(r'\s*AO222D0').findall(line))>0
         or len(re.compile(r'\s*AOI33D0').findall(line))>0
         or len(re.compile(r'\s*OAI33D0').findall(line))>0
         or len(re.compile(r'\s*OAI33D1').findall(line))>0
         or len(re.compile(r'\s*AO33D0').findall(line))>0
         or len(re.compile(r'\s*AO33D1').findall(line))>0
         or len(re.compile(r'\s*MUX4ND0').findall(line))>0
         or len(re.compile(r'\s*OAI222D0').findall(line))>0
         or len(re.compile(r'\s*OAI222D1').findall(line))>0
         or len(re.compile(r'\s*AOI222D0').findall(line))>0):
        if len(re.compile(r'\s*OA222D0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*OA222D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OA222D0'
            prob_s0 = 0.57
            prob_s1 = 0.42
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=0
        elif len(re.compile(r'\s*AOI222D1').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*AOI222D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI222D1'
            prob_s0 = 0.578125
            prob_s1 = 0.421875
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*AO222D0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*AO222D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO222D0'
            prob_s0 = 0.578125
            prob_s1 = 0.421875
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=0
        elif len(re.compile(r'\s*AOI33D0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*AOI33D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI33D0'
            prob_s0 = 0.2343
            prob_s1 = 0.7656
            prob_t1 = 0.1794
            prob_t0 = 0.8205
            inv=1
        elif len(re.compile(r'\s*OAI33D0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*OAI33D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI33D0'
            prob_s0 = 0.2343
            prob_s1 = 0.7656
            prob_t1 = 0.1794
            prob_t0 = 0.8205
            inv=1
        elif len(re.compile(r'\s*AO33D1').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*AO33D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO33D1'
            prob_s0 = 0.7656
            prob_s1 = 0.2343
            prob_t1 = 0.1794
            prob_t0 = 0.8205
            inv=0
        elif len(re.compile(r'\s*AO33D0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*AO33D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AO33D0'
            prob_s0 = 0.7656
            prob_s1 = 0.2343
            prob_t1 = 0.1794
            prob_t0 = 0.8205
            inv=0
        elif len(re.compile(r'\s*OAI33D1').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*OAI33D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI33D1'
            prob_s0 = 0.2343
            prob_s1 = 0.7656
            prob_t1 = 0.1794
            prob_t0 = 0.8205
            inv=1
        elif len(re.compile(r'\s*MUX4ND0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*MUX4ND0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'MUX4ND0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*OAI222D0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*OAI222D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI222D0'
            prob_s0 = 0.421875
            prob_s1 = 0.578125
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*OAI222D1').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*OAI222D1\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'OAI222D1'
            prob_s0 = 0.421875
            prob_s1 = 0.578125
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        elif len(re.compile(r'\s*AOI222D0').findall(line))>0:
            pattern_6ip1op = re.compile(r'\s*AOI222D0\s?(\w*)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'AOI222D0'
            prob_s0 = 0.578125
            prob_s1 = 0.421875
            prob_t1 = 0.2343
            prob_t0 = 0.7657
            inv=1
        matches_6ip1op = pattern_6ip1op.finditer(line)
        in_edge=[]
        instance =''
        out_edge =[]
        for match in matches_6ip1op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            in_edge.append(match.group(3))
            in_edge.append(match.group(4))
            in_edge.append(match.group(5))
            in_edge.append(match.group(6))
            in_edge.append(match.group(7))
            out_edge.append(match.group(8))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    elif (len(re.compile(r'\s*FA1D0').findall(line))>0
        or len(re.compile(r'\s*FICIND1').findall(line))>0
        or len(re.compile(r'\s*EDFD1').findall(line))>0):
        if len(re.compile(r'\s*FA1D0').findall(line))>0:
            pattern_3ip2op = re.compile(r'\s*FA1D0\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\).*?\((.*?)\s*\)')
            node = 'FA1D0'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        elif len(re.compile(r'\s*FICIND1').findall(line))>0:
            pattern_3ip2op = re.compile(r'\s*FICIND1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'FICIND1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
        elif len(re.compile(r'\s*EDFD1').findall(line))>0:
            pattern_3ip2op = re.compile(r'\s*EDFD1\s?([\a-zA-Z0-9_]+)\s*\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
            node = 'EDFD1'
            prob_s0 = 0.5
            prob_s1 = 0.5
            prob_t1 = 0.25
            prob_t0 = 0.75
            inv=0
        matches_3ip2op = pattern_3ip2op.finditer(line)
        in_edge =[]
        instance =''
        out_edge =[]
        for match in matches_3ip2op:
            instance = match.group(1)
            in_edge.append(match.group(2))
            in_edge.append(match.group(3))
            in_edge.append(match.group(4))
            out_edge.append(match.group(5))
            out_edge.append(match.group(6))
        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv
    else:
        return 0,0,0,0,0,0,0,0,0

# Read contents of the netlist file and return it in a variable
def read_contents(filepath):
    with open(filepath,'r') as f:
        for i in range(6):
            next(f)
        contents = f.read()
    return contents

# Parse wires using regex and return the list of wires
def wires_parse(contents):
    # all_wire=[]
    # matches_wire = re.compile(r'wire((\s|.)*?);').finditer(contents)
    # for match in matches_wire:
    #     wires_raw = match.group(1)
    #     wires = wires_raw.replace('\n', '').replace(' ', '').strip().split(',')
    #     all_wire.extend(wires)
    all_wire=[]
    matches_wire = re.compile(r'wire((\s|.)*?);').finditer(contents)
    for match in matches_wire:
        #wires_raw =  match.group(1)
        #wires = wires_raw.replace('\n', '').replace(' ', '').strip().split(',')
        #all_wire.extend(wires)
        wires_raw =  match.group(1)
        all_wire.append(wires_raw)

    all_wires_final=[]
    for wire in all_wire:
        pattenr_wr = re.compile(r'\s*(\[(\d+):(\d+)\])?\s?([a-zA-Z0-9,_\/\\]+)')
        match_wr = pattenr_wr.finditer(wire)
        flag=False
        for match in match_wr:
            if ((match.group(1) is None) and (flag is False)):
                #wire_f=match.group(3)
                wire_f = wire.replace('\n', '').replace(' ', '').strip().split(',')
                all_wires_final.extend(wire_f)
                flag=True
            elif ((match.group(1) is not None) and (flag is False)):
                ll = min(int(match.group(2)), int(match.group(3)))
                ul = max(int(match.group(2)), int(match.group(3)))
                wire_f = match.group(4).replace('\n', '').replace(' ', '').strip().split(',')
                
                for new_wire in wire_f:  
                    for i in range(ul-ll+1):
                        wire_nm = new_wire
                        wire_f1 = wire_nm + '[' + str(i+ll) + ']'
                        all_wires_final.append(wire_f1)
                    flag = True
    return all_wires_final

def create_infoDict(file_path, wires):
    with open(file_path,'r') as netlist:
        for line in netlist:
            if len(re.compile(r'assign').findall(line))>0:
                pattern = re.compile(r'\s*assign\s+?(.*?)\s+=\s+(.*);')
                match_as = pattern.finditer(line)
                for match in match_as:
                    assign[match.group(1)]=match.group(2)
            if len(re.compile(r'input').findall(line))>0:
                pattern = re.compile(r'input\s(\[(\d+):(\d+).*\])?\s?([a-zA-Z0-9_\s,]+)')
                match_ip = pattern.finditer(line)
                for match in match_ip:
                    if match.group(3) is None:
                        #info[match.group(3)] = {'Gate':'core output_bit'}
                        ips_raw = match.group(4)
                        core_i_list = ips_raw.replace('\n', '').replace(' ', '').strip().split(',')
                        #wires.append(core_o_list)
                        #core_ops.append(core_o_list)
                        for op in core_i_list:
                                core_i = op
                                info[core_i] = {'Gate':'core input_vector'}
                                wires.append(core_i)
                                core_ips.append(core_i)
                    else:
                        range_ip = abs(int(match.group(3))-int(match.group(2)))+1
                        for i in range(range_ip):
                            ips=match.group(4)
                            core_i_list=ips.strip().split(',')
                            for ip in core_i_list:
                                core_i = ip + '[' + str(i) + ']'
                                info[core_i] = {'Gate':'core input_vector'}
                                wires.append(core_i)
                                core_ips.append(core_i)
            if len(re.compile(r'output').findall(line))>0:
                pattern = re.compile(r'output\s(\[(\d+):(\d+).*\])?\s?([a-zA-Z0-9_\s,]+)')
                match_op = pattern.finditer(line)
                range_op =0
                for match in match_op:
                    if match.group(3) is None:
                        #info[match.group(3)] = {'Gate':'core output_bit'}
                        ops_raw = match.group(4)
                        core_o_list = ops_raw.replace('\n', '').replace(' ', '').strip().split(',')
                        #wires.append(core_o_list)
                        #core_ops.append(core_o_list)
                        for op in core_o_list:
                                core_o = op
                                info[core_o] = {'Gate':'core output_vector'}
                                wires.append(core_o)
                                core_ops.append(core_o)

                    else:
                        range_op = abs(int(match.group(3))-int(match.group(2)))+1
                        #print(range_op)
                        for i in range(range_op):
                            ops=match.group(4)
                            core_o_list=ops.strip().split(',')
                            for op in core_o_list:
                                core_o = op + '[' + str(i) + ']'
                                info[core_o] = {'Gate':'core output_vector'}
                                wires.append(core_o)
                                core_ops.append(core_o)

            instance, gate, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1,inv = getNE(line)
            if instance != 0:
    #             print(instance,'-',gate,'-',in_edge,'-',out_edge)
    #             info = {'Node':instance}
                if (len(out_edge)==1):
                    info[instance] = {'Gate': gate, 'in_edge':in_edge, 'out_edge':out_edge[0], 'prob_t1': prob_t1, 'prob_t0':prob_t0, 'prob_s0':prob_s0, 'prob_s1':prob_s1,'inv':inv}
                else:
                    for ind in range(len(out_edge)):
                        info[instance+'_'+str(ind)] = {'Gate': gate+'_'+str(ind), 'in_edge':in_edge, 'out_edge':out_edge[ind], 'prob_t1': prob_t1, 'prob_t0':prob_t0, 'prob_s0':prob_s0, 'prob_s1':prob_s1,'inv':inv}

def inedgesTrim():
    for k,v in info.items():
        if((v['Gate']=='core input_bit')or(v['Gate']=='core input_vector')or(v['Gate']=='core output_bit')
        or(v['Gate']=='core output_vector')):
            continue
        v['in_edge'] = [x.strip(' ') for x in v['in_edge']]
        
def updateAssignStatement():
    for k,v in assign.items():
        # print(edges)
        edges[k] = {'out_v':edges[v]['out_v'], 'in_v':[k]}
        node = edges.get(v)['out_v'][0]
        info[node]['out_edge'] = k
        del edges[v]
    return assign

# Write edge information to edges dictionary
def edges_UpdateInfo(wires):
    for k,v in info.items():
        if((v['Gate']=='core input_bit')or(v['Gate']=='core input_vector')or(v['Gate']=='core output_bit')
        or(v['Gate']=='core output_vector')):
            continue
        for wire in wires:
            if wire not in edges:
                edges[wire] = {'out_v':[], 'in_v':[]}
            if wire == v['out_edge'].strip():
                edges[wire]['out_v'].append(k)
                if (wire in core_ops) and (wire not in edges[wire]['in_v']):
                    edges[wire]['in_v'].append(wire)
            elif wire in v['in_edge']:
                edges[wire]['in_v'].append(k)
                if (wire in core_ips) and (wire not in edges[wire]['out_v']):
                    edges[wire]['out_v'].append(wire)
            else:
                continue

def update_graph(DG):
    DG.add_nodes_from(info.keys())
    for key, value in info.items():
        # DG.add_node(key)
        for i,j in value.items():
            DG.nodes[key][i] = j
    for k,v in edges.items():
        for i in range(len(v['in_v'])):
            #print(k, v)
            DG.add_edge(v['out_v'][0], v['in_v'][i])
    for n1, n2, n3 in list(DG.edges(data=True)):
        gate_prop = DG.nodes[n1]['Gate']
        if gate_prop == 'INVD0':
            attrs[(n1,n2)] = {'SC': INVD0[0], 'TC_00_00':INVD0[1],'TC_00_01':INVD0[2],'TC_00_10':INVD0[3],'TC_00_11':INVD0[4],
                              'TC_01_00':INVD0[5],'TC_01_01':INVD0[6],'TC_01_10':INVD0[7],'TC_01_11':INVD0[8],
                              'TC_10_00':INVD0[9],'TC_10_01':INVD0[10],'TC_10_10':INVD0[11],'TC_10_11':INVD0[12],
                              'TC_11_00':INVD0[13],'TC_11_01':INVD0[14],'TC_11_10':INVD0[15],'TC_11_11':INVD0[16]}
                #print(attrs)
        elif gate_prop == 'BUFFD0':
            attrs[(n1,n2)] = {'SC': BUFFD0[0], 'TC_00_00':BUFFD0[1],'TC_00_01':BUFFD0[2],'TC_00_10':BUFFD0[3],'TC_00_11':BUFFD0[4],
                              'TC_01_00':BUFFD0[5],'TC_01_01':BUFFD0[6],'TC_01_10':BUFFD0[7],'TC_01_11':BUFFD0[8],
                              'TC_10_00':BUFFD0[9],'TC_10_01':BUFFD0[10],'TC_10_10':BUFFD0[11],'TC_10_11':BUFFD0[12],
                              'TC_11_00':BUFFD0[13],'TC_11_01':BUFFD0[14],'TC_11_10':BUFFD0[15],'TC_11_11':BUFFD0[16]}
        elif gate_prop == 'BUFFD1':
            attrs[(n1,n2)] = {'SC': BUFFD1[0], 'TC_00_00':BUFFD1[1],'TC_00_01':BUFFD1[2],'TC_00_10':BUFFD1[3],'TC_00_11':BUFFD1[4],
                              'TC_01_00':BUFFD1[5],'TC_01_01':BUFFD1[6],'TC_01_10':BUFFD1[7],'TC_01_11':BUFFD1[8],
                              'TC_10_00':BUFFD1[9],'TC_10_01':BUFFD1[10],'TC_10_10':BUFFD1[11],'TC_10_11':BUFFD1[12],
                              'TC_11_00':BUFFD1[13],'TC_11_01':BUFFD1[14],'TC_11_10':BUFFD1[15],'TC_11_11':BUFFD1[16]}
        elif gate_prop == 'BUFFD2':
            attrs[(n1,n2)] = {'SC': BUFFD2[0], 'TC_00_00':BUFFD2[1],'TC_00_01':BUFFD2[2],'TC_00_10':BUFFD2[3],'TC_00_11':BUFFD2[4],
                              'TC_01_00':BUFFD2[5],'TC_01_01':BUFFD2[6],'TC_01_10':BUFFD2[7],'TC_01_11':BUFFD2[8],
                              'TC_10_00':BUFFD2[9],'TC_10_01':BUFFD2[10],'TC_10_10':BUFFD2[11],'TC_10_11':BUFFD2[12],
                              'TC_11_00':BUFFD2[13],'TC_11_01':BUFFD2[14],'TC_11_10':BUFFD2[15],'TC_11_11':BUFFD2[16]}
        elif gate_prop == 'BUFFD3':
            attrs[(n1,n2)] = {'SC': BUFFD3[0], 'TC_00_00':BUFFD3[1],'TC_00_01':BUFFD3[2],'TC_00_10':BUFFD3[3],'TC_00_11':BUFFD3[4],
                              'TC_01_00':BUFFD3[5],'TC_01_01':BUFFD3[6],'TC_01_10':BUFFD3[7],'TC_01_11':BUFFD3[8],
                              'TC_10_00':BUFFD3[9],'TC_10_01':BUFFD3[10],'TC_10_10':BUFFD3[11],'TC_10_11':BUFFD3[12],
                              'TC_11_00':BUFFD3[13],'TC_11_01':BUFFD3[14],'TC_11_10':BUFFD3[15],'TC_11_11':BUFFD3[16]}
        elif gate_prop == 'CKBD1':
            attrs[(n1,n2)] = {'SC': CKBD1[0], 'TC_00_00':CKBD1[1],'TC_00_01':CKBD1[2],'TC_00_10':CKBD1[3],'TC_00_11':CKBD1[4],
                              'TC_01_00':CKBD1[5],'TC_01_01':CKBD1[6],'TC_01_10':CKBD1[7],'TC_01_11':CKBD1[8],
                              'TC_10_00':CKBD1[9],'TC_10_01':CKBD1[10],'TC_10_10':CKBD1[11],'TC_10_11':CKBD1[12],
                              'TC_11_00':CKBD1[13],'TC_11_01':CKBD1[14],'TC_11_10':CKBD1[15],'TC_11_11':CKBD1[16]}
        elif gate_prop == 'INVD1':
            attrs[(n1,n2)] = {'SC': INVD1[0], 'TC_00_00':INVD1[1],'TC_00_01':INVD1[2],'TC_00_10':INVD1[3],'TC_00_11':INVD1[4],
                              'TC_01_00':INVD1[5],'TC_01_01':INVD1[6],'TC_01_10':INVD1[7],'TC_01_11':INVD1[8],
                              'TC_10_00':INVD1[9],'TC_10_01':INVD1[10],'TC_10_10':INVD1[11],'TC_10_11':INVD1[12],
                              'TC_11_00':INVD1[13],'TC_11_01':INVD1[14],'TC_11_10':INVD1[15],'TC_11_11':INVD1[16]}
        elif gate_prop == 'CKND0':
            attrs[(n1,n2)] = {'SC': CKND0[0], 'TC_00_00':CKND0[1],'TC_00_01':CKND0[2],'TC_00_10':CKND0[3],'TC_00_11':CKND0[4],
                              'TC_01_00':CKND0[5],'TC_01_01':CKND0[6],'TC_01_10':CKND0[7],'TC_01_11':CKND0[8],
                              'TC_10_00':CKND0[9],'TC_10_01':CKND0[10],'TC_10_10':CKND0[11],'TC_10_11':CKND0[12],
                              'TC_11_00':CKND0[13],'TC_11_01':CKND0[14],'TC_11_10':CKND0[15],'TC_11_11':CKND0[16]}
        elif gate_prop == 'CKND1':
            attrs[(n1,n2)] = {'SC': CKND1[0], 'TC_00_00':CKND1[1],'TC_00_01':CKND1[2],'TC_00_10':CKND1[3],'TC_00_11':CKND1[4],
                              'TC_01_00':CKND1[5],'TC_01_01':CKND1[6],'TC_01_10':CKND1[7],'TC_01_11':CKND1[8],
                              'TC_10_00':CKND1[9],'TC_10_01':CKND1[10],'TC_10_10':CKND1[11],'TC_10_11':CKND1[12],
                              'TC_11_00':CKND1[13],'TC_11_01':CKND1[14],'TC_11_10':CKND1[15],'TC_11_11':CKND1[16]}
        elif gate_prop == 'CKNXD0':
            attrs[(n1,n2)] = {'SC': CKNXD0[0], 'TC_00_00':CKNXD0[1],'TC_00_01':CKNXD0[2],'TC_00_10':CKNXD0[3],'TC_00_11':CKNXD0[4],
                              'TC_01_00':CKNXD0[5],'TC_01_01':CKNXD0[6],'TC_01_10':CKNXD0[7],'TC_01_11':CKNXD0[8],
                              'TC_10_00':CKNXD0[9],'TC_10_01':CKNXD0[10],'TC_10_10':CKNXD0[11],'TC_10_11':CKNXD0[12],
                              'TC_11_00':CKNXD0[13],'TC_11_01':CKNXD0[14],'TC_11_10':CKNXD0[15],'TC_11_11':CKNXD0[16]}
        elif gate_prop == 'CKNXD1':
            attrs[(n1,n2)] = {'SC': CKNXD1[0], 'TC_00_00':CKNXD1[1],'TC_00_01':CKNXD1[2],'TC_00_10':CKNXD1[3],'TC_00_11':CKNXD1[4],
                              'TC_01_00':CKNXD1[5],'TC_01_01':CKNXD1[6],'TC_01_10':CKNXD1[7],'TC_01_11':CKNXD1[8],
                              'TC_10_00':CKNXD1[9],'TC_10_01':CKNXD1[10],'TC_10_10':CKNXD1[11],'TC_10_11':CKNXD1[12],
                              'TC_11_00':CKNXD1[13],'TC_11_01':CKNXD1[14],'TC_11_10':CKNXD1[15],'TC_11_11':CKNXD1[16]}
        elif gate_prop == 'CKND2':
            attrs[(n1,n2)] = {'SC': CKND2[0], 'TC_00_00':CKND2[1],'TC_00_01':CKND2[2],'TC_00_10':CKND2[3],'TC_00_11':CKND2[4],
                              'TC_01_00':CKND2[5],'TC_01_01':CKND2[6],'TC_01_10':CKND2[7],'TC_01_11':CKND2[8],
                              'TC_10_00':CKND2[9],'TC_10_01':CKND2[10],'TC_10_10':CKND2[11],'TC_10_11':CKND2[12],
                              'TC_11_00':CKND2[13],'TC_11_01':CKND2[14],'TC_11_10':CKND2[15],'TC_11_11':CKND2[16]}
        elif gate_prop == 'INVD2':
            attrs[(n1,n2)] = {'SC': INVD2[0], 'TC_00_00':INVD2[1],'TC_00_01':INVD2[2],'TC_00_10':INVD2[3],'TC_00_11':INVD2[4],
                              'TC_01_00':INVD2[5],'TC_01_01':INVD2[6],'TC_01_10':INVD2[7],'TC_01_11':INVD2[8],
                              'TC_10_00':INVD2[9],'TC_10_01':INVD2[10],'TC_10_10':INVD2[11],'TC_10_11':INVD2[12],
                              'TC_11_00':INVD2[13],'TC_11_01':INVD2[14],'TC_11_10':INVD2[15],'TC_11_11':INVD2[16]}
        elif gate_prop == 'INVD3':
            attrs[(n1,n2)] = {'SC': INVD3[0], 'TC_00_00':INVD3[1],'TC_00_01':INVD3[2],'TC_00_10':INVD3[3],'TC_00_11':INVD3[4],
                              'TC_01_00':INVD3[5],'TC_01_01':INVD3[6],'TC_01_10':INVD3[7],'TC_01_11':INVD3[8],
                              'TC_10_00':INVD3[9],'TC_10_01':INVD3[10],'TC_10_10':INVD3[11],'TC_10_11':INVD3[12],
                              'TC_11_00':INVD3[13],'TC_11_01':INVD3[14],'TC_11_10':INVD3[15],'TC_11_11':INVD3[16]}
        elif gate_prop == 'INVD6':
            attrs[(n1,n2)] = {'SC': INVD6[0], 'TC_00_00':INVD6[1],'TC_00_01':INVD6[2],'TC_00_10':INVD6[3],'TC_00_11':INVD6[4],
                              'TC_01_00':INVD6[5],'TC_01_01':INVD6[6],'TC_01_10':INVD6[7],'TC_01_11':INVD6[8],
                              'TC_10_00':INVD6[9],'TC_10_01':INVD6[10],'TC_10_10':INVD6[11],'TC_10_11':INVD6[12],
                              'TC_11_00':INVD6[13],'TC_11_01':INVD6[14],'TC_11_10':INVD6[15],'TC_11_11':INVD6[16]}
        elif gate_prop == 'CKBXD0':
            attrs[(n1,n2)] = {'SC': CKBXD0[0], 'TC_00_00':CKBXD0[1],'TC_00_01':CKBXD0[2],'TC_00_10':CKBXD0[3],'TC_00_11':CKBXD0[4],
                              'TC_01_00':CKBXD0[5],'TC_01_01':CKBXD0[6],'TC_01_10':CKBXD0[7],'TC_01_11':CKBXD0[8],
                              'TC_10_00':CKBXD0[9],'TC_10_01':CKBXD0[10],'TC_10_10':CKBXD0[11],'TC_10_11':CKBXD0[12],
                              'TC_11_00':CKBXD0[13],'TC_11_01':CKBXD0[14],'TC_11_10':CKBXD0[15],'TC_11_11':CKBXD0[16]}
        elif gate_prop == 'DFQD1':
            attrs[(n1,n2)] = {'SC': DFQD1[0], 'TC_00_00':DFQD1[1],'TC_00_01':DFQD1[2],'TC_00_10':DFQD1[3],'TC_00_11':DFQD1[4],
                              'TC_01_00':DFQD1[5],'TC_01_01':DFQD1[6],'TC_01_10':DFQD1[7],'TC_01_11':DFQD1[8],
                              'TC_10_00':DFQD1[9],'TC_10_01':DFQD1[10],'TC_10_10':DFQD1[11],'TC_10_11':DFQD1[12],
                              'TC_11_00':DFQD1[13],'TC_11_01':DFQD1[14],'TC_11_10':DFQD1[15],'TC_11_11':DFQD1[16]}
        elif gate_prop == 'DFQD2':
            attrs[(n1,n2)] = {'SC': DFQD2[0], 'TC_00_00':DFQD2[1],'TC_00_01':DFQD2[2],'TC_00_10':DFQD2[3],'TC_00_11':DFQD2[4],
                              'TC_01_00':DFQD2[5],'TC_01_01':DFQD2[6],'TC_01_10':DFQD2[7],'TC_01_11':DFQD2[8],
                              'TC_10_00':DFQD2[9],'TC_10_01':DFQD2[10],'TC_10_10':DFQD2[11],'TC_10_11':DFQD2[12],
                              'TC_11_00':DFQD2[13],'TC_11_01':DFQD2[14],'TC_11_10':DFQD2[15],'TC_11_11':DFQD2[16]}
        elif (gate_prop == 'core input_vector') or (gate_prop == 'core input_bit'):
            attrs[(n1,n2)] = {'SC': DUMMY[0], 'TC_00_00':DUMMY[1],'TC_00_01':DUMMY[2],'TC_00_10':DUMMY[3],'TC_00_11':DUMMY[4],
                              'TC_01_00':DUMMY[5],'TC_01_01':DUMMY[6],'TC_01_10':DUMMY[7],'TC_01_11':DUMMY[8],
                              'TC_10_00':DUMMY[9],'TC_10_01':DUMMY[10],'TC_10_10':DUMMY[11],'TC_10_11':DUMMY[12],
                              'TC_11_00':DUMMY[13],'TC_11_01':DUMMY[14],'TC_11_10':DUMMY[15],'TC_11_11':DUMMY[16]}
        elif gate_prop == 'ND2D0':
            attrs[(n1,n2)] = {'SC': ND2D0[0], 'TC_00_00':ND2D0[1],'TC_00_01':ND2D0[2],'TC_00_10':ND2D0[3],'TC_00_11':ND2D0[4],
                              'TC_01_00':ND2D0[5],'TC_01_01':ND2D0[6],'TC_01_10':ND2D0[7],'TC_01_11':ND2D0[8],
                              'TC_10_00':ND2D0[9],'TC_10_01':ND2D0[10],'TC_10_10':ND2D0[11],'TC_10_11':ND2D0[12],
                              'TC_11_00':ND2D0[13],'TC_11_01':ND2D0[14],'TC_11_10':ND2D0[15],'TC_11_11':ND2D0[16]}
        elif gate_prop == 'CKND2D0':
            attrs[(n1,n2)] = {'SC': CKND2D0[0], 'TC_00_00':CKND2D0[1],'TC_00_01':CKND2D0[2],'TC_00_10':CKND2D0[3],'TC_00_11':CKND2D0[4],
                              'TC_01_00':CKND2D0[5],'TC_01_01':CKND2D0[6],'TC_01_10':CKND2D0[7],'TC_01_11':CKND2D0[8],
                              'TC_10_00':CKND2D0[9],'TC_10_01':CKND2D0[10],'TC_10_10':CKND2D0[11],'TC_10_11':CKND2D0[12],
                              'TC_11_00':CKND2D0[13],'TC_11_01':CKND2D0[14],'TC_11_10':CKND2D0[15],'TC_11_11':CKND2D0[16]}
        elif gate_prop == 'CKND2D1':
            attrs[(n1,n2)] = {'SC': CKND2D1[0], 'TC_00_00':CKND2D1[1],'TC_00_01':CKND2D1[2],'TC_00_10':CKND2D1[3],'TC_00_11':CKND2D1[4],
                              'TC_01_00':CKND2D1[5],'TC_01_01':CKND2D1[6],'TC_01_10':CKND2D1[7],'TC_01_11':CKND2D1[8],
                              'TC_10_00':CKND2D1[9],'TC_10_01':CKND2D1[10],'TC_10_10':CKND2D1[11],'TC_10_11':CKND2D1[12],
                              'TC_11_00':CKND2D1[13],'TC_11_01':CKND2D1[14],'TC_11_10':CKND2D1[15],'TC_11_11':CKND2D1[16]}
        elif gate_prop == 'CKND2D2':
            attrs[(n1,n2)] = {'SC': CKND2D2[0], 'TC_00_00':CKND2D2[1],'TC_00_01':CKND2D2[2],'TC_00_10':CKND2D2[3],'TC_00_11':CKND2D2[4],
                              'TC_01_00':CKND2D2[5],'TC_01_01':CKND2D2[6],'TC_01_10':CKND2D2[7],'TC_01_11':CKND2D2[8],
                              'TC_10_00':CKND2D2[9],'TC_10_01':CKND2D2[10],'TC_10_10':CKND2D2[11],'TC_10_11':CKND2D2[12],
                              'TC_11_00':CKND2D2[13],'TC_11_01':CKND2D2[14],'TC_11_10':CKND2D2[15],'TC_11_11':CKND2D2[16]}
        elif gate_prop == 'ND2D1':
            attrs[(n1,n2)] = {'SC': ND2D1[0], 'TC_00_00':ND2D1[1],'TC_00_01':ND2D1[2],'TC_00_10':ND2D1[3],'TC_00_11':ND2D1[4],
                              'TC_01_00':ND2D1[5],'TC_01_01':ND2D1[6],'TC_01_10':ND2D1[7],'TC_01_11':ND2D1[8],
                              'TC_10_00':ND2D1[9],'TC_10_01':ND2D1[10],'TC_10_10':ND2D1[11],'TC_10_11':ND2D1[12],
                              'TC_11_00':ND2D1[13],'TC_11_01':ND2D1[14],'TC_11_10':ND2D1[15],'TC_11_11':ND2D1[16]}
        elif gate_prop == 'NR2D0':
            attrs[(n1,n2)] = {'SC': NR2D0[0], 'TC_00_00':NR2D0[1],'TC_00_01':NR2D0[2],'TC_00_10':NR2D0[3],'TC_00_11':NR2D0[4],
                              'TC_01_00':NR2D0[5],'TC_01_01':NR2D0[6],'TC_01_10':NR2D0[7],'TC_01_11':NR2D0[8],
                              'TC_10_00':NR2D0[9],'TC_10_01':NR2D0[10],'TC_10_10':NR2D0[11],'TC_10_11':NR2D0[12],
                              'TC_11_00':NR2D0[13],'TC_11_01':NR2D0[14],'TC_11_10':NR2D0[15],'TC_11_11':NR2D0[16]}
        elif gate_prop == 'NR2D3':
            attrs[(n1,n2)] = {'SC': NR2D3[0], 'TC_00_00':NR2D3[1],'TC_00_01':NR2D3[2],'TC_00_10':NR2D3[3],'TC_00_11':NR2D3[4],
                              'TC_01_00':NR2D3[5],'TC_01_01':NR2D3[6],'TC_01_10':NR2D3[7],'TC_01_11':NR2D3[8],
                              'TC_10_00':NR2D3[9],'TC_10_01':NR2D3[10],'TC_10_10':NR2D3[11],'TC_10_11':NR2D3[12],
                              'TC_11_00':NR2D3[13],'TC_11_01':NR2D3[14],'TC_11_10':NR2D3[15],'TC_11_11':NR2D3[16]}
        elif gate_prop == 'AN2D0':
            attrs[(n1,n2)] = {'SC': AN2D0[0], 'TC_00_00':AN2D0[1],'TC_00_01':AN2D0[2],'TC_00_10':AN2D0[3],'TC_00_11':AN2D0[4],
                              'TC_01_00':AN2D0[5],'TC_01_01':AN2D0[6],'TC_01_10':AN2D0[7],'TC_01_11':AN2D0[8],
                              'TC_10_00':AN2D0[9],'TC_10_01':AN2D0[10],'TC_10_10':AN2D0[11],'TC_10_11':AN2D0[12],
                              'TC_11_00':AN2D0[13],'TC_11_01':AN2D0[14],'TC_11_10':AN2D0[15],'TC_11_11':AN2D0[16]}
        elif gate_prop == 'AN2XD1':
            attrs[(n1,n2)] = {'SC': AN2XD1[0], 'TC_00_00':AN2XD1[1],'TC_00_01':AN2XD1[2],'TC_00_10':AN2XD1[3],'TC_00_11':AN2XD1[4],
                              'TC_01_00':AN2XD1[5],'TC_01_01':AN2XD1[6],'TC_01_10':AN2XD1[7],'TC_01_11':AN2XD1[8],
                              'TC_10_00':AN2XD1[9],'TC_10_01':AN2XD1[10],'TC_10_10':AN2XD1[11],'TC_10_11':AN2XD1[12],
                              'TC_11_00':AN2XD1[13],'TC_11_01':AN2XD1[14],'TC_11_10':AN2XD1[15],'TC_11_11':AN2XD1[16]}
        elif gate_prop == 'CKAN2D0':
            attrs[(n1,n2)] = {'SC': CKAN2D0[0], 'TC_00_00':CKAN2D0[1],'TC_00_01':CKAN2D0[2],'TC_00_10':CKAN2D0[3],'TC_00_11':CKAN2D0[4],
                              'TC_01_00':CKAN2D0[5],'TC_01_01':CKAN2D0[6],'TC_01_10':CKAN2D0[7],'TC_01_11':CKAN2D0[8],
                              'TC_10_00':CKAN2D0[9],'TC_10_01':CKAN2D0[10],'TC_10_10':CKAN2D0[11],'TC_10_11':CKAN2D0[12],
                              'TC_11_00':CKAN2D0[13],'TC_11_01':CKAN2D0[14],'TC_11_10':CKAN2D0[15],'TC_11_11':CKAN2D0[16]}
        elif gate_prop == 'CKAN2D1':
            attrs[(n1,n2)] = {'SC': CKAN2D1[0], 'TC_00_00':CKAN2D1[1],'TC_00_01':CKAN2D1[2],'TC_00_10':CKAN2D1[3],'TC_00_11':CKAN2D1[4],
                              'TC_01_00':CKAN2D1[5],'TC_01_01':CKAN2D1[6],'TC_01_10':CKAN2D1[7],'TC_01_11':CKAN2D1[8],
                              'TC_10_00':CKAN2D1[9],'TC_10_01':CKAN2D1[10],'TC_10_10':CKAN2D1[11],'TC_10_11':CKAN2D1[12],
                              'TC_11_00':CKAN2D1[13],'TC_11_01':CKAN2D1[14],'TC_11_10':CKAN2D1[15],'TC_11_11':CKAN2D1[16]}
        elif gate_prop == 'CKAN2D2':
            attrs[(n1,n2)] = {'SC': CKAN2D2[0], 'TC_00_00':CKAN2D2[1],'TC_00_01':CKAN2D2[2],'TC_00_10':CKAN2D2[3],'TC_00_11':CKAN2D2[4],
                              'TC_01_00':CKAN2D2[5],'TC_01_01':CKAN2D2[6],'TC_01_10':CKAN2D2[7],'TC_01_11':CKAN2D2[8],
                              'TC_10_00':CKAN2D2[9],'TC_10_01':CKAN2D2[10],'TC_10_10':CKAN2D2[11],'TC_10_11':CKAN2D2[12],
                              'TC_11_00':CKAN2D2[13],'TC_11_01':CKAN2D2[14],'TC_11_10':CKAN2D2[15],'TC_11_11':CKAN2D2[16]}
        elif gate_prop == 'CKAN2D4':
            attrs[(n1,n2)] = {'SC': CKAN2D4[0], 'TC_00_00':CKAN2D4[1],'TC_00_01':CKAN2D4[2],'TC_00_10':CKAN2D4[3],'TC_00_11':CKAN2D4[4],
                              'TC_01_00':CKAN2D4[5],'TC_01_01':CKAN2D4[6],'TC_01_10':CKAN2D4[7],'TC_01_11':CKAN2D4[8],
                              'TC_10_00':CKAN2D4[9],'TC_10_01':CKAN2D4[10],'TC_10_10':CKAN2D4[11],'TC_10_11':CKAN2D4[12],
                              'TC_11_00':CKAN2D4[13],'TC_11_01':CKAN2D4[14],'TC_11_10':CKAN2D4[15],'TC_11_11':CKAN2D4[16]}
        elif gate_prop == 'CKAN2D8':
            attrs[(n1,n2)] = {'SC': CKAN2D8[0], 'TC_00_00':CKAN2D8[1],'TC_00_01':CKAN2D8[2],'TC_00_10':CKAN2D8[3],'TC_00_11':CKAN2D8[4],
                              'TC_01_00':CKAN2D8[5],'TC_01_01':CKAN2D8[6],'TC_01_10':CKAN2D8[7],'TC_01_11':CKAN2D8[8],
                              'TC_10_00':CKAN2D8[9],'TC_10_01':CKAN2D8[10],'TC_10_10':CKAN2D8[11],'TC_10_11':CKAN2D8[12],
                              'TC_11_00':CKAN2D8[13],'TC_11_01':CKAN2D8[14],'TC_11_10':CKAN2D8[15],'TC_11_11':CKAN2D8[16]}
        elif gate_prop == 'IND2D0':
            attrs[(n1,n2)] = {'SC': IND2D0[0], 'TC_00_00':IND2D0[1],'TC_00_01':IND2D0[2],'TC_00_10':IND2D0[3],'TC_00_11':IND2D0[4],
                              'TC_01_00':IND2D0[5],'TC_01_01':IND2D0[6],'TC_01_10':IND2D0[7],'TC_01_11':IND2D0[8],
                              'TC_10_00':IND2D0[9],'TC_10_01':IND2D0[10],'TC_10_10':IND2D0[11],'TC_10_11':IND2D0[12],
                              'TC_11_00':IND2D0[13],'TC_11_01':IND2D0[14],'TC_11_10':IND2D0[15],'TC_11_11':IND2D0[16]}
        elif gate_prop == 'IND2D1':
            attrs[(n1,n2)] = {'SC': IND2D1[0], 'TC_00_00':IND2D1[1],'TC_00_01':IND2D1[2],'TC_00_10':IND2D1[3],'TC_00_11':IND2D1[4],
                              'TC_01_00':IND2D1[5],'TC_01_01':IND2D1[6],'TC_01_10':IND2D1[7],'TC_01_11':IND2D1[8],
                              'TC_10_00':IND2D1[9],'TC_10_01':IND2D1[10],'TC_10_10':IND2D1[11],'TC_10_11':IND2D1[12],
                              'TC_11_00':IND2D1[13],'TC_11_01':IND2D1[14],'TC_11_10':IND2D1[15],'TC_11_11':IND2D1[16]}
        elif gate_prop == 'IND2D2':
            attrs[(n1,n2)] = {'SC': IND2D2[0], 'TC_00_00':IND2D2[1],'TC_00_01':IND2D2[2],'TC_00_10':IND2D2[3],'TC_00_11':IND2D2[4],
                              'TC_01_00':IND2D2[5],'TC_01_01':IND2D2[6],'TC_01_10':IND2D2[7],'TC_01_11':IND2D2[8],
                              'TC_10_00':IND2D2[9],'TC_10_01':IND2D2[10],'TC_10_10':IND2D2[11],'TC_10_11':IND2D2[12],
                              'TC_11_00':IND2D2[13],'TC_11_01':IND2D2[14],'TC_11_10':IND2D2[15],'TC_11_11':IND2D2[16]}
        elif gate_prop == 'INR2D0':
            attrs[(n1,n2)] = {'SC': INR2D0[0], 'TC_00_00':INR2D0[1],'TC_00_01':INR2D0[2],'TC_00_10':INR2D0[3],'TC_00_11':INR2D0[4],
                              'TC_01_00':INR2D0[5],'TC_01_01':INR2D0[6],'TC_01_10':INR2D0[7],'TC_01_11':INR2D0[8],
                              'TC_10_00':INR2D0[9],'TC_10_01':INR2D0[10],'TC_10_10':INR2D0[11],'TC_10_11':INR2D0[12],
                              'TC_11_00':INR2D0[13],'TC_11_01':INR2D0[14],'TC_11_10':INR2D0[15],'TC_11_11':INR2D0[16]}
        elif gate_prop == 'INR2D1':
            attrs[(n1,n2)] = {'SC': INR2D1[0], 'TC_00_00':INR2D1[1],'TC_00_01':INR2D1[2],'TC_00_10':INR2D1[3],'TC_00_11':INR2D1[4],
                              'TC_01_00':INR2D1[5],'TC_01_01':INR2D1[6],'TC_01_10':INR2D1[7],'TC_01_11':INR2D1[8],
                              'TC_10_00':INR2D1[9],'TC_10_01':INR2D1[10],'TC_10_10':INR2D1[11],'TC_10_11':INR2D1[12],
                              'TC_11_00':INR2D1[13],'TC_11_01':INR2D1[14],'TC_11_10':INR2D1[15],'TC_11_11':INR2D1[16]}
        elif gate_prop == 'ND3D0':
            attrs[(n1,n2)] = {'SC': ND3D0[0], 'TC_00_00':ND3D0[1],'TC_00_01':ND3D0[2],'TC_00_10':ND3D0[3],'TC_00_11':ND3D0[4],
                              'TC_01_00':ND3D0[5],'TC_01_01':ND3D0[6],'TC_01_10':ND3D0[7],'TC_01_11':ND3D0[8],
                              'TC_10_00':ND3D0[9],'TC_10_01':ND3D0[10],'TC_10_10':ND3D0[11],'TC_10_11':ND3D0[12],
                              'TC_11_00':ND3D0[13],'TC_11_01':ND3D0[14],'TC_11_10':ND3D0[15],'TC_11_11':ND3D0[16]}
        elif gate_prop == 'ND3D1':
            attrs[(n1,n2)] = {'SC': ND3D1[0], 'TC_00_00':ND3D1[1],'TC_00_01':ND3D1[2],'TC_00_10':ND3D1[3],'TC_00_11':ND3D1[4],
                              'TC_01_00':ND3D1[5],'TC_01_01':ND3D1[6],'TC_01_10':ND3D1[7],'TC_01_11':ND3D1[8],
                              'TC_10_00':ND3D1[9],'TC_10_01':ND3D1[10],'TC_10_10':ND3D1[11],'TC_10_11':ND3D1[12],
                              'TC_11_00':ND3D1[13],'TC_11_01':ND3D1[14],'TC_11_10':ND3D1[15],'TC_11_11':ND3D1[16]}
        elif gate_prop == 'AN3D0':
            attrs[(n1,n2)] = {'SC': AN3D0[0], 'TC_00_00':AN3D0[1],'TC_00_01':AN3D0[2],'TC_00_10':AN3D0[3],'TC_00_11':AN3D0[4],
                              'TC_01_00':AN3D0[5],'TC_01_01':AN3D0[6],'TC_01_10':AN3D0[7],'TC_01_11':AN3D0[8],
                              'TC_10_00':AN3D0[9],'TC_10_01':AN3D0[10],'TC_10_10':AN3D0[11],'TC_10_11':AN3D0[12],
                              'TC_11_00':AN3D0[13],'TC_11_01':AN3D0[14],'TC_11_10':AN3D0[15],'TC_11_11':AN3D0[16]}
        elif gate_prop == 'AN3D1':
            attrs[(n1,n2)] = {'SC': AN3D1[0], 'TC_00_00':AN3D1[1],'TC_00_01':AN3D1[2],'TC_00_10':AN3D1[3],'TC_00_11':AN3D1[4],
                              'TC_01_00':AN3D1[5],'TC_01_01':AN3D1[6],'TC_01_10':AN3D1[7],'TC_01_11':AN3D1[8],
                              'TC_10_00':AN3D1[9],'TC_10_01':AN3D1[10],'TC_10_10':AN3D1[11],'TC_10_11':AN3D1[12],
                              'TC_11_00':AN3D1[13],'TC_11_01':AN3D1[14],'TC_11_10':AN3D1[15],'TC_11_11':AN3D1[16]}
        elif gate_prop == 'AN3D2':
            attrs[(n1,n2)] = {'SC': AN3D2[0], 'TC_00_00':AN3D2[1],'TC_00_01':AN3D2[2],'TC_00_10':AN3D2[3],'TC_00_11':AN3D2[4],
                              'TC_01_00':AN3D2[5],'TC_01_01':AN3D2[6],'TC_01_10':AN3D2[7],'TC_01_11':AN3D2[8],
                              'TC_10_00':AN3D2[9],'TC_10_01':AN3D2[10],'TC_10_10':AN3D2[11],'TC_10_11':AN3D2[12],
                              'TC_11_00':AN3D2[13],'TC_11_01':AN3D2[14],'TC_11_10':AN3D2[15],'TC_11_11':AN3D2[16]}
        elif gate_prop == 'INR3D0':
            attrs[(n1,n2)] = {'SC': INR3D0[0], 'TC_00_00':INR3D0[1],'TC_00_01':INR3D0[2],'TC_00_10':INR3D0[3],'TC_00_11':INR3D0[4],
                              'TC_01_00':INR3D0[5],'TC_01_01':INR3D0[6],'TC_01_10':INR3D0[7],'TC_01_11':INR3D0[8],
                              'TC_10_00':INR3D0[9],'TC_10_01':INR3D0[10],'TC_10_10':INR3D0[11],'TC_10_11':INR3D0[12],
                              'TC_11_00':INR3D0[13],'TC_11_01':INR3D0[14],'TC_11_10':INR3D0[15],'TC_11_11':INR3D0[16]}
        elif gate_prop == 'INR4D0':
            attrs[(n1,n2)] = {'SC': INR4D0[0], 'TC_00_00':INR4D0[1],'TC_00_01':INR4D0[2],'TC_00_10':INR4D0[3],'TC_00_11':INR4D0[4],
                              'TC_01_00':INR4D0[5],'TC_01_01':INR4D0[6],'TC_01_10':INR4D0[7],'TC_01_11':INR4D0[8],
                              'TC_10_00':INR4D0[9],'TC_10_01':INR4D0[10],'TC_10_10':INR4D0[11],'TC_10_11':INR4D0[12],
                              'TC_11_00':INR4D0[13],'TC_11_01':INR4D0[14],'TC_11_10':INR4D0[15],'TC_11_11':INR4D0[16]}
        elif gate_prop == 'IINR4D0':
            attrs[(n1,n2)] = {'SC': IINR4D0[0], 'TC_00_00':IINR4D0[1],'TC_00_01':IINR4D0[2],'TC_00_10':IINR4D0[3],'TC_00_11':IINR4D0[4],
                              'TC_01_00':IINR4D0[5],'TC_01_01':IINR4D0[6],'TC_01_10':IINR4D0[7],'TC_01_11':IINR4D0[8],
                              'TC_10_00':IINR4D0[9],'TC_10_01':IINR4D0[10],'TC_10_10':IINR4D0[11],'TC_10_11':IINR4D0[12],
                              'TC_11_00':IINR4D0[13],'TC_11_01':IINR4D0[14],'TC_11_10':IINR4D0[15],'TC_11_11':IINR4D0[16]}
        elif gate_prop == 'NR2D1':
            attrs[(n1,n2)] = {'SC': NR2D1[0], 'TC_00_00':NR2D1[1],'TC_00_01':NR2D1[2],'TC_00_10':NR2D1[3],'TC_00_11':NR2D1[4],
                              'TC_01_00':NR2D1[5],'TC_01_01':NR2D1[6],'TC_01_10':NR2D1[7],'TC_01_11':NR2D1[8],
                              'TC_10_00':NR2D1[9],'TC_10_01':NR2D1[10],'TC_10_10':NR2D1[11],'TC_10_11':NR2D1[12],
                              'TC_11_00':NR2D1[13],'TC_11_01':NR2D1[14],'TC_11_10':NR2D1[15],'TC_11_11':NR2D1[16]}
        elif gate_prop == 'ND4D0':
            attrs[(n1,n2)] = {'SC': ND4D0[0], 'TC_00_00':ND4D0[1],'TC_00_01':ND4D0[2],'TC_00_10':ND4D0[3],'TC_00_11':ND4D0[4],
                              'TC_01_00':ND4D0[5],'TC_01_01':ND4D0[6],'TC_01_10':ND4D0[7],'TC_01_11':ND4D0[8],
                              'TC_10_00':ND4D0[9],'TC_10_01':ND4D0[10],'TC_10_10':ND4D0[11],'TC_10_11':ND4D0[12],
                              'TC_11_00':ND4D0[13],'TC_11_01':ND4D0[14],'TC_11_10':ND4D0[15],'TC_11_11':ND4D0[16]}
        elif gate_prop == 'ND4D1':
            attrs[(n1,n2)] = {'SC': ND4D1[0], 'TC_00_00':ND4D1[1],'TC_00_01':ND4D1[2],'TC_00_10':ND4D1[3],'TC_00_11':ND4D1[4],
                              'TC_01_00':ND4D1[5],'TC_01_01':ND4D1[6],'TC_01_10':ND4D1[7],'TC_01_11':ND4D1[8],
                              'TC_10_00':ND4D1[9],'TC_10_01':ND4D1[10],'TC_10_10':ND4D1[11],'TC_10_11':ND4D1[12],
                              'TC_11_00':ND4D1[13],'TC_11_01':ND4D1[14],'TC_11_10':ND4D1[15],'TC_11_11':ND4D1[16]}
        elif gate_prop == 'NR4D0':
            attrs[(n1,n2)] = {'SC': NR4D0[0], 'TC_00_00':NR4D0[1],'TC_00_01':NR4D0[2],'TC_00_10':NR4D0[3],'TC_00_11':NR4D0[4],
                              'TC_01_00':NR4D0[5],'TC_01_01':NR4D0[6],'TC_01_10':NR4D0[7],'TC_01_11':NR4D0[8],
                              'TC_10_00':NR4D0[9],'TC_10_01':NR4D0[10],'TC_10_10':NR4D0[11],'TC_10_11':NR4D0[12],
                              'TC_11_00':NR4D0[13],'TC_11_01':NR4D0[14],'TC_11_10':NR4D0[15],'TC_11_11':NR4D0[16]}
        elif gate_prop == 'IND4D1':
            attrs[(n1,n2)] = {'SC': IND4D1[0], 'TC_00_00':IND4D1[1],'TC_00_01':IND4D1[2],'TC_00_10':IND4D1[3],'TC_00_11':IND4D1[4],
                              'TC_01_00':IND4D1[5],'TC_01_01':IND4D1[6],'TC_01_10':IND4D1[7],'TC_01_11':IND4D1[8],
                              'TC_10_00':IND4D1[9],'TC_10_01':IND4D1[10],'TC_10_10':IND4D1[11],'TC_10_11':IND4D1[12],
                              'TC_11_00':IND4D1[13],'TC_11_01':IND4D1[14],'TC_11_10':IND4D1[15],'TC_11_11':IND4D1[16]}
        elif gate_prop == 'IND4D0':
            attrs[(n1,n2)] = {'SC': IND4D0[0], 'TC_00_00':IND4D0[1],'TC_00_01':IND4D0[2],'TC_00_10':IND4D0[3],'TC_00_11':IND4D0[4],
                              'TC_01_00':IND4D0[5],'TC_01_01':IND4D0[6],'TC_01_10':IND4D0[7],'TC_01_11':IND4D0[8],
                              'TC_10_00':IND4D0[9],'TC_10_01':IND4D0[10],'TC_10_10':IND4D0[11],'TC_10_11':IND4D0[12],
                              'TC_11_00':IND4D0[13],'TC_11_01':IND4D0[14],'TC_11_10':IND4D0[15],'TC_11_11':IND4D0[16]}
        elif gate_prop == 'IIND4D1':
            attrs[(n1,n2)] = {'SC': IIND4D1[0], 'TC_00_00':IIND4D1[1],'TC_00_01':IIND4D1[2],'TC_00_10':IIND4D1[3],'TC_00_11':IIND4D1[4],
                              'TC_01_00':IIND4D1[5],'TC_01_01':IIND4D1[6],'TC_01_10':IIND4D1[7],'TC_01_11':IIND4D1[8],
                              'TC_10_00':IIND4D1[9],'TC_10_01':IIND4D1[10],'TC_10_10':IIND4D1[11],'TC_10_11':IIND4D1[12],
                              'TC_11_00':IIND4D1[13],'TC_11_01':IIND4D1[14],'TC_11_10':IIND4D1[15],'TC_11_11':IIND4D1[16]}
        elif gate_prop == 'INR4D1':
            attrs[(n1,n2)] = {'SC': INR4D1[0], 'TC_00_00':INR4D1[1],'TC_00_01':INR4D1[2],'TC_00_10':INR4D1[3],'TC_00_11':INR4D1[4],
                              'TC_01_00':INR4D1[5],'TC_01_01':INR4D1[6],'TC_01_10':INR4D1[7],'TC_01_11':INR4D1[8],
                              'TC_10_00':INR4D1[9],'TC_10_01':INR4D1[10],'TC_10_10':INR4D1[11],'TC_10_11':INR4D1[12],
                              'TC_11_00':INR4D1[13],'TC_11_01':INR4D1[14],'TC_11_10':INR4D1[15],'TC_11_11':INR4D1[16]}
        elif gate_prop == 'IND3D0':
            attrs[(n1,n2)] = {'SC': IND3D0[0], 'TC_00_00':IND3D0[1],'TC_00_01':IND3D0[2],'TC_00_10':IND3D0[3],'TC_00_11':IND3D0[4],
                              'TC_01_00':IND3D0[5],'TC_01_01':IND3D0[6],'TC_01_10':IND3D0[7],'TC_01_11':IND3D0[8],
                              'TC_10_00':IND3D0[9],'TC_10_01':IND3D0[10],'TC_10_10':IND3D0[11],'TC_10_11':IND3D0[12],
                              'TC_11_00':IND3D0[13],'TC_11_01':IND3D0[14],'TC_11_10':IND3D0[15],'TC_11_11':IND3D0[16]}
        elif gate_prop == 'NR2XD1':
            attrs[(n1,n2)] = {'SC': NR2XD1[0], 'TC_00_00':NR2XD1[1],'TC_00_01':NR2XD1[2],'TC_00_10':NR2XD1[3],'TC_00_11':NR2XD1[4],
                              'TC_01_00':NR2XD1[5],'TC_01_01':NR2XD1[6],'TC_01_10':NR2XD1[7],'TC_01_11':NR2XD1[8],
                              'TC_10_00':NR2XD1[9],'TC_10_01':NR2XD1[10],'TC_10_10':NR2XD1[11],'TC_10_11':NR2XD1[12],
                              'TC_11_00':NR2XD1[13],'TC_11_01':NR2XD1[14],'TC_11_10':NR2XD1[15],'TC_11_11':NR2XD1[16]}
        elif gate_prop == 'NR2XD0':
            attrs[(n1,n2)] = {'SC': NR2XD0[0], 'TC_00_00':NR2XD0[1],'TC_00_01':NR2XD0[2],'TC_00_10':NR2XD0[3],'TC_00_11':NR2XD0[4],
                              'TC_01_00':NR2XD0[5],'TC_01_01':NR2XD0[6],'TC_01_10':NR2XD0[7],'TC_01_11':NR2XD0[8],
                              'TC_10_00':NR2XD0[9],'TC_10_01':NR2XD0[10],'TC_10_10':NR2XD0[11],'TC_10_11':NR2XD0[12],
                              'TC_11_00':NR2XD0[13],'TC_11_01':NR2XD0[14],'TC_11_10':NR2XD0[15],'TC_11_11':NR2XD0[16]}
        elif gate_prop == 'OR3D0':
            attrs[(n1,n2)] = {'SC': OR3D0[0], 'TC_00_00':OR3D0[1],'TC_00_01':OR3D0[2],'TC_00_10':OR3D0[3],'TC_00_11':OR3D0[4],
                              'TC_01_00':OR3D0[5],'TC_01_01':OR3D0[6],'TC_01_10':OR3D0[7],'TC_01_11':OR3D0[8],
                              'TC_10_00':OR3D0[9],'TC_10_01':OR3D0[10],'TC_10_10':OR3D0[11],'TC_10_11':OR3D0[12],
                              'TC_11_00':OR3D0[13],'TC_11_01':OR3D0[14],'TC_11_10':OR3D0[15],'TC_11_11':OR3D0[16]}
        elif gate_prop == 'OR3D2':
            attrs[(n1,n2)] = {'SC': OR3D2[0], 'TC_00_00':OR3D2[1],'TC_00_01':OR3D2[2],'TC_00_10':OR3D2[3],'TC_00_11':OR3D2[4],
                              'TC_01_00':OR3D2[5],'TC_01_01':OR3D2[6],'TC_01_10':OR3D2[7],'TC_01_11':OR3D2[8],
                              'TC_10_00':OR3D2[9],'TC_10_01':OR3D2[10],'TC_10_10':OR3D2[11],'TC_10_11':OR3D2[12],
                              'TC_11_00':OR3D2[13],'TC_11_01':OR3D2[14],'TC_11_10':OR3D2[15],'TC_11_11':OR3D2[16]}
        elif gate_prop == 'NR3D0':
            attrs[(n1,n2)] = {'SC': NR3D0[0], 'TC_00_00':NR3D0[1],'TC_00_01':NR3D0[2],'TC_00_10':NR3D0[3],'TC_00_11':NR3D0[4],
                              'TC_01_00':NR3D0[5],'TC_01_01':NR3D0[6],'TC_01_10':NR3D0[7],'TC_01_11':NR3D0[8],
                              'TC_10_00':NR3D0[9],'TC_10_01':NR3D0[10],'TC_10_10':NR3D0[11],'TC_10_11':NR3D0[12],
                              'TC_11_00':NR3D0[13],'TC_11_01':NR3D0[14],'TC_11_10':NR3D0[15],'TC_11_11':NR3D0[16]}
        elif gate_prop == 'NR3D1':
            attrs[(n1,n2)] = {'SC': NR3D1[0], 'TC_00_00':NR3D1[1],'TC_00_01':NR3D1[2],'TC_00_10':NR3D1[3],'TC_00_11':NR3D1[4],
                              'TC_01_00':NR3D1[5],'TC_01_01':NR3D1[6],'TC_01_10':NR3D1[7],'TC_01_11':NR3D1[8],
                              'TC_10_00':NR3D1[9],'TC_10_01':NR3D1[10],'TC_10_10':NR3D1[11],'TC_10_11':NR3D1[12],
                              'TC_11_00':NR3D1[13],'TC_11_01':NR3D1[14],'TC_11_10':NR3D1[15],'TC_11_11':NR3D1[16]}    
        elif gate_prop == 'OR2D0':
            attrs[(n1,n2)] = {'SC': OR2D0[0], 'TC_00_00':OR2D0[1],'TC_00_01':OR2D0[2],'TC_00_10':OR2D0[3],'TC_00_11':OR2D0[4],
                              'TC_01_00':OR2D0[5],'TC_01_01':OR2D0[6],'TC_01_10':OR2D0[7],'TC_01_11':OR2D0[8],
                              'TC_10_00':OR2D0[9],'TC_10_01':OR2D0[10],'TC_10_10':OR2D0[11],'TC_10_11':OR2D0[12],
                              'TC_11_00':OR2D0[13],'TC_11_01':OR2D0[14],'TC_11_10':OR2D0[15],'TC_11_11':OR2D0[16]}
        elif gate_prop == 'OR2D2':
            attrs[(n1,n2)] = {'SC': OR2D2[0], 'TC_00_00':OR2D2[1],'TC_00_01':OR2D2[2],'TC_00_10':OR2D2[3],'TC_00_11':OR2D2[4],
                              'TC_01_00':OR2D2[5],'TC_01_01':OR2D2[6],'TC_01_10':OR2D2[7],'TC_01_11':OR2D2[8],
                              'TC_10_00':OR2D2[9],'TC_10_01':OR2D2[10],'TC_10_10':OR2D2[11],'TC_10_11':OR2D2[12],
                              'TC_11_00':OR2D2[13],'TC_11_01':OR2D2[14],'TC_11_10':OR2D2[15],'TC_11_11':OR2D2[16]}
        elif gate_prop == 'OR2D4':
            attrs[(n1,n2)] = {'SC': OR2D4[0], 'TC_00_00':OR2D4[1],'TC_00_01':OR2D4[2],'TC_00_10':OR2D4[3],'TC_00_11':OR2D4[4],
                              'TC_01_00':OR2D4[5],'TC_01_01':OR2D4[6],'TC_01_10':OR2D4[7],'TC_01_11':OR2D4[8],
                              'TC_10_00':OR2D4[9],'TC_10_01':OR2D4[10],'TC_10_10':OR2D4[11],'TC_10_11':OR2D4[12],
                              'TC_11_00':OR2D4[13],'TC_11_01':OR2D4[14],'TC_11_10':OR2D4[15],'TC_11_11':OR2D4[16]}
        elif gate_prop == 'OR2D8':
            attrs[(n1,n2)] = {'SC': OR2D8[0], 'TC_00_00':OR2D8[1],'TC_00_01':OR2D8[2],'TC_00_10':OR2D8[3],'TC_00_11':OR2D8[4],
                              'TC_01_00':OR2D8[5],'TC_01_01':OR2D8[6],'TC_01_10':OR2D8[7],'TC_01_11':OR2D8[8],
                              'TC_10_00':OR2D8[9],'TC_10_01':OR2D8[10],'TC_10_10':OR2D8[11],'TC_10_11':OR2D8[12],
                              'TC_11_00':OR2D8[13],'TC_11_01':OR2D8[14],'TC_11_10':OR2D8[15],'TC_11_11':OR2D8[16]}
        elif gate_prop == 'OR2D1':
            attrs[(n1,n2)] = {'SC': OR2D1[0], 'TC_00_00':OR2D1[1],'TC_00_01':OR2D1[2],'TC_00_10':OR2D1[3],'TC_00_11':OR2D1[4],
                              'TC_01_00':OR2D1[5],'TC_01_01':OR2D1[6],'TC_01_10':OR2D1[7],'TC_01_11':OR2D1[8],
                              'TC_10_00':OR2D1[9],'TC_10_01':OR2D1[10],'TC_10_10':OR2D1[11],'TC_10_11':OR2D1[12],
                              'TC_11_00':OR2D1[13],'TC_11_01':OR2D1[14],'TC_11_10':OR2D1[15],'TC_11_11':OR2D1[16]}
        elif gate_prop == 'INR2XD0':
            attrs[(n1,n2)] = {'SC': INR2XD0[0], 'TC_00_00':INR2XD0[1],'TC_00_01':INR2XD0[2],'TC_00_10':INR2XD0[3],'TC_00_11':INR2XD0[4],
                              'TC_01_00':INR2XD0[5],'TC_01_01':INR2XD0[6],'TC_01_10':INR2XD0[7],'TC_01_11':INR2XD0[8],
                              'TC_10_00':INR2XD0[9],'TC_10_01':INR2XD0[10],'TC_10_10':INR2XD0[11],'TC_10_11':INR2XD0[12],
                              'TC_11_00':INR2XD0[13],'TC_11_01':INR2XD0[14],'TC_11_10':INR2XD0[15],'TC_11_11':INR2XD0[16]}
        elif gate_prop == 'INR2XD1':
            attrs[(n1,n2)] = {'SC': INR2XD1[0], 'TC_00_00':INR2XD1[1],'TC_00_01':INR2XD1[2],'TC_00_10':INR2XD1[3],'TC_00_11':INR2XD1[4],
                              'TC_01_00':INR2XD1[5],'TC_01_01':INR2XD1[6],'TC_01_10':INR2XD1[7],'TC_01_11':INR2XD1[8],
                              'TC_10_00':INR2XD1[9],'TC_10_01':INR2XD1[10],'TC_10_10':INR2XD1[11],'TC_10_11':INR2XD1[12],
                              'TC_11_00':INR2XD1[13],'TC_11_01':INR2XD1[14],'TC_11_10':INR2XD1[15],'TC_11_11':INR2XD1[16]}
        elif gate_prop == 'AN4D0':
            attrs[(n1,n2)] = {'SC': AN4D0[0], 'TC_00_00':AN4D0[1],'TC_00_01':AN4D0[2],'TC_00_10':AN4D0[3],'TC_00_11':AN4D0[4],
                              'TC_01_00':AN4D0[5],'TC_01_01':AN4D0[6],'TC_01_10':AN4D0[7],'TC_01_11':AN4D0[8],
                              'TC_10_00':AN4D0[9],'TC_10_01':AN4D0[10],'TC_10_10':AN4D0[11],'TC_10_11':AN4D0[12],
                              'TC_11_00':AN4D0[13],'TC_11_01':AN4D0[14],'TC_11_10':AN4D0[15],'TC_11_11':AN4D0[16]}
        elif gate_prop == 'AN4D2':
            attrs[(n1,n2)] = {'SC': AN4D2[0], 'TC_00_00':AN4D2[1],'TC_00_01':AN4D2[2],'TC_00_10':AN4D2[3],'TC_00_11':AN4D2[4],
                              'TC_01_00':AN4D2[5],'TC_01_01':AN4D2[6],'TC_01_10':AN4D2[7],'TC_01_11':AN4D2[8],
                              'TC_10_00':AN4D2[9],'TC_10_01':AN4D2[10],'TC_10_10':AN4D2[11],'TC_10_11':AN4D2[12],
                              'TC_11_00':AN4D2[13],'TC_11_01':AN4D2[14],'TC_11_10':AN4D2[15],'TC_11_11':AN4D2[16]}
        elif gate_prop == 'OR4D0':
            attrs[(n1,n2)] = {'SC': OR4D0[0], 'TC_00_00':OR4D0[1],'TC_00_01':OR4D0[2],'TC_00_10':OR4D0[3],'TC_00_11':OR4D0[4],
                              'TC_01_00':OR4D0[5],'TC_01_01':OR4D0[6],'TC_01_10':OR4D0[7],'TC_01_11':OR4D0[8],
                              'TC_10_00':OR4D0[9],'TC_10_01':OR4D0[10],'TC_10_10':OR4D0[11],'TC_10_11':OR4D0[12],
                              'TC_11_00':OR4D0[13],'TC_11_01':OR4D0[14],'TC_11_10':OR4D0[15],'TC_11_11':OR4D0[16]}
        elif gate_prop == 'OR4D1':
            attrs[(n1,n2)] = {'SC': OR4D1[0], 'TC_00_00':OR4D1[1],'TC_00_01':OR4D1[2],'TC_00_10':OR4D1[3],'TC_00_11':OR4D1[4],
                              'TC_01_00':OR4D1[5],'TC_01_01':OR4D1[6],'TC_01_10':OR4D1[7],'TC_01_11':OR4D1[8],
                              'TC_10_00':OR4D1[9],'TC_10_01':OR4D1[10],'TC_10_10':OR4D1[11],'TC_10_11':OR4D1[12],
                              'TC_11_00':OR4D1[13],'TC_11_01':OR4D1[14],'TC_11_10':OR4D1[15],'TC_11_11':OR4D1[16]}
        elif gate_prop == 'AN4D1':
            attrs[(n1,n2)] = {'SC': AN4D1[0], 'TC_00_00':AN4D1[1],'TC_00_01':AN4D1[2],'TC_00_10':AN4D1[3],'TC_00_11':AN4D1[4],
                              'TC_01_00':AN4D1[5],'TC_01_01':AN4D1[6],'TC_01_10':AN4D1[7],'TC_01_11':AN4D1[8],
                              'TC_10_00':AN4D1[9],'TC_10_01':AN4D1[10],'TC_10_10':AN4D1[11],'TC_10_11':AN4D1[12],
                              'TC_11_00':AN4D1[13],'TC_11_01':AN4D1[14],'TC_11_10':AN4D1[15],'TC_11_11':AN4D1[16]}
        elif gate_prop == 'AOI22D0':
            attrs[(n1,n2)] = {'SC': AOI22D0[0], 'TC_00_00':AOI22D0[1],'TC_00_01':AOI22D0[2],'TC_00_10':AOI22D0[3],'TC_00_11':AOI22D0[4],
                              'TC_01_00':AOI22D0[5],'TC_01_01':AOI22D0[6],'TC_01_10':AOI22D0[7],'TC_01_11':AOI22D0[8],
                              'TC_10_00':AOI22D0[9],'TC_10_01':AOI22D0[10],'TC_10_10':AOI22D0[11],'TC_10_11':AOI22D0[12],
                              'TC_11_00':AOI22D0[13],'TC_11_01':AOI22D0[14],'TC_11_10':AOI22D0[15],'TC_11_11':AOI22D0[16]}
        elif gate_prop == 'AOI21D0':
            attrs[(n1,n2)] = {'SC': AOI21D0[0], 'TC_00_00':AOI21D0[1],'TC_00_01':AOI21D0[2],'TC_00_10':AOI21D0[3],'TC_00_11':AOI21D0[4],
                              'TC_01_00':AOI21D0[5],'TC_01_01':AOI21D0[6],'TC_01_10':AOI21D0[7],'TC_01_11':AOI21D0[8],
                              'TC_10_00':AOI21D0[9],'TC_10_01':AOI21D0[10],'TC_10_10':AOI21D0[11],'TC_10_11':AOI21D0[12],
                              'TC_11_00':AOI21D0[13],'TC_11_01':AOI21D0[14],'TC_11_10':AOI21D0[15],'TC_11_11':AOI21D0[16]}
        elif gate_prop == 'AOI21D1':
            attrs[(n1,n2)] = {'SC': AOI21D1[0], 'TC_00_00':AOI21D1[1],'TC_00_01':AOI21D1[2],'TC_00_10':AOI21D1[3],'TC_00_11':AOI21D1[4],
                              'TC_01_00':AOI21D1[5],'TC_01_01':AOI21D1[6],'TC_01_10':AOI21D1[7],'TC_01_11':AOI21D1[8],
                              'TC_10_00':AOI21D1[9],'TC_10_01':AOI21D1[10],'TC_10_10':AOI21D1[11],'TC_10_11':AOI21D1[12],
                              'TC_11_00':AOI21D1[13],'TC_11_01':AOI21D1[14],'TC_11_10':AOI21D1[15],'TC_11_11':AOI21D1[16]}
        elif gate_prop == 'OAI21D0':
            attrs[(n1,n2)] = {'SC': OAI21D0[0], 'TC_00_00':OAI21D0[1],'TC_00_01':OAI21D0[2],'TC_00_10':OAI21D0[3],'TC_00_11':OAI21D0[4],
                              'TC_01_00':OAI21D0[5],'TC_01_01':OAI21D0[6],'TC_01_10':OAI21D0[7],'TC_01_11':OAI21D0[8],
                              'TC_10_00':OAI21D0[9],'TC_10_01':OAI21D0[10],'TC_10_10':OAI21D0[11],'TC_10_11':OAI21D0[12],
                              'TC_11_00':OAI21D0[13],'TC_11_01':OAI21D0[14],'TC_11_10':OAI21D0[15],'TC_11_11':OAI21D0[16]}
        elif gate_prop == 'MAOI22D0':
            attrs[(n1,n2)] = {'SC': MAOI22D0[0], 'TC_00_00':MAOI22D0[1],'TC_00_01':MAOI22D0[2],'TC_00_10':MAOI22D0[3],'TC_00_11':MAOI22D0[4],
                              'TC_01_00':MAOI22D0[5],'TC_01_01':MAOI22D0[6],'TC_01_10':MAOI22D0[7],'TC_01_11':MAOI22D0[8],
                              'TC_10_00':MAOI22D0[9],'TC_10_01':MAOI22D0[10],'TC_10_10':MAOI22D0[11],'TC_10_11':MAOI22D0[12],
                              'TC_11_00':MAOI22D0[13],'TC_11_01':MAOI22D0[14],'TC_11_10':MAOI22D0[15],'TC_11_11':MAOI22D0[16]}
        elif gate_prop == 'AO33D0':
            attrs[(n1,n2)] = {'SC': AO33D0[0], 'TC_00_00':AO33D0[1],'TC_00_01':AO33D0[2],'TC_00_10':AO33D0[3],'TC_00_11':AO33D0[4],
                              'TC_01_00':AO33D0[5],'TC_01_01':AO33D0[6],'TC_01_10':AO33D0[7],'TC_01_11':AO33D0[8],
                              'TC_10_00':AO33D0[9],'TC_10_01':AO33D0[10],'TC_10_10':AO33D0[11],'TC_10_11':AO33D0[12],
                              'TC_11_00':AO33D0[13],'TC_11_01':AO33D0[14],'TC_11_10':AO33D0[15],'TC_11_11':AO33D0[16]}
        elif gate_prop == 'AO33D1':
            attrs[(n1,n2)] = {'SC': AO33D1[0], 'TC_00_00':AO33D1[1],'TC_00_01':AO33D1[2],'TC_00_10':AO33D1[3],'TC_00_11':AO33D1[4],
                              'TC_01_00':AO33D1[5],'TC_01_01':AO33D1[6],'TC_01_10':AO33D1[7],'TC_01_11':AO33D1[8],
                              'TC_10_00':AO33D1[9],'TC_10_01':AO33D1[10],'TC_10_10':AO33D1[11],'TC_10_11':AO33D1[12],
                              'TC_11_00':AO33D1[13],'TC_11_01':AO33D1[14],'TC_11_10':AO33D1[15],'TC_11_11':AO33D1[16]}
        elif gate_prop == 'FCICOND1':
            attrs[(n1,n2)] = {'SC': FCICOND1[0], 'TC_00_00':FCICOND1[1],'TC_00_01':FCICOND1[2],'TC_00_10':FCICOND1[3],'TC_00_11':FCICOND1[4],
                              'TC_01_00':FCICOND1[5],'TC_01_01':FCICOND1[6],'TC_01_10':FCICOND1[7],'TC_01_11':FCICOND1[8],
                              'TC_10_00':FCICOND1[9],'TC_10_01':FCICOND1[10],'TC_10_10':FCICOND1[11],'TC_10_11':FCICOND1[12],
                              'TC_11_00':FCICOND1[13],'TC_11_01':FCICOND1[14],'TC_11_10':FCICOND1[15],'TC_11_11':FCICOND1[16]}
        elif gate_prop == 'FCICIND1':
            attrs[(n1,n2)] = {'SC': FCICIND1[0], 'TC_00_00':FCICIND1[1],'TC_00_01':FCICIND1[2],'TC_00_10':FCICIND1[3],'TC_00_11':FCICIND1[4],
                              'TC_01_00':FCICIND1[5],'TC_01_01':FCICIND1[6],'TC_01_10':FCICIND1[7],'TC_01_11':FCICIND1[8],
                              'TC_10_00':FCICIND1[9],'TC_10_01':FCICIND1[10],'TC_10_10':FCICIND1[11],'TC_10_11':FCICIND1[12],
                              'TC_11_00':FCICIND1[13],'TC_11_01':FCICIND1[14],'TC_11_10':FCICIND1[15],'TC_11_11':FCICIND1[16]}
        elif gate_prop == 'OA22D0':
            attrs[(n1,n2)] = {'SC': OA22D0[0], 'TC_00_00':OA22D0[1],'TC_00_01':OA22D0[2],'TC_00_10':OA22D0[3],'TC_00_11':OA22D0[4],
                              'TC_01_00':OA22D0[5],'TC_01_01':OA22D0[6],'TC_01_10':OA22D0[7],'TC_01_11':OA22D0[8],
                              'TC_10_00':OA22D0[9],'TC_10_01':OA22D0[10],'TC_10_10':OA22D0[11],'TC_10_11':OA22D0[12],
                              'TC_11_00':OA22D0[13],'TC_11_01':OA22D0[14],'TC_11_10':OA22D0[15],'TC_11_11':OA22D0[16]}
        elif gate_prop == 'IOA22D1':
            attrs[(n1,n2)] = {'SC': IOA22D1[0], 'TC_00_00':IOA22D1[1],'TC_00_01':IOA22D1[2],'TC_00_10':IOA22D1[3],'TC_00_11':IOA22D1[4],
                              'TC_01_00':IOA22D1[5],'TC_01_01':IOA22D1[6],'TC_01_10':IOA22D1[7],'TC_01_11':IOA22D1[8],
                              'TC_10_00':IOA22D1[9],'TC_10_01':IOA22D1[10],'TC_10_10':IOA22D1[11],'TC_10_11':IOA22D1[12],
                              'TC_11_00':IOA22D1[13],'TC_11_01':IOA22D1[14],'TC_11_10':IOA22D1[15],'TC_11_11':IOA22D1[16]}
        elif gate_prop == 'IOA22D2':
            attrs[(n1,n2)] = {'SC': IOA22D2[0], 'TC_00_00':IOA22D2[1],'TC_00_01':IOA22D2[2],'TC_00_10':IOA22D2[3],'TC_00_11':IOA22D2[4],
                              'TC_01_00':IOA22D2[5],'TC_01_01':IOA22D2[6],'TC_01_10':IOA22D2[7],'TC_01_11':IOA22D2[8],
                              'TC_10_00':IOA22D2[9],'TC_10_01':IOA22D2[10],'TC_10_10':IOA22D2[11],'TC_10_11':IOA22D2[12],
                              'TC_11_00':IOA22D2[13],'TC_11_01':IOA22D2[14],'TC_11_10':IOA22D2[15],'TC_11_11':IOA22D2[16]}
        elif gate_prop == 'OAI22D0':
            attrs[(n1,n2)] = {'SC': OAI22D0[0], 'TC_00_00':OAI22D0[1],'TC_00_01':OAI22D0[2],'TC_00_10':OAI22D0[3],'TC_00_11':OAI22D0[4],
                              'TC_01_00':OAI22D0[5],'TC_01_01':OAI22D0[6],'TC_01_10':OAI22D0[7],'TC_01_11':OAI22D0[8],
                              'TC_10_00':OAI22D0[9],'TC_10_01':OAI22D0[10],'TC_10_10':OAI22D0[11],'TC_10_11':OAI22D0[12],
                              'TC_11_00':OAI22D0[13],'TC_11_01':OAI22D0[14],'TC_11_10':OAI22D0[15],'TC_11_11':OAI22D0[16]}
        elif gate_prop == 'OAI22D1':
            attrs[(n1,n2)] = {'SC': OAI22D1[0], 'TC_00_00':OAI22D1[1],'TC_00_01':OAI22D1[2],'TC_00_10':OAI22D1[3],'TC_00_11':OAI22D1[4],
                              'TC_01_00':OAI22D1[5],'TC_01_01':OAI22D1[6],'TC_01_10':OAI22D1[7],'TC_01_11':OAI22D1[8],
                              'TC_10_00':OAI22D1[9],'TC_10_01':OAI22D1[10],'TC_10_10':OAI22D1[11],'TC_10_11':OAI22D1[12],
                              'TC_11_00':OAI22D1[13],'TC_11_01':OAI22D1[14],'TC_11_10':OAI22D1[15],'TC_11_11':OAI22D1[16]}
        elif gate_prop == 'IAO22D1':
            attrs[(n1,n2)] = {'SC': IAO22D1[0], 'TC_00_00':IAO22D1[1],'TC_00_01':IAO22D1[2],'TC_00_10':IAO22D1[3],'TC_00_11':IAO22D1[4],
                              'TC_01_00':IAO22D1[5],'TC_01_01':IAO22D1[6],'TC_01_10':IAO22D1[7],'TC_01_11':IAO22D1[8],
                              'TC_10_00':IAO22D1[9],'TC_10_01':IAO22D1[10],'TC_10_10':IAO22D1[11],'TC_10_11':IAO22D1[12],
                              'TC_11_00':IAO22D1[13],'TC_11_01':IAO22D1[14],'TC_11_10':IAO22D1[15],'TC_11_11':IAO22D1[16]}
        elif gate_prop == 'MOAI22D0':
            attrs[(n1,n2)] = {'SC': MOAI22D0[0], 'TC_00_00':MOAI22D0[1],'TC_00_01':MOAI22D0[2],'TC_00_10':MOAI22D0[3],'TC_00_11':MOAI22D0[4],
                              'TC_01_00':MOAI22D0[5],'TC_01_01':MOAI22D0[6],'TC_01_10':MOAI22D0[7],'TC_01_11':MOAI22D0[8],
                              'TC_10_00':MOAI22D0[9],'TC_10_01':MOAI22D0[10],'TC_10_10':MOAI22D0[11],'TC_10_11':MOAI22D0[12],
                              'TC_11_00':MOAI22D0[13],'TC_11_01':MOAI22D0[14],'TC_11_10':MOAI22D0[15],'TC_11_11':MOAI22D0[16]}
        elif gate_prop == 'MAOI222D0':
            attrs[(n1,n2)] = {'SC': MAOI222D0[0], 'TC_00_00':MAOI222D0[1],'TC_00_01':MAOI222D0[2],'TC_00_10':MAOI222D0[3],'TC_00_11':MAOI222D0[4],
                              'TC_01_00':MAOI222D0[5],'TC_01_01':MAOI222D0[6],'TC_01_10':MAOI222D0[7],'TC_01_11':MAOI222D0[8],
                              'TC_10_00':MAOI222D0[9],'TC_10_01':MAOI222D0[10],'TC_10_10':MAOI222D0[11],'TC_10_11':MAOI222D0[12],
                              'TC_11_00':MAOI222D0[13],'TC_11_01':MAOI222D0[14],'TC_11_10':MAOI222D0[15],'TC_11_11':MAOI222D0[16]}
        elif gate_prop == 'MAOI222D1':
            attrs[(n1,n2)] = {'SC': MAOI222D1[0], 'TC_00_00':MAOI222D1[1],'TC_00_01':MAOI222D1[2],'TC_00_10':MAOI222D1[3],'TC_00_11':MAOI222D1[4],
                              'TC_01_00':MAOI222D1[5],'TC_01_01':MAOI222D1[6],'TC_01_10':MAOI222D1[7],'TC_01_11':MAOI222D1[8],
                              'TC_10_00':MAOI222D1[9],'TC_10_01':MAOI222D1[10],'TC_10_10':MAOI222D1[11],'TC_10_11':MAOI222D1[12],
                              'TC_11_00':MAOI222D1[13],'TC_11_01':MAOI222D1[14],'TC_11_10':MAOI222D1[15],'TC_11_11':MAOI222D1[16]}
        elif gate_prop == 'FA1D0_0':
            attrs[(n1,n2)] = {'SC': FA1D0_0[0], 'TC_00_00':FA1D0_0[1],'TC_00_01':FA1D0_0[2],'TC_00_10':FA1D0_0[3],'TC_00_11':FA1D0_0[4],
                              'TC_01_00':FA1D0_0[5],'TC_01_01':FA1D0_0[6],'TC_01_10':FA1D0_0[7],'TC_01_11':FA1D0_0[8],
                              'TC_10_00':FA1D0_0[9],'TC_10_01':FA1D0_0[10],'TC_10_10':FA1D0_0[11],'TC_10_11':FA1D0_0[12],
                              'TC_11_00':FA1D0_0[13],'TC_11_01':FA1D0_0[14],'TC_11_10':FA1D0_0[15],'TC_11_11':FA1D0_0[16]}
        elif gate_prop == 'FA1D0_1':
            attrs[(n1,n2)] = {'SC': FA1D0_1[0], 'TC_00_00':FA1D0_1[1],'TC_00_01':FA1D0_1[2],'TC_00_10':FA1D0_1[3],'TC_00_11':FA1D0_1[4],
                              'TC_01_00':FA1D0_1[5],'TC_01_01':FA1D0_1[6],'TC_01_10':FA1D0_1[7],'TC_01_11':FA1D0_1[8],
                              'TC_10_00':FA1D0_1[9],'TC_10_01':FA1D0_1[10],'TC_10_10':FA1D0_1[11],'TC_10_11':FA1D0_1[12],
                              'TC_11_00':FA1D0_1[13],'TC_11_01':FA1D0_1[14],'TC_11_10':FA1D0_1[15],'TC_11_11':FA1D0_1[16]}
        elif gate_prop == 'FICIND1_0':
            attrs[(n1,n2)] = {'SC': FICIND1_0[0], 'TC_00_00':FICIND1_0[1],'TC_00_01':FICIND1_0[2],'TC_00_10':FICIND1_0[3],'TC_00_11':FICIND1_0[4],
                              'TC_01_00':FICIND1_0[5],'TC_01_01':FICIND1_0[6],'TC_01_10':FICIND1_0[7],'TC_01_11':FICIND1_0[8],
                              'TC_10_00':FICIND1_0[9],'TC_10_01':FICIND1_0[10],'TC_10_10':FICIND1_0[11],'TC_10_11':FICIND1_0[12],
                              'TC_11_00':FICIND1_0[13],'TC_11_01':FICIND1_0[14],'TC_11_10':FICIND1_0[15],'TC_11_11':FICIND1_0[16]}
        elif gate_prop == 'FICIND1_1':
            attrs[(n1,n2)] = {'SC': FICIND1_1[0], 'TC_00_00':FICIND1_1[1],'TC_00_01':FICIND1_1[2],'TC_00_10':FICIND1_1[3],'TC_00_11':FICIND1_1[4],
                              'TC_01_00':FICIND1_1[5],'TC_01_01':FICIND1_1[6],'TC_01_10':FICIND1_1[7],'TC_01_11':FICIND1_1[8],
                              'TC_10_00':FICIND1_1[9],'TC_10_01':FICIND1_1[10],'TC_10_10':FICIND1_1[11],'TC_10_11':FICIND1_1[12],
                              'TC_11_00':FICIND1_1[13],'TC_11_01':FICIND1_1[14],'TC_11_10':FICIND1_1[15],'TC_11_11':FICIND1_1[16]}
        elif gate_prop == 'CMPE42D1_0':
            attrs[(n1,n2)] = {'SC': CMPE42D1_0[0], 'TC_00_00':CMPE42D1_0[1],'TC_00_01':CMPE42D1_0[2],'TC_00_10':CMPE42D1_0[3],'TC_00_11':CMPE42D1_0[4],
                              'TC_01_00':CMPE42D1_0[5],'TC_01_01':CMPE42D1_0[6],'TC_01_10':CMPE42D1_0[7],'TC_01_11':CMPE42D1_0[8],
                              'TC_10_00':CMPE42D1_0[9],'TC_10_01':CMPE42D1_0[10],'TC_10_10':CMPE42D1_0[11],'TC_10_11':CMPE42D1_0[12],
                              'TC_11_00':CMPE42D1_0[13],'TC_11_01':CMPE42D1_0[14],'TC_11_10':CMPE42D1_0[15],'TC_11_11':CMPE42D1_0[16]}
        elif gate_prop == 'CMPE42D1_1':
            attrs[(n1,n2)] = {'SC': CMPE42D1_1[0], 'TC_00_00':CMPE42D1_1[1],'TC_00_01':CMPE42D1_1[2],'TC_00_10':CMPE42D1_1[3],'TC_00_11':CMPE42D1_1[4],
                              'TC_01_00':CMPE42D1_1[5],'TC_01_01':CMPE42D1_1[6],'TC_01_10':CMPE42D1_1[7],'TC_01_11':CMPE42D1_1[8],
                              'TC_10_00':CMPE42D1_1[9],'TC_10_01':CMPE42D1_1[10],'TC_10_10':CMPE42D1_1[11],'TC_10_11':CMPE42D1_1[12],
                              'TC_11_00':CMPE42D1_1[13],'TC_11_01':CMPE42D1_1[14],'TC_11_10':CMPE42D1_1[15],'TC_11_11':CMPE42D1_1[16]}
        elif gate_prop == 'CMPE42D1_2':
            attrs[(n1,n2)] = {'SC': CMPE42D1_2[0], 'TC_00_00':CMPE42D1_2[1],'TC_00_01':CMPE42D1_2[2],'TC_00_10':CMPE42D1_2[3],'TC_00_11':CMPE42D1_2[4],
                              'TC_01_00':CMPE42D1_2[5],'TC_01_01':CMPE42D1_2[6],'TC_01_10':CMPE42D1_2[7],'TC_01_11':CMPE42D1_2[8],
                              'TC_10_00':CMPE42D1_2[9],'TC_10_01':CMPE42D1_2[10],'TC_10_10':CMPE42D1_2[11],'TC_10_11':CMPE42D1_2[12],
                              'TC_11_00':CMPE42D1_2[13],'TC_11_01':CMPE42D1_2[14],'TC_11_10':CMPE42D1_2[15],'TC_11_11':CMPE42D1_2[16]}
        elif gate_prop == 'OAI21D1':
            attrs[(n1,n2)] = {'SC': OAI21D1[0], 'TC_00_00':OAI21D1[1],'TC_00_01':OAI21D1[2],'TC_00_10':OAI21D1[3],'TC_00_11':OAI21D1[4],
                              'TC_01_00':OAI21D1[5],'TC_01_01':OAI21D1[6],'TC_01_10':OAI21D1[7],'TC_01_11':OAI21D1[8],
                              'TC_10_00':OAI21D1[9],'TC_10_01':OAI21D1[10],'TC_10_10':OAI21D1[11],'TC_10_11':OAI21D1[12],
                              'TC_11_00':OAI21D1[13],'TC_11_01':OAI21D1[14],'TC_11_10':OAI21D1[15],'TC_11_11':OAI21D1[16]}
        elif gate_prop == 'IOA21D0':
            attrs[(n1,n2)] = {'SC': IOA21D0[0], 'TC_00_00':IOA21D0[1],'TC_00_01':IOA21D0[2],'TC_00_10':IOA21D0[3],'TC_00_11':IOA21D0[4],
                              'TC_01_00':IOA21D0[5],'TC_01_01':IOA21D0[6],'TC_01_10':IOA21D0[7],'TC_01_11':IOA21D0[8],
                              'TC_10_00':IOA21D0[9],'TC_10_01':IOA21D0[10],'TC_10_10':IOA21D0[11],'TC_10_11':IOA21D0[12],
                              'TC_11_00':IOA21D0[13],'TC_11_01':IOA21D0[14],'TC_11_10':IOA21D0[15],'TC_11_11':IOA21D0[16]}
        elif gate_prop == 'IOA21D1':
            attrs[(n1,n2)] = {'SC': IOA21D1[0], 'TC_00_00':IOA21D1[1],'TC_00_01':IOA21D1[2],'TC_00_10':IOA21D1[3],'TC_00_11':IOA21D1[4],
                              'TC_01_00':IOA21D1[5],'TC_01_01':IOA21D1[6],'TC_01_10':IOA21D1[7],'TC_01_11':IOA21D1[8],
                              'TC_10_00':IOA21D1[9],'TC_10_01':IOA21D1[10],'TC_10_10':IOA21D1[11],'TC_10_11':IOA21D1[12],
                              'TC_11_00':IOA21D1[13],'TC_11_01':IOA21D1[14],'TC_11_10':IOA21D1[15],'TC_11_11':IOA21D1[16]}
        elif gate_prop == 'IOA21D2':
            attrs[(n1,n2)] = {'SC': IOA21D2[0], 'TC_00_00':IOA21D2[1],'TC_00_01':IOA21D2[2],'TC_00_10':IOA21D2[3],'TC_00_11':IOA21D2[4],
                              'TC_01_00':IOA21D2[5],'TC_01_01':IOA21D2[6],'TC_01_10':IOA21D2[7],'TC_01_11':IOA21D2[8],
                              'TC_10_00':IOA21D2[9],'TC_10_01':IOA21D2[10],'TC_10_10':IOA21D2[11],'TC_10_11':IOA21D2[12],
                              'TC_11_00':IOA21D2[13],'TC_11_01':IOA21D2[14],'TC_11_10':IOA21D2[15],'TC_11_11':IOA21D2[16]}
        elif gate_prop == 'OA21D0':
            attrs[(n1,n2)] = {'SC': OA21D0[0], 'TC_00_00':OA21D0[1],'TC_00_01':OA21D0[2],'TC_00_10':OA21D0[3],'TC_00_11':OA21D0[4],
                              'TC_01_00':OA21D0[5],'TC_01_01':OA21D0[6],'TC_01_10':OA21D0[7],'TC_01_11':OA21D0[8],
                              'TC_10_00':OA21D0[9],'TC_10_01':OA21D0[10],'TC_10_10':OA21D0[11],'TC_10_11':OA21D0[12],
                              'TC_11_00':OA21D0[13],'TC_11_01':OA21D0[14],'TC_11_10':OA21D0[15],'TC_11_11':OA21D0[16]}
        elif gate_prop == 'OA21D1':
            attrs[(n1,n2)] = {'SC': OA21D1[0], 'TC_00_00':OA21D1[1],'TC_00_01':OA21D1[2],'TC_00_10':OA21D1[3],'TC_00_11':OA21D1[4],
                              'TC_01_00':OA21D1[5],'TC_01_01':OA21D1[6],'TC_01_10':OA21D1[7],'TC_01_11':OA21D1[8],
                              'TC_10_00':OA21D1[9],'TC_10_01':OA21D1[10],'TC_10_10':OA21D1[11],'TC_10_11':OA21D1[12],
                              'TC_11_00':OA21D1[13],'TC_11_01':OA21D1[14],'TC_11_10':OA21D1[15],'TC_11_11':OA21D1[16]}
        elif gate_prop == 'IAO21D0':
            attrs[(n1,n2)] = {'SC': IAO21D0[0], 'TC_00_00':IAO21D0[1],'TC_00_01':IAO21D0[2],'TC_00_10':IAO21D0[3],'TC_00_11':IAO21D0[4],
                              'TC_01_00':IAO21D0[5],'TC_01_01':IAO21D0[6],'TC_01_10':IAO21D0[7],'TC_01_11':IAO21D0[8],
                              'TC_10_00':IAO21D0[9],'TC_10_01':IAO21D0[10],'TC_10_10':IAO21D0[11],'TC_10_11':IAO21D0[12],
                              'TC_11_00':IAO21D0[13],'TC_11_01':IAO21D0[14],'TC_11_10':IAO21D0[15],'TC_11_11':IAO21D0[16]}
        elif gate_prop == 'IAO21D1':
            attrs[(n1,n2)] = {'SC': IAO21D1[0], 'TC_00_00':IAO21D1[1],'TC_00_01':IAO21D1[2],'TC_00_10':IAO21D1[3],'TC_00_11':IAO21D1[4],
                              'TC_01_00':IAO21D1[5],'TC_01_01':IAO21D1[6],'TC_01_10':IAO21D1[7],'TC_01_11':IAO21D1[8],
                              'TC_10_00':IAO21D1[9],'TC_10_01':IAO21D1[10],'TC_10_10':IAO21D1[11],'TC_10_11':IAO21D1[12],
                              'TC_11_00':IAO21D1[13],'TC_11_01':IAO21D1[14],'TC_11_10':IAO21D1[15],'TC_11_11':IAO21D1[16]}
        elif gate_prop == 'AO21D0':
            attrs[(n1,n2)] = {'SC': AO21D0[0], 'TC_00_00':AO21D0[1],'TC_00_01':AO21D0[2],'TC_00_10':AO21D0[3],'TC_00_11':AO21D0[4],
                              'TC_01_00':AO21D0[5],'TC_01_01':AO21D0[6],'TC_01_10':AO21D0[7],'TC_01_11':AO21D0[8],
                              'TC_10_00':AO21D0[9],'TC_10_01':AO21D0[10],'TC_10_10':AO21D0[11],'TC_10_11':AO21D0[12],
                              'TC_11_00':AO21D0[13],'TC_11_01':AO21D0[14],'TC_11_10':AO21D0[15],'TC_11_11':AO21D0[16]}
        elif gate_prop == 'MUX2D0':
            attrs[(n1,n2)] = {'SC': MUX2D0[0], 'TC_00_00':MUX2D0[1],'TC_00_01':MUX2D0[2],'TC_00_10':MUX2D0[3],'TC_00_11':MUX2D0[4],
                              'TC_01_00':MUX2D0[5],'TC_01_01':MUX2D0[6],'TC_01_10':MUX2D0[7],'TC_01_11':MUX2D0[8],
                              'TC_10_00':MUX2D0[9],'TC_10_01':MUX2D0[10],'TC_10_10':MUX2D0[11],'TC_10_11':MUX2D0[12],
                              'TC_11_00':MUX2D0[13],'TC_11_01':MUX2D0[14],'TC_11_10':MUX2D0[15],'TC_11_11':MUX2D0[16]}
        elif gate_prop == 'MUX2ND0':
            attrs[(n1,n2)] = {'SC': MUX2ND0[0], 'TC_00_00':MUX2ND0[1],'TC_00_01':MUX2ND0[2],'TC_00_10':MUX2ND0[3],'TC_00_11':MUX2ND0[4],
                              'TC_01_00':MUX2ND0[5],'TC_01_01':MUX2ND0[6],'TC_01_10':MUX2ND0[7],'TC_01_11':MUX2ND0[8],
                              'TC_10_00':MUX2ND0[9],'TC_10_01':MUX2ND0[10],'TC_10_10':MUX2ND0[11],'TC_10_11':MUX2ND0[12],
                              'TC_11_00':MUX2ND0[13],'TC_11_01':MUX2ND0[14],'TC_11_10':MUX2ND0[15],'TC_11_11':MUX2ND0[16]}
        elif gate_prop == 'MUX3ND0':
            attrs[(n1,n2)] = {'SC': MUX3ND0[0], 'TC_00_00':MUX3ND0[1],'TC_00_01':MUX3ND0[2],'TC_00_10':MUX3ND0[3],'TC_00_11':MUX3ND0[4],
                              'TC_01_00':MUX3ND0[5],'TC_01_01':MUX3ND0[6],'TC_01_10':MUX3ND0[7],'TC_01_11':MUX3ND0[8],
                              'TC_10_00':MUX3ND0[9],'TC_10_01':MUX3ND0[10],'TC_10_10':MUX3ND0[11],'TC_10_11':MUX3ND0[12],
                              'TC_11_00':MUX3ND0[13],'TC_11_01':MUX3ND0[14],'TC_11_10':MUX3ND0[15],'TC_11_11':MUX3ND0[16]}
        elif gate_prop == 'AO22D0':
            attrs[(n1,n2)] = {'SC': AO22D0[0], 'TC_00_00':AO22D0[1],'TC_00_01':AO22D0[2],'TC_00_10':AO22D0[3],'TC_00_11':AO22D0[4],
                              'TC_01_00':AO22D0[5],'TC_01_01':AO22D0[6],'TC_01_10':AO22D0[7],'TC_01_11':AO22D0[8],
                              'TC_10_00':AO22D0[9],'TC_10_01':AO22D0[10],'TC_10_10':AO22D0[11],'TC_10_11':AO22D0[12],
                              'TC_11_00':AO22D0[13],'TC_11_01':AO22D0[14],'TC_11_10':AO22D0[15],'TC_11_11':AO22D0[16]}
        elif gate_prop == 'OAI31D0':
            attrs[(n1,n2)] = {'SC': OAI31D0[0], 'TC_00_00':OAI31D0[1],'TC_00_01':OAI31D0[2],'TC_00_10':OAI31D0[3],'TC_00_11':OAI31D0[4],
                              'TC_01_00':OAI31D0[5],'TC_01_01':OAI31D0[6],'TC_01_10':OAI31D0[7],'TC_01_11':OAI31D0[8],
                              'TC_10_00':OAI31D0[9],'TC_10_01':OAI31D0[10],'TC_10_10':OAI31D0[11],'TC_10_11':OAI31D0[12],
                              'TC_11_00':OAI31D0[13],'TC_11_01':OAI31D0[14],'TC_11_10':OAI31D0[15],'TC_11_11':OAI31D0[16]}
        elif gate_prop == 'OAI31D1':
            attrs[(n1,n2)] = {'SC': OAI31D1[0], 'TC_00_00':OAI31D1[1],'TC_00_01':OAI31D1[2],'TC_00_10':OAI31D1[3],'TC_00_11':OAI31D1[4],
                              'TC_01_00':OAI31D1[5],'TC_01_01':OAI31D1[6],'TC_01_10':OAI31D1[7],'TC_01_11':OAI31D1[8],
                              'TC_10_00':OAI31D1[9],'TC_10_01':OAI31D1[10],'TC_10_10':OAI31D1[11],'TC_10_11':OAI31D1[12],
                              'TC_11_00':OAI31D1[13],'TC_11_01':OAI31D1[14],'TC_11_10':OAI31D1[15],'TC_11_11':OAI31D1[16]}
        elif gate_prop == 'AOI31D0':
            attrs[(n1,n2)] = {'SC': AOI31D0[0], 'TC_00_00':AOI31D0[1],'TC_00_01':AOI31D0[2],'TC_00_10':AOI31D0[3],'TC_00_11':AOI31D0[4],
                              'TC_01_00':AOI31D0[5],'TC_01_01':AOI31D0[6],'TC_01_10':AOI31D0[7],'TC_01_11':AOI31D0[8],
                              'TC_10_00':AOI31D0[9],'TC_10_01':AOI31D0[10],'TC_10_10':AOI31D0[11],'TC_10_11':AOI31D0[12],
                              'TC_11_00':AOI31D0[13],'TC_11_01':AOI31D0[14],'TC_11_10':AOI31D0[15],'TC_11_11':AOI31D0[16]}
        elif gate_prop == 'AOI31D1':
            attrs[(n1,n2)] = {'SC': AOI31D1[0], 'TC_00_00':AOI31D1[1],'TC_00_01':AOI31D1[2],'TC_00_10':AOI31D1[3],'TC_00_11':AOI31D1[4],
                              'TC_01_00':AOI31D1[5],'TC_01_01':AOI31D1[6],'TC_01_10':AOI31D1[7],'TC_01_11':AOI31D1[8],
                              'TC_10_00':AOI31D1[9],'TC_10_01':AOI31D1[10],'TC_10_10':AOI31D1[11],'TC_10_11':AOI31D1[12],
                              'TC_11_00':AOI31D1[13],'TC_11_01':AOI31D1[14],'TC_11_10':AOI31D1[15],'TC_11_11':AOI31D1[16]}
        elif gate_prop == 'OAI31D2':
            attrs[(n1,n2)] = {'SC': OAI31D2[0], 'TC_00_00':OAI31D2[1],'TC_00_01':OAI31D2[2],'TC_00_10':OAI31D2[3],'TC_00_11':OAI31D2[4],
                              'TC_01_00':OAI31D2[5],'TC_01_01':OAI31D2[6],'TC_01_10':OAI31D2[7],'TC_01_11':OAI31D2[8],
                              'TC_10_00':OAI31D2[9],'TC_10_01':OAI31D2[10],'TC_10_10':OAI31D2[11],'TC_10_11':OAI31D2[12],
                              'TC_11_00':OAI31D2[13],'TC_11_01':OAI31D2[14],'TC_11_10':OAI31D2[15],'TC_11_11':OAI31D2[16]}
        elif gate_prop == 'OA31D0':
            attrs[(n1,n2)] = {'SC': OA31D0[0], 'TC_00_00':OA31D0[1],'TC_00_01':OA31D0[2],'TC_00_10':OA31D0[3],'TC_00_11':OA31D0[4],
                              'TC_01_00':OA31D0[5],'TC_01_01':OA31D0[6],'TC_01_10':OA31D0[7],'TC_01_11':OA31D0[8],
                              'TC_10_00':OA31D0[9],'TC_10_01':OA31D0[10],'TC_10_10':OA31D0[11],'TC_10_11':OA31D0[12],
                              'TC_11_00':OA31D0[13],'TC_11_01':OA31D0[14],'TC_11_10':OA31D0[15],'TC_11_11':OA31D0[16]}
        elif gate_prop == 'OA31D1':
            attrs[(n1,n2)] = {'SC': OA31D1[0], 'TC_00_00':OA31D1[1],'TC_00_01':OA31D1[2],'TC_00_10':OA31D1[3],'TC_00_11':OA31D1[4],
                              'TC_01_00':OA31D1[5],'TC_01_01':OA31D1[6],'TC_01_10':OA31D1[7],'TC_01_11':OA31D1[8],
                              'TC_10_00':OA31D1[9],'TC_10_01':OA31D1[10],'TC_10_10':OA31D1[11],'TC_10_11':OA31D1[12],
                              'TC_11_00':OA31D1[13],'TC_11_01':OA31D1[14],'TC_11_10':OA31D1[15],'TC_11_11':OA31D1[16]}
        elif gate_prop == 'AO31D0':
            attrs[(n1,n2)] = {'SC': AO31D0[0], 'TC_00_00':AO31D0[1],'TC_00_01':AO31D0[2],'TC_00_10':AO31D0[3],'TC_00_11':AO31D0[4],
                              'TC_01_00':AO31D0[5],'TC_01_01':AO31D0[6],'TC_01_10':AO31D0[7],'TC_01_11':AO31D0[8],
                              'TC_10_00':AO31D0[9],'TC_10_01':AO31D0[10],'TC_10_10':AO31D0[11],'TC_10_11':AO31D0[12],
                              'TC_11_00':AO31D0[13],'TC_11_01':AO31D0[14],'TC_11_10':AO31D0[15],'TC_11_11':AO31D0[16]}
        elif gate_prop == 'AO31D1':
            attrs[(n1,n2)] = {'SC': AO31D1[0], 'TC_00_00':AO31D1[1],'TC_00_01':AO31D1[2],'TC_00_10':AO31D1[3],'TC_00_11':AO31D1[4],
                              'TC_01_00':AO31D1[5],'TC_01_01':AO31D1[6],'TC_01_10':AO31D1[7],'TC_01_11':AO31D1[8],
                              'TC_10_00':AO31D1[9],'TC_10_01':AO31D1[10],'TC_10_10':AO31D1[11],'TC_10_11':AO31D1[12],
                              'TC_11_00':AO31D1[13],'TC_11_01':AO31D1[14],'TC_11_10':AO31D1[15],'TC_11_11':AO31D1[16]}
        elif gate_prop == 'AO31D2':
            attrs[(n1,n2)] = {'SC': AO31D2[0], 'TC_00_00':AO31D2[1],'TC_00_01':AO31D2[2],'TC_00_10':AO31D2[3],'TC_00_11':AO31D2[4],
                              'TC_01_00':AO31D2[5],'TC_01_01':AO31D2[6],'TC_01_10':AO31D2[7],'TC_01_11':AO31D2[8],
                              'TC_10_00':AO31D2[9],'TC_10_01':AO31D2[10],'TC_10_10':AO31D2[11],'TC_10_11':AO31D2[12],
                              'TC_11_00':AO31D2[13],'TC_11_01':AO31D2[14],'TC_11_10':AO31D2[15],'TC_11_11':AO31D2[16]}
        elif gate_prop == 'AO211D0':
            attrs[(n1,n2)] = {'SC': AO211D0[0], 'TC_00_00':AO211D0[1],'TC_00_01':AO211D0[2],'TC_00_10':AO211D0[3],'TC_00_11':AO211D0[4],
                              'TC_01_00':AO211D0[5],'TC_01_01':AO211D0[6],'TC_01_10':AO211D0[7],'TC_01_11':AO211D0[8],
                              'TC_10_00':AO211D0[9],'TC_10_01':AO211D0[10],'TC_10_10':AO211D0[11],'TC_10_11':AO211D0[12],
                              'TC_11_00':AO211D0[13],'TC_11_01':AO211D0[14],'TC_11_10':AO211D0[15],'TC_11_11':AO211D0[16]}
        elif gate_prop == 'AO211D2':
            attrs[(n1,n2)] = {'SC': AO211D2[0], 'TC_00_00':AO211D2[1],'TC_00_01':AO211D2[2],'TC_00_10':AO211D2[3],'TC_00_11':AO211D2[4],
                              'TC_01_00':AO211D2[5],'TC_01_01':AO211D2[6],'TC_01_10':AO211D2[7],'TC_01_11':AO211D2[8],
                              'TC_10_00':AO211D2[9],'TC_10_01':AO211D2[10],'TC_10_10':AO211D2[11],'TC_10_11':AO211D2[12],
                              'TC_11_00':AO211D2[13],'TC_11_01':AO211D2[14],'TC_11_10':AO211D2[15],'TC_11_11':AO211D2[16]}
        elif gate_prop == 'OAI211D0':
            attrs[(n1,n2)] = {'SC': OAI211D0[0], 'TC_00_00':OAI211D0[1],'TC_00_01':OAI211D0[2],'TC_00_10':OAI211D0[3],'TC_00_11':OAI211D0[4],
                              'TC_01_00':OAI211D0[5],'TC_01_01':OAI211D0[6],'TC_01_10':OAI211D0[7],'TC_01_11':OAI211D0[8],
                              'TC_10_00':OAI211D0[9],'TC_10_01':OAI211D0[10],'TC_10_10':OAI211D0[11],'TC_10_11':OAI211D0[12],
                              'TC_11_00':OAI211D0[13],'TC_11_01':OAI211D0[14],'TC_11_10':OAI211D0[15],'TC_11_11':OAI211D0[16]}
        elif gate_prop == 'OAI211D1':
            attrs[(n1,n2)] = {'SC': OAI211D1[0], 'TC_00_00':OAI211D1[1],'TC_00_01':OAI211D1[2],'TC_00_10':OAI211D1[3],'TC_00_11':OAI211D1[4],
                              'TC_01_00':OAI211D1[5],'TC_01_01':OAI211D1[6],'TC_01_10':OAI211D1[7],'TC_01_11':OAI211D1[8],
                              'TC_10_00':OAI211D1[9],'TC_10_01':OAI211D1[10],'TC_10_10':OAI211D1[11],'TC_10_11':OAI211D1[12],
                              'TC_11_00':OAI211D1[13],'TC_11_01':OAI211D1[14],'TC_11_10':OAI211D1[15],'TC_11_11':OAI211D1[16]}
        elif gate_prop == 'AOI211D0':
            attrs[(n1,n2)] = {'SC': AOI211D0[0], 'TC_00_00':AOI211D0[1],'TC_00_01':AOI211D0[2],'TC_00_10':AOI211D0[3],'TC_00_11':AOI211D0[4],
                              'TC_01_00':AOI211D0[5],'TC_01_01':AOI211D0[6],'TC_01_10':AOI211D0[7],'TC_01_11':AOI211D0[8],
                              'TC_10_00':AOI211D0[9],'TC_10_01':AOI211D0[10],'TC_10_10':AOI211D0[11],'TC_10_11':AOI211D0[12],
                              'TC_11_00':AOI211D0[13],'TC_11_01':AOI211D0[14],'TC_11_10':AOI211D0[15],'TC_11_11':AOI211D0[16]}
        elif gate_prop == 'OA211D0':
            attrs[(n1,n2)] = {'SC': OA211D0[0], 'TC_00_00':OA211D0[1],'TC_00_01':OA211D0[2],'TC_00_10':OA211D0[3],'TC_00_11':OA211D0[4],
                              'TC_01_00':OA211D0[5],'TC_01_01':OA211D0[6],'TC_01_10':OA211D0[7],'TC_01_11':OA211D0[8],
                              'TC_10_00':OA211D0[9],'TC_10_01':OA211D0[10],'TC_10_10':OA211D0[11],'TC_10_11':OA211D0[12],
                              'TC_11_00':OA211D0[13],'TC_11_01':OA211D0[14],'TC_11_10':OA211D0[15],'TC_11_11':OA211D0[16]}
        elif gate_prop == 'OA211D2':
            attrs[(n1,n2)] = {'SC': OA211D2[0], 'TC_00_00':OA211D2[1],'TC_00_01':OA211D2[2],'TC_00_10':OA211D2[3],'TC_00_11':OA211D2[4],
                              'TC_01_00':OA211D2[5],'TC_01_01':OA211D2[6],'TC_01_10':OA211D2[7],'TC_01_11':OA211D2[8],
                              'TC_10_00':OA211D2[9],'TC_10_01':OA211D2[10],'TC_10_10':OA211D2[11],'TC_10_11':OA211D2[12],
                              'TC_11_00':OA211D2[13],'TC_11_01':OA211D2[14],'TC_11_10':OA211D2[15],'TC_11_11':OA211D2[16]}
        elif gate_prop == 'AOI211XD0':
            attrs[(n1,n2)] = {'SC': AOI211XD0[0], 'TC_00_00':AOI211XD0[1],'TC_00_01':AOI211XD0[2],'TC_00_10':AOI211XD0[3],'TC_00_11':AOI211XD0[4],
                              'TC_01_00':AOI211XD0[5],'TC_01_01':AOI211XD0[6],'TC_01_10':AOI211XD0[7],'TC_01_11':AOI211XD0[8],
                              'TC_10_00':AOI211XD0[9],'TC_10_01':AOI211XD0[10],'TC_10_10':AOI211XD0[11],'TC_10_11':AOI211XD0[12],
                              'TC_11_00':AOI211XD0[13],'TC_11_01':AOI211XD0[14],'TC_11_10':AOI211XD0[15],'TC_11_11':AOI211XD0[16]}
        elif gate_prop == 'OA222D0':
            attrs[(n1,n2)] = {'SC': OA222D0[0], 'TC_00_00':OA222D0[1],'TC_00_01':OA222D0[2],'TC_00_10':OA222D0[3],'TC_00_11':OA222D0[4],
                              'TC_01_00':OA222D0[5],'TC_01_01':OA222D0[6],'TC_01_10':OA222D0[7],'TC_01_11':OA222D0[8],
                              'TC_10_00':OA222D0[9],'TC_10_01':OA222D0[10],'TC_10_10':OA222D0[11],'TC_10_11':OA222D0[12],
                              'TC_11_00':OA222D0[13],'TC_11_01':OA222D0[14],'TC_11_10':OA222D0[15],'TC_11_11':OA222D0[16]}
        elif gate_prop == 'AOI222D1':
            attrs[(n1,n2)] = {'SC': AOI222D1[0], 'TC_00_00':AOI222D1[1],'TC_00_01':AOI222D1[2],'TC_00_10':AOI222D1[3],'TC_00_11':AOI222D1[4],
                              'TC_01_00':AOI222D1[5],'TC_01_01':AOI222D1[6],'TC_01_10':AOI222D1[7],'TC_01_11':AOI222D1[8],
                              'TC_10_00':AOI222D1[9],'TC_10_01':AOI222D1[10],'TC_10_10':AOI222D1[11],'TC_10_11':AOI222D1[12],
                              'TC_11_00':AOI222D1[13],'TC_11_01':AOI222D1[14],'TC_11_10':AOI222D1[15],'TC_11_11':AOI222D1[16]}
        elif gate_prop == 'AOI33D0':
            attrs[(n1,n2)] = {'SC': AOI33D0[0], 'TC_00_00':AOI33D0[1],'TC_00_01':AOI33D0[2],'TC_00_10':AOI33D0[3],'TC_00_11':AOI33D0[4],
                              'TC_01_00':AOI33D0[5],'TC_01_01':AOI33D0[6],'TC_01_10':AOI33D0[7],'TC_01_11':AOI33D0[8],
                              'TC_10_00':AOI33D0[9],'TC_10_01':AOI33D0[10],'TC_10_10':AOI33D0[11],'TC_10_11':AOI33D0[12],
                              'TC_11_00':AOI33D0[13],'TC_11_01':AOI33D0[14],'TC_11_10':AOI33D0[15],'TC_11_11':AOI33D0[16]}
        elif gate_prop == 'OAI33D0':
            attrs[(n1,n2)] = {'SC': OAI33D0[0], 'TC_00_00':OAI33D0[1],'TC_00_01':OAI33D0[2],'TC_00_10':OAI33D0[3],'TC_00_11':OAI33D0[4],
                              'TC_01_00':OAI33D0[5],'TC_01_01':OAI33D0[6],'TC_01_10':OAI33D0[7],'TC_01_11':OAI33D0[8],
                              'TC_10_00':OAI33D0[9],'TC_10_01':OAI33D0[10],'TC_10_10':OAI33D0[11],'TC_10_11':OAI33D0[12],
                              'TC_11_00':OAI33D0[13],'TC_11_01':OAI33D0[14],'TC_11_10':OAI33D0[15],'TC_11_11':OAI33D0[16]}
        elif gate_prop == 'OAI33D1':
            attrs[(n1,n2)] = {'SC': OAI33D1[0], 'TC_00_00':OAI33D1[1],'TC_00_01':OAI33D1[2],'TC_00_10':OAI33D1[3],'TC_00_11':OAI33D1[4],
                              'TC_01_00':OAI33D1[5],'TC_01_01':OAI33D1[6],'TC_01_10':OAI33D1[7],'TC_01_11':OAI33D1[8],
                              'TC_10_00':OAI33D1[9],'TC_10_01':OAI33D1[10],'TC_10_10':OAI33D1[11],'TC_10_11':OAI33D1[12],
                              'TC_11_00':OAI33D1[13],'TC_11_01':OAI33D1[14],'TC_11_10':OAI33D1[15],'TC_11_11':OAI33D1[16]}
        elif gate_prop == 'MUX4ND0':
            attrs[(n1,n2)] = {'SC': MUX4ND0[0], 'TC_00_00':MUX4ND0[1],'TC_00_01':MUX4ND0[2],'TC_00_10':MUX4ND0[3],'TC_00_11':MUX4ND0[4],
                              'TC_01_00':MUX4ND0[5],'TC_01_01':MUX4ND0[6],'TC_01_10':MUX4ND0[7],'TC_01_11':MUX4ND0[8],
                              'TC_10_00':MUX4ND0[9],'TC_10_01':MUX4ND0[10],'TC_10_10':MUX4ND0[11],'TC_10_11':MUX4ND0[12],
                              'TC_11_00':MUX4ND0[13],'TC_11_01':MUX4ND0[14],'TC_11_10':MUX4ND0[15],'TC_11_11':MUX4ND0[16]}
        elif gate_prop == 'AOI222D0':
            attrs[(n1,n2)] = {'SC': AOI222D0[0], 'TC_00_00':AOI222D0[1],'TC_00_01':AOI222D0[2],'TC_00_10':AOI222D0[3],'TC_00_11':AOI222D0[4],
                              'TC_01_00':AOI222D0[5],'TC_01_01':AOI222D0[6],'TC_01_10':AOI222D0[7],'TC_01_11':AOI222D0[8],
                              'TC_10_00':AOI222D0[9],'TC_10_01':AOI222D0[10],'TC_10_10':AOI222D0[11],'TC_10_11':AOI222D0[12],
                              'TC_11_00':AOI222D0[13],'TC_11_01':AOI222D0[14],'TC_11_10':AOI222D0[15],'TC_11_11':AOI222D0[16]}
        elif gate_prop == 'AO222D0':
            attrs[(n1,n2)] = {'SC': AO222D0[0], 'TC_00_00':AO222D0[1],'TC_00_01':AO222D0[2],'TC_00_10':AO222D0[3],'TC_00_11':AO222D0[4],
                              'TC_01_00':AO222D0[5],'TC_01_01':AO222D0[6],'TC_01_10':AO222D0[7],'TC_01_11':AO222D0[8],
                              'TC_10_00':AO222D0[9],'TC_10_01':AO222D0[10],'TC_10_10':AO222D0[11],'TC_10_11':AO222D0[12],
                              'TC_11_00':AO222D0[13],'TC_11_01':AO222D0[14],'TC_11_10':AO222D0[15],'TC_11_11':AO222D0[16]}
        elif gate_prop == 'OAI222D0':
            attrs[(n1,n2)] = {'SC': OAI222D0[0], 'TC_00_00':OAI222D0[1],'TC_00_01':OAI222D0[2],'TC_00_10':OAI222D0[3],'TC_00_11':OAI222D0[4],
                              'TC_01_00':OAI222D0[5],'TC_01_01':OAI222D0[6],'TC_01_10':OAI222D0[7],'TC_01_11':OAI222D0[8],
                              'TC_10_00':OAI222D0[9],'TC_10_01':OAI222D0[10],'TC_10_10':OAI222D0[11],'TC_10_11':OAI222D0[12],
                              'TC_11_00':OAI222D0[13],'TC_11_01':OAI222D0[14],'TC_11_10':OAI222D0[15],'TC_11_11':OAI222D0[16]}
        elif gate_prop == 'OAI222D1':
            attrs[(n1,n2)] = {'SC': OAI222D1[0], 'TC_00_00':OAI222D1[1],'TC_00_01':OAI222D1[2],'TC_00_10':OAI222D1[3],'TC_00_11':OAI222D1[4],
                              'TC_01_00':OAI222D1[5],'TC_01_01':OAI222D1[6],'TC_01_10':OAI222D1[7],'TC_01_11':OAI222D1[8],
                              'TC_10_00':OAI222D1[9],'TC_10_01':OAI222D1[10],'TC_10_10':OAI222D1[11],'TC_10_11':OAI222D1[12],
                              'TC_11_00':OAI222D1[13],'TC_11_01':OAI222D1[14],'TC_11_10':OAI222D1[15],'TC_11_11':OAI222D1[16]}
        elif gate_prop == 'XNR2D0':
            attrs[(n1,n2)] = {'SC': XNR2D0[0], 'TC_00_00':XNR2D0[1],'TC_00_01':XNR2D0[2],'TC_00_10':XNR2D0[3],'TC_00_11':XNR2D0[4],
                              'TC_01_00':XNR2D0[5],'TC_01_01':XNR2D0[6],'TC_01_10':XNR2D0[7],'TC_01_11':XNR2D0[8],
                              'TC_10_00':XNR2D0[9],'TC_10_01':XNR2D0[10],'TC_10_10':XNR2D0[11],'TC_10_11':XNR2D0[12],
                              'TC_11_00':XNR2D0[13],'TC_11_01':XNR2D0[14],'TC_11_10':XNR2D0[15],'TC_11_11':XNR2D0[16]}
        elif gate_prop == 'XNR2D1':
            attrs[(n1,n2)] = {'SC': XNR2D1[0], 'TC_00_00':XNR2D1[1],'TC_00_01':XNR2D1[2],'TC_00_10':XNR2D1[3],'TC_00_11':XNR2D1[4],
                              'TC_01_00':XNR2D1[5],'TC_01_01':XNR2D1[6],'TC_01_10':XNR2D1[7],'TC_01_11':XNR2D1[8],
                              'TC_10_00':XNR2D1[9],'TC_10_01':XNR2D1[10],'TC_10_10':XNR2D1[11],'TC_10_11':XNR2D1[12],
                              'TC_11_00':XNR2D1[13],'TC_11_01':XNR2D1[14],'TC_11_10':XNR2D1[15],'TC_11_11':XNR2D1[16]}
        elif gate_prop == 'XOR2D0':
            attrs[(n1,n2)] = {'SC': XOR2D0[0], 'TC_00_00':XOR2D0[1],'TC_00_01':XOR2D0[2],'TC_00_10':XOR2D0[3],'TC_00_11':XOR2D0[4],
                              'TC_01_00':XOR2D0[5],'TC_01_01':XOR2D0[6],'TC_01_10':XOR2D0[7],'TC_01_11':XOR2D0[8],
                              'TC_10_00':XOR2D0[9],'TC_10_01':XOR2D0[10],'TC_10_10':XOR2D0[11],'TC_10_11':XOR2D0[12],
                              'TC_11_00':XOR2D0[13],'TC_11_01':XOR2D0[14],'TC_11_10':XOR2D0[15],'TC_11_11':XOR2D0[16]}
        elif gate_prop == 'XOR2D1':
            attrs[(n1,n2)] = {'SC': XOR2D1[0], 'TC_00_00':XOR2D1[1],'TC_00_01':XOR2D1[2],'TC_00_10':XOR2D1[3],'TC_00_11':XOR2D1[4],
                              'TC_01_00':XOR2D1[5],'TC_01_01':XOR2D1[6],'TC_01_10':XOR2D1[7],'TC_01_11':XOR2D1[8],
                              'TC_10_00':XOR2D1[9],'TC_10_01':XOR2D1[10],'TC_10_10':XOR2D1[11],'TC_10_11':XOR2D1[12],
                              'TC_11_00':XOR2D1[13],'TC_11_01':XOR2D1[14],'TC_11_10':XOR2D1[15],'TC_11_11':XOR2D1[16]}
        elif gate_prop == 'CKXOR2D0':
            attrs[(n1,n2)] = {'SC': CKXOR2D0[0], 'TC_00_00':CKXOR2D0[1],'TC_00_01':CKXOR2D0[2],'TC_00_10':CKXOR2D0[3],'TC_00_11':CKXOR2D0[4],
                              'TC_01_00':CKXOR2D0[5],'TC_01_01':CKXOR2D0[6],'TC_01_10':CKXOR2D0[7],'TC_01_11':CKXOR2D0[8],
                              'TC_10_00':CKXOR2D0[9],'TC_10_01':CKXOR2D0[10],'TC_10_10':CKXOR2D0[11],'TC_10_11':CKXOR2D0[12],
                              'TC_11_00':CKXOR2D0[13],'TC_11_01':CKXOR2D0[14],'TC_11_10':CKXOR2D0[15],'TC_11_11':CKXOR2D0[16]}
        elif gate_prop == 'CKXOR2D1':
            attrs[(n1,n2)] = {'SC': CKXOR2D1[0], 'TC_00_00':CKXOR2D1[1],'TC_00_01':CKXOR2D1[2],'TC_00_10':CKXOR2D1[3],'TC_00_11':CKXOR2D1[4],
                              'TC_01_00':CKXOR2D1[5],'TC_01_01':CKXOR2D1[6],'TC_01_10':CKXOR2D1[7],'TC_01_11':CKXOR2D1[8],
                              'TC_10_00':CKXOR2D1[9],'TC_10_01':CKXOR2D1[10],'TC_10_10':CKXOR2D1[11],'TC_10_11':CKXOR2D1[12],
                              'TC_11_00':CKXOR2D1[13],'TC_11_01':CKXOR2D1[14],'TC_11_10':CKXOR2D1[15],'TC_11_11':CKXOR2D1[16]}
        elif gate_prop == 'XOR3D1':
            attrs[(n1,n2)] = {'SC': XOR3D1[0], 'TC_00_00':XOR3D1[1],'TC_00_01':XOR3D1[2],'TC_00_10':XOR3D1[3],'TC_00_11':XOR3D1[4],
                              'TC_01_00':XOR3D1[5],'TC_01_01':XOR3D1[6],'TC_01_10':XOR3D1[7],'TC_01_11':XOR3D1[8],
                              'TC_10_00':XOR3D1[9],'TC_10_01':XOR3D1[10],'TC_10_10':XOR3D1[11],'TC_10_11':XOR3D1[12],
                              'TC_11_00':XOR3D1[13],'TC_11_01':XOR3D1[14],'TC_11_10':XOR3D1[15],'TC_11_11':XOR3D1[16]}
        elif gate_prop == 'XNR3D1':
            attrs[(n1,n2)] = {'SC': XNR3D1[0], 'TC_00_00':XNR3D1[1],'TC_00_01':XNR3D1[2],'TC_00_10':XNR3D1[3],'TC_00_11':XNR3D1[4],
                              'TC_01_00':XNR3D1[5],'TC_01_01':XNR3D1[6],'TC_01_10':XNR3D1[7],'TC_01_11':XNR3D1[8],
                              'TC_10_00':XNR3D1[9],'TC_10_01':XNR3D1[10],'TC_10_10':XNR3D1[11],'TC_10_11':XNR3D1[12],
                              'TC_11_00':XNR3D1[13],'TC_11_01':XNR3D1[14],'TC_11_10':XNR3D1[15],'TC_11_11':XNR3D1[16]}
        elif gate_prop == 'XOR4D0':
            attrs[(n1,n2)] = {'SC': XOR4D0[0], 'TC_00_00':XOR4D0[1],'TC_00_01':XOR4D0[2],'TC_00_10':XOR4D0[3],'TC_00_11':XOR4D0[4],
                              'TC_01_00':XOR4D0[5],'TC_01_01':XOR4D0[6],'TC_01_10':XOR4D0[7],'TC_01_11':XOR4D0[8],
                              'TC_10_00':XOR4D0[9],'TC_10_01':XOR4D0[10],'TC_10_10':XOR4D0[11],'TC_10_11':XOR4D0[12],
                              'TC_11_00':XOR4D0[13],'TC_11_01':XOR4D0[14],'TC_11_10':XOR4D0[15],'TC_11_11':XOR4D0[16]}
        elif gate_prop == 'XOR4D1':
            attrs[(n1,n2)] = {'SC': XOR4D1[0], 'TC_00_00':XOR4D1[1],'TC_00_01':XOR4D1[2],'TC_00_10':XOR4D1[3],'TC_00_11':XOR4D1[4],
                              'TC_01_00':XOR4D1[5],'TC_01_01':XOR4D1[6],'TC_01_10':XOR4D1[7],'TC_01_11':XOR4D1[8],
                              'TC_10_00':XOR4D1[9],'TC_10_01':XOR4D1[10],'TC_10_10':XOR4D1[11],'TC_10_11':XOR4D1[12],
                              'TC_11_00':XOR4D1[13],'TC_11_01':XOR4D1[14],'TC_11_10':XOR4D1[15],'TC_11_11':XOR4D1[16]}
        elif gate_prop == 'XNR3D0':
            attrs[(n1,n2)] = {'SC': XNR3D0[0], 'TC_00_00':XNR3D0[1],'TC_00_01':XNR3D0[2],'TC_00_10':XNR3D0[3],'TC_00_11':XNR3D0[4],
                              'TC_01_00':XNR3D0[5],'TC_01_01':XNR3D0[6],'TC_01_10':XNR3D0[7],'TC_01_11':XNR3D0[8],
                              'TC_10_00':XNR3D0[9],'TC_10_01':XNR3D0[10],'TC_10_10':XNR3D0[11],'TC_10_11':XNR3D0[12],
                              'TC_11_00':XNR3D0[13],'TC_11_01':XNR3D0[14],'TC_11_10':XNR3D0[15],'TC_11_11':XNR3D0[16]}
        elif gate_prop == 'XNR4D0':
            attrs[(n1,n2)] = {'SC': XNR4D0[0], 'TC_00_00':XNR4D0[1],'TC_00_01':XNR4D0[2],'TC_00_10':XNR4D0[3],'TC_00_11':XNR4D0[4],
                              'TC_01_00':XNR4D0[5],'TC_01_01':XNR4D0[6],'TC_01_10':XNR4D0[7],'TC_01_11':XNR4D0[8],
                              'TC_10_00':XNR4D0[9],'TC_10_01':XNR4D0[10],'TC_10_10':XNR4D0[11],'TC_10_11':XNR4D0[12],
                              'TC_11_00':XNR4D0[13],'TC_11_01':XNR4D0[14],'TC_11_10':XNR4D0[15],'TC_11_11':XNR4D0[16]}
        elif gate_prop == 'LHQD1':
            attrs[(n1,n2)] = {'SC': LHQD1[0], 'TC_00_00':LHQD1[1],'TC_00_01':LHQD1[2],'TC_00_10':LHQD1[3],'TC_00_11':LHQD1[4],
                              'TC_01_00':LHQD1[5],'TC_01_01':LHQD1[6],'TC_01_10':LHQD1[7],'TC_01_11':LHQD1[8],
                              'TC_10_00':LHQD1[9],'TC_10_01':LHQD1[10],'TC_10_10':LHQD1[11],'TC_10_11':LHQD1[12],
                              'TC_11_00':LHQD1[13],'TC_11_01':LHQD1[14],'TC_11_10':LHQD1[15],'TC_11_11':LHQD1[16]}
        elif gate_prop == 'EDFD1':
            attrs[(n1,n2)] = {'SC': EDFD1[0], 'TC_00_00':EDFD1[1],'TC_00_01':EDFD1[2],'TC_00_10':EDFD1[3],'TC_00_11':EDFD1[4],
                              'TC_01_00':EDFD1[5],'TC_01_01':EDFD1[6],'TC_01_10':EDFD1[7],'TC_01_11':EDFD1[8],
                              'TC_10_00':EDFD1[9],'TC_10_01':EDFD1[10],'TC_10_10':EDFD1[11],'TC_10_11':EDFD1[12],
                              'TC_11_00':EDFD1[13],'TC_11_01':EDFD1[14],'TC_11_10':EDFD1[15],'TC_11_11':EDFD1[16]}
        elif gate_prop == 'OAI221D0':
            attrs[(n1,n2)] = {'SC': OAI221D0[0], 'TC_00_00':OAI221D0[1],'TC_00_01':OAI221D0[2],'TC_00_10':OAI221D0[3],'TC_00_11':OAI221D0[4],
                              'TC_01_00':OAI221D0[5],'TC_01_01':OAI221D0[6],'TC_01_10':OAI221D0[7],'TC_01_11':OAI221D0[8],
                              'TC_10_00':OAI221D0[9],'TC_10_01':OAI221D0[10],'TC_10_10':OAI221D0[11],'TC_10_11':OAI221D0[12],
                              'TC_11_00':OAI221D0[13],'TC_11_01':OAI221D0[14],'TC_11_10':OAI221D0[15],'TC_11_11':OAI221D0[16]}
        elif gate_prop == 'OAI221D4':
            attrs[(n1,n2)] = {'SC': OAI221D4[0], 'TC_00_00':OAI221D4[1],'TC_00_01':OAI221D4[2],'TC_00_10':OAI221D4[3],'TC_00_11':OAI221D4[4],
                              'TC_01_00':OAI221D4[5],'TC_01_01':OAI221D4[6],'TC_01_10':OAI221D4[7],'TC_01_11':OAI221D4[8],
                              'TC_10_00':OAI221D4[9],'TC_10_01':OAI221D4[10],'TC_10_10':OAI221D4[11],'TC_10_11':OAI221D4[12],
                              'TC_11_00':OAI221D4[13],'TC_11_01':OAI221D4[14],'TC_11_10':OAI221D4[15],'TC_11_11':OAI221D4[16]}
        elif gate_prop == 'AOI221D0':
            attrs[(n1,n2)] = {'SC': AOI221D0[0], 'TC_00_00':AOI221D0[1],'TC_00_01':AOI221D0[2],'TC_00_10':AOI221D0[3],'TC_00_11':AOI221D0[4],
                              'TC_01_00':AOI221D0[5],'TC_01_01':AOI221D0[6],'TC_01_10':AOI221D0[7],'TC_01_11':AOI221D0[8],
                              'TC_10_00':AOI221D0[9],'TC_10_01':AOI221D0[10],'TC_10_10':AOI221D0[11],'TC_10_11':AOI221D0[12],
                              'TC_11_00':AOI221D0[13],'TC_11_01':AOI221D0[14],'TC_11_10':AOI221D0[15],'TC_11_11':AOI221D0[16]}
        elif gate_prop == 'AOI221D1':
            attrs[(n1,n2)] = {'SC': AOI221D1[0], 'TC_00_00':AOI221D1[1],'TC_00_01':AOI221D1[2],'TC_00_10':AOI221D1[3],'TC_00_11':AOI221D1[4],
                              'TC_01_00':AOI221D1[5],'TC_01_01':AOI221D1[6],'TC_01_10':AOI221D1[7],'TC_01_11':AOI221D1[8],
                              'TC_10_00':AOI221D1[9],'TC_10_01':AOI221D1[10],'TC_10_10':AOI221D1[11],'TC_10_11':AOI221D1[12],
                              'TC_11_00':AOI221D1[13],'TC_11_01':AOI221D1[14],'TC_11_10':AOI221D1[15],'TC_11_11':AOI221D1[16]}
        elif gate_prop == 'AOI221D4':
            attrs[(n1,n2)] = {'SC': AOI221D4[0], 'TC_00_00':AOI221D4[1],'TC_00_01':AOI221D4[2],'TC_00_10':AOI221D4[3],'TC_00_11':AOI221D4[4],
                              'TC_01_00':AOI221D4[5],'TC_01_01':AOI221D4[6],'TC_01_10':AOI221D4[7],'TC_01_11':AOI221D4[8],
                              'TC_10_00':AOI221D4[9],'TC_10_01':AOI221D4[10],'TC_10_10':AOI221D4[11],'TC_10_11':AOI221D4[12],
                              'TC_11_00':AOI221D4[13],'TC_11_01':AOI221D4[14],'TC_11_10':AOI221D4[15],'TC_11_11':AOI221D4[16]}
        elif gate_prop == 'AO221D0':
            attrs[(n1,n2)] = {'SC': AO221D0[0], 'TC_00_00':AO221D0[1],'TC_00_01':AO221D0[2],'TC_00_10':AO221D0[3],'TC_00_11':AO221D0[4],
                              'TC_01_00':AO221D0[5],'TC_01_01':AO221D0[6],'TC_01_10':AO221D0[7],'TC_01_11':AO221D0[8],
                              'TC_10_00':AO221D0[9],'TC_10_01':AO221D0[10],'TC_10_10':AO221D0[11],'TC_10_11':AO221D0[12],
                              'TC_11_00':AO221D0[13],'TC_11_01':AO221D0[14],'TC_11_10':AO221D0[15],'TC_11_11':AO221D0[16]}
        elif gate_prop == 'OA221D0':
            attrs[(n1,n2)] = {'SC': OA221D0[0], 'TC_00_00':OA221D0[1],'TC_00_01':OA221D0[2],'TC_00_10':OA221D0[3],'TC_00_11':OA221D0[4],
                              'TC_01_00':OA221D0[5],'TC_01_01':OA221D0[6],'TC_01_10':OA221D0[7],'TC_01_11':OA221D0[8],
                              'TC_10_00':OA221D0[9],'TC_10_01':OA221D0[10],'TC_10_10':OA221D0[11],'TC_10_11':OA221D0[12],
                              'TC_11_00':OA221D0[13],'TC_11_01':OA221D0[14],'TC_11_10':OA221D0[15],'TC_11_11':OA221D0[16]}
        elif gate_prop == 'AOI211D1':
            attrs[(n1,n2)] = {'SC': AOI211D1[0], 'TC_00_00':AOI211D1[1],'TC_00_01':AOI211D1[2],'TC_00_10':AOI211D1[3],'TC_00_11':AOI211D1[4],
                              'TC_01_00':AOI211D1[5],'TC_01_01':AOI211D1[6],'TC_01_10':AOI211D1[7],'TC_01_11':AOI211D1[8],
                              'TC_10_00':AOI211D1[9],'TC_10_01':AOI211D1[10],'TC_10_10':AOI211D1[11],'TC_10_11':AOI211D1[12],
                              'TC_11_00':AOI211D1[13],'TC_11_01':AOI211D1[14],'TC_11_10':AOI211D1[15],'TC_11_11':AOI211D1[16]}
        elif gate_prop == 'AOI22D1':
            attrs[(n1,n2)] = {'SC': AOI22D1[0], 'TC_00_00':AOI22D1[1],'TC_00_01':AOI22D1[2],'TC_00_10':AOI22D1[3],'TC_00_11':AOI22D1[4],
                              'TC_01_00':AOI22D1[5],'TC_01_01':AOI22D1[6],'TC_01_10':AOI22D1[7],'TC_01_11':AOI22D1[8],
                              'TC_10_00':AOI22D1[9],'TC_10_01':AOI22D1[10],'TC_10_10':AOI22D1[11],'TC_10_11':AOI22D1[12],
                              'TC_11_00':AOI22D1[13],'TC_11_01':AOI22D1[14],'TC_11_10':AOI22D1[15],'TC_11_11':AOI22D1[16]}
        elif gate_prop == 'AO32D0':
            attrs[(n1,n2)] = {'SC': AO32D0[0], 'TC_00_00':AO32D0[1],'TC_00_01':AO32D0[2],'TC_00_10':AO32D0[3],'TC_00_11':AO32D0[4],
                              'TC_01_00':AO32D0[5],'TC_01_01':AO32D0[6],'TC_01_10':AO32D0[7],'TC_01_11':AO32D0[8],
                              'TC_10_00':AO32D0[9],'TC_10_01':AO32D0[10],'TC_10_10':AO32D0[11],'TC_10_11':AO32D0[12],
                              'TC_11_00':AO32D0[13],'TC_11_01':AO32D0[14],'TC_11_10':AO32D0[15],'TC_11_11':AO32D0[16]}
        elif gate_prop == 'OAI32D0':
            attrs[(n1,n2)] = {'SC': OAI32D0[0], 'TC_00_00':OAI32D0[1],'TC_00_01':OAI32D0[2],'TC_00_10':OAI32D0[3],'TC_00_11':OAI32D0[4],
                              'TC_01_00':OAI32D0[5],'TC_01_01':OAI32D0[6],'TC_01_10':OAI32D0[7],'TC_01_11':OAI32D0[8],
                              'TC_10_00':OAI32D0[9],'TC_10_01':OAI32D0[10],'TC_10_10':OAI32D0[11],'TC_10_11':OAI32D0[12],
                              'TC_11_00':OAI32D0[13],'TC_11_01':OAI32D0[14],'TC_11_10':OAI32D0[15],'TC_11_11':OAI32D0[16]}
        elif gate_prop == 'OAI32D1':
            attrs[(n1,n2)] = {'SC': OAI32D1[0], 'TC_00_00':OAI32D1[1],'TC_00_01':OAI32D1[2],'TC_00_10':OAI32D1[3],'TC_00_11':OAI32D1[4],
                              'TC_01_00':OAI32D1[5],'TC_01_01':OAI32D1[6],'TC_01_10':OAI32D1[7],'TC_01_11':OAI32D1[8],
                              'TC_10_00':OAI32D1[9],'TC_10_01':OAI32D1[10],'TC_10_10':OAI32D1[11],'TC_10_11':OAI32D1[12],
                              'TC_11_00':OAI32D1[13],'TC_11_01':OAI32D1[14],'TC_11_10':OAI32D1[15],'TC_11_11':OAI32D1[16]}
        elif gate_prop == 'OA32D0':
            attrs[(n1,n2)] = {'SC': OA32D0[0], 'TC_00_00':OA32D0[1],'TC_00_01':OA32D0[2],'TC_00_10':OA32D0[3],'TC_00_11':OA32D0[4],
                              'TC_01_00':OA32D0[5],'TC_01_01':OA32D0[6],'TC_01_10':OA32D0[7],'TC_01_11':OA32D0[8],
                              'TC_10_00':OA32D0[9],'TC_10_01':OA32D0[10],'TC_10_10':OA32D0[11],'TC_10_11':OA32D0[12],
                              'TC_11_00':OA32D0[13],'TC_11_01':OA32D0[14],'TC_11_10':OA32D0[15],'TC_11_11':OA32D0[16]}
        elif gate_prop == 'OA32D2':
            attrs[(n1,n2)] = {'SC': OA32D2[0], 'TC_00_00':OA32D2[1],'TC_00_01':OA32D2[2],'TC_00_10':OA32D2[3],'TC_00_11':OA32D2[4],
                              'TC_01_00':OA32D2[5],'TC_01_01':OA32D2[6],'TC_01_10':OA32D2[7],'TC_01_11':OA32D2[8],
                              'TC_10_00':OA32D2[9],'TC_10_01':OA32D2[10],'TC_10_10':OA32D2[11],'TC_10_11':OA32D2[12],
                              'TC_11_00':OA32D2[13],'TC_11_01':OA32D2[14],'TC_11_10':OA32D2[15],'TC_11_11':OA32D2[16]}
        elif gate_prop == 'AOI32D0':
            attrs[(n1,n2)] = {'SC': AOI32D0[0], 'TC_00_00':AOI32D0[1],'TC_00_01':AOI32D0[2],'TC_00_10':AOI32D0[3],'TC_00_11':AOI32D0[4],
                              'TC_01_00':AOI32D0[5],'TC_01_01':AOI32D0[6],'TC_01_10':AOI32D0[7],'TC_01_11':AOI32D0[8],
                              'TC_10_00':AOI32D0[9],'TC_10_01':AOI32D0[10],'TC_10_10':AOI32D0[11],'TC_10_11':AOI32D0[12],
                              'TC_11_00':AOI32D0[13],'TC_11_01':AOI32D0[14],'TC_11_10':AOI32D0[15],'TC_11_11':AOI32D0[16]}
        elif gate_prop == 'NR4D1':
            attrs[(n1,n2)] = {'SC': NR4D1[0], 'TC_00_00':NR4D1[1],'TC_00_01':NR4D1[2],'TC_00_10':NR4D1[3],'TC_00_11':NR4D1[4],
                              'TC_01_00':NR4D1[5],'TC_01_01':NR4D1[6],'TC_01_10':NR4D1[7],'TC_01_11':NR4D1[8],
                              'TC_10_00':NR4D1[9],'TC_10_01':NR4D1[10],'TC_10_10':NR4D1[11],'TC_10_11':NR4D1[12],
                              'TC_11_00':NR4D1[13],'TC_11_01':NR4D1[14],'TC_11_10':NR4D1[15],'TC_11_11':NR4D1[16]}
        else:
            #print(gate_prop)
            print('Something wrong, please check!!')
    nx.set_edge_attributes(DG, attrs)


def getInfo():
    return info

def getcoreipsops():
    return core_ips, core_ops

def getEdges():
    return edges

def resetAllVars():
    info.clear()
    attrs.clear()
    edges.clear()
    assign.clear()
    core_ips.clear()
    core_ops.clear()


#    elif (len(re.compile(r'\s*FA1D0').findall(line))>0):
#        if len(re.compile(r'\s*FA1D0').findall(line))>0:
#            pattern_3ip21op = re.compile(r'\s*FA1D0\s?([\a-zA-Z0-9_]+)\s\(.*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\).*?\((.*?)\)')
#            node = 'FA1D0'
#            prob_s0 = 0.5
#            prob_s1 = 0.5
#            prob_t1 = 0.50
#            prob_t0 = 0.50
#        matches_3ip21op = pattern_3ip21op.finditer(line)
#        in_edge=[]
#        instance =''
#        out_edge =''
#        for match in matches_3ip21op:
#            instance = match.group(1)
#            print(instance)
#            in_edge.append(match.group(2))
#            in_edge.append(match.group(3))
#            in_edge.append(match.group(4))
#            out_edge = (match.group(6))
#            print("/*/*/*/*/*/*/*/*/*/*/*/")
#        return instance, node, in_edge, out_edge, prob_t1, prob_t0, prob_s0, prob_s1

#all_wire.insert(0,all_wire[442])

    # all_wires_final=[]
    # for wire in all_wire:
    #     #print(wire)
    #     pattenr_wr = re.compile(r'(\[(\d+):(\d+)\])?\s?([a-zA-Z0-9,_\/\\]+)')
    #     match_wr = pattenr_wr.finditer(wire)
    #     for match in match_wr:
    #         if (match.group(1) is None):
    #             #wire_f=match.group(3)
    #             all_wires_final.append(wire)
    #         elif (match.group(1) is not None):
    #             ll = min(int(match.group(2)), int(match.group(3)))
    #             ul = max(int(match.group(2)), int(match.group(3)))
    #             for i in range(int(ul-ll+1)):
    #                 wire_nm=match.group(4)
    #                 wire_f = wire_nm + '[' + str(i+ll) + ']'
    #                 all_wires_final.append(wire_f)
    #             wires=all_wires_final