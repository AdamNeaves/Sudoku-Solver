
class SudokuBoard:

    def __init__(self):

        # TILE LAYOUT
        # n-10|n-9 |n-8
        # n-1 | n  |n+1
        # n+8 |n+9 |n+10

        # 00|01|02||03|04|05||06|07|08
        # 09|10|11||12|13|14||15|16|17
        # 18|19|20||21|22|23||24|25|26
        # ========++========++========
        # 27|28|29|30
        # 36|37
        #
        #
        #

        self.all_tiles = []
        for x in range(0, 9*9):
            self.all_tiles.append(SudokuTile())

        self.all_rows = [9]
        self.all_cols = [9]
        self.all_sqrs = [9]

        for x in range(0, 9):
            row = []
            col = []
            sqr = []
            for y in range(0, 9):
                row.append(self.all_tiles[(x*9)+y])
                col.append(self.all_tiles[(x+(y*9))])
            sqr_cent = (x*3)


class SudokuTile:

    def __init__(self):
        self.pos_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.val = ''

    def set_val(self, val):
        self.val = val
