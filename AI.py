import random
class chess:
    def __init__(self, data):
        self.data = data
        self.child = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.child.append(child)

theChessboard = [["bR1", "bH1", "bB1", "bQ1", "bK1", "bB2", "bH2", "bR2"],
                 ["bP1", "bP2", "bP3", "bP4", "bP5", "bP6", "bP7", "bP8"],
                 ["ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1"],
                 ["ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1"],
                 ["ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1"],
                 ["ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1", "ES1"],
                 ["wP1", "wP2", "wP3", "wP4", "wP5", "wP6", "wP7", "wP8"],
                 ["wR1", "wH1", "wB1", "wQ1", "wK1", "wB2", "wH2", "wR2"]]


treeDepth = 0
currentChessboard = None
column = None
row = None
#chessPosition = (column, row)                  first arg = column(array of array) second = row (array)
notinrange = False
blackTurn = False
whiteTurn = True
whosTurn = None
notCheckmated = True
state = False
possiblePath = []
collidedPath = []
moveCol = None
moveRow = None
moveRes = None
collided = False
isThisChessAPawn = False
promotionAvailabe = False
whiteEvaluationHash = {"wP1":1, "wP2":1,"wP3":1,"wP4":1,"wP5":1,"wP6":1,"wP7":1, "wP8":1, "wR1":10, "wR2":10, "wH1":10, "wH2":10, "wB1":10, "wB2":10, "wQ1":100, "wK1":10000 }
blackEvaluationHash = {"bP1":1, "bP2":1,"bP3":1,"bP4":1,"bP5":1,"bP6":1,"bP7":1, "bP8":1, "bR1":10, "bR2":10, "bH1":10, "bH2":10, "bB1":10, "bB2":10, "bQ1":100, "bK1":10000 }

def initialiseStartBoard():                      #initialise the board
    root = chess(theChessboard)
    return root

def evaluationFunction(inputNode, whiteHash, blackHash, whiteOrBlack):
    whiteval =0
    blackval =0
    tmp = 10168
    for i in inputNode.data:
        for j in i:
            if (j in whiteHash):
                whiteval = whiteval + whiteHash.get(j, 0)
            if (j in blackHash):
                blackval = blackval + blackHash.get(j, 0)
    if (whiteOrBlack == True):
        totalValue = whiteval+(tmp-blackval)
    else:
        totalValue = blackval + (tmp - whiteval)


    return totalValue

def minimax(inputNode, treeDepth, computer, whiteOrBlack, wHash, bHash, alpha, beta):
    gameEnd = False
    King = 1;
    tmpData = inputNode.data
    print(tmpData)
    for i in inputNode.data:
        for j in i:
            if (whiteOrBlack == True):
                if j=="wK1":
                    King-=1
            else:
                if j=="bK1":
                    King -=1
    if King==1:
        gameEnd = True
    if treeDepth==0 or gameEnd:
        thisNodeValue = evaluationFunction(inputNode, wHash, bHash, whiteOrBlack)
        return thisNodeValue, tmpData
    if (computer):
        maxVal = -10000000
        for i in inputNode.child:
            tmpVal, tmpData = minimax(i, treeDepth-1, not computer, not whiteOrBlack, wHash, bHash, alpha, beta)

            maxVal = max(maxVal, tmpVal)
            print(i.data)
            if (maxVal == tmpVal):
                tmpData = i.data
            alpha = max(alpha, tmpVal)
            if (beta<=alpha):
                break
        return maxVal, tmpData
    else:
        minVal = 10000000
        for i in inputNode.child:
            tmpVal, tmpData = minimax(i, treeDepth-1, not computer, not whiteOrBlack, wHash, bHash, alpha, beta)
            minVal = min(minVal, tmpVal)
            print(i.data)
            if (minVal == tmpVal):
                tmpData = i.data
            beta = min(beta, tmpVal)
            if beta<=alpha:
                break
        return minVal, tmpData

def getMovePos(treeNode,white,black):
    while True:
        tmpCol = input("Please enter what is the column you want your chess to be moved to:  ")
        if (47 < ord(tmpCol) < 56):
            print("Valid Input")
            col = int(tmpCol)
            break
        else:
            print("Invalid Input")

    while True:
        tmpRow = input("Please enter what is the row you want your chess to be moved to:  ")
        if (47 < ord(tmpRow) < 56):
            print("Valid Input")
            trow = int(tmpRow)
            break
        else:
            print("Invalid Input")

    return col,trow

def getUserInput(treeNode, white, black):
    while True:
        while True:
            tmpCol = input("Please enter what is the column of your to-be-moved chess:  ")
            if (47 < ord(tmpCol) < 56):
                print("Valid Input")
                col =  int(tmpCol)
                break
            else:
                print("Invalid Input")

        while True:
            tmpRow = input("Please enter what is the row of your to-be-moved chess:  ")
            if (47 < ord(tmpRow) < 56):
                print("Valid Input")
                trow = int(tmpRow)
                break
            else:
                print("Invalid Input")
        if (white == True):
            if (treeNode.data[trow][col][0] == 'w'):
                print("You have chosen (", col, ",", trow, ") which is", treeNode.data[trow][col])
                return col, trow
            else:
                print("Invalid Chess")

        elif (black == True):
            if (treeNode.data[trow][col][0] == 'b'):
                print("You have chosen (", col, ",", trow, ") which is", treeNode.data[trow][col])
                return col, trow
            else:
                print("Invalid Chess")

def getUserResponse():
    while True:
        res = input("Do you want to re-choose? Y/N ")
        if ((res=='Y' or res=='y' or res=='N' or res=='n')):
            return res
        else:
            print("Invalid Input")

def isCollided(tmpCol, tmpRow, treeNode):
    if(treeNode.data[tmpRow][tmpCol] != "ES1"):
        return True
    else:
        return False

def rookRule(rookPosition, treeNode):

    availablePath = []
    collidedPath = []
    if (0 < rookPosition[0] < 7 and 0 < rookPosition[1] < 7):
        i = 1
        while (rookPosition[0] + i < 8):
            print(i)
            if (treeNode.data[rookPosition[1]][rookPosition[0] + i]) == "ES1":
                availablePath.append((rookPosition[0] + i, rookPosition[1]))
                i = i + 1
            else:
                collidedPath.append((rookPosition[0] + i, rookPosition[1]))
                break
        j = 1
        while (rookPosition[0] - j > -1):
            print(j)
            if (treeNode.data[rookPosition[1]][rookPosition[0] - j]) == "ES1":
                availablePath.append((rookPosition[0] - j, rookPosition[1]))
                j += 1
            else:
                collidedPath.append((rookPosition[0] - j, rookPosition[1]))
                break
        k = 1
        while (rookPosition[1] + k < 8):
            print(k)
            if (treeNode.data[rookPosition[1] + k][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] + k))
                k += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] + k))
                break

        l = 1
        while (rookPosition[1] - l > -1):
            print(l)
            if (treeNode.data[rookPosition[1] - l][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] - l))
                l += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] - l))
                break

    if (0 < rookPosition[0] < 7 and rookPosition[1] == 0):
        i = 1
        while (rookPosition[0] + i < 8):
            print("  5 ")
            if (treeNode.data[rookPosition[1]][rookPosition[0] + i]) == "ES1":
                availablePath.append((rookPosition[0] + i, rookPosition[1]))
                i += 1
            else:
                collidedPath.append((rookPosition[0] + i, rookPosition[1]))
                break
        j = 1

        while (rookPosition[0] - j > -1):
            print("6")
            if (treeNode.data[rookPosition[1]][rookPosition[0] - j]) == "ES1":
                availablePath.append((rookPosition[0] - j, rookPosition[1]))
                j += 1
            else:
                collidedPath.append((rookPosition[0] - j, rookPosition[1]))
                break

        k = 1
        while (rookPosition[1] + k < 8):
            if (treeNode.data[rookPosition[1] + k][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] + k))
                k += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] + k))
                break

    if (0 < rookPosition[0] < 7 and rookPosition[1] == 7):
        i = 1
        j = 1
        k = 1
        while (rookPosition[0] + i < 8):
            if (treeNode.data[rookPosition[1]][rookPosition[0] + i]) == "ES1":
                availablePath.append((rookPosition[0] + i, rookPosition[1]))
            else:
                collidedPath.append((rookPosition[0] + i, rookPosition[1]))
                break
        while (rookPosition[0] - j > -1):
            if (treeNode.data[rookPosition[1]][rookPosition[0] - j]) == "ES1":
                availablePath.append((rookPosition[0] - j, rookPosition[1]))
                j += 1
            else:
                collidedPath.append((rookPosition[0] - j, rookPosition[1]))
                break
        while (rookPosition[1] - k > -1):
            if (treeNode.data[rookPosition[1] - k][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] - k))
                k += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] - k))
                break

    if (rookPosition[0] == 0 and 0 < rookPosition[1] < 7):
        i = 1
        j = 1
        k = 1
        while (rookPosition[0] + i > 8):
            if (treeNode.data[rookPosition[1]][rookPosition[0] + i]) == "ES1":
                availablePath.append((rookPosition[0] + i, rookPosition[1]))
                i += 1
            else:
                collidedPath.append((rookPosition[0] + i, rookPosition[1]))
                break
        while (rookPosition[1] + j > 8):
            if (treeNode.data[rookPosition[1] + j][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] + j))
                j += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] + j))
                break
        while (rookPosition[1] - k > -1):
            if (treeNode.data[rookPosition[1] - k][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] - k))
                k += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] - k))
                break

    if (rookPosition[0] == 0 and rookPosition[1] == 0):
        i = 1
        j = 1
        while (rookPosition[0] + i < 8):
            if (treeNode.data[rookPosition[1]][rookPosition[0] + i]) == "ES1":
                availablePath.append((rookPosition[0] + i, rookPosition[1]))
                i += 1
            else:
                collidedPath.append((rookPosition[0] + i, rookPosition[1]))
                break
        while (rookPosition[1] + j < 8):
            if (treeNode.data[rookPosition[1] + j][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] + j))
                j += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] + j))
                break

    if (rookPosition[0] == 0 and rookPosition[1] == 7):
        i = 1
        j = 1
        while (rookPosition[0] + i < 8):
            if (treeNode.data[rookPosition[1]][rookPosition[0] + i]) == "ES1":
                availablePath.append((rookPosition[0] + i, rookPosition[1]))
                i += 1
            else:
                collidedPath.append((rookPosition[0] + i, rookPosition[1]))
                break
        while (rookPosition[1] - j > -1):
            if (treeNode.data[rookPosition[1] - j][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] - j))
                j += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] - j))
                break

    if (rookPosition[0] == 7 and 0 < rookPosition[1] < 7):
        i = 1
        j = 1
        k = 1
        while (rookPosition[0] - i > -1):
            if (treeNode.data[rookPosition[1]][rookPosition[0] - i]) == "ES1":
                availablePath.append((rookPosition[0] - i, rookPosition[1]))
                i += 1
            else:
                collidedPath.append((rookPosition[0] - i, rookPosition[1]))
                break
        while (rookPosition[1] + j < 8):
            if (treeNode.data[rookPosition[1] + j][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] + j))
                j += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] + j))
                break

        while (rookPosition[1] - k > -1):
            if (treeNode.data[rookPosition[1] - k][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] - k))
                k += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] - k))
                break

    if (rookPosition[0] == 7 and rookPosition[1] == 0):
        i = 1
        j = 1
        while (rookPosition[0] - i > -1):
            if (treeNode.data[rookPosition[1]][rookPosition[0] - i]) == "ES1":
                availablePath.append((rookPosition[0] - i, rookPosition[1]))
                i += 1
            else:
                collidedPath.append((rookPosition[0] - i, rookPosition[1]))
                break
        while (rookPosition[1] + j < 8):
            if (treeNode.data[rookPosition[1] + j][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] + j))
                j += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] + j))
                break

    if (rookPosition[0] == 7 and rookPosition[1] == 7):
        i = 1
        j = 1
        while (rookPosition[0] - i > -1):
            if (treeNode.data[rookPosition[1]][rookPosition[0] - i]) == "ES1":
                availablePath.append((rookPosition[0] - i, rookPosition[1]))
                i += 1
            else:
                collidedPath.append((rookPosition[0] - i, rookPosition[1]))
                break
        while (rookPosition[1] - j > -1):
            if (treeNode.data[rookPosition[1] - j][rookPosition[0]]) == "ES1":
                availablePath.append((rookPosition[0], rookPosition[1] - j))
                j += 1
            else:
                collidedPath.append((rookPosition[0], rookPosition[1] - j))
                break

    return availablePath,collidedPath

def knightRule(horsePosition, treeNode):
    availablePath = []
    collidedPath = []
    if not(horsePosition[0]+1>7 or horsePosition[1]+2>7 ):
        if (treeNode.data[horsePosition[1] + 2][horsePosition[0] + 1] == "ES1" ):
            availablePath.append((horsePosition[0]+1,horsePosition[1]+2))
        else:
            collidedPath.append((horsePosition[0]+1,horsePosition[1]+2))
    if not(horsePosition[0]+2>7 or horsePosition[1]+1>7):
        if (treeNode.data[horsePosition[1] + 1][horsePosition[0] + 2] == "ES1" ):
            availablePath.append((horsePosition[0] + 2, horsePosition[1] + 1))
        else:
            collidedPath.append((horsePosition[0] + 2, horsePosition[1] + 1))
    if not(horsePosition[0]-2<0 or horsePosition[1]+1>7):
        if(treeNode.data[horsePosition[1] + 1][horsePosition[0] - 2] == "ES1" ):
            availablePath.append((horsePosition[0] - 2, horsePosition[1] + 1))
        else:
            collidedPath.append((horsePosition[0] - 2, horsePosition[1] + 1))
    if not (horsePosition[0] - 1 < 0 or horsePosition[1] + 2 > 7):
        if (treeNode.data[horsePosition[1] + 2][horsePosition[0] - 1] == "ES1"):
            availablePath.append((horsePosition[0] - 1, horsePosition[1] + 2))
        else:
            collidedPath.append((horsePosition[0] - 1, horsePosition[1] + 2))
    if not (horsePosition[0] + 2 > 7 or horsePosition[1] - 1 < 0 ):
        if (treeNode.data[horsePosition[1] - 1][horsePosition[0] + 2] == "ES1"):
            availablePath.append((horsePosition[0] + 2, horsePosition[1] - 1))
        else:
            collidedPath.append((horsePosition[0] + 2, horsePosition[1] - 1))
    if not (horsePosition[0] + 1 > 7 or horsePosition[1] - 2 < 0):
        if (treeNode.data[horsePosition[1] - 2][horsePosition[0] + 1] == "ES1"):
            availablePath.append((horsePosition[0] + 1, horsePosition[1] - 2))
        else:
            collidedPath.append((horsePosition[0] + 1, horsePosition[1] - 2))
    if not (horsePosition[0] - 1 < 0 or horsePosition[1] - 2 < 0):
        if (treeNode.data[horsePosition[1] - 2][horsePosition[0] - 1] == "ES1"):
            availablePath.append((horsePosition[0] - 1, horsePosition[1] - 2))
        else:
            collidedPath.append((horsePosition[0] - 1, horsePosition[1] - 2))
    if not (horsePosition[0] - 2 < 0 or horsePosition[1] - 1 < 0):
        if (treeNode.data[horsePosition[1] - 1][horsePosition[0] - 2] == "ES1"):
            availablePath.append((horsePosition[0] - 2, horsePosition[1] - 1))
        else:
            collidedPath.append((horsePosition[0] - 2, horsePosition[1] - 1))
    return availablePath, collidedPath

def bishopRule(bishopPosition, treeNode):
    availablePath = []
    collidedPath = []
    if (bishopPosition[0] == 0 and bishopPosition[1] == 0):  # if bishop in left bottom
        a = 1
        b = 1
        while (bishopPosition[0] + a <= 7 and bishopPosition[1] + b <= 7):
            if (treeNode.data[bishopPosition[0] + b][bishopPosition[0] + a] == "ES1"):
                availablePath.append((bishopPosition[0] + 1, bishopPosition[1] + 1))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] + 1, bishopPosition[1] + 1))
                break

    if (bishopPosition[0] == 0 and bishopPosition[1] == 7):  # if bishop in left up
        a = 1
        b = 1
        while (bishopPosition[0] + a <= 7 and bishopPosition[1] - b >= 0):
            if (treeNode.data[bishopPosition[1] - b][bishopPosition[0] + a] == "ES1"):
                availablePath.append((bishopPosition[0] + a, bishopPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] + a, bishopPosition[1] - b))
                break

    if (bishopPosition[0] == 7 and bishopPosition[1] == 7):  # if bishop in right up
        a = 1
        b = 1
        while (bishopPosition[0] - a >= 0 and bishopPosition[1] - b >= 0):
            if (treeNode.data[bishopPosition[1] - b][bishopPosition[0] - a] == "ES1"):
                availablePath.append((bishopPosition[0] - a, bishopPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] - a, bishopPosition[1] - b))
                break

    if (bishopPosition[0] == 7 and bishopPosition[1] == 0):  # if bishop in right bottom
        a = 1
        b = 1
        while (bishopPosition[0] - a >= 7 and bishopPosition[1] + b <= 7):
            if (treeNode.data[bishopPosition[1] + b][bishopPosition[0] - a] == "ES1"):
                availablePath.append((bishopPosition[0] - a, bishopPosition[1] + b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] - a, bishopPosition[1] + b))
                break

    if (bishopPosition[0] == 0 and 0 < bishopPosition < 7):  # if bishop on left
        a = 1
        b = 1
        while (bishopPosition[0] + a <= 7 and bishopPosition[1] - b >= 0):
            if (treeNode.data[bishopPosition[1] - b][bishopPosition[0] + a] == "ES1"):
                availablePath.append((bishopPosition[0] + a, bishopPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] + a, bishopPosition[1] - b))
                break
        c = 1
        d = 1
        while (bishopPosition[0] + c <= 7 and bishopPosition[1] + d <= 7):
            if (treeNode.data[bishopPosition[1] + d][bishopPosition[0] + c] == "ES1"):
                availablePath.append((bishopPosition[0] + c, bishopPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((bishopPosition[0] + c, bishopPosition[1] + d))
                break

    if (bishopPosition[0] == 7 and 0 < bishopPosition[1] < 7):  # if bishop on right
        a = 1
        b = 1
        while (bishopPosition[0] - a >= 0 and bishopPosition[1] - b >= 0):
            if (treeNode.data[bishopPosition[1] - b][bishopPosition[0] - a] == "ES1"):
                availablePath.append((bishopPosition[0] - a, bishopPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] - a, bishopPosition[1] - b))
                break
        c = 1
        d = 1
        while (bishopPosition[0] - c >= 0 and bishopPosition[1] + d <= 7):
            if (treeNode.data[bishopPosition[1] + d][bishopPosition[0] - c] == "ES1"):
                availablePath.append((bishopPosition[0] - c, bishopPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((bishopPosition[0] - c, bishopPosition[1] + d))
                break

    if (0 < bishopPosition[0] < 7 and bishopPosition[1] == 0):  # if bishop on top
        a = 1
        b = 1
        while (bishopPosition[0] - a >= 0 and bishopPosition[1] + b <= 7):
            if (treeNode.data[bishopPosition[1] + b][bishopPosition[0] - a] == "ES1"):
                availablePath.append((bishopPosition[0] - a, bishopPosition[1] + b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] - a, bishopPosition[1] + b))
                break
        c = 1
        d = 1
        while (bishopPosition[0] +c <= 7 and bishopPosition[1] + d <= 7):
            if (treeNode.data[bishopPosition[1] + d][bishopPosition[0] + c] == "ES1"):
                availablePath.append((bishopPosition[0] + c, bishopPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((bishopPosition[0] + c, bishopPosition[1] + d))
                break

    if (0 < bishopPosition[0] < 7 and bishopPosition[1] == 7):  # if bishop on bottom
        a = 1
        b = 1
        while (bishopPosition[0] - a >= 0 and bishopPosition[1] - b >= 0):

            if (treeNode.data[bishopPosition[1] - b][bishopPosition[0] - a] == "ES1"):
                availablePath.append((bishopPosition[0] - a, bishopPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] - a, bishopPosition[1] - b))
                break
        c = 1
        d = 1
        while (bishopPosition[0] + c <= 7 and bishopPosition[1] - d >= 0):
            if (treeNode.data[bishopPosition[1] - d][bishopPosition[0] + c] == "ES1"):
                availablePath.append((bishopPosition[0] + c, bishopPosition[1] - d))
                c += 1
                d += 1
            else:
                collidedPath.append((bishopPosition[0] + c, bishopPosition[1] - d))
                break

    if (0 < bishopPosition[0] < 7 and 0 < bishopPosition[1] < 7):  # if bishop in middle
        a = 1
        b = 1
        while (bishopPosition[0] + a <= 7 and bishopPosition[1] + b <= 7):
            if (treeNode.data[bishopPosition[1] + b][bishopPosition[0] + a] == "ES1"):
                availablePath.append((bishopPosition[0] + a, bishopPosition[1] + b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] + a, bishopPosition[1] + b))
                break
        c = 1
        d = 1
        while (bishopPosition[0] - c >= 0 and bishopPosition[1] + d <= 7):
            if (treeNode.data[bishopPosition[1] + d][bishopPosition[0] - c] == "ES1"):
                availablePath.append((bishopPosition[0] - c, bishopPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((bishopPosition[0] - c, bishopPosition[1] + d))
                break
        a = 1
        b = 1
        while (bishopPosition[0] + a <= 7 and bishopPosition[1] - b >= 0):
            if (treeNode.data[bishopPosition[1] - b][bishopPosition[0] + a] == "ES1"):
                availablePath.append((bishopPosition[0] + a, bishopPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((bishopPosition[0] + a, bishopPosition[1] - b))
                break
        c = 1
        d = 1
        while (bishopPosition[0] - c >= 0 and bishopPosition[1] - d >= 0):
            if (treeNode.data[bishopPosition[1] - d][bishopPosition[0] - c] == "ES1"):
                availablePath.append((bishopPosition[0] - c, bishopPosition[1] - d))
                c += 1
                d += 1
            else:
                collidedPath.append((bishopPosition[0] - c, bishopPosition[1] - d))
                break

    return availablePath, collidedPath

def kingRule(kingPosition, treeNode):
    availablePath = []
    collidedPath = []
    if not (kingPosition[0]+1 >7 and kingPosition[1]+1>7):
        if ( treeNode.data[kingPosition[1]+1][kingPosition[0]+1] == "ES1"):
            availablePath.append((kingPosition[0]+1, kingPosition[1]+1))
        else:
            collidedPath.append((kingPosition[0]+1, kingPosition[1]+1))
    if not (kingPosition[1]+1>7):
        if ( treeNode.data[kingPosition[1]+1][kingPosition[0]] == "ES1"):
            availablePath.append((kingPosition[0] , kingPosition[1] + 1))
        else:
            collidedPath.append((kingPosition[0] , kingPosition[1] + 1))
    if not (kingPosition[0]-1< 0 and kingPosition[1]+1 > 7):
        if (treeNode.data[kingPosition[1] + 1][kingPosition[0] - 1] == "ES1"):
            availablePath.append((kingPosition[0] - 1, kingPosition[1] + 1))
        else:
            collidedPath.append((kingPosition[0] - 1, kingPosition[1] + 1))
    if not (kingPosition[0] - 1 < 0):
        if ( treeNode.data[kingPosition[1]][kingPosition[0]-1] == "ES1"):
            availablePath.append((kingPosition[0]-1 , kingPosition[1]))
        else:
            collidedPath.append((kingPosition[0]-1 , kingPosition[1]))
    if not (kingPosition[0]-1< 0 and kingPosition[1]-1 <0):
        if (treeNode.data[kingPosition[1] - 1][kingPosition[0] - 1] == "ES1"):
            availablePath.append((kingPosition[0] - 1, kingPosition[1] - 1))
        else:
            collidedPath.append((kingPosition[0] - 1, kingPosition[1] - 1))
    if not (kingPosition[1]-1<0):
        if ( treeNode.data[kingPosition[1]-1][kingPosition[0]] == "ES1"):
            availablePath.append((kingPosition[0] , kingPosition[1] - 1))
        else:
            collidedPath.append((kingPosition[0] , kingPosition[1] - 1))
    if not (kingPosition[0]+1 > 7 and kingPosition[1]-1 <0):
        if (treeNode.data[kingPosition[1] - 1][kingPosition[0] + 1] == "ES1"):
            availablePath.append((kingPosition[0] + 1, kingPosition[1] - 1))
        else:
            collidedPath.append((kingPosition[0] + 1, kingPosition[1] - 1))
    if not (kingPosition[0] + 1 > 7):
        if ( treeNode.data[kingPosition[1]][kingPosition[0]+1] == "ES1"):
            availablePath.append((kingPosition[0] + 1, kingPosition[1]))
        else:
            collidedPath.append((kingPosition[0] + 1, kingPosition[1]))
    return availablePath, collidedPath

def queenRule(queenPosition, treeNode):
    availablePath = []
    collidedPath = []
    if (0 < queenPosition[0] < 7 and 0 < queenPosition[1] < 7):
        i = 1
        while (queenPosition[0] + i < 8):
            print(i)
            if (treeNode.data[queenPosition[1]][queenPosition[0] + i]) == "ES1":
                availablePath.append((queenPosition[0] + i, queenPosition[1]))
                i = i + 1
            else:
                collidedPath.append((queenPosition[0] + i, queenPosition[1]))
                break
        j = 1
        while (queenPosition[0] - j > -1):
            print(j)
            if (treeNode.data[queenPosition[1]][queenPosition[0] - j]) == "ES1":
                availablePath.append((queenPosition[0] - j, queenPosition[1]))
                j += 1
            else:
                collidedPath.append((queenPosition[0] - j, queenPosition[1]))
                break
        k = 1
        while (queenPosition[1] + k < 8):
            print(k)
            if (treeNode.data[queenPosition[1] + k][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] + k))
                k += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] + k))
                break

        l = 1
        while (queenPosition[1] - l > -1):
            print(l)
            if (treeNode.data[queenPosition[1] - l][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] - l))
                l += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] - l))
                break

    if (0 < queenPosition[0] < 7 and queenPosition[1] == 0):
        i = 1
        while (queenPosition[0] + i < 8):
            print("  5 ")
            if (treeNode.data[queenPosition[1]][queenPosition[0] + i]) == "ES1":
                availablePath.append((queenPosition[0] + i, queenPosition[1]))
                i += 1
            else:
                collidedPath.append((queenPosition[0] + i, queenPosition[1]))
                break
        j = 1

        while (queenPosition[0] - j > -1):
            print("6")
            if (treeNode.data[queenPosition[1]][queenPosition[0] - j]) == "ES1":
                availablePath.append((queenPosition[0] - j, queenPosition[1]))
                j += 1
            else:
                collidedPath.append((queenPosition[0] - j, queenPosition[1]))
                break

        k = 1
        while (queenPosition[1] + k < 8):
            if (treeNode.data[queenPosition[1] + k][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] + k))
                k += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] + k))
                break

    if (0 < queenPosition[0] < 7 and queenPosition[1] == 7):
        i = 1
        j = 1
        k = 1
        while (queenPosition[0] + i < 8):
            if (treeNode.data[queenPosition[1]][queenPosition[0] + i]) == "ES1":
                availablePath.append((queenPosition[0] + i, queenPosition[1]))
            else:
                collidedPath.append((queenPosition[0] + i, queenPosition[1]))
                break
        while (queenPosition[0] - j > -1):
            if (treeNode.data[queenPosition[1]][queenPosition[0] - j]) == "ES1":
                availablePath.append((queenPosition[0] - j, queenPosition[1]))
                j += 1
            else:
                collidedPath.append((queenPosition[0] - j, queenPosition[1]))
                break
        while (queenPosition[1] - k > -1):
            if (treeNode.data[queenPosition[1] - k][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] - k))
                k += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] - k))
                break

    if (queenPosition[0] == 0 and 0 < queenPosition[1] < 7):
        i = 1
        j = 1
        k = 1
        while (queenPosition[0] + i > 8):
            if (treeNode.data[queenPosition[1]][queenPosition[0] + i]) == "ES1":
                availablePath.append((queenPosition[0] + i, queenPosition[1]))
                i += 1
            else:
                collidedPath.append((queenPosition[0] + i, queenPosition[1]))
                break
        while (queenPosition[1] + j > 8):
            if (treeNode.data[queenPosition[1] + j][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] + j))
                j += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] + j))
                break
        while (queenPosition[1] - k > -1):
            if (treeNode.data[queenPosition[1] - k][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] - k))
                k += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] - k))
                break

    if (queenPosition[0] == 0 and queenPosition[1] == 0):
        i = 1
        j = 1
        while (queenPosition[0] + i < 8):
            if (treeNode.data[queenPosition[1]][queenPosition[0] + i]) == "ES1":
                availablePath.append((queenPosition[0] + i, queenPosition[1]))
                i += 1
            else:
                collidedPath.append((queenPosition[0] + i, queenPosition[1]))
                break
        while (queenPosition[1] + j < 8):
            if (treeNode.data[queenPosition[1] + j][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] + j))
                j += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] + j))
                break

    if (queenPosition[0] == 0 and queenPosition[1] == 7):
        i = 1
        j = 1
        while (queenPosition[0] + i < 8):
            if (treeNode.data[queenPosition[1]][queenPosition[0] + i]) == "ES1":
                availablePath.append((queenPosition[0] + i, queenPosition[1]))
                i += 1
            else:
                collidedPath.append((queenPosition[0] + i, queenPosition[1]))
                break
        while (queenPosition[1] - j > -1):
            if (treeNode.data[queenPosition[1] - j][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] - j))
                j += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] - j))
                break

    if (queenPosition[0] == 7 and 0 < queenPosition[1] < 7):
        i = 1
        j = 1
        k = 1
        while (queenPosition[0] - i > -1):
            if (treeNode.data[queenPosition[1]][queenPosition[0] - i]) == "ES1":
                availablePath.append((queenPosition[0] - i, queenPosition[1]))
                i += 1
            else:
                collidedPath.append((queenPosition[0] - i, queenPosition[1]))
                break
        while (queenPosition[1] + j < 8):
            if (treeNode.data[queenPosition[1] + j][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] + j))
                j += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] + j))
                break

        while (queenPosition[1] - k > -1):
            if (treeNode.data[queenPosition[1] - k][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] - k))
                k += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] - k))
                break

    if (queenPosition[0] == 7 and queenPosition[1] == 0):
        i = 1
        j = 1
        while (queenPosition[0] - i > -1):
            if (treeNode.data[queenPosition[1]][queenPosition[0] - i]) == "ES1":
                availablePath.append((queenPosition[0] - i, queenPosition[1]))
                i += 1
            else:
                collidedPath.append((queenPosition[0] - i, queenPosition[1]))
                break
        while (queenPosition[1] + j < 8):
            if (treeNode.data[queenPosition[1] + j][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] + j))
                j += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] + j))
                break

    if (queenPosition[0] == 7 and queenPosition[1] == 7):
        i = 1
        j = 1
        while (queenPosition[0] - i > -1):
            if (treeNode.data[queenPosition[1]][queenPosition[0] - i]) == "ES1":
                availablePath.append((queenPosition[0] - i, queenPosition[1]))
                i += 1
            else:
                collidedPath.append((queenPosition[0] - i, queenPosition[1]))
                break
        while (queenPosition[1] - j > -1):
            if (treeNode.data[queenPosition[1] - j][queenPosition[0]]) == "ES1":
                availablePath.append((queenPosition[0], queenPosition[1] - j))
                j += 1
            else:
                collidedPath.append((queenPosition[0], queenPosition[1] - j))
                break

    if (queenPosition[0] == 0 and queenPosition[1] == 0):  # if bishop in left bottom
        a = 1
        b = 1
        while (queenPosition[0] + a <= 7 and queenPosition[1] + b <= 7):
            if (treeNode.data[queenPosition[0] + b][queenPosition[0] + a] == "ES1"):
                availablePath.append((queenPosition[0] + 1, queenPosition[1] + 1))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] + 1, queenPosition[1] + 1))
                break

    if (queenPosition[0] == 0 and queenPosition[1] == 7):  # if bishop in left up
        a = 1
        b = 1
        while (queenPosition[0] + a <= 7 and queenPosition[1] - b >= 0):
            if (treeNode.data[queenPosition[1] - b][queenPosition[0] + a] == "ES1"):
                availablePath.append((queenPosition[0] + a, queenPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] + a, queenPosition[1] - b))
                break

    if (queenPosition[0] == 7 and queenPosition[1] == 7):  # if bishop in right up
        a = 1
        b = 1
        while (queenPosition[0] - a >= 0 and queenPosition[1] - b >= 0):
            if (treeNode.data[queenPosition[1] - b][queenPosition[0] - a] == "ES1"):
                availablePath.append((queenPosition[0] - a, queenPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] - a, queenPosition[1] - b))
                break

    if (queenPosition[0] == 7 and queenPosition[1] == 0):  # if bishop in right bottom
        a = 1
        b = 1
        while (queenPosition[0] - a >= 7 and queenPosition[1] + b <= 7):
            if (treeNode.data[queenPosition[1] + b][queenPosition[0] - a] == "ES1"):
                availablePath.append((queenPosition[0] - a, queenPosition[1] + b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] - a, queenPosition[1] + b))
                break

    if (queenPosition[0] == 0 and 0 < queenPosition[1] < 7):  # if bishop on left
        a = 1
        b = 1
        while (queenPosition[0] + a <= 7 and queenPosition[1] - b >= 0):
            if (treeNode.data[queenPosition[1] - b][queenPosition[0] + a] == "ES1"):
                availablePath.append((queenPosition[0] + a, queenPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] + a, queenPosition[1] - b))
                break
        c = 1
        d = 1
        while (queenPosition[0] + c <= 7 and queenPosition[1] + d <= 7):
            if (treeNode.data[queenPosition[1] + d][queenPosition[0] + c] == "ES1"):
                availablePath.append((queenPosition[0] + c, queenPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((queenPosition[0] + c, queenPosition[1] + d))
                break

    if (queenPosition[0] == 7 and 0 < queenPosition[1] < 7):  # if bishop on right
        a = 1
        b = 1
        while (queenPosition[0] - a >= 0 and queenPosition[1] - b >= 0):
            if (treeNode.data[queenPosition[1] - b][queenPosition[0] - a] == "ES1"):
                availablePath.append((queenPosition[0] - a, queenPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] - a, queenPosition[1] - b))
                break
        c = 1
        d = 1
        while (queenPosition[0] - c >= 0 and queenPosition[1] + d <= 7):
            if (treeNode.data[queenPosition[1] + d][queenPosition[0] - c] == "ES1"):
                availablePath.append((queenPosition[0] - c, queenPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((queenPosition[0] - c, queenPosition[1] + d))
                break

    if (0 < queenPosition[0] < 7 and queenPosition[1] == 0):  # if bishop on top
        a = 1
        b = 1
        while (queenPosition[0] - a >= 0 and queenPosition[1] + b <= 7):
            if (treeNode.data[queenPosition[1] + b][queenPosition[0] - a] == "ES1"):
                availablePath.append((queenPosition[0] - a, queenPosition[1] + b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] - a, queenPosition[1] + b))
                break
        c = 1
        d = 1
        while (queenPosition[0] +c <= 7 and queenPosition[1] + d <= 7):
            if (treeNode.data[queenPosition[1] + d][queenPosition[0] + c] == "ES1"):
                availablePath.append((queenPosition[0] + c, queenPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((queenPosition[0] + c, queenPosition[1] + d))
                break

    if (0 < queenPosition[0] < 7 and queenPosition[1] == 7):  # if bishop on bottom
        a = 1
        b = 1
        while (queenPosition[0] - a >= 0 and queenPosition[1] - b >= 0):

            if (treeNode.data[queenPosition[1] - b][queenPosition[0] - a] == "ES1"):
                availablePath.append((queenPosition[0] - a, queenPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] - a, queenPosition[1] - b))
                break
        c = 1
        d = 1
        while (queenPosition[0] + c <= 7 and queenPosition[1] - d >= 0):
            if (treeNode.data[queenPosition[1] - d][queenPosition[0] + c] == "ES1"):
                availablePath.append((queenPosition[0] + c, queenPosition[1] - d))
                c += 1
                d += 1
            else:
                collidedPath.append((queenPosition[0] + c, queenPosition[1] - d))
                break

    if (0 < queenPosition[0] < 7 and 0 < queenPosition[1] < 7):  # if bishop in middle
        a = 1
        b = 1
        while (queenPosition[0] + a <= 7 and queenPosition[1] + b <= 7):
            if (treeNode.data[queenPosition[1] + b][queenPosition[0] + a] == "ES1"):
                availablePath.append((queenPosition[0] + a, queenPosition[1] + b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] + a, queenPosition[1] + b))
                break
        c = 1
        d = 1
        while (queenPosition[0] - c >= 0 and queenPosition[1] + d <= 7):
            if (treeNode.data[queenPosition[1] + d][queenPosition[0] - c] == "ES1"):
                availablePath.append((queenPosition[0] - c, queenPosition[1] + d))
                c += 1
                d += 1
            else:
                collidedPath.append((queenPosition[0] - c, queenPosition[1] + d))
                break
        a = 1
        b = 1
        while (queenPosition[0] + a <= 7 and queenPosition[1] - b >= 0):
            if (treeNode.data[queenPosition[1] - b][queenPosition[0] + a] == "ES1"):
                availablePath.append((queenPosition[0] + a, queenPosition[1] - b))
                a += 1
                b += 1
            else:
                collidedPath.append((queenPosition[0] + a, queenPosition[1] - b))
                break
        c = 1
        d = 1
        while (queenPosition[0] - c >= 0 and queenPosition[1] - d >= 0):
            if (treeNode.data[queenPosition[1] - d][queenPosition[0] - c] == "ES1"):
                availablePath.append((queenPosition[0] - c, queenPosition[1] - d))
                c += 1
                d += 1
            else:
                collidedPath.append((queenPosition[0] - c, queenPosition[1] - d))
                break

    return availablePath, collidedPath

def pawnPromotion(whiteOrBlack):
    if (whiteOrBlack == True):#True = white false = black
        while True:
            a = input("What chess do you want your pawn to be promoted? Queen Knight Bishop Rook")
            if (a == "Queen"):
                return "wQ1"
            elif (a == "Knight"):
                return "wH1"
            elif (a == "Bishop"):
                return "wB1"
            elif (a == "Rook"):
                return "wR1"
            else:
                print("Invalid Input")
    else:
        while True:
            a = input("What chess do you want your pawn to be promoted? You can choose Queen, Knight, Bishop or Rook:   ")
            if (a == "Queen"):
                return "bQ1"
            elif (a == "Knight"):
                return "bH1"
            elif (a == "Bishop"):
                return "bB1"
            elif (a == "Rook"):
                return "bR1"
            else:
                print("Invalid Input")

def pawnRule(pawnPosition, treeNode, whiteOrBlack):
    collidedPath = []
    availablePath = []
    if (whiteOrBlack==True):                       #white = true
        if (pawnPosition[1]==6):
            if (treeNode.data[pawnPosition[1]-1][pawnPosition[0]]=="ES1"):
                availablePath.append((pawnPosition[0], pawnPosition[1]-1))
                if (treeNode.data[pawnPosition[1]-2][pawnPosition[0]]=="ES1"):
                    availablePath.append((pawnPosition[0], pawnPosition[1] - 2))

            if (pawnPosition[0]==0):
                if(treeNode.data[pawnPosition[1]-1][pawnPosition[0]+1]!="ES1"):
                    collidedPath.append((pawnPosition[0]+1,pawnPosition[1]-1))

            elif(pawnPosition[0]==7):
                if (treeNode.data[pawnPosition[1] - 1][pawnPosition[0] - 1] != "ES1"):
                    collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] - 1))
            else:
                if (treeNode.data[pawnPosition[1] - 1][pawnPosition[0] - 1] != "ES1"):
                    collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] - 1))
                if (treeNode.data[pawnPosition[1] - 1][pawnPosition[0] + 1] != "ES1"):
                    collidedPath.append((pawnPosition[0] + 1, pawnPosition[1] - 1))
        if (pawnPosition[1]!=6):
            if (pawnPosition[1]-1>=0):
                if (treeNode.data[pawnPosition[1]-1][pawnPosition[0]]=="ES1"):
                    availablePath.append((pawnPosition[0], pawnPosition[1]-1))
                if (pawnPosition[0] == 0):
                    if (treeNode.data[pawnPosition[1] - 1][pawnPosition[0] + 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] + 1, pawnPosition[1] - 1))

                elif (pawnPosition[0] == 7):
                    if (treeNode.data[pawnPosition[1] - 1][pawnPosition[0] - 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] - 1))
                else:
                    if (treeNode.data[pawnPosition[1] - 1][pawnPosition[0] - 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] - 1))
                    if (treeNode.data[pawnPosition[1] - 1][pawnPosition[0] + 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] + 1, pawnPosition[1] - 1))



    else:
        if (pawnPosition[1]==1):
            if (treeNode.data[pawnPosition[1]+1][pawnPosition[0]]=="ES1"):
                availablePath.append((pawnPosition[0], pawnPosition[1]+1))
                if (treeNode.data[pawnPosition[1]+2][pawnPosition[0]]=="ES1"):
                    availablePath.append((pawnPosition[0], pawnPosition[1] + 2))

            if (pawnPosition[0]==0):
                if(treeNode.data[pawnPosition[1]+1][pawnPosition[0]+1]!="ES1"):
                    collidedPath.append((pawnPosition[0]+1,pawnPosition[1]+1))
            elif(pawnPosition[0]==7):
                if (treeNode.data[pawnPosition[1] + 1][pawnPosition[0] - 1] != "ES1"):
                    collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] + 1))
            else:
                if (treeNode.data[pawnPosition[1] + 1][pawnPosition[0] + 1] != "ES1"):
                    collidedPath.append((pawnPosition[0] + 1, pawnPosition[1] + 1))
                if (treeNode.data[pawnPosition[1] + 1][pawnPosition[0] - 1] != "ES1"):
                    collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] + 1))
        if (pawnPosition[1]!=1):
            if (pawnPosition[1]+1<=7):
                if (treeNode.data[pawnPosition[1]+1][pawnPosition[0]]=="ES1"):
                    availablePath.append((pawnPosition[0], pawnPosition[1]+1))
                if (pawnPosition[0] == 0):
                    if (treeNode.data[pawnPosition[1] + 1][pawnPosition[0] + 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] + 1, pawnPosition[1] + 1))
                elif (pawnPosition[0] == 7):
                    if (treeNode.data[pawnPosition[1] + 1][pawnPosition[0] - 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] + 1))
                else:
                    if (treeNode.data[pawnPosition[1] + 1][pawnPosition[0] + 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] + 1, pawnPosition[1] + 1))
                    if (treeNode.data[pawnPosition[1] + 1][pawnPosition[0] - 1] != "ES1"):
                        collidedPath.append((pawnPosition[0] - 1, pawnPosition[1] + 1))
    return availablePath, collidedPath



def collisionHappened():
    return

def computerMove(treeNode, whiteOrBlack, wHash, bHash):
    availableChess = []
    thePosofChess = []
    cpuAllPath = []

    promotionChoice = ['Q', 'R', 'B', 'K']
    cpuIsTheChessAPawn = False
    for i in range(8):
        for j in range(8):
            if(whiteOrBlack==True):
                if (treeNode.data[i][j][0]=='w'):
                    availableChess.append(treeNode.data[i][j])
                    thePosofChess.append([i,j])
            else:
                if (treeNode.data[i][j][0]=='b'):
                    availableChess.append(treeNode.data[i][j])
                    thePosofChess.append([i, j])

    for i in range(len(availableChess)):
        if (availableChess[i][1] == 'R'):
            print("Rook rule")
            cpuIsTheChessAPawn = False
            possiblePath, collidedPath = rookRule((column, row), currentChessboard)
            for j in possiblePath:
                cpuAllPath.append(j)
            for j in collidedPath:
                cpuAllPath.append(j)
            for k in range(len(cpuAllPath)):
                tmpNode = treeNode.data
                tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == availableChess[i]
                tmpNode[thePosofChess[i][0]][thePosofChess[i][1]] == "ES1"
                treeNode.add_child(chess(tmpNode))



        elif (availableChess[i][1] == 'H'):
            print("Knight rule")
            cpuIsTheChessAPawn = False
            possiblePath, collidedPath = knightRule((column, row), currentChessboard)
            for j in possiblePath:
                cpuAllPath.append(j)
            for j in collidedPath:
                cpuAllPath.append(j)
            for k in range(len(cpuAllPath)):
                tmpNode = treeNode.data
                tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == availableChess[i]
                tmpNode[thePosofChess[i][0]][thePosofChess[i][1]] == "ES1"
                treeNode.add_child(chess(tmpNode))

        elif (availableChess[i][1] == 'P'):
            print("Pawn rule")
            cpuIsTheChessAPawn = True
            possiblePath, collidedPath = pawnRule((column, row), currentChessboard, whiteTurn)
            for j in possiblePath:
                cpuAllPath.append(j)
            for j in collidedPath:
                cpuAllPath.append(j)
            for k in range(len(cpuAllPath)):
                if (cpuAllPath[k][0]==7):
                    for l in promotionChoice:
                        tmpNode = treeNode.data
                        if (l =='Q'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "bQ1"
                        elif(l=='B'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "bB1"
                        elif (l == 'R'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "bR1"
                        elif (l == 'K'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "bH1"
                        tmpNode[thePosofChess[i][0]][thePosofChess[i][1]] == "ES1"#cpu promotion not yet done
                        treeNode.add_child(chess(tmpNode))
                elif (cpuAllPath[k][0]==0):
                    for l in promotionChoice:
                        tmpNode = treeNode.data
                        if (l == 'Q'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "wQ1"
                        elif (l == 'B'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "wB1"
                        elif (l == 'R'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "wR1"
                        elif (l == 'K'):
                            tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == "wH1"
                        tmpNode[thePosofChess[i][0]][thePosofChess[i][1]] == "ES1"
                        treeNode.add_child(chess(tmpNode))
                else:
                    tmpNode = treeNode.data
                    tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == availableChess[i]
                    tmpNode[thePosofChess[i][0]][thePosofChess[i][1]] == "ES1"
                    treeNode.add_child(chess(tmpNode))

        elif (availableChess[i][1] == 'K'):
            print("King rule")
            cpuIsTheChessAPawn = False
            possiblePath, collidedPath = kingRule((column, row), currentChessboard)
            for j in possiblePath:
                cpuAllPath.append(j)
            for j in collidedPath:
                cpuAllPath.append(j)
            for k in range(len(cpuAllPath)):
                tmpNode = treeNode.data
                tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == availableChess[i]
                tmpNode[thePosofChess[i][0]][thePosofChess[i][1]] == "ES1"
                treeNode.add_child(chess(tmpNode))


        elif (availableChess[i][1] == 'Q'):
            print("Queen rule")
            cpuIsTheChessAPawn = False
            possiblePath, collidedPath = queenRule((column, row), currentChessboard)
            for j in possiblePath:
                cpuAllPath.append(j)
            for j in collidedPath:
                cpuAllPath.append(j)
            for k in range(len(cpuAllPath)):
                print(k)
                tmpNode = treeNode.data
                tmpNode[cpuAllPath[k][1]][cpuAllPath[k][0]] == availableChess[i]
                tmpNode[thePosofChess[i][0]][thePosofChess[i][1]] == "ES1"
                treeNode.add_child(chess(tmpNode))



    return treeNode

while not state:                                #ask whether the player will play black or white
        whoStart = input("Please choose your desire chess colour first: White / Black   ")
        if whoStart == "White" or whoStart =="white":
            whosTurn = "Player"
            whiteTurn = True
            blackTurn = False
            state = True;
        elif whoStart =="Black" or whoStart == "black":
            whosTurn = "Computer"
            state = True
            whiteTurn = True
            blackTurn = False
        else:
            print("Unknown Input")
            state = False
parentChessboard = initialiseStartBoard()
currentChessboard = parentChessboard

while notCheckmated:
    print("    0    1    2    3    4    5    6    7")
    for i in range(8):
        print(i, " ", end='')

        for j in range(8):
            if (currentChessboard.data[i][j] == "ES1"):
                print(currentChessboard.data[i][j], " ", end='')
            else:
                print(currentChessboard.data[i][j], " ", end='')
            if(j==7):
                print()
    if (whosTurn == "Player"):
        print("------Player's Turn------")
        column, row = getUserInput(currentChessboard, whiteTurn, blackTurn)
        response = getUserResponse()
        while (response == 'Y' or response == 'y'):
            column, row = getUserInput(currentChessboard, whiteTurn, blackTurn)
            response = getUserResponse()

        if (currentChessboard.data[row][column][1] == 'R'):
            print("Rook rule")
            isThisChessAPawn = False
            possiblePath, collidedPath = rookRule((column, row), currentChessboard)

        elif (currentChessboard.data[row][column][1] == 'H'):
            print("Knight rule")
            isThisChessAPawn = False
            possiblePath, collidedPath = knightRule((column, row), currentChessboard)

        elif (currentChessboard.data[row][column][1] == 'P'):
            print("Pawn rule")
            isThisChessAPawn = True
            possiblePath, collidedPath = pawnRule((column, row), currentChessboard, whiteTurn)
        elif (currentChessboard.data[row][column][1] == 'K'):
            print("King rule")
            isThisChessAPawn = False
            possiblePath, collidedPath = kingRule((column, row), currentChessboard)

        elif (currentChessboard.data[row][column][1] == 'Q'):
            print("Queen rule")
            isThisChessAPawn = False
            possiblePath, collidedPath = queenRule((column, row), currentChessboard)

        moveCol, moveRow = getMovePos(currentChessboard, whiteTurn, blackTurn)
        moveRes = getUserResponse()
        combinedPath = possiblePath + collidedPath
        while True:
            while (moveRes == 'Y' or moveRes == 'y' or notinrange):
                moveCol, moveRow = getMovePos(currentChessboard, whiteTurn, blackTurn)
                moveRes = getUserResponse()
                notinrange = False

            iter = 0
            for i in combinedPath:
                print("in Combined Path")
                print(i)
                iter += 1
                if (moveCol==i[0]  and moveRow==i[1]  ):
                    if (currentChessboard.data[moveRow][moveCol] == "ES1"):
                        if (isThisChessAPawn ==False):
                            print("Pass through first")
                            temp = currentChessboard.data[row][column]
                            currentChessboard.data[row][column] = "ES1"
                            currentChessboard.data[moveRow][moveCol] = temp
                            parentChessboard.add_child(currentChessboard)
                            notinrange = False
                            break
                        elif (isThisChessAPawn == True):
                            if(moveRow==0 or moveRow == 7):
                                print("Promotion")
                                temp = currentChessboard.data[row][column]
                                currentChessboard.data[moveRow][moveCol] = pawnPromotion(whiteTurn)
                                currentChessboard.data[row][column] = "ES1"
                                parentChessboard.add_child(currentChessboard)
                                notinrange = False
                                break
                            else:
                                print("Normal Pawn movement")
                                temp = currentChessboard.data[row][column]
                                currentChessboard.data[row][column] = "ES1"
                                currentChessboard.data[moveRow][moveCol] = temp
                                parentChessboard.add_child(currentChessboard)
                                notinrange = False
                                break




                    else:
                        if (currentChessboard.data[moveRow][moveCol][1] == 'K'):
                            notCheckmated = False
                            notinrange = False
                            break
                        else :
                            if(isThisChessAPawn == True):
                                if((moveRow==0 or moveRow==7)):
                                    print("Promotion")
                                    currentChessboard.data[moveRow][moveCol] = pawnPromotion(whiteTurn)
                                    currentChessboard.data[row][column] = "ES1"
                                    parentChessboard.add_child(currentChessboard)
                                    notinrange = False
                                    break
                                else:
                                    print("BUG")
                                    temp = currentChessboard.data[row][column]
                                    currentChessboard.data[row][column] = "ES1"
                                    currentChessboard.data[moveRow][moveCol] = temp

                                    parentChessboard.add_child(currentChessboard)
                                    notinrange = False



                            else:
                                print("Pass through second")

                                temp = currentChessboard.data[row][column]
                                currentChessboard.data[row][column] == "ES1"
                                currentChessboard.data[moveRow][moveCol] = temp
                                parentChessboard.add_child(currentChessboard)
                                notinrange = False
                                break
                else:

                    notinrange = True

            if (iter == len(combinedPath) and notinrange==True):
                print("not in range!")
                continue
            else:
                print("In range")
                break
        print("Outside")
        whosTurn = "Computer"
        whiteTurn = not whiteTurn
        blackTurn = not blackTurn
        continue





    else:
        print("------Computer's Turn------")
        #print(computerMove(currentChessboard, whiteTurn, whiteEvaluationHash, blackEvaluationHash))
        currentTree= computerMove(currentChessboard, whiteTurn, whiteEvaluationHash, blackEvaluationHash)
        #break
        for i in range(len(currentTree.child)):
            currentTree.child[i].add_child(computerMove(currentTree.child[i],not whiteTurn, whiteEvaluationHash, blackEvaluationHash))
        for i in range(len(currentTree.child)):
            for j in range(len(currentTree.child[i].child)):
                currentTree.child[i].child[j].add_child(computerMove(currentTree.child[i].child[j], whiteTurn, whiteEvaluationHash, blackEvaluationHash))
        val, bestmove = minimax(currentTree, 2, True, whiteTurn, whiteEvaluationHash, blackEvaluationHash, -1000000, 1000000)
        bestmove = currentChessboard.data
        whosTurn = "Player"
        whiteTurn = not whiteTurn
        blackTurn = not blackTurn
        continue




