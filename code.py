import math
import random
import operator
import numpy as np
from copy import copy
import matplotlib.pyplot as plt
from random import randint, seed
from graphviz import Digraph, Source
from IPython.display import Image, display

random.seed(42)

Cobweb_parameters        = {'NUM_FIRMS': 50,'H': 10, 'A': 4.48, 'B': 0.048, 'x': 0, 'y': 0.016}
Evolution_parameters     = {'GENERATIONS': 100,'POP_SIZE': 150, 'MIN_DEPTH': 2, 'MAX_DEPTH': 17, 'TOURNAMENT_SIZE': 3, 'PCROSS': 0.9, 'PMUT': 0.033}

def add(x, y): return x + y
def sub(x, y): return x - y
def mul(x, y): return x * y
def div(x, y): return x / y if y != 0 else 1 #protected division function
def log(x): return math.log(x) if x > 0 else 1
def sin(x): return math.sin(x)
def cos(x): return math.cos(x)

FUNCTIONS = [[add, sub, mul, div], [log, sin, cos]]
TERMINALS = [round(random.uniform(-9.99, 9.99), 3)]

class GPTree:
    def __init__(self, Evolution_parameters, data = None, left = None, right = None):
        self.data  = data
        self.left  = left
        self.right = right
        self.MIN_DEPTH = Evolution_parameters.get('MIN_DEPTH')
        self.PMUT = Evolution_parameters.get('PMUT')

    def node_label(self): # return string label
        d = FUNCTIONS[0] + FUNCTIONS[1]
        if (self.data in d):
            return self.data.__name__
        else: 
            return str(self.data)

    def print_tree(self, prefix = ""): # textual printout
        print("%s%s" % (prefix, self.node_label()))        
        if self.left:  self.left.print_tree (prefix + "   ") #Recursive here
        if self.right: self.right.print_tree(prefix + "   ")

    def draw(self, dot, count): # dot & count are lists in order to pass "by reference" 
        node_name = str(count[0])
        dot[0].node(node_name, self.node_label())
        if self.left:
            count[0] += 1
            dot[0].edge(node_name, str(count[0]))
            self.left.draw(dot, count)
        if self.right:
            count[0] += 1
            dot[0].edge(node_name, str(count[0]))
            self.right.draw(dot, count)
        
    def draw_tree(self, fname, footer):
        dot = [Digraph()]
        dot[0].attr(kw='graph', label = footer)
        count = [0]
        self.draw(dot, count)
        Source(dot[0], filename = fname + ".gv", format="png").render()
        display(Image(filename = fname + ".gv.png"))

    def compute_tree(self): 
        if (self.data in FUNCTIONS[0]): 
            return self.data(self.left.compute_tree(), self.right.compute_tree())
        elif (self.data in FUNCTIONS[1]):
            return self.data(self.left.compute_tree())
        else: return self.data #self.data in  TERMINALS

    def random_tree(self, grow, max_depth, depth = 0): # create random tree using either grow or full method
        d = FUNCTIONS[0] + FUNCTIONS[1]
        if depth < self.MIN_DEPTH or (depth < max_depth and not grow): 
            self.data = d[randint(0, len(d)-1)]
        elif depth >= max_depth:   
            self.data = TERMINALS[randint(0, len(TERMINALS)-1)]
        else: # intermediate depth, grow
            if random.random() > 0.5: 
                self.data = TERMINALS[randint(0, len(TERMINALS)-1)]
            else:
                self.data = d[randint(0, len(d)-1)]
        if self.data in FUNCTIONS[0]:
            self.left = GPTree(Evolution_parameters)          
            self.left.random_tree(grow, max_depth, depth = depth + 1)            
            self.right = GPTree(Evolution_parameters)
            self.right.random_tree(grow, max_depth, depth = depth + 1)
        elif self.data in FUNCTIONS[1]:
            self.left = GPTree(Evolution_parameters)
            self.left.random_tree(grow, max_depth, depth = depth + 1)

    def mutation(self):
        if random.random() < self.PMUT: # mutate at this node
            self.random_tree(grow = True, max_depth = 2)
        elif self.left: self.left.mutation()
        elif self.right: self.right.mutation()

    def size(self): # tree size in nodes
        if self.data in TERMINALS: return 1
        l = self.left.size()  if self.left  else 0
        r = self.right.size() if self.right else 0
        return 1 + l + r

    def build_subtree(self): # count is list in order to pass "by reference"
        t = GPTree(Evolution_parameters)
        t.data = self.data
        if self.left:  t.left  = self.left.build_subtree()
        if self.right: t.right = self.right.build_subtree()
        return t

    def scan_tree(self, count, second): # note: count is list, so it's passed "by reference"
        count[0] -= 1            
        if count[0] <= 1: 
            if not second: # return subtree rooted here
                return self.build_subtree()
            else: # glue subtree here
                self.data  = second.data
                self.left  = second.left
                self.right = second.right
        else:  
            ret = None              
            if self.left  and count[0] > 1: ret = self.left.scan_tree(count, second)  
            if self.right and count[0] > 1: ret = self.right.scan_tree(count, second)  
            return ret

class Cobweb():
    def __init__(self, Cobweb_parameters):
        self.NUM_FIRMS = Cobweb_parameters.get('NUM_FIRMS')
        self.A = Cobweb_parameters.get('A')
        self.B = Cobweb_parameters.get('B')
        self.x = Cobweb_parameters.get('x')
        self.y = Cobweb_parameters.get('y')

    def quantity(self, expected_price):
        return max(0, (expected_price - self.x)/ (self.y * self.NUM_FIRMS))

    def cost(self, quantity):
        return (self.x * quantity + 0.5 * self.y * self.NUM_FIRMS * pow(quantity, 2))
  
    def market_price(self, list_quantity):
        return max(0, self.A - self.B * sum(list_quantity))

    def adjusted_profit(self, market_price, quantity, cost):
        profit = market_price * quantity - cost
        if profit >= -10:
            return profit + 10
        else:
            return 0

class GP():
    def __init__(self, Evolution_parameters):
        self.MIN_DEPTH = Evolution_parameters.get('MIN_DEPTH')
        self.MAX_DEPTH = Evolution_parameters.get('MAX_DEPTH')
        self.TOURNAMENT_SIZE = Evolution_parameters.get('TOURNAMENT_SIZE')
        self.PCROSS = Evolution_parameters.get('PCROSS')
        self.PMUT = Evolution_parameters.get('PMUT')
        self.POP_SIZE = Evolution_parameters.get('POP_SIZE')

    def init_population(self): # ramped half-and-half
        pop = []
        for md in range(self.MIN_DEPTH, self.MAX_DEPTH + 1):
            for i in range(int(self.POP_SIZE/30)):
                t = GPTree(Evolution_parameters)
                t.random_tree(grow = True, max_depth = md) # grow
                pop.append(t) 
            for i in range(int(self.POP_SIZE/30)):
                t = GPTree(Evolution_parameters)
                t.random_tree(grow = False, max_depth = md) # full
                pop.append(t)
        return pop

    def select_parent(self, population):
        parents = []
        if len(population) > 1:
            if len(population) % 2 == 0:
                for i in range(0, len(population), 2):
                    parents.append([population[i], population[i+1]])
            else:
                for i in range(0, len(population) - 1, 2):
                    parents.append([population[i], population[i+1]])
        else:
            parents.append(population * 2)
        return parents

    def crossover(self, parents):
        child1 = copy(parents[0])
        child2 = copy(parents[1])
        if random.random() < self.PCROSS:
            first = child1.scan_tree([randint(1, child1.size())], None)
            second = child2.scan_tree([randint(1, child2.size())], None)
            child1.scan_tree([randint(1, child1.size())], second)
            child2.scan_tree([randint(1, child2.size())], first)
        child1.mutation()
        child2.mutation()
        return [child1, child2]

    def selection(self, dict_profit): # select one individual using tournament selection
        list_indivivual = list(dict_profit.keys())
        tournament = random.sample(list_indivivual, self.TOURNAMENT_SIZE)
        tournament_fitnesses = [dict_profit[tournament[i]] for i in range(self.TOURNAMENT_SIZE)]
        return tournament[tournament_fitnesses.index(max(tournament_fitnesses))]

model = Cobweb(Cobweb_parameters)
tree = GPTree(Evolution_parameters)
Evolution = GP(Evolution_parameters)

def init_pop(Cobweb_parameters):
    raw_population= {} 
    for i in range(Cobweb_parameters['NUM_FIRMS']):
        raw_population[i] = Evolution.init_population()

    initial_population = []
    for i in range(Cobweb_parameters['NUM_FIRMS']):
        dic = {}
        for j in raw_population[i]:
            if j not in dic:
                dic[j] = 1
            else:
                dic[j] += 1
        initial_population.append(dic)

    competing_strategies = []
    for i in range(Cobweb_parameters['NUM_FIRMS']):
        firm_strategies = initial_population[i]
        competing_strategies.append(random.choice(list(firm_strategies.keys())))
    
    return initial_population, competing_strategies

def new_pop(Cobweb_parameters, initial_population):
    new_population = []
    for i in range(Cobweb_parameters['NUM_FIRMS']):
        current_population = copy(start_pop[i]) #dict(str: count)
        lst_children = []
        parents = Evolution.select_parent(list(current_population.keys()))
        for j in parents:
            lst_children += Evolution.crossover(j)
        for i in lst_children:
            if i in current_population:
                current_population[i] += 1
            else:
                current_population[i] = 1
        new_population.append(current_population)
    return new_population

initial_population, competing_strategies = init_pop(Cobweb_parameters)

list_price = []
update_terminals = []
list_expected_price = [{} for _ in range(Cobweb_parameters['NUM_FIRMS'])]

for gen in range(Evolution_parameters['GENERATIONS']):
      
    start_pop = initial_population #list(dict(str: count))
    start_competing_strategies = competing_strategies #list

    new_population = new_pop(Cobweb_parameters, start_pop)

    dict_quantity = {}
    for i in range(Cobweb_parameters['NUM_FIRMS']):
        firm_population = new_population[i]
        for j in list(firm_population.keys()):
            if j not in dict_quantity:
                dict_quantity[j] = model.quantity(j.compute_tree())

    list_competing_quantity = []
    for i in start_competing_strategies:
        list_competing_quantity.append(dict_quantity[i])
    
    price = round(model.market_price(list_competing_quantity), 3)
    list_price.append(price)

    TERMINALS = []
    update_terminals.append(price)
    if len(update_terminals) > Cobweb_parameters['H']:
        update_terminals.pop(0)
    TERMINALS += update_terminals

    next_population = []
    next_competing_strategies = []

    for firm in range(Cobweb_parameters['NUM_FIRMS']):
        
        population = new_population[firm]
        lst_stra = list(population.keys())

        firm_quantity = {}
        for i in list(lst_stra):
            firm_quantity[i] = dict_quantity[i]

        firm_cost = {}
        for i in list(lst_stra):
            firm_cost[i] = model.cost(firm_quantity[i])

        firm_profit = {}
        for i in list(lst_stra):
            firm_profit[i] = model.adjusted_profit(price, firm_quantity[i], firm_cost[i])

        ind_selection = []
        for i in range(Evolution_parameters['POP_SIZE']):
            ind_selection.append(Evolution.selection(firm_profit))

        survival = {}
        for i in ind_selection:
            if i not in lst_stra:
                survival[i] == 1
            else:
                survival[i] = population[i]

        survival_profit = {}
        for i in survival:
            survival_profit[i] = firm_profit[i]

        submitted_strategy = Evolution.selection(survival_profit)

        next_population.append(survival)
        next_competing_strategies.append(submitted_strategy)
        list_expected_price[firm][gen] = competing_strategies[firm].compute_tree()

    initial_population = next_population
    competing_strategies = next_competing_strategies

fig = plt.figure(figsize=(8,6), dpi=100)
ax = fig.add_subplot()
fig.subplots_adjust(top=0.7)
ax.annotate('rational expectation price', xy=(80, 1.12), xytext=(60, -1),
            arrowprops=dict(facecolor='black', shrink=0.005))
period = range(Evolution_parameters['GENERATIONS'])
plt.plot(period, list(list_expected_price[5].values()), label = 'expected price')
plt.plot(period, list_price, label = 'market price')
plt.xlabel('price')
plt.ylabel('period')
plt.legend(loc = 'upper right')
plt.show()