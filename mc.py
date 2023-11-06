import ctlmc.ts.parser
import ctlmc.ctl.parser
import ctlmc.ctl.ctl

import sys
import graphviz
import ctlmc.ts.parser


with open(sys.argv[1],'r') as ff: 
    inp = ff.read ()

with open(sys.argv[2],'r') as ff: 
    prop = ff.read ()

def predOf (S):
    for s in S:
        for t in s.getPred ():
            yield t.getFrom ()
        
    
class ModelChecker:
    def __init__(self,ts):
        self._ts = ts
    def Check (self,ctl):
        print (f"Check: {str(ctl)}")
        
        match ctl:
            case ctlmc.ctl.ctl.CTLProp():
                res = set ()
                
                for s in self._ts.getStates ():
                    if ctl.getProp () in s.getProps ():
                        res.add (s)
                return res
            case ctlmc.ctl.ctl.Conjunction():
                l = self.Check (ctl.getLeft ())
                r = self.Check (ctl.getRight ())
                return l.intersection (r)
            case ctlmc.ctl.ctl.Negation():
                neg = self.Check (ctl.getNegation ())
                res = set ()
                for s in self._ts.getStates ():
                    if s not in neg:
                        res.add(s)
                return res
                        
            case ctlmc.ctl.ctl.ExistsNext():
                n = self.Check (ctl.getNext ())
                res = set ()
                for s in predOf(self.Check (ctl.getNext ())):
                    res.add (s)
                return res
            
            case ctlmc.ctl.ctl.ExistsUntil():
                _left = self.Check (ctl.getLeft ())
                _right = self.Check (ctl.getRight ())
                res = _right.copy ()
                while True:
                    old = res
                    pred = predOf (old)
                    _left_cap_pred = _left.intersection (pred)
                    res = _right.union (_left_cap_pred)
                    if old == res:
                        break
                return res
                    
            case ctlmc.ctl.ctl.ExistsAlways():
                n = self.Check (ctl.getAlways ())
                res = n
                while True:
                    old = res.copy ()
                    pred = predOf (old)
                    res  = old.intersection (pred)
                    if res == old:
                        break
                return res
                    
                

ts = ctlmc.ts.parser.Parser ().parse(inp)
ctl = ctlmc.ctl.parser.Parser (ts.getProps ()).parse(prop)


mc = ModelChecker (ts)
res = mc.Check (ctl)



for s in res:
    print (str(s))
                

#Visualise
dot = graphviz.Digraph('Transition SYstem', comment='TS')

waiting = [ts.getInitial ()]
passed = {ts.getInitial ()}

def newnode (ll):
    if ll in res:    
        dot.attr('node',style='filled', color='red') 
    else:
        dot.attr('node',style='ellipse', color='black') 
        
            
    f = ",".join (str(p) for p  in ll.getProps () )
    dot.node (str(ll),f)

newnode (ts.getInitial ())
while len(waiting) > 0:
    l = waiting.pop ()
    for f in l.getTrans ():
        dst = f.getTo ()
        
        if dst not in passed:
            newnode (dst)
            waiting.append (dst)
            passed.add (dst)
        dot.edge (str(l),str(dst))
        
dot.view ()

    



    
    
