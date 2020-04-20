from alpha import *
class AlphaPlus(Alpha):
    def __init__(self, log, splines='ortho'):
        super().__init__(log, splines)
        self.a = Alpha(log=self.log, splines=splines)
        self.fl1l = self.get_fl1l() # set of places with self-loop
        self.loop1 = self.get_loop1()   # a △ b, means there is a subsequence ...aba... in the logs
        self.loop2 = self.get_loop2()   # a ♢ b, means are sequences ...aba... and ...bab...
        self.cs = self.causality_new()   # causality a -> b <=> a > b and ( b /> a or a ♢ b )
        self.inv_cs = self.inv_causality()
        self.pr = self.parallel_new()    # parralelism a > b and b > a and not(a ♢ b)
        self.l1l = self.get_l1l()   # gets all identify all one-loop transitions, i.e. ...aa..., so a -> a, causality 
        self.t_prim = self.tl - self.l1l
        self.log = self.log_minus_l1l()
        #self.G = MyGraph()  
    

    def get_loop1(self):
        # a △ b
        loop1 = set()
        for trace in self.log:
            if len(trace) > 2:
                for i in range(0, len(trace)-3):
                    try:
                        if trace[i] == trace[i+2] and trace[i] != trace[i+1]:
                            loop1.add((trace[i], trace[i+1]))
                    except:
                        pass
        return loop1
    
    def get_loop2(self):
        # a ♢ b
        loop2 = set()
        for l in self.loop1:
            for k in self.loop1:
                if l == k[::-1]:
                    loop2.add(l)
           
        return loop2 


    def get_l1l(self):
        # ...aa...
        l1l = set()
        for pair in self.ds:
            if pair == pair[::-1]:
                l1l.add(pair[0])
        return l1l

    def get_fl1l(self):
        # places where there are self-loops
        fl1l = []
        for trace in self.log:
            for i in range(1, len(trace)-2): 
                try:
                    if trace[i] == trace[i+1] and trace[i] != trace[i+2]:
                        fl1l.append((trace[i-1], trace[i], trace[i+2]))
                except:
                    pass
        return fl1l
                    


    def parallel_new(self): # redefined
        # (x || y) & (y || x)
        pr = set()
        for pair in self.ds:
            if pair[::-1] in self.ds and pair not in self.loop2:
                pr.add(pair)
        return pr

    def causality_new(self):
        # x -> y
        cs = {}
        for pair in self.ds:
            if pair[::-1] not in self.ds or pair in self.loop2:
                if pair[0] in cs.keys():
                    cs[pair[0]].append(pair[1])
                else:
                    cs[pair[0]] = [pair[1]]
        return cs

    def log_minus_l1l(self):
        log_minus_l1l = self.log
        for j in range(0, len(log_minus_l1l)):
            for i in range(0, len(log_minus_l1l[j])-2):
                try:
                    if log_minus_l1l[j][i] == log_minus_l1l[j][i+1]:
                        log_minus_l1l[j] = [value for value in log_minus_l1l[j] if value != log_minus_l1l[j][i]]
                        print(trace)
                except:
                    pass
        
        return log_minus_l1l


    def run_alpha(self):
        self.a.pr = self.pr
        self.a.cs = self.cs
        self.a.inv_cs = self.inv_cs
        self.G = self.a.create_graph(l1l=self.l1l)
        
    def run_alpha_plus(self, filename):
        '''for i in self.l1l:
            self.G.add_self_loops(source=i)'''
        self.G.render('../graphs/' + filename, view=False)

    
