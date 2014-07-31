# Jialun Zhang
# Project PICOBOT!
# Dec 5th, 2013

import random

HEIGHT = 25
WIDTH = 25
NUMSTATES = 5

class Program:
    def __init__(self):
        '''the constructor for objects of class Program'''
        
        self.rules = {}

    def __repr__(self):
        '''returns a string representation for an object of type Board'''
        
        keylist = self.rules.keys()
        sortlist = sorted(keylist)
        s = ''
        
        for i in range(len(keylist)):
            s += str(sortlist[i][0]) + ' '
            s += sortlist[i][1] + ' '
            s += '->' + ' '
            s += self.rules[sortlist[i]][0] +' '
            s += str(self.rules[sortlist[i]][1])
            s += '\n'
                            
        return s
            

    def randomize(self):
        '''generates random rules for 45 situations and adds them to the
           dictionary'''
        
        sur = ['xxxx','Nxxx','NExx','NxWx','xxxS','xExS','xxWS','xExx','xxWx']
        directions = ['N','E','W','S']
        situations = []
        PossibleMoves = []
        
        # this loop creates a list of tuples: (state, surroundings)
        for i in range(5):
            situations += [(i,pattern) for pattern in sur]

        
        # this loop creates another list of tuples, indicating the
        # next move: (movedirection,state)
        for i in range(5):
            PossibleMoves += [(face,i) for face in directions]
            
        # this loop generates random rules for each situation and adds them to the dictionary.
        for i in range(len(situations)):
            movedir = random.choice(PossibleMoves)
            while movedir[0] in situations[i][1]:
                movedir = random.choice(PossibleMoves)
            
            self.rules[situations[i]] = movedir

    def getMove(self,state,surroundings):
        '''takes an integer state and a surroundings ("xExx") as input
           and returns a tuple that contains the next move and the
           new state'''

        situations = (state, surroundings)
        return self.rules[situations]


    def mutate(self):
        '''this method chooses a single rule from self.rule and it should change
           the value(the move and new state) for that rule.'''

        PossibleMoves = []
        directions = ['N','E','W','S']
        
        mutate_pattern = random.choice(self.rules.keys())
        

        for i in range(5):
            PossibleMoves += [(face,i) for face in directions]
    

        movedir = random.choice(PossibleMoves)
        
        while movedir[0] in mutate_pattern[1]:
            movedir = random.choice(PossibleMoves)

        self.rules[mutate_pattern] = movedir


    def crossover(self,other):
        '''this method takes an "other" object of type Program as input. It
           should return a new "offspring" Program that contains some of the
           rules from self and the rest from other'''

        newRules = Program()
        
        parent = self.rules
        cross_overstate = random.choice(range(5))
        

        for i in range(45):
            if parent.keys()[i][0] <= cross_overstate:
                newRules.rules[parent.keys()[i]] = parent[parent.keys()[i]]

            if other.rules.keys()[i][0] > cross_overstate:
                newRules.rules[other.rules.keys()[i]] = other.rules[other.rules.keys()[i]]

        return newRules
    
        

        

        

        
class World:
    '''picobot's humble home'''

    def __init__(self,initial_row,initial_col,program):
        '''the constructor of objects of class World'''
        self.prow = initial_row
        self.pcol = initial_col
        self.state = 0
        self.prog = program
        room = [['W']+[' ']*WIDTH+['W'] for x in range(HEIGHT)]
        self.room = [['W']*(WIDTH+2)] + room + [['W']*(WIDTH+2)]
        self.visited = [] # a list of tuples indicating the positions that picobot has visited

    def __repr__(self):
        '''returns a string representation of the object of class World'''
        room = 'W'*(WIDTH+3)
        room += '\n'

        for row in range(HEIGHT):
            for col in range(WIDTH+2):
                
                if col == 0:
                    room += 'W'

                if (row,col-1) == (self.prow,self.pcol):
                    room += 'P'
                    
                
                if (row,col-1) in self.visited and \
                   (row,col-1) != (self.prow,self.pcol):
                    room += 'O'
                    
                
                if col == 26:
                    room += 'W'
                    room += '\n'

                if col !=0 and \
                   (row,col-1)!=(self.prow,self.pcol)and \
                   (row,col-1) not in self.visited and col !=26:
                    room += ' '

        room += 'W'*(WIDTH+3)                   
        return room



    def getCurrentSurroundings(self):
        '''returns a surroundings string such as "xExx", for the current
           position of Picobot.'''

        if self.prow == 0:
            if self.pcol == 0:
                return 'NxWx'
            if self.pcol == 24:
                return 'NExx'
            else:
                return 'Nxxx'

        elif self.prow == 24:
            if self.pcol == 0:
                return 'xxWS'
            if self.pcol == 24:
                return 'xExS'
            else:
                return 'xxxS'

        elif self.pcol == 0:
            return 'xxWx'

        elif self.pcol == 24:
            return 'xExx'

        else:
            return 'xxxx'


    def step(self):
        '''this method moves the Picobot one step, updates the self.room
           and updates the state, row, and col of Picobot, using the
           program self.prog. Doesn't return anything'''

        program = self.prog
        state = self.state
        surroundings = self.getCurrentSurroundings()
        nextMove = program.getMove(state,surroundings)

        self.state = nextMove[1]

        if nextMove[0] == 'N':
            self.prow += -1
        if nextMove[0] == 'E':
            self.pcol += 1
        if nextMove[0] == 'W':
            self.pcol += -1
        if nextMove[0] == 'S':
            self.prow += 1


    def run(self,steps):
        '''takes the number of steps as input. The run method should
           execute that number of steps using the step method. This
           is a Picobot simulator!'''

        
        
        for i in range(steps):
            if (self.prow, self.pcol) not in self.visited:
                self.visited += [(self.prow,self.pcol)]
            # the previous line creates a list of tuples containing
            # the visited positions of Picobot

            self.step()
            

    def fractionVisitedCells(self):
        '''this is the method that returns the floating-point fraction of
           cells in self.room that are marked as visited.'''

        visitedCells = len(self.visited)

        if float(visitedCells)/625 > 1:
            print self.visited

        return float(visitedCells)/625



# the construction is (almost) complete!

def random_programs(size):
    '''takes as input a population size and returns a population (a python
       list) of that many random Picobot programs.'''

    program = Program()
    program_list = []

    for i in range(size):
        program.randomize()
        program_list += [program]

    return program_list


def evaluateFitness(program, trials, steps):
    '''this function takes as input a Picobot program, a positive integer trials
       that indicates the number of random starting points that are to be
       tested, and a positive integer steps that indicates how many steps of
       the simulation each trial should be allowed to take. The function returns
       a fitness that is the fraction of the cells visited by this Picobot program,
       averaged over the give number of trials.'''

    totalFraction = 0

    for i in range(trials):
        startingRow = random.choice(range(25))
        startingCol = random.choice(range(25))

        picobot = World(startingRow, startingCol, program)
        picobot.run(steps)

        totalFraction += picobot.fractionVisitedCells()


    Fraction = totalFraction/trials
##    print Fraction
    return Fraction



def nextGen(currentGen):
    '''takes in the current generation of programs and
       generates the next generation of Picobot programs'''

    trials = 15 # the number of trials that each picobot program runs
    steps = 800 # the number of steps that each picobot program runs
    listofFitness = []
    listofPrograms = currentGen #the current population of programs
    popsize = len(currentGen)
    survival_rate = 0.1 #the percentage of surviving programs
    mutation_rate = 0.8 #the percentage of surviving programs that mutates
    survival_population = survival_rate * popsize
    survivor_programs = [] # a list of surviving programs
    crossover_programs = []
    nextGeneration = [] # the list of the next generation of programs
    total_fitness = 0 # the total fitness of one generation of programs
    random_index = 0

    
    for i in range(popsize):
        # print evaluateFitness(listofPrograms[i],trials,1000)
        fitness = (evaluateFitness(listofPrograms[i],trials,1000), listofPrograms[i])
        listofFitness += [fitness]

    sortedFitness = sorted(listofFitness)
    survivor_list = sortedFitness[popsize-int(popsize*survival_rate) : popsize ]
    

    for i in range(popsize):
        total_fitness += sortedFitness[i][0]
    

    average_fitness = total_fitness/popsize
    best_fitness = sortedFitness[-1][0]
    bestProgram = sortedFitness[-1][1]
    
    
    # print sortedFitness[-1]

    print "Fitness is measured using", trials, "random trials running for", steps, "steps"
    print "Average fitness:", average_fitness,"Best fitness:",best_fitness
    print "\n"

    
    for i in range(len(survivor_list)):
        survivor_programs += [survivor_list[i][1]]
    

    for i in range(len(survivor_programs)):
        for j in range(len(survivor_programs)):
            if i != j:
                crossover_programs += [survivor_programs[i].crossover(survivor_programs[j])]
                

    # thus, crossover_programs give us a list of n*(n-1) new programs, where n is the number
    # of surviving programs. Now we randomly choose mutation_rate of these programs to
    # mutate
    

    

    number_of_mutations = int(len(crossover_programs)*mutation_rate)

    for i in range(number_of_mutations):
        random_index = random.choice(range(len(crossover_programs)))
        crossover_programs[random_index].mutate()

    # the crossover_programs have randomly mutated. We now randomly choose popsize programs
    # from this list of crossovered and mutated programs

    for i in range(popsize):
        nextGeneration += [random.choice(crossover_programs)]

    return [nextGeneration, bestProgram]

    

def GA(popsize, numgens):
    '''this functions creates popsize random Picobot programs as the initial population.
       Then it 1. evaluate the fitness of all of those programs. 2. extract
       the subset of the most-fit programs that will survive 3. create a new
       population(of the same size as the original) by using crossover and
       mutate methods on the most-fit programs from the previous population.
       then, with repeat the whole process. At the end, the function returns
       the best program from the last generation'''

    currentGen = random_programs(popsize)
    
    
    for i in range(numgens):
        print "Generation",i+1
        
        [currentGen, bestfit] = nextGen(currentGen)

    return bestfit

    

    

    
