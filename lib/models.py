import random
from lib import utils
from collections import defaultdict


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
    """
    If their given name matches one in the (not yet implemented) monster collection, their stats will be initialized with 
    default data.
    """
    def __init__(self, name, *args, **kwargs):
        super(Monster, self).__init__(name, stats)
        
    

class CharacterCollection(object):
    """
    A wrapper for a bunch of objects with similar function calls.
    """
    
    def __init__(self, members=None):
        self._members = members or set()

    def __iter__(self):
        return self._members
        
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
    
    def __init__(self, *args, **kwargs):
        super(InitManager, self).__init__(*args, **kwargs)
        self._inits = []
        self.current_init_number = None
        self.current_init_index = 0
    
    def add(self, what):
        if isinstance(what, CharacterCollection):
            self.add_collection(what)
        else:
            super(InitManager, self).add(what)

        if self.current_init_number is not None:
            current = self.get_current()
            self._inits.append((what.roll('init'), what))
            self.resort(current)
            
    def add_collection(self, what):
        for item in what:
            super(InitManager, self).add(item)
        if self.current_init_number is not None:
            current = self.get_current()
            for item in what:
                self._inits.append((item.roll('init'), item))
            self.resort(current)

    def resort(self, current):
        self.sort_inits()
        #figure out the index of the creature that currently has init
        self.current_init_index = self._inits.index(current) 
        
    def sort_inits(self):
        self._inits.sort() #sorting a list of tuples sorts on the first element of each tuple
        self._inits.reverse()
        
        dupes = self.get_duplicates()
        if dupes:
            for dupe_group in dupes:
                for roll, entity in dupe_group:
                    self._inits.remove((roll, entity))
                    new_roll = float(int(roll)) + float((entity.stats.dex))/100 + float(utils.roll(1, 100))/(100*100)
                    self._inits.append((new_roll, entity))
            self._inits.sort()
            self._inits.reverse()
        
    
    def get_duplicates(self):
        dupes = defaultdict(list)
        for item in self._inits:
            dupes[item[0]].append(item)
        return [dupes[key] for key in dupes if len(dupes[key]) > 1]
            
    def reset(self, keep_PCs=True):
        if not keep_PCs:
            self._members = set()
        else:
            for item in self._members:
                if not isinstance(item, PC):
                    self._members.remove(item)
        self.current_init = None
        self._inits = []
    
    def get_current(self):
        return self._inits[self.current_init_index]
    current = property(get_current)
    
    def start(self):
        self._inits = []
        for item in self._members:
            self._inits.append((item.roll('init'), item))
        self.sort_inits()
        self.current_init_number = self._inits[0][0] #first initiative
        return self._inits[0]
    
    def get_next(self):
        self.current_init_index += 1
        try:
            return self._inits[self.current_init_index]
        except IndexError:
            self.current_init_index = 0
            return self._inits[self.current_init_index]
    next = property(get_next)
    


        
    
    
            
            
        
        
    
    