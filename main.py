from inspect import getclasstree
from pydoc import plain
import sys

class PropositionalLogic:
    # Accepts input string in text format
    # Returns a tuple of func and array of args (which can recurse)
    # example: ('implies', [('and', ['p', 'q', 'r']), ('or', ['p', 'q', 'r'])])
    def getClauses(self, input):
        input = input[1:]
        cur = input.split(" ", 1)[1]
        func = input.split(" ", 1)[0]
        args = []
        while (" " in cur):
            if (cur[0] == "("):
                args.append(self.getClauses(cur))
                parCount = 1
                index = 1
                while (parCount > 0):
                    if (cur[index] == ")"):
                        parCount -= 1
                    elif (cur[index] == "("):
                        parCount += 1
                    index += 1
                if (len(cur) > index and cur[index] == " "):
                    index += 1
                if (len(cur) > index and cur[index] == ")"):
                    return func, args
                cur = cur[index:]
            else:
                if (cur[0] == " "):
                    cur = cur[1:]
                    continue
                if (len(cur.split(" ", 1)[0]) > 1):
                    args.append(cur.split(" ", 1)[0][0])
                    return func, args
                args.append(cur.split(" ", 1)[0])
                cur = cur.split(" ", 1)[1]
        if (len(cur) > 0 and cur[0] != ")"):
            args.append(cur[0])
        return func, args

    # Modifies an array of variables found in clauses
    def getVariables(self, clauses, var):
        for arg in clauses[1]:
            if (isinstance(arg, tuple)):
                self.getVariables(arg, var)
            elif (not(arg in var)):
                var.append(arg)

    # Builds a table of 0 and 1 for rows 2^n
    def buildTable(self, n):
        if n < 1:
            return [[]]
        subtable = self.buildTable(n-1)
        return [ row + [v] for row in subtable for v in [0,1] ]

    # Recursively solves a formula
    # Returns a boolean
    def solve(self, clauses, dict):
        if (len(clauses) == 1):
            return dict[clauses]
        if (clauses[0] == "implies"):
            return (not self.solve(clauses[1][0], dict) or self.solve(clauses[1][1], dict))
        elif (clauses[0] == "neg" or clauses[0] == "not"):
            return not self.solve(clauses[1][0], dict)
        elif (clauses[0] == "or"):
            if (len(clauses[1]) > 2):
                return self.solve(clauses[1][0], dict) or self.solve(tuple([clauses[0], clauses[1][1:]]), dict)
            return self.solve(clauses[1][0], dict) or self.solve(clauses[1][1], dict)
        elif (clauses[0] == "and"):
            if (len(clauses[1]) > 2):
                return self.solve(clauses[1][0], dict) and self.solve(tuple([clauses[0], clauses[1][1:]]), dict)
            return self.solve(clauses[1][0], dict) and self.solve(clauses[1][1], dict)
        elif (clauses[0] == "iff"):
            return self.solve(clauses[1][0], dict) == self.solve(clauses[1][1], dict)
    
    # Prints the table
    def printTable(self, table, var, ans):
        print("Truth Table: ")
        for x in var:
            print(x, " ", end = " ")
        print("Formula")
        for i in range(len(table)):
            for x in table[i]:
                print(x, " ", end = " ")
            print(str(ans[i])[0])
        if (self.isValid(ans)):
            print("Valid")
        else:
            print("Not Valid")

    # Returns true or false given an ans array
    def isValid(self, ans):
        for res in ans:
            if not res:
                return False
        return True
        
    # Main method
    def main(self):
        file = open(sys.argv[1])
        input = file.read()
        if (input == ""):
            print("No input provided")
            return
        print("Formula =", input)
        clauses = self.getClauses(input)
        var = []
        self.getVariables(clauses, var)
        table = self.buildTable(len(var))
        ans = []
        for row in table:
            dict = {}
            for i in range(len(var)):
                dict[var[i]] = row[i]
            temp = self.solve(clauses, dict)
            if (temp == 0):
                temp = False
            elif (temp == 1):
                temp = True
            ans.append(temp)
        self.printTable(table, var, ans)
        
    
if __name__ == "__main__":
    pl = PropositionalLogic()
    pl.main()
