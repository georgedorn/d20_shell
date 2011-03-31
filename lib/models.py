import random


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
    
class Character(object):
    
    def __init__(self, name, stats=None, skills=None):
        self.name = name
        self.stats = stats or {}
        self.skills = skills or {}
        
    
class PC(Character):
    pass

class Monster(Character):
    pass