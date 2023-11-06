

class CTLProp:
    def __init__ (self,prop):
        self._prop = prop

    def __str__(self):
        return str(self._prop)

    def getProp (self):
        return self._prop
    
class Conjunction:
    def __init__(self,left,right):
        self._left = left
        self._right = right


    def __str__(self):
        return f"{str(self._left)} && {str(self._right)}" 


    def getLeft (self):
        return self._left

    def getRight (self):
        return self._right
    
    
class Negation:
    def __init__(self,neg):
        self._neg = neg


    def __str__(self):
        return f"!{str(self._neg)}" 

    def getNegation (self):
        return self._neg
    
class ExistsNext:
    def __init__(self,next_):
        self._next = next_


    def __str__(self):
        return f"EX ({str(self._next)})" 

    def getNext (self):
        return self._next

class ExistsAlways:
    def __init__(self,always_):
        self._always = always_


    def __str__(self):
        return f"E[] ({str(self._always)})" 

    def getAlways (self):
        return self._always

    
class ExistsUntil:
    def __init__(self,left,right):
        self._left = left
        self._right = right
        
    def __str__(self):
        return f"E[{str(self._left)} U {str(self._right)} ]" 

    def getLeft (self):
        return self._left

    def getRight (self):
        return self._right
    



