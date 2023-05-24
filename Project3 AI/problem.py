from sys import exit

class Problem:
    """
    This class is used to create a problem instance from 3 input files and provides methods
    to prepare the problem to be solved.
    """
    def __init__(self, attr, constr, pref):
        """
        This constructor creates a Problem instance and accepts 3 files containing data
        relevant to the problem.
        :param attr:    The file containing attributes formatted as pairs of items.
        :param constr:  The file containing constraints to exclude certain pairs of items.
        :param pref:    The file containing preferences that tells how much a user likes
                        a pair of items.
        """
        self.attributesFile = attr
        self.constraintsFile = constr
        self.preferencesFile = pref
        self.attributes = {}                # dict for converting items to #'s
        self.rev_attributes = {}            # dict for converting #'s to items
        self.numAttributes = 0              # number of boolean variables
        self.constraints = []
        self.numConstraints = 0
        self.preferences = []               # preferences = [[preference, penalty/tolerance],[...],[...]]

    def getAttributes(self):
        """
        This function parses the attributes file for pairs of items and gives them a number
        variable based on the line they come from. In this pair, the first item is represented
        as positive and the second item negative. These number variables are stored in a dictionary
        with the names of the items as keys. A reverse dictionary is created as well just in case.
        :return: None
        """
        try:
            f = open(self.attributesFile, 'r')
        except IOError:
            print('cannot open', self.attributesFile)
        try:
            for line in f:
                line = line.replace(',', '').strip('\n').split(' ')
                self.numAttributes += 1
                self.attributes[line[1]] = self.numAttributes
                self.attributes[line[2]] = self.numAttributes * -1
                self.rev_attributes[self.numAttributes] = line[1]
                self.rev_attributes[self.numAttributes * -1] = line[2]
        except Exception:
            print("Error: attributes file not formatted correctly")
            exit()
        f.close()

    def getConstraints(self):
        """
        This function parses the constraints file for pairs of items, converts them to their variable
        representation, formats them for clasp, and adds them to a list.
        :return: None
        """
        try:
            f = open(self.constraintsFile, 'r')
        except IOError:
            print('cannot open', self.constraintsFile)
        try:
            for line in f:
                line = line.replace('NOT ', '').replace('OR ', '').strip('\n').split(' ')
                self.numConstraints += 1
                self.constraints.append(str(self.attributes[line[0]] * -1)+' '+str(self.attributes[line[1]] * -1)+' 0')
        except Exception:
            print("Error: constraints file not formatted correctly\n")
            exit()
        f.close()

    def getPreferences(self):
        """
        This function parses the preferences file for pairs of items and their preference
        number, formats them for clasp, and adds them to a list.
        :return: None
        """
        try:
            f = open(self.preferencesFile, 'r')
        except IOError:
            print('cannot open', self.preferencesFile)
        try:
            for line in f:
                line = line.strip('\n').split(', ')
                line = [line[0].replace('OR ', '').split(' '), line[1]]
                clause = ''
                for element in line[0]:
                    if element == 'AND':
                        clause += '0\n'
                        continue
                    clause += str(self.attributes[element]) + ' '
                self.preferences.append([clause + '0', line[1]])
        except Exception:
            print("Error: preferences file not formatted correctly")
            exit()
        f.close()

    def writeConstraints(self):
        """
        This function writes the previously collected constraints and writes them to a file.
        This file will be used by the Solver to compute feasible models.
        :return:    None
        """
        try:
            f = open('clasp-input.txt', 'w')
        except IOError:
            print('cannot create clasp-input.txt')
        f.write('p cnf ' + str(self.numAttributes) + ' ' + str(self.numConstraints) + '\n')
        for constraint in self.constraints:
            f.write(constraint + '\n')
        f.close()