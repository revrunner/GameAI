import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Returns a function to determine whether a state meets a rule's requirements.
    # This code runs once, when the rules are constructed before the search is attempted

    def check(state):
        for tools in rule['Requires']:
            if tools not in state.items:
                return False

        for mats in rule['Consumes']:
            if mats not in state.items:
                return False
            elif state[mats] < rule['Consumes'][mats]:
                return False

        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        return True

    return check


def make_effector(rule):
    # Returns a function which transitions from state to new_state given the rule.
    # This code runs once, when the rules are constructed before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = state.copy()

        for make in rule['Produces'].keys():
            if make in next_state.keys():
                next_state[make] += rule['Produces'][make]
            else:
                next_state[make] = rule['Produces'][make]

        if 'Consumes' in rule:
            for use in rule['Consumes'].keys():
                if state[use] - rule['Consumes'][use] == 0:
                    del next_state[use]
                else:
                    next_state[use] -= rule['Consumes'][use]

        return next_state

    return effect


def make_goal_checker(goal):
    # Returns a function which checks if the state has met the goal criteria.
    # This code runs once, before the search is attempted.

    def is_goal(state):
        # This code is used in the search process and may be called millions of times.
        for itemName in state.keys():
            if itemName not in goal.keys():
                return False

            if state[itemName] < goal[itemName]:
                return False

        return True

    return is_goal


def viablegraph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)

def nonviablegraph(state):
    for r in all_recipes:
        if (not r.check(state)):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    # This heuristic function should guide your search.
    return 0


def search(graph, state, is_goal, limit, heuristic):
    start_time = time()
    newest_state = state.copy()

    # Search
    while time() - start_time < limit:
        nonviablegraph = nonviablegraph(state)
        viablegraph = viablegraph(state)



        pass

    # Failed to find a path
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # List of items that can be in your inventory:
    print('All items:',Crafting['Items'])

    # List of items in your initial inventory with amounts:
    print('Initial inventory:',Crafting['Initial'])

    # List of items needed to be in your inventory at the end of the plan:
    print('Goal:',Crafting['Goal'])

    # Dict of crafting recipes (each is a dict):
    print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])


    # Search - This is you!
    itemsHave = {}
    tools = []
    usedTools = []

    for item in Crafting['Goal'].keys():
            itemsHave[item] = Crafting['Goal'][item]
    for have in itemsHave:
        for recipeName, rule in Crafting['Recipes'].items():
            if 'Requires' in rule:
                if have in rule['Requires'].keys():
                    usedTools.append(have)

    recipesUsed = []
    possibleRecipes = []
    temp = True
    endIngredients = {}
  #  print(recipesUsed)
   # print(itemsHave)
    #print(tools)

    while(True):
        if(len(itemsHave) == 0):
            # get last tool and rule for that tool
            tool = tools.pop()
            usedTools.append(tool)
            for recipeName, rule in Crafting['Recipes'].items():
                if tool in rule['Produces']:
                    if recipeName not in recipesUsed:
                        recipesUsed.append(recipeName)
                    for add in rule['Consumes']:
                        if add not in itemsHave:
                            itemsHave[add] = rule['Consumes'][add]
                        else:
                            itemsHave[add] += rule['Consumes'][add]
                    break
            continue
        else:
            for item in itemsHave:
                # get rule for item
                for recipeName, rule in Crafting['Recipes'].items():
                  #  print(tools)
                   # print(itemsHave)
                    #print(usedTools)
                    dont_add = False
                    if 'Requires' in rule:
                        for tool in rule['Requires']:
                            if tool in usedTools:
                                dont_add = True
                            for name2, rule2 in Crafting['Recipes'].items():
                                for tool2 in rule2['Produces']:
                                    if tool is tool2:
                                        for name3, rule3 in Crafting['Recipes'].items():
                                            if 'Consumes' in rule2:
                                                for consume in rule2['Consumes']:
                                                    if consume in rule3['Produces']:
                                                        for used in usedTools:
                                                            if 'Requires' in rule3:
                                                                if used in rule3['Requires']:
                                                                    dont_add = True
                    if dont_add:
                        continue

                    if item in rule['Produces']:
                        recipesUsed.append(recipeName)
                        if 'Consumes' in rule:
                            for add in rule['Consumes']:
                                if add not in itemsHave:
                                    itemsHave[add] = rule['Consumes'][add]
                                else:
                                    itemsHave[add] += rule['Consumes'][add]
                        for minus in rule['Produces']:
                            itemsHave[minus] -= rule['Produces'][minus]
                            if itemsHave[minus] <= 0:
                                del itemsHave[minus]
                            break
                        if 'Requires' in rule:
                            for tool in rule['Requires']:
                                if tool not in tools and tool not in usedTools:
                                    tools.append(tool)
                        break
                break


        if len(itemsHave) == 0 and len(tools) == 0:
            break
  #  print(recipesUsed)
   # print(itemsHave)
    #print(tools)

    recipesUsed.reverse()
    total_time = 0
    count = 0
    items = Crafting['Initial']
    for each in recipesUsed:
        for name, check, effect, time in all_recipes:
            if each is name:
                total_time += time

                print("(", time, ", ", each, ",", effect(state), ")")
        count+=1
    print("{ total cost: ", total_time, ", total length: ", count, "}")