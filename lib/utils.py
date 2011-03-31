import re
import random

def render_string(item):
    #first, [x,y,z] items
    res = re.findall("\[(.+?,.+?)\]", item)
    for match in res:
        choices = re.split(",\s*", match)
        item = item.replace("[%s]"% match, random.choice(choices))

    #random rolls like (1, 10)
    res = re.findall("\(\d+\s*-\s*\d+\)", item)
    for match in res:
        range = re.search("(\d+)\s*-\s*(\d+)", match)
        low = int(range.groups()[0])
        high = int(range.groups()[1])
        roll_result = random.randint(int(low), int(high))
        item = item.replace(match, str(roll_result))

    item = re.sub('(\d+)d(\d+)([+\-](\d+)|)', repl=dice_callback, string=item)
        

    return item

def roll(number=1, sides=20, addition=0):
    res = 0
    for i in range(number):
        res += random.randint(1, sides)
    return res+addition

def dice_callback(matchobj):
    """
    Callback function to return the result of a roll; good for use with re.sub()
    """
    groups = matchobj.groups()
    number = int(groups[0])
    sides = int(groups[1])
    if groups[2]:
        addition = int(groups[2])
    else:
        addition = 0
    return str(roll(number, sides, addition))

import readline

def raw_input_no_history(output=None):
    input = raw_input(output)
    readline.remove_history_item(readline.get_current_history_length()-1)
    return input
    
    
    