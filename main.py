from inspect import getclasstree
from pydoc import plain
import sys

class PropositionalLogic:
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

    def getVariables(self, clauses, var):
        for arg in clauses[1]:
            if (isinstance(arg, tuple)):
                self.getVariables(arg, var)
            elif (not(arg in var)):
                var.append(arg)

    def buildTable(self, n):
        if n < 1:
            return [[]]
        subtable = self.buildTable(n-1)
        return [ row + [v] for row in subtable for v in [0,1] ]

    def solve(self, clauses, dict):
        if (len(clauses) == 1):
            return dict[clauses]
        if (clauses[0] == "implies"):
            return (not self.solve(clauses[1][0], dict) or self.solve(clauses[1][1], dict))
        elif (clauses[0] == "neg"):
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
        


    def main(self):
        file = open(sys.argv[1])
        input = file.read()
        if (input == ""):
            print("No input provided")
            return
        clauses = self.getClauses(input)
        print (clauses)
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
        print(table)
        print(ans)
        
    
if __name__ == "__main__":
    pl = PropositionalLogic()
    pl.main()
