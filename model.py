from dgl.nn import GraphConv
import dgl
import dgl.function as fn
import torch
import torch.nn as nn
import torch.nn.functional as F

# def msg_sending(fc_out, edges):
reduce_func = dgl.function.sum('m', 'a')
class GCNLayer(nn.Module):
    def __init__(self, in_feats, out_feats):
        super(GCNLayer, self).__init__()
        self.linear = nn.Linear(16, out_feats)
        self.embed = None

    def edge_udf(self, edges):
        # print(edges.data)
        # if len(edges.src['_ID']) == 0:
        #     return {'m': edges.src['h']}
        # print('Here-------------------------------------')
        # print(self.embed, self.embed.size())
        # print(edges.data['TC_00_00'], edges.data['TC_00_00'].size())
        # print(edges.data)
        edge_feat_tc = torch.cat((edges.data['TC_00_00'], edges.data['TC_00_01'], edges.data['TC_00_10'], edges.data['TC_00_11'], edges.data['TC_01_00'], edges.data['TC_01_01'], edges.data['TC_01_10'], edges.data['TC_01_11'], edges.data['TC_10_00'], edges.data['TC_10_01'], edges.data['TC_10_10'], edges.data['TC_10_11'], edges.data['TC_11_00'], edges.data['TC_11_01'], edges.data['TC_11_10'], edges.data['TC_11_11']), 1) 
        return {'m': edges.data['SC']*edge_feat_tc}

    # def node_udf(self, nodes):
    #     return {nodes['a']*self.store}

    def forward(self, g, feature):
        # Creating a local scope so that all the stored ndata and edata
        # (such as the `'h'` ndata below) are automatically popped out
        # when the scope exits.
        with g.local_scope():
            g.ndata['h'] = feature
            # self.embed = self.linear(g.ndata['h'])
            dgl.prop_nodes_topo(g, self.edge_udf, reduce_func)
            h = g.ndata['a']
            return self.linear(h)
            
class gnn(nn.Module):
    def __init__(self):
        super().__init__()
        self.store = 0
        # self.embed = None
        self.fc1 = nn.Linear(4,128)
        self.fcfeat1 = nn.Linear(5,128)
        # self.fcfeat2 = nn.Linear(17,1)
        self.gcn = GCNLayer(128, 128)
        self.fc2 = nn.Linear(128, 32)
        self.fc3 = nn.Linear(32,4)
        self.softmax = nn.Softmax(dim=1)

    def edge_udf(self, edges):
        # print(edges.src)
        # print(self.store)
        if len(edges.src['_ID']) == 0:
            # print(self.store)
            x = edges.src['_ID']
            # return {'m': 0}
        # for nodeid in edges.src['_ID']:
        # print(edges.src)
        return {'m': edges.dst['prob_s0']}

    def forward(self, x, dgl_graph, feat, edges=None):
        # x = torch.flatten(x,1)
        x = self.fc1(x)
        x = F.relu(x)
        self.store = x

        feat = self.fcfeat1(feat)
        x = self.gcn(dgl_graph, feat)
        # x = torch.dot(x,self.store)
        x = F.relu(x)

        x = self.fc2(x)
        x = self.fc3(x)

        # print(x.shape)
        # self.embed = x

        # reduce_func = dgl.function.sum('m', 'prob_s0')
        # message_func = dgl.function.copy_edge('Correlation', 'm')
        # dgl.prop_nodes_topo(dgl_graph, self.edge_udf, reduce_func)
       # print(x.size())
        # feat = self.fcfeat1(feat)
        # edges=self.fcfeat2(edges)
        
        # x = self.gcn(dgl_graph, feat=feat, edge_weight=edges)
        # print(x)
        # print(x.size())
        # x = F.relu(x)
        # x = self.fc2(x)
        # x = F.relu(x)
        # x = self.fc3(x)
        out = self.softmax(x)
        # out = dgl_graph.ndata['a']
        return out
