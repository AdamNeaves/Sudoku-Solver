
class SudokuBoard:

    def __init__(self, file):

        # TILE LAYOUT
        # n-10|n-9 |n-8
        # n-1 | n  |n+1
        # n+8 |n+9 |n+10

        # 00|01|02||03|04|05||06|07|08
        # 09|10|11||12|13|14||15|16|17
        # 18|19|20||21|22|23||24|25|26
        # ========++========++========
        # 27|28|29||30|31|32||33|34|35
        # 36|37|38||39|40|41||42|43|44
        # 45|46|47||48|49|50||51|52|53
        # ========++==================
        # 54|55|56||57|58|59||60|61|62
        # 63|64|65||66|67|68||69|70|71
        #
        self.num_filled = 0
        self.all_tiles = []
        for x in range(0, 9*9):
            self.all_tiles.append(SudokuTile(num=x))

        self.all_rows = []
        self.all_cols = []
        self.all_sqrs = []

        for x in range(0, 9):
            row = []
            col = []
            sqr = []
            for y in range(0, 9):
                row.append(self.all_tiles[(x*9)+y])
                col.append(self.all_tiles[(x+(y*9))])
            self.all_rows.append(row)
            self.all_cols.append(row)
            if x < 3:
                sqr_cent = (x*3)+10
            elif x < 6:
                sqr_cent = (x*3)+28
            else:
                sqr_cent = (x*3)+46

            sqr.append(self.all_tiles[sqr_cent-10])
            sqr.append(self.all_tiles[sqr_cent-9])
            sqr.append(self.all_tiles[sqr_cent-8])
            sqr.append(self.all_tiles[sqr_cent-1])
            sqr.append(self.all_tiles[sqr_cent])
            sqr.append(self.all_tiles[sqr_cent+1])
            sqr.append(self.all_tiles[sqr_cent+8])
            sqr.append(self.all_tiles[sqr_cent+9])
            sqr.append(self.all_tiles[sqr_cent+10])

            self.all_sqrs.append(sqr)

        if file:
            with open(file) as file:
                for count, line in enumerate(file):
                    for v_count, val in enumerate(line):
                        if val.isdigit():
                            tile = self.all_rows[count][v_count]
                            self.set_tile_val(tile, int(val))

    def remove_pos_from_set(self, group, val):
        for tile in group:
            if val in tile.pos_vals:
                tile.pos_vals.remove(val)
                if len(tile.pos_vals) == 1:
                    self.set_tile_val(tile, tile.pos_vals[0])
                elif len(tile.pos_vals) == 0:
                    # PROBLEM OCCUR
                    return

    def set_tile_val(self, tile, val):
        tile.set_val(val)
        self.num_filled += 1
        print("NUMBER FILLED: {}".format(self.num_filled))
        for row in self.all_rows:  # remove val from possible vals of all cells in row
            if tile in row:
                for r_tile in row:
                    if val in r_tile.pos_vals:
                        r_tile.pos_vals.remove(val)
                        if len(r_tile.pos_vals) == 1:  # if only one left in the list of possible vals
                            self.set_tile_val(r_tile, r_tile.pos_vals[0])
                break
        for col in self.all_cols:  # remove val from possible vals of all cells in column
            if tile in col:
                for c_tile in col:
                    if val in c_tile.pos_vals:
                        c_tile.pos_vals.remove(val)
                        if len(c_tile.pos_vals) == 1:
                            self.set_tile_val(c_tile, c_tile.pos_vals[0])
                break
        for sqr in self.all_sqrs:  # remove val from possible vals of all cells in square
            if tile in sqr:
                for s_tile in sqr:
                    if val in s_tile.pos_vals:
                        s_tile.pos_vals.remove(val)
                        if len(s_tile.pos_vals) == 1:
                            self.set_tile_val(s_tile, s_tile.pos_vals[0])
                break

    def check_group(self, groups, tile):
        for group in groups:
            if tile in group:
                pos_vals = set(tile.pos_vals)
                for g_tile in group:
                    if g_tile is not tile:
                        pos_vals = pos_vals - set(g_tile.pos_vals)
                # print("FROM GROUP, POSIBILITIES FOR TILE {} ARE {}".format(tile.number, pos_vals))
                if len(pos_vals) == 1:
                    self.set_tile_val(tile, pos_vals.pop())
                break

    def start_solve(self):
        # check for tile with only one possibility (done in the set thing?)-
        # check for tile where its the only one that can be a certain value
        start_filled = self.num_filled
        for tile in self.all_tiles:
            # for each tile
            if tile.get_val() != 0:
                continue
            # check if its only one in its row/column/square that has a certain value in its pos_vals
            self.check_group(self.all_rows, tile)
            self.check_group(self.all_cols, tile)
            self.check_group(self.all_sqrs, tile)
        if self.num_filled == start_filled:
            print("NONE CHANGED THIS TURN. NEED TO GUESS")
            return False
        else:
            return True

    def print_grid(self):
        for count, row in enumerate(self.all_rows):
            if count % 3:
                self.print_line(row)
            else:
                print('+=+========+=+========+=+========+=+')
                self.print_line(row)

        print('+=+========+=+========+=+========+=+')

    def print_line(self, row):
        line = ''
        for count, tile in enumerate(row):
            if count % 3:
                line += "|"
            else:
                line += " # "
            val = tile.get_val()
            if val:
                line += "{: 2}".format(tile.get_val())
            else:
                line += "  "
        line += " # "
        print(line)


class SudokuTile:

    def __init__(self,  num, val=None):
        self.number = num
        if val is not None:
            self.val = val
            self.pos_vals = []
        else:
            self.pos_vals = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            self.val = None

    def set_val(self, val):
        if val in self.pos_vals:
            self.val = val
            self.pos_vals = []
        else:
            # hmmm...
            self.val = val
            pass

    def get_val(self):
        if self.val:
            return self.val
        else:
            return 0


def solve_board(board):
    while board.num_filled < 81:
        changed = board.start_solve()
        if not changed:
            return False, board
    return True, board


if __name__ == "__main__":
    board = SudokuBoard("./Boards/test_board.txt")
    board.print_grid()
    solved, new_board = solve_board(board)
    if solved:
        print("SOLVED:")
        new_board.print_grid()
        exit(0)
    else:
        pass
        # save current board
        # try a tile that has only 2 options
            # if solved, sorted
            # if gets to a point where it doesnt work (tile given a pos list with no items)
