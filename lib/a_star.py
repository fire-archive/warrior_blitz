# A* implementation
#
# By: Henry McLaughlin
#
# Written for Ludum Dare #23 ("Tiny Worlds")
#
# This file is licensed under the terms of the
# cc0 license, which is equivalent to public
# domain. Basically, do whatever you want with
# it. I don't mind. :)
#

from math import *

# The cost of a node link where
# one of the two is blocked.
BLOCKED = -1

class PathNode(object):
    
    def __init__(self,blocked,pos):
        super(PathNode,self).__init__()
        
        self.links = {}
        
        self.blocked = blocked
        
        self.pos = tuple(pos)
        
    
    def __cmp__(self,other):
        if self is other:
            return 0
            
        else:
            # Otherwise, compare names
            # It's abritrary but deterministic.
            return self.pos.__cmp__(other.pos)
            
        
    
    def __str__(self):
        return type(self).__name__ + ': '+str(self.pos)
        
    

class PathGrid(object):
    
    def __init__(self,nodes=None):
        super(PathGrid,self).__init__()
        
        self.nodes = {}
        
        if nodes:
            for node in nodes.values():
                self.addNode(node)
                
            
        
    
    def addNode(self,node):
        if node.pos in self.nodes:
            raise ValueError('Node named '+str(node.pos)+' already exists in this path graph')
            
        
        self.nodes[node.pos] = node
        
        for link in node.links:
            # Unpack the link's contents
            to,cost = link
            
            # Link the given node to the destination
            # node with the link's cost.
            self.linkNodes(node,to,cost)
            
        
    
    def linkNodes(self,node_1,node_2,cost):
        if node_1.pos not in node_2.links:
            # If node_2 does not have a link
            # to node_1, add one.
            node_2.links[node_1.pos] = [node_1,cost]
            
        
        if node_2.pos not in node_1.links:
            # If node_1 does not have a link
            # to node_2, add one.
            node_1.links[node_2.pos] = [node_2,cost]
            
        
        
    
    def costBetween(self,node_1,node_2):
        if (node_2.pos not in node_1.links and
            node_1.pos not in node_2.links):
            raise ValueError('Nodes given are not linked (nodes given were '+str(node_1)+' and '+str(node_2)+')')
            
        
        if node_1.blocked or node_2.blocked:
            return BLOCKED
            
        
        if node_2.pos in node_1.links:
            return node_1.links[node_2.pos][1]
            
        else:
            return node_2.links[node_1.pos][1]
            
        
    
    def findPathBetween(self,node_1,node_2):
        path = []
        
        open_nodes = []
        closed_nodes = []
        
        open_nodes.insert(0,(node_1,0,0,0,None))
        
        found = False
        no_path = False
        
        def cmp_f(n_1,n_2):
            return n_1[3].__cmp__(n_2[3])
            
        
        while not (found or no_path):
            for link in open_nodes[0].links:
                to,g = link
                parent = open_nodes[0]
                
                dist_x = abs(node_2.pos[0] - node.pos[0])
                dist_y = abs(node_2.pos[1] - node.pos[1])
                
                h = dist_x+dist_y
                
                f = g + h
                
                node_data = to,g,h,f,parent
                
                # Add the node to the open list
                open_nodes.append(node_data)
                
            
            open_nodes.sort(cmp_f)
            
            for node_data in open_nodes:
                # Unpack the node data
                to,g,h,f,parent = node_data
                
            
        
        closed_nodes.append(open_nodes.pop(0))
        
        # TODO: Build the path
        # TODO: If there isn't a path, return an empty path.
        
        return path
        
    
