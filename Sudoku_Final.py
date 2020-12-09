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

print("Type in numbers for each sudoku space from left to right, top to bottom, type 0 for empty spaces")
for i in range(9):
    for k in range(9):
        print(sudoku)
        var = int(input())
        sudoku[i, k] = var
print(sudoku)

# ----------------------------------------------------------------------------------------------------------------------


def create_keys(n):
    c = list(zip(*np.where(n == 0)))
    p = {}
    i = 0
    for _ in range(len(c)):
        p[c[i]] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        i += 1
    return p


coordinates = list(zip(*np.where(sudoku == 0)))
possible_values = create_keys(sudoku)


# ----------------------------------------------------------------------------------------------------------------------


def sudoku_square_format(n):
    n2 = n.copy()
    a, b = 0, 1
    for _ in range(3):
        n2[a, 3:6], n2[b, :3] = n2[b, :3], n2[a, 3:6].copy()
        b += 1
        n2[a, 6:], n2[b, :3] = n2[b, :3], n2[a, 6:].copy()
        a += 1
        n2[a, 6:], n2[b, 3:6] = n2[b, 3:6], n2[a, 6:].copy()
        a += 2
        b += 2
    return n2


def check_for_possible_values(n):

    row = coordinates[n][0]
    column = 0
    for _ in range(9):
        if sudoku[row, column] != 0:
            if sudoku[row, column] in possible_values[coordinates[n]]:
                possible_values[coordinates[n]].remove(sudoku[row, column])
        column += 1

    column = coordinates[n][1]
    row = 0
    for _ in range(9):
        if sudoku[row, column] != 0:
            if sudoku[row, column] in possible_values[coordinates[n]]:
                possible_values[coordinates[n]].remove(sudoku[row, column])
        row += 1

    sudoku_square = sudoku_square_format(sudoku)
    row = (coordinates[n][1] // 3) + ((coordinates[n][0] // 3) * 3)
    column = 0
    for _ in range(9):
        if sudoku_square[row, column] != 0:
            if sudoku_square[row, column] in possible_values[coordinates[n]]:
                possible_values[coordinates[n]].remove(sudoku_square[row, column])
        column += 1

    return possible_values[coordinates[n]]


# ----------------------------------------------------------------------------------------------------------------------


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


counter = np.count_nonzero(sudoku == 0)

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


print(sudoku)
