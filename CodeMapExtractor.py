import xml.etree.ElementTree as ET
import os.path
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
class CodeMapExtractor:
    def __init__(self):
        self.RELATION = 'CodeSchema_Calls'
        self.NODE_TYPE = 'CodeSchema_Method'
        self.PATH = 'CodeMap1.dgml'
        self.G = nx.DiGraph()
        self.Dict = {}

    def check_data(self):
        if os.path.isfile(self.PATH):
            return True
        else:
            return False

    def generate_nodes_and_links(self):
        tree = ET.parse('CodeMap1.dgml')
        root = tree.getroot()
        for child in root:
            if 'Nodes' in child.tag:
                self.NODES = child
            elif 'Links' in child.tag:
                self.LINKS =  child

    def find_id_by_name(self,myList,  name):
        ret =0
        for [a,b] in myList:
            if b == name:
                ret = a
                break
        return ret

    def find_index(self, myList, myToken):
        ret = -1
        for i, tmp in enumerate(myList):
            if tmp[0] == myToken:
                ret =i
                break
        return ret
    def create_matrix(self):
        length =  len(self.NODE_ID_NAME)
        length2 = len(self.LINK_SRC_DEST)
        out =  np.zeros(shape=(length, length), dtype=np.int8)
        for i in range(0, length2):
            src_id = self.LINK_SRC_DEST[i][0]
            dest_id = self.LINK_SRC_DEST[i][1]
            #print(src_id, dest_id)
            src_index = self.find_index(self.NODE_ID_NAME, src_id)
            dest_index =  self.find_index(self.NODE_ID_NAME, dest_id)
            if src_index == -1 or dest_index == -1:
                continue
            else:
                out[src_index][dest_index] = 1
                self.G.add_edge(src_id, dest_id, color='blue')
                #print(src_index, dest_index)
        return out
    def extract_adjacency_matrix(self):
        self.NODE_ID_NAME=[]
        self.LINK_SRC_DEST=[]
        counter = 0
        for node in self.NODES:
            if node.get('Category') == self.NODE_TYPE:
                nid = node.get('Id')
                nlabel = node.get('Label')
                self.NODE_ID_NAME.append([nid,nlabel])
                self.Dict[nid] = nlabel
        counter2 = 0
        for link in self.LINKS:
            counter +=1
            if link.get('Category') == self.RELATION:
                counter2 += 1
                self.LINK_SRC_DEST.append([link.get('Source'), link.get('Target')])
        self.ADJ_MATRIX = self.create_matrix()
        #print(self.NODE_ID_NAME)



    def draw_graph(self):
        plt.title('Call Graph')
        nx.draw(self.G, with_labels=True)
        plt.show()

    def callee_network(self, method, limit):
        mId = self.find_id_by_name(self.NODE_ID_NAME, method)
        T = nx.dfs_tree(self.G, source=mId, depth_limit=limit)
        T = nx.relabel_nodes(T, self.Dict)
        plt.title("Callee graph of "+method +" at depth "+str(limit))
        nx.draw(T, with_labels=True)
        plt.show()

    def caller_network(self, method, limit):
        mId = self.find_id_by_name(self.NODE_ID_NAME, method)
        T = nx.dfs_tree(self.G.reverse(), source=mId, depth_limit=limit)
        T = nx.relabel_nodes(T, self.Dict)
        plt.title("Caller graph of "+method +" at depth "+str(limit))
        nx.draw(T.reverse(), with_labels=True)
        plt.show()

if __name__ == "__main__":
    CME =  CodeMapExtractor()
    if CME.check_data():
        CME.generate_nodes_and_links()
        CME.extract_adjacency_matrix()
        while True:
            print('Press 0 to exit')
            print('Press 1 to generate whole call graph')
            print('Press 2 to get callee network')
            print('Press 3 to get caller network')
            decision= int(input())
            if decision == 0:
                break
            elif decision ==1:
                CME.draw_graph()
            elif decision == 2:
                print("Enter function name and depth")
                print('For Example: Main, 3')
                tmp = input()
                if ',' in tmp:
                    tmp2 = tmp.split(',')
                    method= tmp2[0]
                    limit= int(tmp2[1])
                CME.callee_network(method, limit)
            elif decision == 3:
                print("Enter function name and depth")
                print('For Example: executeUnitTestVS, 3')
                tmp = input()
                if ',' in tmp:
                    tmp2 = tmp.split(',')
                    method= tmp2[0]
                    limit= int(tmp2[1])
                CME.caller_network(method, limit)
    else:
        print('Please put the dgml file in the root directory')
