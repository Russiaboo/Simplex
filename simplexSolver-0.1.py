# Simplex Solver
# By Howard Selden V, All Rights Reserved

import numpy as np

def simplex():
    # the objective function
    objFunc = -np.array([20, 15, 50, 10, 19, 10, 4, 22]) #-np.array(eval(input("What are the coefficients of x in the objective function? Format as [1, 2, 3...]\n*They all should be positive\n")))
    
    # constraint matrix
    numVariables = objFunc.size
    numConstraints = 8 #int(input("How many constraints are there?\n"))
    A = np.zeros((numConstraints, numVariables))
    #for i in range(numConstraints):
    #    A[i] = np.array(eval(input(f"What are the coefficients of x in row {i + 1}? Format as [1, 2, 3...]\n")))
    A[0] = [112, 74, 341, 128, 95, 32, 45, 250]
    A[1] = [22.5, 6.2, 22, 4.7, 8.8, 0.7, 0.8, 17.9]
    A[2] = [0, 0.1, 62, 12, 4.8, 4.9, 8.1, 0]
    A[3] = [1.9, 5, 1.4, 9, 4.4, 0.3, 0.4, 17.9]
    A[4] = [0, 0, 15.5, 9.8, 0, 2, 0, 0]
    A[5] = [66, 65, 5, 4.5, 34, 1, 0, 304]
    A[6] = [28.9, 7.9, -33.8, -6, 6.5, -4, -7.1, 17.9]
    A[7] = [-17.4, 7.3, -18.2, 19.6, 3.1, 0.1, 0.3, 30.4]

    # slack identity
    slack = np.eye(numConstraints)
    slack = np.vstack([np.zeros(numConstraints), slack])
        
    # z column
    zColumn = np.vstack(np.hstack([[1], np.zeros(numConstraints)]))

    # RHS column
    rhsColumn = np.vstack([0, 3646, 319, 456, 101, 50, 2300, 0, 0]) #np.vstack(np.hstack([[0], eval(input("Going from top to bottom, what are the values of the right hand side? Format as [1, 2, 3...]\n*Excluding the objective function\n"))]))

    # RT column
    rtColumn = np.vstack(np.zeros(numConstraints + 1))

    # form into tableau
    tableau = np.vstack([objFunc, A])
    tableau = np.hstack([zColumn, tableau, slack, rhsColumn])

    # BV column
    bvColumn = np.vstack(["z"])
        
    # header
    header = ["z"]
    for i in range(numVariables):
        header = np.hstack([header, [f"x{i + 1}"]])
    for i in range(numConstraints):
        header = np.hstack([header, [f"s{i + 1}"]])
        bvColumn = np.vstack([bvColumn, [f"s{i + 1}"]])

    # display stuff
    def updateDisplay():
        print("Tableau:\n", tableau, "\nBV:")
        for row in range(tableau.shape[0]):
            print(bvColumn[row], " = ", tableau[row, -1])
        print("RT:\n", rtColumn)
    updateDisplay()

    multdiv = 0
    arith = 0

    # simplex function
    iteration = 0
    while iteration < 100:
        iteration += 1
        
        # find lowest value and select that column
        minVal = 0.0
        minValColIn = 0
        for column in range(tableau.shape[1] - 1):
            if tableau[0, column] < minVal:
                minVal = tableau[0, column]
                minValColIn = column           
        if minVal == 0.0:
            updateDisplay()
            print(f"Number of arithmetic operations: {arith}\n",
                  f"Number of multiplications/divisions: {multdiv}")
            # for row in range(8):
                # if type(eval(bvColumn[row])) == "Variable":
                    # print("yippee")
            
            # intellectual property of Josette Frazell      
            x1 = float(input('x1: '))
            x2 = float(input('x2: '))
            x3 = float(input('x3: '))
            x4 = float(input('x4: '))
            x5 = float(input('x5: '))
            x6 = float(input('x6: '))
            x7 = float(input('x7: '))
            x8 = float(input('x8: '))

            Calories = 112*x1 + 74*x2 + 341*x3 + 138*x4 + 95*x5 + 32*x6 + 45*x7 + 250*x8
            Protein = 22.5*x1 + 6.2*x2 + 22*x3 + 4.7*x4 + 8.8*x5 + 0.7*x6 + 0.8*x7 + 17.9*x8
            Carbs = 0.1*x2 + 62*x3 + 12*x4 + 4.8*x5 + 4.9*x6 + 8.1*x7
            Fat = 1.9*x1 + 5*x2 + 1.4*x3 +9*x4 + 4.4*x5 + 0.3*x6 + 0.4*x7 + 17.9*x8
            Fiber = 15.5*x3 + 9.8*x4 + 2*x6
            Sodium = 66*x1 + 65*x2 + 5*x3 + 4.5*x4 + 34*x5 + x6 + 304*x8

            print(f'Calories = {Calories}\n'+
                f'Protein = {Protein}\n'+
                f'Carbs = {Carbs}\n'+
                f'Fat = {Fat}\n'+
                f'Fiber = {Fiber}\n'+
                f'Sodium = {Sodium}')
            # intellectual property of Josette Frazell
            
            print("DONE")
            break
        
        # ratio test and selct row
        for row in range(tableau.shape[0] - 1):
            row += 1
            if tableau[row, minValColIn] <= 0.0:
                rtColumn[row] = np.inf
            else:
                rtColumn[row] = np.divide(tableau[row, -1], tableau[row, minValColIn])
                multdiv += 1
        minRatio = np.inf
        minRatioRowIn = 0
        for row in range(tableau.shape[0] - 1):
            row += 1
            if rtColumn[row] < minRatio:
                minRatio = rtColumn[row]
                minRatioRowIn = row
        pivotVar = tableau[minRatioRowIn, minValColIn]

        # normalize the row
        for column in range(tableau.shape[1]):
            tableau[minRatioRowIn, column] = np.divide(tableau[minRatioRowIn, column], pivotVar)
            multdiv += 1
            
        # EROs
        for row in range(tableau.shape[0]):
            ratio = tableau[row, minValColIn]
            if row == minRatioRowIn:
                continue
            else:
                for column in range(tableau.shape[1]):
                    tableau[row, column] = tableau[row, column] - (tableau[minRatioRowIn, column] * ratio)
                    arith += 1; multdiv += 1

        # update BVs
        bvColumn[minRatioRowIn] = header[minValColIn]

        # output
        print(f"Iteration {iteration}:")
        print("RT:\n", rtColumn)
        updateDisplay()
        if iteration == 100:
            print("Iterated 100 times. Something is probably wrong.")
            for row in (range(tableau.shape[0])):
                for column in (range(tableau.shape[1])):
                    tableau [row, column] = int(np.round(tableau[row, column]))
                print(bvColumn[row], " = ", tableau[row, -1])
                print(f"row {row + 1}: ", list(tableau[row]))
simplex()          