#! /usr/bin/env python3
# coding: utf-8
import itertools
import copy
from graph import MyGraph
class Alpha():
    def __init__(self, log, splines='ortho'):
        self.log = log
        self.tl = self.get_TL_set() # all tasks in the log
        self.ti = self.get_TI_set() # tasks that appear at least once as first task of a case 
        self.to = self.get_TO_set() # tasks that appear at least once as last task in a case
        self.ds = self.direct_succession()  # direct successors a > b
        self.cs = self.causality()   # causality a -> b <=> a > b and b /> a
        self.pr = self.parallel()    # parralelism a > b and b > a
        self.ind = self.choice()   # no direct succession a # b and b # a
        self.xl = self.get_XL_set() # potential task connections (a->b or a->(b#c) or (b#c)->d)
        self.yl = self.get_YL_set() # subset of XL: eliminating a->b and a->c if there exists some a->(b#c), eliminating b->c and b->d if there exists some (b#c)->d. 
        self.G = MyGraph(splines)  
        self.inv_cs = self.inv_causality()   # inverse causality 
    
    def __str__(self):
        alpha_sets = []
        alpha_sets.append("TL set: {}".format(self.tl))
        alpha_sets.append("TI set: {}".format(self.ti))
        alpha_sets.append("TO set: {}".format(self.to))
        alpha_sets.append("XL set: {}".format(self.xl))
        alpha_sets.append("YL set: {}".format(self.yl))
        return '\n'.join(alpha_sets)

    def get_TL_set(self):
        tl = set()
        for item in self.log:
            for i in item:
                tl.add(i)
        return tl
        
    def get_TI_set(self):
        ti = set()
        for item in self.log:
            ti.add(item[0])
        return ti

    def get_TO_set(self):
        to = set()
        for item in self.log:
            to.add(item[-1])
        return to
    
    def get_XL_set(self):
        xl = set()
        subsets = itertools.chain.from_iterable(itertools.combinations(self.tl, r) for r in range(1, len(self.tl) + 1))
        independent_a_or_b = [a_or_b for a_or_b in subsets if self.__is_ind_set(a_or_b, self.ind)]
        for a, b in itertools.product(independent_a_or_b, independent_a_or_b):
            if self.__is_cs_set((a, b), self.cs):
                xl.add((a, b))
        return xl

    def __is_ind_set(self, s, ind):
        if len(s) == 1:
            return True
        else:
            s_all = itertools.combinations(s, 2)
            for pair in s_all:
                if pair not in ind:
                    return False
            return True
    
    def __is_cs_set(self, s, cs):
        set_a, set_b = s[0], s[1]
        s_all = itertools.product(set_a, set_b)
        for pair in s_all:
            if pair not in cs:
                return False
        return True
    
    def get_YL_set(self):
        yl = copy.deepcopy(self.xl)
        s_all = itertools.combinations(yl, 2)
        for pair in s_all:
            if self.__issubset(pair[0], pair[1]):
                yl.discard(pair[0])
            elif self.__issubset(pair[1], pair[0]):
                yl.discard(pair[1])
    
        # remove self-loops
        self_loop = set()
        for pair in self.pr:
            if pair == pair[::-1]:  # if we found pairs like (b,b), add b into self-loop sets
                self_loop.add(pair[0])

        to_be_deleted = set()
        for pair in yl:
            if self.__contains(pair, self_loop):
                to_be_deleted.add(pair)
        for pair in to_be_deleted:
            yl.discard(pair)
        return yl
    
    def __issubset(self, a, b):
        if set(a[0]).issubset(b[0]) and set(a[1]).issubset(b[1]):
            return True
        return False
    
    def __contains(self, a, b):
        # return True if nested tuple "a" contains any letter in set "b"
        # e.g. __contains((('a',), ('b',)), ('b', 'c')) -> True
        return any(j == i[0] for i in a for j in b)
    
    def get_footprint(self):
        footprint = []
        footprint.append("All transitions: {}".format(self.tl))
        footprint.append("Direct succession: {}".format(self.ds))
        footprint.append("Causality: {}".format(self.cs))
        footprint.append("Parallel: {}".format(self.pr))
        footprint.append("Choice: {}".format(self.ind))
        return '\n'.join(footprint)
    
    def generate_footprint(self, txtfile='footprint.txt'):
        with open(txtfile, 'w') as f:
            f.write(self.get_footprint())
    
    def direct_succession(self):
        # x > y
        ds = set()
        for trace in self.log:
            for x, y in zip(trace, trace[1:]):
                ds.add((x, y))
        return ds
    
    def causality(self):
        # x -> y
        cs = {}
        for pair in self.ds:
            if pair[::-1] not in self.ds:
                if pair[0] in cs.keys():
                    cs[pair[0]].append(pair[1])
                else:
                    cs[pair[0]] = [pair[1]]
        return cs

    def inv_causality(self):
        # only for causality cases which has one succesor
        inv_cs = {}
        for key, values in self.cs.items():
            if len(values) == 1:
                if values[0] in inv_cs.keys():
                  inv_cs[values[0]].append(key)
                else:
                  inv_cs[values[0]] = [key]
        return inv_cs

    
    def parallel(self):
        # (x || y) & (y || x)
        pr = set()
        for pair in self.ds:
            if pair[::-1] in self.ds:
                pr.add(pair)
        return pr
    
    def choice(self):
        # (x # y) & (y # x)
        ind = set()  # ind is the abbreviation of independent
        all_permutations = itertools.permutations(self.tl, 2)
        '''for pair in all_permutations:
            if pair not in self.cs and pair[::-1] not in self.cs and pair not in self.pr:
                ind.add(pair)'''
        for pair in all_permutations:
            if pair not in self.ds and pair[::-1] not in self.ds:
                ind.add(pair)
        return ind

    def set_contain(self, s, value):
        for i in s:
            for j in i:
                if j == value:
                    return True
        
        return False

    def create_graph(self, filename='graph', view=False, l1l=None):
        # adding split gateways based on causality
        for event in self.cs:
            if len(self.cs[event]) > 1:
                if tuple(self.cs[event]) in self.pr:
                    self.G.add_and_split_gateway(event,self.cs[event])
                #elif tuple(self.cs[event]) in self.ind:
                #    self.G.add_xor_split_gateway(event,self.cs[event])
                else:
                    if l1l is not None and event in l1l:
                        temp_cs = self.cs[event]
                        temp_cs.append(event)
                        self.G.add_xor_split_gateway(event,temp_cs)
                    else:
                        self.G.add_xor_split_gateway(event,self.cs[event])
                    
    
        # adding merge gateways based on inverted causality
        for event in self.inv_cs:
            if len(self.inv_cs[event]) > 1:
                if tuple(self.inv_cs[event]) in self.pr:
                    self.G.add_and_merge_gateway(self.inv_cs[event],event)
                else:
                    if l1l is not None and any(elem in self.inv_cs[event] for elem in l1l):
                        temp_event = [event]
                        for i in self.inv_cs[event]:
                            temp_event.append(i)
                        self.G.add_xor_merge_split_gateway(self.inv_cs[event],temp_event)
                    else:
                        self.G.add_xor_merge_gateway(self.inv_cs[event],event)
            elif len(self.inv_cs[event]) == 1:
                if l1l is not None and self.inv_cs[event][0] in l1l:
                    temp_inv_cs = [event]
                    temp_inv_cs.append(self.inv_cs[event][0])
                    self.G.add_xor_split_gateway(self.inv_cs[event][0],temp_inv_cs)
                else:
                    source = list(self.inv_cs[event])[0]
                    self.G.edge(source,event)
                
            
        # adding start event
        self.G.add_event("start")
        if len(self.ti) > 1:
            if tuple(self.ti) in self.pr: 
                self.G.add_and_split_gateway("start",self.ti)
            else:
                self.G.add_xor_split_gateway("start",self.ti)
        else: 
            self.G.edge("start",list(self.ti)[0])
         
        # adding end event
        self.G.add_event("end")
        if len(self.to) > 1:
            if tuple(self.to) in self.pr: 
                self.G.add_and_merge_gateway(self.to,"end")
            else:
                self.G.add_xor_merge_gateway(self.to,"end")    
        else: 
            self.G.edge(list(self.to)[0],"end")


        self.G.render('../graphs/' + filename, view=view)

        return self.G
        
        
        #self.G.view(filename)
        