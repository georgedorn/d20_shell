import random
from lib import utils


class Table(object):

    def __init__(self, items, range_inclusive=True):
        table = []
        if range_inclusive:
            range = 1
        else:
            range = 0
        for item in items:
            weight = abs(item[0]) + range
            table.extend( weight * [item[1]] )
        self.table = table
        self.unique_items = items

    def pick_item(self, render=True):
        item = random.choice(self.table)
        if render:
            return render_string(item)
        else:
            return item

    def pick_items(self, number, unique=False, render=True):
        results = []
        while len(results) < number:
            item = self.pick_item(render=False)
            if unique and item in results:
                continue
            results.append(item)
        return [ render_string(r) for r in results]
    
class StatCollection(object):
    
    def __init__(self, owner, collection_type='stat', member_cleanup_callback=int):
        self._owner = owner
        self._collection_type = collection_type #name of the stat collection (e.g. 'stat', 'skill')
        self._cleanup_callback = member_cleanup_callback
        
        
    def __getattr__(self, name):
        res = utils.raw_input_no_history(">>>%s %s %s?" % (self._owner.name, name, self._collection_type))
        res = self._cleanup_callback(res)
        setattr(self, name, res)
        return res

class Character(object):
    
    def __init__(self, name, stats=None):
        self.name = name
        self.stats = StatCollection(self)

    def roll(self, what, type='d20'):
        value = getattr(self.stats, what)
        if type == 'd20':
            return utils.roll(number=1, sides=20, addition=value)
        
    
    
    
class PC(Character):
    pass

class Monster(Character):
    pass

class CharacterCollection():
    """
    A wrapper for a bunch of objects with similar function calls.
    """
    
    def __init__(self, members=None):
        self._members = members or set()
        
    def roll(self, what, output='console'):
        res = [ (c.name, c.roll(what)) for c in self._members]
        
        if output == 'console':
            for r in res:
                print "%s's %s: %s" % (r[0], what, r[1])
            return
        else:
            return res
        
    def add(self, what):
        self._members.add(what)
        
    def __getattr__(self, name):
        for c in self._members:
            if c.name == name:
                return c
        return None
    
class InitManager(CharacterCollection):
    pass
    
    
            
            
        
        
    
    