"""Class was made purely for organization. @staticmethod is a decorator it can be called from an uninstantiated class object.
For example, in @staticmethod, no cls parameter is passed (no self, either). The program is split up into three different part.
 The beginning is actually at the very end of the code, it begins with alpha = input... Then it moves onto clean_expression(exprn) and then
 evaluate(exprn). def clean_expression(exprn) basically cleans up the expression. It looks for negative values, subtraction and divison operators.
It also checks if there is no 0 as a denominator while dividing operands."""

import sys # provides access to any command-line arguments via the sys.argv
import re

class mycalculator:
    @staticmethod
    def clean_expression(exprn):
        expression = exprn
        operators = {'+', '-', '*', '/'}  # List of the operators
        for i in range(len(expression)):
            if (expression[i] in operators) and expression[i + 1] == '-': #This is for negative values
                expression[i + 1] = None
                expression[i + 2] = -float(expression[i + 2])
        expression = [term for term in expression if term != None] # != not equivalent to None
        for i in range(len(expression)):
            if expression[i] not in operators:  # goes through entire expression and checks for any term not in operators, string to float
                expression[i] = float(expression[i])
        for i in range(len(expression)):
            if expression[i] in operators:  # If in the operators, it stays in string mode
                if expression[i] == '-': # If Statement for subtraction
                    expression[i] = '+'
                    expression[i + 1] = -float(
                        expression[i + 1])  # If term in operators, negative float for second operand and operator changes to addition
                elif expression[i] == '/': # If Statement for division
                    try:
                        expression[i] = '*'
                        expression[i + 1] = 1 / float(expression[i + 1]) # If term in operators, replace with * and change second operand with its reciprocal
                    except:
                        if expression[i + 1] == 0:
                            print(ZeroDivisionError('Ooops, you have a zero in the denominator!'))  # the program will crash if this is not there
        return expression

    @staticmethod
    def evaluate(exprn):
        """This @staticmethod takes each operand and operations into a binary tree. It goes through exponents, multiplications, and additions.
        Remember that division falls under the category of multiplication and subtraction falls under the category of addition. """

        operators = {'+', '-', '*', '/'}

        # isdisjoint = not overlapping, list of elements
        # set function- of all the unique terms in the list
        # guaranteeing that the expression is just one number so it returns that number (which would be the final term)

        if operators.isdisjoint(set(exprn)):
            return exprn
        elif '*' in exprn:
            expression = exprn
            for term in range(len(expression)):
                if expression[term] == '*':
                    result = expression[term - 1] * expression[term + 1]
                    expression[term] = result
                    expression[term - 1] = expression[term + 1] = None
                    expression = [term for term in expression if term != None]
                    return mycalculator.evaluate(expression)
        elif '+' in exprn:
            expression = exprn
            for term in range(len(expression)):
                if expression[term] == '+':
                    result = expression[term - 1] + expression[term + 1]
                    expression[term] = result
                    expression[term - 1] = expression[term + 1] = None
                    expression = [term for term in expression if term != None]
                    return mycalculator.evaluate(expression)

    @staticmethod
    def calculator(raw_exprn):
        """ This @staticmethod, calculator (raw_exprn) checks to make sure that the user used appropriate characters, if not, it will shows an error.
        If the user uses all the appropriate characters, it will move to the else statement; first each element will be split and placed into a list.
        Then the expression will move through the previous steps. """

        allowed_symbols = '0123456789.+-*/' # there needs to be a space during the input
        InputValueDetect = list(map(lambda x: x in allowed_symbols, raw_exprn)) # List form iterable, the map object can be cast onto a tuple or list
        c = int(0)
        try:
            a = raw_exprn.split(' ') # Splits each of the elements (operands and operators)
            b = mycalculator.clean_expression(a) # Goes through the first method
            c = mycalculator.evaluate(b) # Goes through the second method
        except:
            if False in InputValueDetect:  # the returns will not be a number, it will be True/False
                print(ValueError('Bad Values! Please use only numbers and basic operators!'))  # Flags an error
                return(alpha)
        return c[0]

if len(sys.argv) == 1:
    while True: #Go on infinitely until False
        alpha = input('Please type an expression or type END to exit: \n')
        #re.sub('\s+', '', alpha)
        if alpha == 'END' or alpha == 'end':
            break
        else:
             print(mycalculator.calculator(alpha))
else: # multiple arguments
    for file in sys.argv:
        if file != './mycalculator.py': # so the program doesn't pick itself
            with open(file) as fp:  # opens the text file
                line = fp.readline()  # reads each expression in each line in the text file
                while line:  # creates a while loop for each file
                    print('File: ',file, "\nExpression {} = {}".format(line,(mycalculator.calculator(line.strip()))))  # prints out the value for an expression in a line
                    line = fp.readline()  # moves on to the next expression, next linex