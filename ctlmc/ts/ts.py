class Proposition:
    def __init__(self,name):
        self._name = name

    def __str__(self):
        return self._name

    def getName(self):
        return self._name
    
        
class State:
    def __init__(self,name, propositions= None):
        self._name = name
        self._props = propositions or {}
        self._trans = []
        self._pred = []
        
    def __str__(self):
        return str(self._name)

    def getName (self):
        return self._name

    def addTrans (self,trans):
        self._trans.append (trans)

    def addPred (self,trans):
        self._pred.append (trans)
        
        
    def getTrans (self):
        return self._trans

    def getPred (self):
        return self._pred
    
    
    def getProps (self):
        return self._props

class Transition:
    def __init__(self,src,dst):
        self._src = src
        self._dst = dst


    def getFrom (self):
        return self._src

    def getTo (self):
        return self._dst

class TransitionSystem:
    def __init__ (self,props,states,initialstate,transitions):
        self._props = props
        self._states = states
        self._initialstate = initialstate
        self._transitions = transitions


    def getStates (self):
        return self._states
        
    def getInitial(self):
        return self._initialstate

    def getProps (self):
        return self._props
