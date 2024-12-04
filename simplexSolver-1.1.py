# Simplex Solver
# By Howard Selden V, All Rights Reserved

import numpy as np

def simplex():
    # the objective function
    objFunc = -np.array([10, 9, 8, 6, 5, 7]) #-np.array(eval(input("What are the coefficients of x in the objective function? Format as [1, 2, 3...]\n*They all should be positive\n")))
    # constraint matrix
    numVariables = objFunc.size
    numConstraints = 12 #int(input("How many constraints are there?\n"))
    A = np.zeros((numConstraints, numVariables))
    #for i in range(numConstraints):
    #    A[i] = np.array(eval(input(f"What are the coefficients of x in row {i + 1}? Format as [1, 2, 3...]\n")))
    A[0] = [112, 74, 341, 128, 95, 32]
    A[1] = [22.5, 6.2, 22, 4.7, 8.8, 0.7]
    A[2] = [0, 0.1, 62, 12, 4.8, 4.9]
    A[3] = [1.9, 5, 1.4, 9, 4.4, 0.3]
    A[4] = [0, 0, -15.5, -9.8, 0, -2]
    A[5] = [66, 65, 5, 4.5, 34, 1]
    # these rows are for minimum calories, fat, carbs, sodium, and protein rather than just one more than the other for macros
    A[6] = [-22.5, -6.2, -22, -4.7, -8.8, -0.7]
    A[7] = [-112, -74, -341, -138, -95, -32]
    A[8] = [0, -0.1, -62, -12, -4.8, -4.9]
    A[9] = [-1.9, -5, -1.4, -9, -4.4, -0.3]
    A[10] = [-66, -65, -5, -4.5, -34, -1]
    A[11] = [73, 411, 0, 0, 17, 0]

    # slack identity
    slack = np.eye(numConstraints)
    slack = np.vstack([np.zeros(numConstraints), slack])
        
    # z column
    zColumn = np.vstack(np.hstack([[1], np.zeros(numConstraints)]))

    # RHS column
    rhsColumn = np.vstack([0, 3646, 319, 456, 101, -25, 2300, -273, -3146, -410, -81, -500, 300]) #np.vstack(np.hstack([[0], eval(input("Going from top to bottom, what are the values of the right hand side? Format as [1, 2, 3...]\n*Excluding the objective function\n"))]))

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
            print("DONE")
            break
        
        # ratio test and selct row
        for row in range(tableau.shape[0] - 1):
            row += 1
            if tableau[row, minValColIn] <= 0.0:
                rtColumn[row] = np.inf
            else:
                rtColumn[row] = np.divide(tableau[row, -1], tableau[row, minValColIn])
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
            
        # EROs
        for row in range(tableau.shape[0]):
            ratio = tableau[row, minValColIn]
            if row == minRatioRowIn:
                continue
            else:
                for column in range(tableau.shape[1]):
                    tableau[row, column] = tableau[row, column] - (tableau[minRatioRowIn, column] * ratio)

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

            