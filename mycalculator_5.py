"""
Nandini Chatterjee
BMI 503
Project 1 - Basic Calculator
"""

"""I imported sys, to provide access to any command-line arguments via the sys.argv. 
I imported re, Regular Expression Operators, used to find consecutive operators.
I imported traceback, it mimics the behavior of the Python interpreter when it prints a stack trace.

Class was made purely for organization.
For this project, my class is called mycalculator.
@staticmethod is a decorator it can be called from an unsubstantiated class object."""

"""The program is split up into several different parts.
In findConsecutiveOperator(exprn), it finds consecutive operators in alpha.
It searches for +, -, *, and /. If it sees any combination of these operators, it will raise a ValueError.
Traceback will where the expression stopped working, and where the error is in the expression."""

"""Then it moves onto clean_expression(exprn), where the code cleans up the expression.
At first, the code looks for patterns such as 4.3 or 44.3 or 444.34.
If it sees these patterns, it will create a new list. 
The for loop looks at each element in the new list, and converts each operand to floats.
The operators stay as a string. Line 85 is an If Statement for subtraction. 
The right hand side becomes a negative value and the operator changes to +.
Line 89 is an If Statement for division.
The right hand side becomes turns into its reciprocal, and the operator changes to *.
If it is /0, an error would be printed -- Print expressions change depending on the mode."""

"""evaluate(exprn) takes each operand and operations into a binary tree.
It goes through multiplications (& divisions), and additions (& subtractions).
isdisjoint is not overlapping the list of elements.
The set function gets all unique elements in the list.
It guarantees that the expression is just one number so it returns that number (which would be the final term)"""

"""Lastly, calculator(raw_exprn) sees that the user used appropriate characters & executes the expression.
InputValueDetect is a list form iterable, the map object can be cast onto a tuple or list.
If any part of the expression is not included in allowed_symbols, ValueError will be printed.
This will also check for decimal points. If there are more than one point, it will raise an error.
Next the code will find operators in the front of the expression.
If there is +, *, or / in the beginning, an error will show up.
If the user uses all the appropriate characters, it will move to the 'recursive' part.
First is the original input.
First is used to search for Consecutive Operators, beginning operators, and multiple decimals.
Intermediate is the result when first goes through clean_expression.
The result is after intermediate goes through evaluate.
"""

import sys  # provides access to any command-line arguments via the sys.argv
import re  # Regular Expression Operators- used to find consecutive operators
import traceback


class mycalculator:

    @staticmethod
    def findConsecutiveOperator(exprn):  # Look at line 16 for description
        m = re.search('(\+|\-|\*|\/|\.){2,}', exprn)
        if m:
            raise print(ValueError('{a} : There are consecutive operators!'.format(a=exprn)))

    @staticmethod
    def findInvalidDecimal(exprn):
        operands = re.split('[\*\+\-\/]',exprn)
        for x in operands:
            if x.count('.') > 1:
                raise ValueError('Invalid operand ' + x)
 
    @staticmethod
    def clean_expression(exprn):  # Look at line 26 for description
        global interactiveMode
        expression = exprn
        operators = {'+', '-', '*', '/'}  # List of the operators

        new_term = re.split('(\d+\.*\d*)', exprn)
        new_exp = list()
        for x in new_term:
            if x != '':
                new_exp.append(x)

        for i in range(len(new_exp)):
            if new_exp[i] not in operators:
                new_exp[i] = float(new_exp[i])
        expression = new_exp

        for i in range(len(expression)):
            if expression[i] in operators:
                if expression[i] == '-':
                    expression[i] = '+'
                    expression[i + 1] = -float(expression[i + 1])
                elif expression[i] == '/':
                    try:
                        expression[i] = '*'
                        expression[i + 1] = 1 / float(expression[i + 1])
                    except:
                        if expression[i + 1] == 0:
                            if interactiveMode:
                                print(ZeroDivisionError('Oops, you have a zero in the denominator!'))
                            else:
                                print('ILLEGAL!')
                        return expression
        return expression

    @staticmethod
    def evaluate(exprn):  # Look at Line 36 for description
        operators = {'+', '-', '*', '/'}
        if operators.isdisjoint(set(exprn)):
            return exprn
        elif '*' in exprn:
            expression = exprn
            for term in range(len(expression)):
                if expression[term] == '*':
                    result = expression[term - 1] * expression[term + 1]
                    expression[term] = result
                    expression[term - 1] = expression[term + 1] = None
                    expression = [term for term in expression if term is not None]
                    return mycalculator.evaluate(expression)
        elif '+' in exprn:
            expression = exprn
            for term in range(len(expression)):
                if expression[term] == '+':
                    result = expression[term - 1] + expression[term + 1]
                    expression[term] = result
                    expression[term - 1] = expression[term + 1] = None
                    expression = [term for term in expression if term is not None]
                    return mycalculator.evaluate(expression)

    @staticmethod
    def calculator(raw_exprn):  # Look at Line 36 for description
        allowed_symbols = '0123456789.+-*/'
        operators = {'+', '-', '*', '/'}
        try:
            #  Valid characters
            InputValueDetect = list(map(lambda x: x in allowed_symbols, raw_exprn))  # Look at Line 43 for description
            if False in InputValueDetect:
                if interactiveMode:
                    print(ValueError('Use only numbers and basic operators in ' + raw_exprn))
                else:
                    print('ILLEGAL!')
                return raw_exprn

            # Check for multiple decimals
            mycalculator.findInvalidDecimal(raw_exprn)

            #  Check for operators in the beginning
            if raw_exprn[:1] != '+' and raw_exprn[:1] != '*' and raw_exprn[:1] != '/':
                for i in range(1, len(raw_exprn) - 1):  # Checks for consecutive operators
                    if raw_exprn[i] in operators:
                        if raw_exprn[i] == '-':
                            if raw_exprn[i + 1] in operators:
                                break
                        else:
                            if raw_exprn[i - 1] in operators:
                                break
                            if raw_exprn[i + 1] in operators:
                                if raw_exprn[i + 1] != '-':
                                    break
            else:
                print('You are beginning with an operator!')

            first = raw_exprn
            mycalculator.findConsecutiveOperator(first)
            intermediate = mycalculator.clean_expression(first)
            result = mycalculator.evaluate(intermediate)

        except ValueError as err:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            print(err)

        return result[0]

# Interactive Mode versus Automatic Mode
'''If the length of the arguments is only one, then run the interactive mode which is set as TRUE.
While true will continue until it becomes false. 
Try to run alpha_raw is the input and alpha is the expression without intermediate tabs and spaces.
If the input is either END or end, the code will stop running; hence, 'break'.
Otherwise, the expression will go through all the previous staticmethods.
If the user doesn't end the program correctly, a KeyboardInterrupt will be printed.
'''

'''If there are more multiple arguments, then run the automatic mode, which is set as FALSE.
For every file in the argument, if it's not mycalculator.py, open the first text file.
fp.readline reads each line in the first text file.
The while loop, reads each line in the text file, and calculates the expression in each line.
line = fp.line moves onto the next expression (next line)
'''

interactiveMode = True if len(sys.argv) == 1 else False
if len(sys.argv) == 1:
    while True:
        try:
            alpha_raw = input('Please type an expression or type END to exit: \n')
            alpha = ''.join(alpha_raw.split())
            if alpha == 'END' or alpha == 'end':
                break
            else:
                print('RESULT: {x}'.format(x=mycalculator.calculator(alpha)))
        except:
            print(KeyboardInterrupt('You stopped the program incorrectly.'))

else:
    for file in sys.argv:
        if file != './mycalculator.py':
            with open(file) as fp:
                line = fp.readline()
                while line:
                    print('File: ', file, "\nExpression {} = {}\n".format(line, (mycalculator.calculator(line.strip()))))
                    line = fp.readline()
