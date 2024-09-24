import dgl
from numpy import core
import torch
import networkx as nx
from fixedPointAdder_TC_concatenate import read_contents, wires_parse, create_infoDict, inedgesTrim, updateAssignStatement, edges_UpdateInfo, update_graph, getInfo, getcoreipsops, getEdges, resetAllVars
from parse_saif import read_saif_contents, idmap_tagIdentifier, dataframe_Construct, update_coreNodesInfo, calc_Groundtruths, convert_dict_excel, resetParseVars, updateDFQ
from model import gnn
import matplotlib.pyplot as plt
import numpy as np
import torch.optim as optim
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime

#from sklearn.metrics import accuracy_score
import pandas as pd
import time
#from gpu_cpu_monitor import Monitor_gpu,Monitor_cpu

# import wandb
# wandb.init()

#cpu_usage = psutil.cpu_percent(interval=1, percpu=False)
#print(dgl.__version__)
# from torchinfo import summary

DG = nx.DiGraph()
list_ = []


filepaths_list =[['c432_netlist.v','c432_netlist.saif'],['int2float_netlist.v','int2float_netlist.saif'],['c499_netlist.v', 'c499_netlist.saif'],['adder_netlist.v','adder_netlist.saif'],['c880_netlist.v', 'c880_netlist.saif'] ,['c1908_netlist.v', 'c1908_netlist.saif'],['c2670_netlist.v','c2670_netlist.saif'],
['pri_encoder_netlist.v','pri_encoder_netlist.saif'],['decoder_netlist.v','decoder_netlist.saif'],['cavlc_netlist.v','cavlc_netlist.saif'],['c3540_netlist.v','c3540_netlist.saif'],['qadd_netlist.v', 'qadd_netlist.saif'],['c5315_netlist.v','c5315_netlist.saif'],['c7552_netlist.v','c7552_netlist.saif'],['c6288_netlist.v', 'c6288_netlist.saif'],['barrel_netlist.v','barrel_netlist.saif'],['fp_mul_netlist.v','fp_mul_netlist.saif'],['fp_add_netlist.v','fp_add_netlist.saif'],['qmult_netlist.v','qmult_netlist.saif'],['max_netlist.v','max_rtl.saif']]


# Get the graph object, edges and node information from netlist file ['fp_add_netlist.v','fp_add_netlist.vcd'],['arbiter_netlist.v', 'arbiter_netlist.vcd'],['barrel_netlist.v', 'barrel_netlist.vcd'],

def getGraphObj(filepath):
    contents = read_contents(filepath)
    wires = wires_parse(contents)
    create_infoDict(filepath, wires)
    inedgesTrim()
    assign = updateAssignStatement()
    coreips, coreops = getcoreipsops()
    edges_UpdateInfo(wires)
    info_nodes = getInfo()
    edges = getEdges()
    return info_nodes, edges, coreips, coreops, assign
    
def parseSAIF(filepath,coreips, coreops, info_nodes, edges, assign, DG):
    duration,con = read_saif_contents(filepath)
    idmap_tagIdentifier(con)
    ipToggleRates, opToggleRates, wireToggleRates = dataframe_Construct(coreips, coreops,duration)
    update_coreNodesInfo(ipToggleRates, opToggleRates, info_nodes)
    for k,v in info_nodes.items():
        if (v.get('out_edge') != None) and (v.get('out_edge') in coreops):
            list_.append((k,v.get('out_edge')))
    calc_Groundtruths(edges, info_nodes, wireToggleRates, ipToggleRates, opToggleRates, coreips, coreops, assign)
    # with open ('file1.txt','a') as op_file:
    #     for key, value in info_nodes.items(): 
    #         op_file.write('%s:%s\n' % (key, value))
    update_graph(DG)
    for ele in list_:
        DG.remove_edge(*ele)
        DG.remove_node(ele[1])
    return ipToggleRates



model = gnn()

loss_fn = torch.nn.MSELoss(reduction='sum')
learning_rate = 1e-6
optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

#19
def train_one_epoch(epoch, tb_writer):
    running_loss = 0.

    for i in range(19):
        optimizer.zero_grad()
        info_nodes, edges, coreips, coreops, assign = getGraphObj(filepaths_list[i][0])
        ipToggleRates = parseSAIF(filepaths_list[i][1], coreips, coreops, info_nodes, edges, assign, DG)
        dgl_graph = dgl.from_networkx(DG, node_attrs=['prob_s0','prob_s1','prob_t1','prob_t0','inv','avg_p0', 'avg_p1', 'avg_psw01', 'avg_psw10'], edge_attrs=['SC','TC_00_00','TC_00_01','TC_00_10','TC_00_11','TC_01_00','TC_01_01','TC_01_10','TC_01_11','TC_10_00','TC_10_01','TC_10_10','TC_10_11','TC_11_00','TC_11_01','TC_11_10','TC_11_11'])
        gt_avgp0 = dgl_graph.ndata['avg_p0']
        gt_avgp1 = dgl_graph.ndata['avg_p1']
        gt_avgpsw01 = dgl_graph.ndata['avg_psw01']
        #print(gt_avgpsw01)
        #print(len(gt_avgpsw01))
        gt_avgpsw10 = dgl_graph.ndata['avg_psw10']

        del dgl_graph.ndata['avg_p0']
        del dgl_graph.ndata['avg_p1']
        del dgl_graph.ndata['avg_psw01']
        del dgl_graph.ndata['avg_psw10']
        feat_prob0 = torch.transpose((dgl_graph.ndata['prob_s0'][None,:]), 0, 1)
        feat_prob1 = torch.transpose((dgl_graph.ndata['prob_s1'][None,:]), 0, 1)
        feat_prob2 = torch.transpose((dgl_graph.ndata['prob_t1'][None,:]), 0, 1)
        feat_prob3 = torch.transpose((dgl_graph.ndata['prob_t0'][None,:]), 0, 1)
        feat_inv = torch.transpose((dgl_graph.ndata['inv'][None,:]), 0, 1)
        feat = torch.cat((feat_prob0,feat_prob1,feat_prob2,feat_prob3, feat_inv), 1) 

        dgl_graph.ndata['prob_s0'] = dgl_graph.ndata['prob_s0'].view(dgl_graph.num_nodes(),1)
        dgl_graph.ndata['prob_s1'] = dgl_graph.ndata['prob_s1'].view(dgl_graph.num_nodes(),1)
        dgl_graph.ndata['prob_t1'] = dgl_graph.ndata['prob_t1'].view(dgl_graph.num_nodes(),1)
        dgl_graph.ndata['prob_t0'] = dgl_graph.ndata['prob_t0'].view(dgl_graph.num_nodes(),1)
        dgl_graph.ndata['inv'] = dgl_graph.ndata['inv'].view(dgl_graph.num_nodes(),1)


        dgl_graph.edata['SC'] = dgl_graph.edata['SC'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_00_00'] = dgl_graph.edata['TC_00_00'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_00_01'] = dgl_graph.edata['TC_00_01'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_00_10'] = dgl_graph.edata['TC_00_10'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_00_11'] = dgl_graph.edata['TC_00_11'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_01_00'] = dgl_graph.edata['TC_01_00'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_01_01'] = dgl_graph.edata['TC_01_01'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_01_10'] = dgl_graph.edata['TC_01_10'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_01_11'] = dgl_graph.edata['TC_01_11'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_10_00'] = dgl_graph.edata['TC_10_00'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_10_01'] = dgl_graph.edata['TC_10_01'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_10_10'] = dgl_graph.edata['TC_10_10'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_10_11'] = dgl_graph.edata['TC_10_11'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_11_00'] = dgl_graph.edata['TC_11_00'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_11_01'] = dgl_graph.edata['TC_11_01'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_11_10'] = dgl_graph.edata['TC_11_10'].view(dgl_graph.num_edges(), 1)
        dgl_graph.edata['TC_11_11'] = dgl_graph.edata['TC_11_11'].view(dgl_graph.num_edges(), 1)
        
        ipToggleRates_tensor = torch.from_numpy(ipToggleRates[:,1:].astype(np.float))
        y_pred = model(ipToggleRates_tensor.float(), dgl_graph, feat)
        loss = loss_fn(torch.flatten(y_pred[:,2:3]), gt_avgpsw01)
        loss.backward()
        optimizer.step()

        running_loss += loss.item()

        print('Circuit:', filepaths_list[i][0], 'Epoch:%d, loss: %.3f', (i + 1, running_loss))
    # for epoch in range(5):
    #     model.train()
    #     running_loss = 0.0
    #     optimizer.zero_grad()
    #     y_pred = model(ipToggleRates_tensor.float(), dgl_graph, feat)
    #     #y_pred_mean = torch.mean(y_pred, 0)
    #     loss = loss_fn(torch.flatten(y_pred[:,2:3]), gt_avgpsw01)
    #     loss.backward()
    #     optimizer.step()
        
    #     running_loss += loss.item()
    
    #     print('Circuit:', filepaths_list[i][0], 'Epoch:%d, loss: %.3f', (epoch + 1, running_loss))
        tb_writer.add_scalar('Loss:', running_loss, epoch*19+i+1)
        resetAllVars()
        resetParseVars()
        DG.clear()
        list_.clear()   

    running_loss = running_loss/19
    return running_loss

timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
writer = SummaryWriter('runs/fashion_trainer_{}'.format(timestamp))
epoch_number = 0

EPOCHS = 5

for epoch in range(EPOCHS):
    print('EPOCH {}:'.format(epoch_number + 1))

    # Make sure gradient tracking is on, and do a pass over the data
    model.train(True)
    avg_loss = train_one_epoch(epoch_number, writer)

    # We don't need gradients on to do reporting
    # model.train(False)

    # running_vloss = 0.0
    # for i, vdata in enumerate(validation_loader):
    #     vinputs, vlabels = vdata
    #     voutputs = model(vinputs)
    #     vloss = loss_fn(voutputs, vlabels)
    #     running_vloss += vloss

    # avg_vloss = running_vloss / (i + 1)
    # print('LOSS train {} valid {}'.format(avg_loss, avg_vloss))

    # Log the running loss averaged per batch
    # for both training and validation
    # writer.add_scalars('Training vs. Validation Loss',
    #                 { 'Training' : avg_loss, 'Validation' : avg_vloss },
    #                 epoch_number + 1)
    writer.flush()

    # Track best performance, and save the model's state
    # if avg_vloss < best_vloss:
    #     best_vloss = avg_vloss
    #     model_path = 'model_{}_{}'.format(timestamp, epoch_number)
    #     torch.save(model.state_dict(), model_path)

    epoch_number += 1

model.train(False)

info_nodes, edges, coreips, coreops, assign = getGraphObj(filepaths_list[19][0])
# ipToggleRates = parseVCD(filepaths_list[6][1], 1007, coreips, coreops, info_nodes, edges, assign, DG)
start1 = time.time()
duration,con = read_saif_contents('max_rtl.saif')
idmap_tagIdentifier(con)
ipToggleRates, opToggleRates, wireToggleRates = dataframe_Construct(coreips, coreops,duration)
update_coreNodesInfo(ipToggleRates, opToggleRates, info_nodes)
updateDFQ(info_nodes, coreips, coreops)


for k,v in info_nodes.items():
    if (v.get('out_edge') != None) and (v.get('out_edge') in coreops):
        list_.append((k,v.get('out_edge')))

un_id = 0
for k,v in info_nodes.items():
    v['un_id'] = un_id
    un_id += 1
un_id = 0

update_graph(DG)
for ele in list_:
    DG.remove_edge(*ele)
    DG.remove_node(ele[1])

dgl_graph = dgl.from_networkx(DG, node_attrs=['prob_s0','prob_s1','prob_t1','prob_t0','inv', 'un_id'], edge_attrs=['SC','TC_00_00','TC_00_01','TC_00_10','TC_00_11','TC_01_00','TC_01_01','TC_01_10','TC_01_11','TC_10_00','TC_10_01','TC_10_10','TC_10_11','TC_11_00','TC_11_01','TC_11_10','TC_11_11'])    
end1 = time.time()
time1 = end1-start1
ids = dgl_graph.ndata['un_id']
wire_names = []
#print(ids)
for id in ids:
    for k,v in info_nodes.items():
        if id == v['un_id']:
            if v['Gate'] == 'core input_vector':
                wire_names.append(k)
            else:
                wire_names.append(v['out_edge'])
            break

wire_names_df = pd.DataFrame(wire_names, columns=['wire_name'])
del dgl_graph.ndata['un_id']

start2=time.time()
feat_prob0 = torch.transpose((dgl_graph.ndata['prob_s0'][None,:]), 0, 1)
feat_prob1 = torch.transpose((dgl_graph.ndata['prob_s1'][None,:]), 0, 1)
feat_prob2 = torch.transpose((dgl_graph.ndata['prob_t1'][None,:]), 0, 1)
feat_prob3 = torch.transpose((dgl_graph.ndata['prob_t0'][None,:]), 0, 1)
feat_inv = torch.transpose((dgl_graph.ndata['inv'][None,:]), 0, 1)
feat = torch.cat((feat_prob0,feat_prob1,feat_prob2,feat_prob3, feat_inv), 1) 

dgl_graph.ndata['prob_s0'] = dgl_graph.ndata['prob_s0'].view(dgl_graph.num_nodes(),1)
dgl_graph.ndata['prob_s1'] = dgl_graph.ndata['prob_s1'].view(dgl_graph.num_nodes(),1)
dgl_graph.ndata['prob_t1'] = dgl_graph.ndata['prob_t1'].view(dgl_graph.num_nodes(),1)
dgl_graph.ndata['prob_t0'] = dgl_graph.ndata['prob_t0'].view(dgl_graph.num_nodes(),1)
dgl_graph.ndata['inv'] = dgl_graph.ndata['inv'].view(dgl_graph.num_nodes(),1)


dgl_graph.edata['SC'] = dgl_graph.edata['SC'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_00_00'] = dgl_graph.edata['TC_00_00'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_00_01'] = dgl_graph.edata['TC_00_01'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_00_10'] = dgl_graph.edata['TC_00_10'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_00_11'] = dgl_graph.edata['TC_00_11'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_01_00'] = dgl_graph.edata['TC_01_00'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_01_01'] = dgl_graph.edata['TC_01_01'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_01_10'] = dgl_graph.edata['TC_01_10'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_01_11'] = dgl_graph.edata['TC_01_11'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_10_00'] = dgl_graph.edata['TC_10_00'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_10_01'] = dgl_graph.edata['TC_10_01'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_10_10'] = dgl_graph.edata['TC_10_10'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_10_11'] = dgl_graph.edata['TC_10_11'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_11_00'] = dgl_graph.edata['TC_11_00'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_11_01'] = dgl_graph.edata['TC_11_01'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_11_10'] = dgl_graph.edata['TC_11_10'].view(dgl_graph.num_edges(), 1)
dgl_graph.edata['TC_11_11'] = dgl_graph.edata['TC_11_11'].view(dgl_graph.num_edges(), 1)

ipToggleRates_tensor = torch.from_numpy(ipToggleRates[:,1:].astype(np.float))

# y_pred = model(ipToggleRates_tensor.float(),dgl_graph,dgl_graph.ndata['prob_s0'],dgl_graph.edata['SC'])
y_pred = model(ipToggleRates_tensor.float(), dgl_graph, feat)
#print(loss_fn(torch.flatten(y_pred[:,2:3]), gt_avgpsw01))
#print(y_pred)
# y_pred_mean = torch.mean(y_pred, 0)
y_pred = y_pred.detach().numpy()
end2=time.time()
df = pd.DataFrame(y_pred)
df = pd.concat([wire_names_df, df], axis=1)

df.to_excel('predictedValues_max_wires_saif.xlsx', header=['wire_name','avg_p0', 'avg_p1', 'avg_psw01', 'avg_psw10'])
time2= end2-start2
#monitor_gpu.stop()
#monitor_cpu.stop()
print("The time of execution of above program is :", time2+time1)
