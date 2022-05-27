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

    def CNF(self, clauses):
        # Step 1
        clauses = self.iff(clauses)
        # Step 2
        clauses = self.implies(clauses)
        # Step 3
        clauses = self.neg(clauses)
        # Step 4
        clauses = self.myOr(clauses)
        # Cleaning
        clauses = self.combineAndOr(clauses)
        # Output
        self.outputCNF(clauses)
        return clauses

    def iff(self, clauses):
        # change clauses to list from tuple so can modify
        temp = list(clauses)
        for i in range(len(clauses[1])):
            if (isinstance(clauses[1][i], tuple)):
                temp[1][i] = self.iff(temp[1][i])
        if (clauses[0] == "iff"):
            arg1 = clauses[1][0]
            arg2 = clauses[1][1]
            # change iff to and then add implies to each
            temp[0] = "and"
            # add implies for first arg
            tempList = []
            tempList.append(arg1)
            tempList.append(arg2)
            tempTuple = ("implies", tempList)
            temp[1][0] = tempTuple
            # add implies for second arg
            tempList = []
            tempList.append(arg2)
            tempList.append(arg1)
            tempTuple = ("implies", tempList)
            temp[1][1] = tempTuple
        clauses = tuple(temp)
        return clauses

    def implies(self, clauses):
        # change clauses to list from tuple so can modify
        temp = list(clauses)
        for i in range(len(clauses[1])):
            if (isinstance(clauses[1][i], tuple)):
                temp[1][i] = self.implies(temp[1][i])
        if (clauses[0] == "implies"):
            # change implies to or
            temp[0] = "or"
            # add not in first arg
            tempList = []
            tempList.append(clauses[1][0])
            tempTuple = ("not", tempList)
            temp[1][0] = tempTuple
        clauses = tuple(temp)
        return clauses

    def neg(self, clauses):
        # change clauses to list from tuple so can modify
        temp = list(clauses)
        if (clauses[0] == "neg" or clauses[0] == "not"):
            if (isinstance(clauses[1][0], tuple)):
                if (clauses[1][0][0] == "neg" or clauses[1][0][0] == "not"):
                    temp = clauses[1][0][1][0]
                    return temp
                elif (clauses[1][0][0] == "and" or clauses[1][0][0] == "or"):
                    # change not to and/or then add not to each
                    if (clauses[1][0][0] == "and"):
                        temp[0] = "or"
                    else:
                        temp[0] = "and"

                    outerList = []
                    for i in range(len(clauses[1][0][1])):
                        # add not for first arg
                        tempList = []
                        tempList.append(clauses[1][0][1][i])
                        tempTuple = ("not", tempList)
                        outerList.append(tempTuple)
                    temp[1] = outerList
        clauses = tuple(temp)
        for i in range(len(clauses[1])):
            if (isinstance(clauses[1][i], tuple)):
                temp[1][i] = self.neg(temp[1][i])
        return clauses

    # distribution law
    def myOr(self, clauses):
        if(type(clauses) == str):
            return clauses
        # change clauses to list from tuple so can modify
        temp = list(clauses)
        for i in range(len(clauses[1])):
            if (isinstance(clauses[1][i], tuple)):
                temp[1][i] = self.myOr(temp[1][i])
        if (clauses[0] == "or"):
            i = 0
            size = len(temp[1])
            outerList = []
            while(i < size):
                if (i == size - 1):
                    outerList.append(clauses[1][i])
                elif (isinstance(clauses[1][i], str) and isinstance(clauses[1][i + 1], tuple)):
                    if (clauses[1][i + 1][0] == "and"):
                        arg1 = clauses[1][i]
                        temp[0] = "and"

                        outerList = []
                        # add not for first arg
                        for j in range(len(clauses[1][i + 1][1])):
                            tempList = []
                            tempList.append(arg1)
                            tempList.append(clauses[1][i + 1][1][j])
                            tempTuple = ("or", tempList)
                            outerList.append(tempTuple)
                        i += 1
                    else:
                        outerList.append(clauses[1][i])
                
                # if order is reversed
                elif (isinstance(clauses[1][i + 1], str) and isinstance(clauses[1][i], tuple)):
                    if (clauses[1][i][0] == "and"):
                        arg1 = clauses[1][i + 1]
                        # change or to and then add or arg1 to each
                        temp[0] = "and"

                        # add not for first arg
                        for j in range(len(clauses[1][i][1])):
                            tempList = []
                            tempList.append(clauses[1][i][1][j])
                            tempList.append(arg1)
                            tempTuple = ("or", tempList)
                            outerList.append(tempTuple)
                        i += 1
                    else:
                        outerList.append(clauses[1][i])

                elif (isinstance(clauses[1][i], tuple) and isinstance(clauses[1][i + 1], tuple)):
                    if (clauses[1][i][0] == "and" or clauses[1][i + 1][0] == "and"):
                        index1 = i
                        index2 = i + 1
                        index3 = i + 2
                        if(clauses[1][i + 1][0] == "and"):
                            index1 += 1
                            index2 -= 1
                        if(size < 3 or len(clauses[1][2]) == 1):
                            index3 = index2
                        for k in range(len(clauses[1][index1][1])):
                            arg1 = clauses[1][index1][1][k]
                            temp[0] = "and"

                            # add not for first arg
                            if(clauses[1][index2][0] == "or"):
                                tempList = [arg1]
                                for j2 in range(len(clauses[1][index2][1])):
                                    tempList.append(clauses[1][index2][1][j2])
                                tempTuple = ("or", tempList)
                                outerList.append(tempTuple)
                            else:
                                for j in range(len(clauses[1][index2][1])):
                                    for k3 in range(len(clauses[1][index3][1])):
                                        tempList = [arg1]
                                        for k2 in range(len(clauses[1])):
                                            if (k2 == index1):
                                                None
                                            elif (len(clauses[1][k2]) == 1):
                                                tempList.append(clauses[1][k2])
                                            else:
                                                tempList.append(clauses[1][k2][1][k3])
                                    
                                        tempTuple = ("or", tempList)
                                        outerList.append(tempTuple)
                            
                        i += 1
                    else:
                        outerList.append(clauses[1][i])
                else:
                    outerList.append(clauses[1][i])
                i += 1
            temp[1] = outerList

        # if and is first clause
        elif (clauses[0] == "and"):
            i = 0
            size = len(temp[1])
            outerList = []
            while(i < size):
                if (i == size - 1):
                    outerList.append(clauses[1][i])
                elif (isinstance(clauses[1][i], str) and isinstance(clauses[1][i + 1], tuple)):
                    if (clauses[1][i + 1][0] == "or"):
                        arg1 = clauses[1][i]
                        temp[0] = "or"

                        outerList = []
                        # add not for first arg
                        for j in range(len(clauses[1][i + 1][1])):
                            tempList = []
                            tempList.append(arg1)
                            tempList.append(clauses[1][i + 1][1][j])
                            tempTuple = ("and", tempList)
                            outerList.append(tempTuple)
                        i += 1
                    else:
                        outerList.append(clauses[1][i])
                
                # if order is reversed
                elif (isinstance(clauses[1][i + 1], str) and isinstance(clauses[1][i], tuple)):
                    if (clauses[1][i][0] == "or"):
                        arg1 = clauses[1][i + 1]
                        # change and to or then add and arg1 to each
                        temp[0] = "or"

                        # add not for first arg
                        for j in range(len(clauses[1][i][1])):
                            tempList = []
                            tempList.append(clauses[1][i][1][j])
                            tempList.append(arg1)
                            tempTuple = ("or", tempList)
                            outerList.append(tempTuple)
                        i += 1
                    else:
                        outerList.append(clauses[1][i])
                else:
                    outerList.append(clauses[1][i])
                i += 1
            temp[1] = outerList
        clauses = tuple(temp)
        return clauses
    
    def combineAndOr(self, clauses):
        if(type(clauses) == str):
            return clauses
        # change clauses to list from tuple so can modify
        temp = list(clauses)
        for i in range(len(clauses[1])):
            if (isinstance(clauses[1][i], tuple)):
                temp[1][i] = self.combineAndOr(temp[1][i])
        if (temp[0] == "or"):
            newList = []
            for i in range(len(temp[1])):
                if (isinstance(temp[1][i], tuple)):
                    if (temp[1][i][0] == "or"):
                        for j in range(len(temp[1][i][1])):
                            newList.append(temp[1][i][1][j])
                    else:
                        newList.append(temp[1][i])
                else:
                    newList.append(temp[1][i])
            temp[1] = newList
        if (temp[0] == "and"):
            newList = []
            for i in range(len(temp[1])):
                if (isinstance(temp[1][i], tuple)):
                    if (temp[1][i][0] == "and"):
                        for j in range(len(temp[1][i][1])):
                            newList.append(temp[1][i][1][j])
                    else:
                        newList.append(temp[1][i])
                else:
                    newList.append(temp[1][i])
            temp[1] = newList
        clauses = tuple(temp)
        return clauses

    def outputCNF(self, clauses):
        f = open("output.txt", "w")
        if (clauses[0] == "and"):
            for i in range(len(clauses[1])):
                f.write(self.outputHelper(clauses[1][i]))
                if (i < len(clauses[1]) - 1):
                    f.write(" ^ ")
                    f.write("\n")
        else :
            f.write(self.outputHelper(clauses))     

    def outputHelper(self, clauses):
        if (type(clauses) == str):
            return clauses
        if (clauses[0] == "not"):
            return "(not " + self.outputHelper(clauses[1][0]) + ")"
        if (clauses[0] == "and"):
            temp = "(and"
            for x in clauses[1]:
                temp += " " + self.outputHelper(x)
            temp += ")"
            return temp
        if (clauses[0] == "or"):
            temp = "(or"
            for x in clauses[1]:
                temp += " " + self.outputHelper(x)
            temp += ")"
            return temp

        
    # Main method
    def main(self):
        file = open(sys.argv[1])
        input = file.read()
        if (input == ""):
            print("No input provided")
            return
        print("Formula =", input)
        clauses = self.getClauses(input)
        self.CNF(clauses)
        
    
if __name__ == "__main__":
    pl = PropositionalLogic()
    pl.main()