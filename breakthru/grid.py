grid = [['-'] * 11 for n in range(11)]
for row in range(len(grid)):
    for column in range(len(grid[row])):
        if row == 0 or row == 10:
            grid[row][column] = '*'
        elif column == 0 or column == 10:
            grid[row][column] = '*'
        if row in {1, 9}:
            grid[row][3:8] = ['S' for n in range(5)]
        elif row in {3, 4, 5, 6, 7} and column in {1, 9}:
            grid[row][column] = 'S'
        elif row in {3, 7}:
            grid[row][4:7] = ['G' for n in range(3)]
        elif row in {4, 5, 6} and column in {3, 7}:
            grid[row][column] = 'G'
grid[5][5] = 'K'

margin_side = [0 for n in range(1, 12)]
for i in range(1, 12):
    margin_side[i - 1] = 12 - i


# like in chess
margin_down = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
margin_side = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
# like matrices
margin_down_num = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
margin_side_num = margin_down_num


if __name__ == "__main__":
    for i in grid:
        print(i)
    # print(margin_side)
