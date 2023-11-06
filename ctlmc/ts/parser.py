import pyparsing as pp
import ctlmc.ts.ts

class TmpPropList:
    def __init__(self,l):
        self._List = l

class TmpTransList:
    def __init__(self,l):
        self._List = l

class TmpStateList:
    def __init__(self,l):
        self._List = l

class Propositions:
    def __init__(self,props):
        self._props = props

        
class Parser:
    def __init__(self):
        PROP = pp.CaselessLiteral ("Propositions")
        LBRACE = pp.Literal ("{")
        prop = pp.Regex ("[a-z]+").setParseAction (lambda s,l,t: ctlmc.ts.ts.Proposition (t[0]))
        RBRACE = pp.Literal ("}")
        propparser = (PROP + LBRACE + pp.delimitedList (prop).setParseAction (lambda s,l,t: Propositions(t))
                        + RBRACE).setParseAction (lambda s,l,t: t[2])



        States = pp.CaselessLiteral ("States")
        prop = pp.Regex ("[a-z]+").setParseAction (lambda s,l,t: t[0])
        state = pp.Regex ("[A-Z]+").setParseAction (lambda s,l,t: t[0])
        
        statesparser = (States +
                        pp.delimitedList (
                        (state     
                        + LBRACE + pp.delimitedList (prop).setParseAction (lambda s,l,t: TmpPropList(t))
                            + RBRACE).setParseAction (lambda s,l,t: (t[0],t[2])))
                        ).setParseAction (lambda s,l,t: TmpStateList(t[1:]))


        transitions = pp.CaselessLiteral ("Transitions")
        state = pp.Regex ("[A-Z]+").setParseAction (lambda s,l,t: t[0])
        
        transparser = (
            transitions +
            pp.delimitedList ((state + pp.Literal ("->") + state).setParseAction (lambda s,l,t: ((t[0],t[2])))).setParseAction (lambda s,l,t: TmpTransList (t))).setParseAction (lambda s,l,t: t[1])
            
        
        self._parser = (propparser + statesparser + transparser)
        
        
        
        

    def parse (self,string):
        props,nstates,transs =  self._parser.parseString (string,parseAll = True)
        
        propositions = []
        states= []
        transitions = []
        propmap = dict()
        statemap = dict()
        
        
        for p in props._props:
            propositions.append (p)
            propmap[p.getName ()] = p


        for s in nstates._List:
            prop = []
            for i in  s[1]._List:
                pp = propmap.get(i,None)
                prop.append (pp)
            states.append (ctlmc.ts.ts.State (s[0],prop))
            statemap[s[0]] = states[-1]
            #print (s[0])
        
        for s in transs._List:
            src = statemap[s[0]]
            dst = statemap[s[1]]
            transitions.append (ctlmc.ts.ts.Transition (src,dst))
            src.addTrans (transitions[-1])
            dst.addPred (transitions[-1])
        return ctlmc.ts.ts.TransitionSystem (propositions,states,states[0],transitions)
            
            
        #print (props)
        #print (states)
        
