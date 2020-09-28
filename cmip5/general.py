import glob, os
from copy import copy

class NestedDict(dict):
    """Nested dictionary that automatically instantiate a new level
    on request.
    
    Methods
    -------
    keylevel(level)
      Return all keys at the given level.
    walk(subset)
      Iterate through all entries, returning the sequence of keys and 
      the value. Specify subsets to iterate from at different levels. 
    get(keys)
      Return the value stored at the given sequence of keys.
    set(keys, value)
      Set the value at the given sequence of keys.
    
    Example
    -------
    >>> D = NestedDict()
    >>> D[1][2][3][4] = True
    >>> D['a']['b'] = 'foo'
    >>> D['a']['b1'] = 'bar'
    
    >>> print(D)
    {'a': {'b': 'foo', 'b1': 'bar'}, 1: {2: {3: {4: True}}}}
    
    >>> D.depth
    4
    
    >>> D.size
    3
    
    >>> D.keylevel(1)
    set([2, 'b', 'b1'])
    
    >>> [(keys, val) for (keys, val) in D.walk({0:['a',]})]
    [(('a', 'b'), 'foo'), (('a', 'b1'), 'bar')]
    
    >>> D.get((1,2,3,4))
    True
    
    >>> D.set((4,5,6), False)
    >>> D[4][5][6]
    False
    
    """
    
    def __missing__(self, key):
            self[key] = NestedDict()
            return self[key]
    
    def keylevel(self, level):
        """Return a set-like object providing a view of keys at the 
        given level.
        """
        if level == 0:
            return set(self.keys())
        else:
            
            keys = []
            for v in list(self.values()):
                if isinstance(v, NestedDict):
                    keys.append(v.keylevel(level-1))
            if keys == []:
                return set()
            else:
                return set.union(*keys)

    def get(self, keys):
        """Return the NestedDict stored at the keys sequence.
        """
        o = self
        for key in keys:
            if key in o:
                o = o[key]
            else:
                raise AttributeError("This key does not exist: %s"%key)
        return o
        
    def set(self, keys, value):
        """Set the value of the NestedDict at the given keys sequence.
        """
        o = self
        for key in keys[:-1]:
            o = o[key]
        o[keys[-1]] = value
        
    
    def depth():
        """The maximum number of levels."""
        def fget(self):
            i = 0
            while True:
                if self.keylevel(i) == set():
                    return i
                else:
                    i += 1
        return locals()
    depth = property(**depth())
    
    def size():
        """The total number of values stored.""" 
        def fget(self):
            i = 0
            for tmp in self.walk():
                i += 1
            return i
        return locals()
    size = property(**size())
            
    def walk(self, subset={}):
        """Return a generator iterating through all items or a subset 
        of items, returning a sequence of keys and the value.
        
        Parameters
        ----------
        **subset : {int : seq}
          Dictionary keyed by level containing a sequence of keys 
          defining the subset. If the subset is indicated by a list, 
          walk will traverse elements of the subset if they are 
          present. If the subset is a tuple, walk will traverse the 
          subset *only if* the node holds all subset items.
          
        Returns
        -------
        out : generator
          Generator yielding (sequence of keys, value).
          
        """
        subset = copy(subset)
        valid = subset.pop(0, None)
        
        # Prepare subset for next level.
        subset = dict([(key-1, val) for (key, val) in list(subset.items())])
        
        # Iterate through valid keys.
        for key, value in list(self.items()):
            if valid is None or key in valid:
                if type(valid) == tuple:
                    if not set(valid).issubset(list(self.keys())):
                        break
                if isinstance(value, NestedDict):
                    for tup, tip in value.walk(subset):
                        yield (key, ) + tup, tip
                else:
                    yield (key,), value
    
    def copy(self, subset={}):
        """Return a copy of a subset of the NestedDict."""
        out = NestedDict()
        for keys, value in self.walk(subset):
            out.set(keys, copy(value))
        return out
        
    def update(self, *args, **kwds):
        """Update NestedDict with values from another NestedDict or a 
        standard dictionary.
        """
        if len(args) == 1 and isinstance(args[0], NestedDict):
            E = args[0]
            for key, val in E.walk():
                self.set(key, val)
            
        else:
            dict.update(self, *args, **kwds)    
        

