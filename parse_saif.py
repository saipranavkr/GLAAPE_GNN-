import re
import pandas as pd
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

id_map = {}

def read_saif_contents(path):
    useful = []
    flag = False
    with open (path,"r") as myfile:
        for i,line in enumerate(myfile):
            if len(re.compile(r'DURATION').findall(line))>0:
                pattern = re.compile(r'\s*DURATION\s?(\d+)')
                matches = pattern.finditer(line)
                for match in matches:
                    duration = match.group(1)
            if(re.search(r'\s*INSTANCE\s',line)!=None and flag == True):
                flag = False
                break
            if (flag == True):
                useful.append(line)
            if(re.search(r'\s*INSTANCE\s(uut|DUT)\s',line)!=None and flag == False):
                flag = True
    con = "".join(useful)
    return duration,con

def idmap_tagIdentifier(con):
    pattern = re.compile(r'\s*?\((.*?)\n\s*\((.*?(\d+))\)\s\((.*?(\d+))\)\s\((.*?(\d+))\)\n\s*\((.*?(\d+))\)\s\((.*?(\d+))\)\n\s*\)')
    matches = pattern.finditer(con)
    for match in matches:
        wire_name=match.group(1)
        if wire_name not in id_map:
            id_map[wire_name] = {'p_0':match.group(3), 'p_1':match.group(5) , 'p_sw_0_1':match.group(9) , 'p_sw_1_0':match.group(9)}
        else:
            continue
    

def dataframe_Construct(coreips, coreops,duration):
    ipToggleRates = np.empty((0,5))
    opToggleRates = np.empty((0,5))
    wireToggleRates = np.empty((0,5))
    for wires,values in id_map.items():
        wire_name = wires
        p_0 = float(values['p_0'])/float(duration)
        p_1 = float(values['p_1'])/float(duration)
        p_sw_0_1 = (float(values['p_sw_0_1'])/float(duration)*1000)
        p_sw_1_0 = (float(values['p_sw_1_0'])/float(duration)*1000)
        if wire_name.replace(' ', '') in coreips:
            ipToggleRates = np.append(ipToggleRates, np.array([[wire_name.replace(' ', ''), p_0,p_1,p_sw_0_1,p_sw_1_0]]), axis=0)
        elif wire_name.replace(' ', '') in coreops:
            opToggleRates = np.append(opToggleRates, np.array([[wire_name.replace(' ', ''), p_0,p_1,p_sw_0_1,p_sw_1_0]]), axis=0)
        else:
            wireToggleRates = np.append(wireToggleRates, np.array([[wire_name, p_0,p_1,p_sw_0_1,p_sw_1_0]]), axis=0)
    return ipToggleRates, opToggleRates, wireToggleRates

def calc_Groundtruths(edges, info_nodes, wireToggleRates, ipToggleRates, opToggleRates, coreips, coreops, assign):
    for i in range(wireToggleRates.shape[0]):
        # instance_name = edges.get(wireToggleRates[i][0])['out_v'][0]
        # print(wireToggleRates[i][0])
        # print(edges.get(wireToggleRates[i][0]))
        # print('-------------------')
        flag = True
        for k,v in assign.items():
            if v == wireToggleRates[i][0]:
                flag = False
                break
        if flag != False:
            instance_name = edges.get(wireToggleRates[i][0])['out_v'][0]
            if instance_name==None:
                print("Something wrong, please check")
                break
            info_nodes[instance_name]['avg_p0'] = float(wireToggleRates[i][1])
            info_nodes[instance_name]['avg_p1'] = float(wireToggleRates[i][2])
            info_nodes[instance_name]['avg_psw01'] = float(wireToggleRates[i][3])
            info_nodes[instance_name]['avg_psw10'] = float(wireToggleRates[i][4])
        # with open ('file.txt','a') as op_file:
        #     op_file.write(instance_name+'\n')
    for i in range(ipToggleRates.shape[0]):
        instance_name = edges.get(ipToggleRates[i][0])['out_v'][0]
        if instance_name == None:
            print('Input toggle rates ground truths error')
            break
        info_nodes[instance_name]['avg_p0'] = float(ipToggleRates[i][1])
        info_nodes[instance_name]['avg_p1'] = float(ipToggleRates[i][2])
        info_nodes[instance_name]['avg_psw01'] = float(ipToggleRates[i][3])
        info_nodes[instance_name]['avg_psw10'] = float(ipToggleRates[i][4])

    for i in range(opToggleRates.shape[0]):
        instance_name = str(opToggleRates[i][0])
        # instance_name = edges.get(opToggleRates[i][0])['out_v'][0]
        if instance_name == None:
            print('Output toggle rates ground truths error')
            break
        info_nodes[instance_name]['avg_p0'] = float(opToggleRates[i][1])
        info_nodes[instance_name]['avg_p1'] = float(opToggleRates[i][2])
        info_nodes[instance_name]['avg_psw01'] = float(opToggleRates[i][3])
        info_nodes[instance_name]['avg_psw10'] = float(opToggleRates[i][4])

        prev = edges.get(opToggleRates[i][0])['out_v'][0]
        if prev == None:
            print('Output toggle rates ground truth error 2')
            break

        info_nodes[prev]['avg_p0'] = float(opToggleRates[i][1])
        info_nodes[prev]['avg_p1'] = float(opToggleRates[i][2])
        info_nodes[prev]['avg_psw01'] = float(opToggleRates[i][3])
        info_nodes[prev]['avg_psw10'] = float(opToggleRates[i][4])

    for k,v in info_nodes.items():
        if (v['Gate'] == 'DFQD1') or (v['Gate'] == 'DFQD2'):
            prev_edge = v['in_edge']
            next_edge = v['out_edge']
            if (len(prev_edge) == 1) and (prev_edge[0] in coreips):
                continue
            if next_edge in coreops:
                continue
            v['prob_s0'] = 0.75
            v['prob_s1'] = 0.25
            v['prob_t1'] = 0.1875
            v['prob_t0'] = 0.8125
            v['inv'] = 0.
    

def convert_dict_excel(info_nodes, edges):
    # df = pd.DataFrame(columns=['Gate_Name', 'count', 'p_0', 'p_1', 'p_sw_0_1', 'p_sw_1_0'])
    new_dict = info_nodes.copy()
    for k,v in new_dict.items():
        if v['Gate'] == 'core input_vector':
            outedge = edges.get(k)['out_v'][0]
            print(outedge)
    # df = pd.DataFrame(dict).T
    # df.to_excel('averageToggleRates.xlsx', float_format="%.6f", columns=list(df.columns), index_label='Sl. No.')

def update_coreNodesInfo(ipToggleRates, opToggleRates, info_nodes):
    for i in range(0, ipToggleRates.shape[0], 1):
        info_nodes[ipToggleRates[i][0]] = {'Gate': 'core input_vector', 'prob_s0':float(ipToggleRates[i][1]), 'prob_s1':float(ipToggleRates[i][2]),'prob_t1': float(ipToggleRates[i][3]), 'prob_t0': float(ipToggleRates[i][4]), 'inv':0}
    for i in range(0, opToggleRates.shape[0], 1):
        info_nodes[opToggleRates[i][0]] = {'Gate': 'core output_vector', 'prob_s0':float(opToggleRates[i][1]), 'prob_s1':float(opToggleRates[i][2]),'prob_t1': float(opToggleRates[i][3]), 'prob_t0': float(opToggleRates[i][4]), 'inv':0 }

def resetParseVars():
    id_map.clear()
   

def updateDFQ(info_nodes, coreips, coreops):
    for k,v in info_nodes.items():
        if (v['Gate'] == 'DFQD1') or (v['Gate'] == 'DFQD2'):
            prev_edge = v['in_edge']
            next_edge = v['out_edge']
            if (len(prev_edge) == 1) and (prev_edge[0] in coreips):
                continue
            if next_edge in coreops:
                continue
            v['prob_s0'] = 0.75
            v['prob_s1'] = 0.25
            v['prob_t1'] = 0.1875
            v['prob_t0'] = 0.8125
            v['inv'] = 0.

