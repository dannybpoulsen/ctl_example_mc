import sys
import graphviz
import ctlmc.ts.parser


with open(sys.argv[1],'r') as ff: 
    inp = ff.read ()


ts = ctlmc.ts.parser.Parser ().parse(inp)

dot = graphviz.Digraph('Transition SYstem', comment='TS')


waiting = [ts.getInitial ()]
passed = {ts.getInitial ()}

while len(waiting) > 0:
    l = waiting.pop ()
    f = ",".join (str(p) for p  in l.getProps () )
    dot.node (str(l),f)
    
    for f in l.getTrans ():
        dst = f.getTo ()
        dot.edge (str(l),str(dst))
        if dst not in passed:
            waiting.append (dst)
            passed.add (dst)
    
dot.view ()
