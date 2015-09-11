import matplotlib
matplotlib.use('GTK')
import matplotlib.pyplot as plt
import networkx as nx
import Queue as q

class Node(object):
    def __init__(self, uid, system):
        self.system = system
        self.in_queue = q.Queue()
        self.out_queue = q.Queue()
        self.uid = uid
            
    def init(self):
        pass
            
    def send(self, msg, to):
        self.out_queue.put((to, msg))
    
    def neighbours(self):
        return list(nx.all_neighbors(self.system.G, self.uid))
    
    def receive(self):
        if (self.in_queue.empty()):
            return None
        else:
            return self.in_queue.get()
    
    def step(self):
        pass
    
class LeaderNode(Node):
    def __init__(self, uid, system):
        super(LeaderNode, self).__init__(uid, system)
        self.leader=uid
        
    def init(self):
        for n in self.neighbours():
            self.send(self.uid, n)
        
    def step(self):
        while(not self.in_queue.empty()):
            msg = self.receive()
            if (msg > self.leader):
                self.leader = msg
                for n in self.neighbours():
                    self.send(self.leader, n)            

        
class NodeFactory:
    def __init__(self, nodeclass=Node, system=None):
        self.nodeclass = nodeclass        
        self.system = system
    
    def node(self, uid):
        return self.nodeclass(uid, self.system)
        

class System: 
    def __init__(self, G, nodeclass):
        NF = NodeFactory(nodeclass=nodeclass, system=self)
        self.G = G
        self.nodes = {}
        for n in G.nodes():
            self.nodes[n] = NF.node(n)
        for n in self.allnodes():
            n.init()
            
            
    def allnodes(self):
        return self.nodes.values()
                  
    def step(self):
        for node in self.allnodes():            
            node.step()
        for node in self.allnodes():        
            while (not node.out_queue.empty()):                
                msg = node.out_queue.get()
                self.nodes[msg[0]].in_queue.put(msg[1])

            
G = nx.barabasi_albert_graph(20,3)

S = System(G, nodeclass=LeaderNode)
for x in range(nx.diameter(G)+1):
    S.step()
    
for node in S.allnodes():
    print("Node {0} has leader {1}".format(node.uid, node.leader))
    
