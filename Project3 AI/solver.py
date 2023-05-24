from os import system, remove
from random import randint
from operator import itemgetter
from sys import stdout, exit

class Solver:
    """
    This class performs calculations on the problem it is constructed with. It contains
    functions to compute the feasible models w.r.t the constraints, the preferences of
    those models, the relationship between two random models, an optimal model, and all
    optimal models. There is also a toString function which is used to print the
    information gathered from the functions mentioned above.
    """
    def __init__(self, problem):
        """
        This function constructs a Solver object to work on an existing Problem object.
        It inherits the data structures of the Problem object and uses them in some
        of its own calculations.
        :param problem:     The problem object with information to work with
        """
        self.problem = problem
        self.models = []
        self.numModels = 0
        self.modelsNprefs = []
        self.optimalModel = None
        self.optimalModels = []

    def runClasp(self):
        """
        This function runs clasp on an input file containing formatted constraints
        data created by the Problem class. The results of this computation are stored
        in a file.
        :return:    None
        """
        system("clasp clasp-input.txt -n 0 > clasp-output.txt")
        remove("clasp-input.txt")

    def getFeasibleModels(self):
        """
        This function parses the results of the clasp computation which are stored in
        a file. It looks for lines containing models and adds them to a list.
        :return:    None
        """
        # get the feasible models w.r.t constraints
        try:
            f = open('clasp-output.txt', 'r')
        except IOError:
            print ('error opening clasp-output.txt')
        for line in f:
            if line[0] == 'v':
                self.models.append(line.replace('v ', '').strip('0\n'))
        f.close()
        remove("clasp-output.txt")
        # determine how many there were
        self.numModels = len(self.models)
        if self.numModels == 0:
            print ("There are no meals available w.r.t. the constraints given.")
            exit()              # exit because no point in further calculations

    def whichLogic(self):
        """
        This function looks at an object in the preferences list and determines
        which preference logic (penalty or preference) to use. A preference value
        greater than or equal to one corresponds to penalty logic and a value less
        than one corresponds to possibilistic logic.
        :return:    None
        """
        # Which kind of logic? (Possibilistic or Penalty)
        if float(self.problem.preferences[0][1]) >= 1:
            self.penaltyLogic = True
            self.penalties = []              # list of penalties
        else:
            self.penaltyLogic = False        # propositional logic used
            self.tolerances = []             # list of tolerance values

    def calculatePreferences(self):
        """
        This function calculates the total preference for each model w.r.t all
        of the preferences. It writes the preference to a file along with the
        truth assignment of the model and runs clasp in it, which determines
        whether or not that model satisfies the preference. The output of the
        clasp computation is stored in another file which is parsed for
        unsatisfied preferences. With all the unsatisfied preferences considered,
        the total preference for a model is deduced. The model and this preference
        are finally stored in the modelsNprefs list.
        :return:    None
        """
        # calculate preference for feasible models
        numCalculations = float(self.numModels * len(self.problem.preferences))
        numDone = 0
        for model in self.models:
            for preference in self.problem.preferences:
                # write a claspable file with preference clauses and model's truth assignment literals
                try:
                    f = open('preference-input.txt', 'w')
                except IOError:
                    print ('cannot create preference-input.txt')
                f.write('p cnf '+str(self.problem.numAttributes)+' 0\n')     # 0 for number of clauses b/c it doesn't seem to matter
                f.write(preference[0]+'\n')
                f.write(model.replace(' ', ' 0\n'))
                f.close()
                # run clasp on it and capture results
                system("clasp preference-input.txt -n 0 > preference-output.txt")
                # check if satisfiable
                try:
                    f = open('preference-output.txt', 'r')
                except IOError:
                    print ('cannot open preference-output.txt')
                for line in f:
                    if line[0] == 's':
                        if line[2] == 'U':
                            # implement penalty
                            if self.penaltyLogic:
                                self.penalties.append(int(preference[1]))
                            else:
                                self.tolerances.append(1 - float(preference[1]))
                f.close()
                # inform user of calculation progress
                numDone += 1
                percentage = (float(numDone)/numCalculations) * 50
                stdout.write('\r')
                stdout.write("Calculating [%-50s] %d%%" % ('='*int(percentage), percentage * 2))
                stdout.flush()
            # calculate the relevant penalty or tolerance for the model
            if self.penaltyLogic:
                penaltySum = 0
                for penalty in self.penalties:
                    penaltySum += penalty
                model = (model, penaltySum)
                self.penalties = []
            else:
                minTolerance = 1
                for tolerance in self.tolerances:
                    if tolerance < minTolerance:
                        minTolerance = tolerance
                model = (model, minTolerance)
                self.tolerances = []
            # add updated model with penalty/tolerance to list
            self.modelsNprefs.append(model)
        remove("preference-input.txt")
        remove("preference-output.txt")

    def twoRandomModels(self):
        """
        This function selects two random models from the modelsNprefs list
        and stores them. The actual comparison takes place in the toString()
        function which determines whether one is preferred to the other or
        if they are equally preferred.
        :return:    None
        """

        self.randModelOne = self.modelsNprefs[randint(0, self.numModels - 1)]
        self.randModelTwo = self.modelsNprefs[randint(0, self.numModels - 1)]
        while self.randModelTwo == self.randModelOne:
            self.randModelTwo = self.modelsNprefs[randint(0, self.numModels - 1)]

    def optimization(self):
        """
        This function scans all of the models and preferences in modelsNprefs
        and keeps track of the model with the best preference. This model is
        an optimal model and is stored in variable called optimalModel.
        :return:    None
        """
        minPenalty = 999999999             # will become the optimal penalty
        maxTolerance = 0.0                 # will become the optimal tolerance
        for model,pref in self.modelsNprefs:
            if (self.penaltyLogic):
                if pref < minPenalty:
                    minPenalty = pref
                    self.optimalModel = (model, pref)
            else:
                if pref > maxTolerance:
                    maxTolerance = pref
                    self.optimalModel = (model, pref)

    def omniOptimization(self):
        """
        This function sorts the list of modelsNprefs based on the preferences. It
        is sorted from low to high if penalty logic is used and from high to low if
        possibilistic logic is used. It then scans the sorted list and appends the
        objects it sees to the optimalModels list until it encounters a model with a
        preference different from the previous.
        :return:    None
        """
        i = 0
        if self.penaltyLogic:
            self.modelsNprefs.sort(key=itemgetter(1))
            bestPenalty = self.modelsNprefs[0][1]
            while self.modelsNprefs[i][1] == bestPenalty:
                self.optimalModels.append(self.modelsNprefs[i])
                i += 1
        else:
            self.modelsNprefs.sort(key=itemgetter(1), reverse=True)
            bestTolerance = self.modelsNprefs[0][1]
            while self.modelsNprefs[i][1] == bestTolerance:
                self.optimalModels.append(self.modelsNprefs[i])
                i += 1

    def toString(self):
        """
        This function gathers data computed by the Solver and prints it in a
        report where the number variables of models are converted to their
        descriptors as necessary. The data undergoes formatting for user
        readability.
        :return:    None
        """
        print("\n\nProgram Report")
        print("------------------------")

        # number of models
        print("Number of models: "+ str(2 ** self.problem.numAttributes))

        # number of feasible models
        print("Number of feasible models w.r.t constraints: "+str(self.numModels))

        # the logic used to calculate preference
        if (self.penaltyLogic):
            print("\nPenalty logic used to calculate preferences")
        else:
            print("\nPossibilistic logic used to calculate preferences")

        # the feasible models and their preference
        print("\nFeasible models and their preference: ")
        for model,pref in self.modelsNprefs:
            print "Model: ( ",
            model = model.strip(" ").split(" ")
            for item in model:
                print self.problem.rev_attributes[int(item)] + " ",
            print ") has preference: " + str(pref)

        # two random models and how their preferences compare
        randModelOne, prefOne = self.randModelOne
        randModelTwo, prefTwo = self.randModelTwo
        print"\nRandom model #1:\t( ",
        randModelOne = randModelOne.strip(" ").split(" ")
        for item in randModelOne:
            print self.problem.rev_attributes[int(item)] + " ",
        print") has preference: "+str(prefOne)
        randModelTwo = randModelTwo.strip(" ").split(" ")
        print"Random model #2:\t( ",
        for item in randModelTwo:
            print self.problem.rev_attributes[int(item)] + " ",
        print") has preference: "+str(prefTwo)
        if self.penaltyLogic:               # if penalty logic
            if prefOne < prefTwo:
                print("Model #1 is strictly better than model #2")
            elif prefOne > prefTwo:
                print("Model #2 is strictly better than model #1")
            else:
                print("Model #1 and model #2 are equivalent")
        else:                               # if possibilistic logic
            if prefOne > prefTwo:
                print("Model #1 is strictly better than model #2")
            elif prefOne < prefTwo:
                print("Model #2 is strictly better than model #1")
            else:
                print("Model #1 and model #2 are equivalent")

        # A signle optimal model
        print"\nAn optimal model:\nModel: ( ",
        model,pref = self.optimalModel
        model = model.strip(" ").split(" ")
        for item in model:
            print self.problem.rev_attributes[int(item)] + " ",
        print ") has preference: " + str(pref)

        # all optimal models
        print ("\nOptimal models: ")
        for model,pref in self.optimalModels:
            model = model.strip(" ").split(" ")
            print "Model: (",
            for item in model:
                print self.problem.rev_attributes[int(item)] + " ",
            print ") has preference: " + str(pref)