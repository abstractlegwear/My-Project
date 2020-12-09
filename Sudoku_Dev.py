import numpy as np

sudoku = np.array([[8, 0, 0, 2, 6, 0, 0, 0, 4],
                   [0, 1, 0, 0, 8, 3, 0, 6, 2],
                   [2, 6, 0, 7, 4, 0, 1, 0, 0],
                   [0, 0, 6, 0, 7, 8, 2, 1, 0],
                   [0, 0, 4, 0, 3, 2, 0, 8, 0],
                   [0, 2, 0, 0, 0, 9, 0, 0, 7],
                   [7, 4, 0, 0, 1, 6, 0, 2, 0],
                   [0, 3, 0, 8, 0, 4, 0, 7, 1],
                   [0, 0, 1, 0, 2, 7, 0, 0, 6]])

sudoku_answer = np.array([[8, 9, 7, 2, 6, 1, 3, 5, 4],
                          [4, 1, 5, 9, 8, 3, 7, 6, 2],
                          [2, 6, 3, 7, 4, 5, 1, 9, 8],
                          [3, 5, 6, 4, 7, 8, 2, 1, 9],
                          [9, 7, 4, 1, 3, 2, 6, 8, 5],
                          [1, 2, 8, 6, 5, 9, 4, 3, 7],
                          [7, 4, 9, 5, 1, 6, 8, 2, 3],
                          [6, 3, 2, 8, 9, 4, 5, 7, 1],
                          [5, 8, 1, 3, 2, 7, 9, 4, 6]])



# creates a dictionary with the coordinates of every empty space 0 being a key
# each key has a list of numbers 1-9, if a number is in same row/column/square, remove from list
# if a key has only one number in its list, then it's correct


# ----------------------------------------------------------------------------------------------------------------------


def create_keys(n):
    c = list(zip(*np.where(n == 0)))  # list of empty space coordinates
    p = {}  # possible values for empty spaces
    i = 0  # i is the index of the elements in list coordinates
    for _ in range(len(c)):
        p[c[i]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        i += 1
    return p


coordinates = list(zip(*np.where(sudoku == 0)))  # list of coordinates for empty spaces
possible_values = create_keys(sudoku)  # dictionary for the possible values of the empty spaces


# ----------------------------------------------------------------------------------------------------------------------


def sudoku_square_format(n):  # rearranging sudoku so that every row contains all the values in each 3x3 square
    n2 = n.copy()  # avoids error where original sudoku array is changed
    a, b = 0, 1
    # found a trick in swapping certain elements that successfully rearranges into square format
    for _ in range(3):
        n2[a, 3:6], n2[b, :3] = n2[b, :3], n2[a, 3:6].copy()
        b += 1
        n2[a, 6:], n2[b, :3] = n2[b, :3], n2[a, 6:].copy()
        a += 1
        n2[a, 6:], n2[b, 3:6] = n2[b, 3:6], n2[a, 6:].copy()
        a += 2
        b += 2
    return n2


def check_for_possible_values(n):  # n is the index for coordinates

    # checks for horizontal values
    row = coordinates[n][0]
    column = 0
    for _ in range(9):
        if sudoku[row, column] != 0:  # a number on the puzzle in same row as empty space being tested
            # if number being tested is in list of possible values for the empty space, remove from that list
            if sudoku[row, column] in possible_values[coordinates[n]]:
                possible_values[coordinates[n]].remove(sudoku[row, column])
        column += 1

    # checks for vertical values
    column = coordinates[n][1]
    row = 0
    for _ in range(9):
        if sudoku[row, column] != 0:
            if sudoku[row, column] in possible_values[coordinates[n]]:
                possible_values[coordinates[n]].remove(sudoku[row, column])
        row += 1

    # checks for square values
    sudoku_square = sudoku_square_format(sudoku)  # uses square format
    row = (coordinates[n][1] // 3) + ((coordinates[n][0] // 3) * 3)  # found trick to convert coordinate to row number
    column = 0
    for _ in range(9):
        if sudoku_square[row, column] != 0:
            if sudoku_square[row, column] in possible_values[coordinates[n]]:
                possible_values[coordinates[n]].remove(sudoku_square[row, column])
        column += 1

    return possible_values[coordinates[n]]


# ----------------------------------------------------------------------------------------------------------------------


# takes a certain row and finds all the possible values for empty spaces in it, and if there are any
# possible values that appear only once then it's an answer


def rowcol_solve(n, m, axis):  # n is the row number, m is sudoku array
    pos_values = np.array([0, 0, 0, 0, 0, 0, 0, 0, 0])  # array of possible values
    index = 0
    coord_list = []  # list of empty space coords in row n
    for i in range(len(coordinates)):
        # finds empty spaces in that row and their possible values
        if coordinates[index][axis] == n:
            coord_list.append(coordinates[index])
            a = possible_values[coordinates[index]].copy()
            for _ in range(9 - len(possible_values[coordinates[index]])):  # changes length of list to 9 elements
                a.append(0)
            k = np.array(a)
            pos_values = np.vstack((pos_values, k))  # adds possible values to array
        index += 1
    pos_values = np.vstack((pos_values, m[n]))
    pos_values = np.vstack((pos_values, m[n]))
    pos_values = np.delete(pos_values, 0, axis=0)  # removes redundant first row
    for i in range(0, 10):  # finds which number(s) is unique and solves it in actual sudoku puzzle
        if np.count_nonzero(pos_values == i) == 1:
            x = np.where(pos_values == i)[0]  # finds which row the unique number appears in
            x1 = x[0]
            m[coord_list[x1]] = i
            if coord_list[x1] in possible_values:
                del possible_values[coord_list[x1]]
            if coord_list[x1] in coordinates:
                coordinates.remove(coord_list[x1])


# ----------------------------------------------------------------------------------------------------------------------


def sudoku_check_answer(a, b):  # this will not be part of the final code, it's just to help debug
    for i in range(9):
        for k in range(9):
            if a[i, k] != 0 and a[i, k] != b[i, k]:
                return False
    return True


# process of solving the sudoku by constantly reducing the number of possible values for each empty space until
# only one is left
counter = np.count_nonzero(sudoku == 0)
print(counter)
while np.count_nonzero(sudoku == 0) > 0:
    coord_index = 0  # index for coordinate list
    while coord_index < len(coordinates):
        check_for_possible_values(coord_index)
        if len(possible_values[coordinates[coord_index]]) == 1:  # if a solution is found
            sudoku[coordinates[coord_index]] = possible_values[coordinates[coord_index]][0]  # change sudoku puzzle
            del possible_values[coordinates[coord_index]]  # clean up
            del coordinates[coord_index]  # clean up
            coord_index = 0
        coord_index += 1
    for i in range(9):
        rowcol_solve(i, sudoku, 0)
    if counter == np.count_nonzero(sudoku == 0):
        for i in range(9):
            rowcol_solve(i, sudoku, 0)
    counter = np.count_nonzero(sudoku == 0)  # sees if code is stuck
    print(np.count_nonzero(sudoku == 0))
    if not sudoku_check_answer(sudoku, sudoku_answer):
        break

print(sudoku)

"""
IMPORTANT 
IT WOOOOOOOOORKS

\\\\error: 
\\\\sudoku[3, 1] solves incorrectly to a 9, not sure why

////when printing out coordinates and possible_values, (3, 1) still exists
////so, error might be due to not deleting (3, 1) when doing row_solve()

////update: problem appears to be that coordinate (3, 1) was skipped over, as it was the only coordinate to not be 
////affected by check_for_possible_values(), being [1, 2, 3, ... 9] until it magically disappears

\\\\update: problem solved, fixed by restarting from the first empty space after finding a solution, coordinate
\\\\(3, 1) would get skipped without this

////error: dammit (8, 6) broke for some reason, it contains possible values [1, 7] and should solve to 7 
////but instead solves to 1, (8, 7) solves correctly to 1, not sure how this happened, will continue tmrw

////update: reason for error found, only occurs if empty space is last one in its row
////row_solve() is happening before check_for_possible_values() could 

\\\\possible solution:
\\\\no idea, need sleep

IT WOOOOOORKS

error: (6, 8) solved to 8 instead of 3

error: can only solve easy problems

problem: only has row_solve(), need to add column_solve() and square_solve(), and for even harder puzzles
have to add more advanced techniques
"""
