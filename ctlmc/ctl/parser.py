import pyparsing as pp
import ctlmc.ctl.ctl

class Parser:
    def __init__(self,props):
        self._propmap = dict ()
        for p in props:
            self._propmap[p.getName ()] = p

    def parse (self,string):
        
        
        ctl = pp.Forward()

        prop =  pp.Regex ("[a-z]+").setParseAction (lambda s,l,t: ctlmc.ctl.ctl.CTLProp (self._propmap.get(t[0])))

        conjunction = (pp.Literal ("(") + ctl + pp.Literal ("&&")  + ctl + pp.Literal (")") ).setParseAction (lambda s,l,t: ctlmc.ctl.ctl.Conjunction (t[1],t[3]))

        negation = (pp.Literal ("!") +pp.Literal ("(") + ctl +   pp.Literal (")") ).setParseAction (lambda s,l,t: ctlmc.ctl.ctl.Negation (t[2]))
        
        

        until = ( pp.Literal ("E")  + pp.Literal ("[") + ctl + pp.Literal ("U")  + ctl + pp.Literal ("]") ).setParseAction (lambda s,l,t: ctlmc.ctl.ctl.ExistsUntil (t[2],t[4]))
        
        
        existsNext = (pp.Literal ("EX") + pp.Literal ("(") + ctl +pp.Literal (")") ).setParseAction (lambda s,l,t: ctlmc.ctl.ctl.ExistsNext (t[2]))
        existsAlways = (pp.Literal ("E[]") + pp.Literal ("(") + ctl +pp.Literal (")") ).setParseAction (lambda s,l,t: ctlmc.ctl.ctl.ExistsAlways (t[2]))
        
        
        
        ctl << (prop |  negation | until | existsNext | conjunction | existsAlways).setParseAction (lambda s,l,t: t[0])
        return ctl.parseString (string,parseAll = True)[0]
    
    

class Prop:
    def __init__ (self,p):
        self._name = p

    def getName (self):
        return self._name



