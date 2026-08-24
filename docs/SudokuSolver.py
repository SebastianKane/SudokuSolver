import copy

class Cell:
    def __init__(self, value=0):
        #The following in_column, in_box and in_row arrays hold references to all the cells in the corresponding group.
        self.in_column=[]
        self.in_row=[]
        self.in_box=[]
        self.value=value
    
    def __str__(self):
        return str(self.value)

    def __int__(self):
        return int(self.value)
    
    def set_value(self, value):
        self.value=value
    
    def possible_values(self):
        column_values=set([int(cell) for cell in self.in_column])
        row_values=set([int(cell) for cell in self.in_row])
        box_values=set([int(cell) for cell in self.in_box])
        return set(range(1,10)) - column_values - row_values - box_values

    def set_column(self, column:list):
        self.in_column=column

    def set_row(self, row:list):
        self.in_row=row

    def set_box(self, box:list):
        self.in_box=box

class Puzzle:
    def __init__(self):
        '''
        Creates a new puzzle object.
        numbers: A 81 digit string that's used to denote a sudoku puzzle read left to right starting at the top going down to the bottom.
        '''
        self.cells = []
        self.solutions=set()

        #Creates 3 lists composed of 9 empty lists for the 9 representives of each group.
        columns = [[] for _ in range(9)]
        rows = [[] for _ in range(9)]
        boxes=[[] for _ in range(9)]

        #Initializes cells and adds them to the corresponding column, row and box lists.
        for index in range(81): 
            cell=Cell(0)
            self.cells.append(cell)
            column_num=index//9
            row_num=index%9
            columns[column_num].append(cell)
            rows[row_num].append(cell)
            boxes[column_num//3+(row_num//3)*3].append(cell)
        
        #Associates the reference for each column, row and box to their corresponding cell.
        for x in range(9):
            for cell in columns[x]:
                cell.set_column(columns[x])

            for cell in rows[x]:
                cell.set_row(rows[x])

            for cell in boxes[x]:
                cell.set_box(boxes[x])
    
    def __str__(self) -> str:
        '''
        Returns a string representation of the puzzle with a new line every 9 characters.
        '''
        line = ''.join(str(int(x)) for x in self.cells)
        out=""
        for x in range(0,9):
            out+=f'{line[0+x*9:9+x*9]}\n'
        return out
    
    def load_puzzle(self, numbers:str):
            for index, num in enumerate(numbers):
                self.cells[index].set_value(int(num))
    
    def solve(self):
        '''
        Solves the puzzle and returns the solution.
        '''
        #Checks to see if the puzzle is solved
        if '0' in str(self):

            #Starts by finding the cell with the fewest possibilities.
            fewest_tuple=self.find_fewest()
            curr_cell=fewest_tuple[0]
            possibilities=fewest_tuple[1] 
            possibilities_length=len(possibilities)

            if possibilities_length == 0: #Not solvable
                return None

            if possibilities_length == 1: #If there is only one possibility than 
                old_value = curr_cell.value
                curr_cell.set_value(list(possibilities)[0])
                solve=self.solve()
                if solve != None:
                    return solve
                else:
                    curr_cell.set_value(old_value)
                    return None
            
            if possibilities_length > 1:
                for value in possibilities:
                    old_value = curr_cell.value
                    curr_cell.set_value(value)
                    solve=self.solve()
                    if solve != None:
                        return solve
                    else:
                        curr_cell.set_value(old_value)
        else:
            return str(self)




    def find_fewest(self):
        '''
        Finds the cell with the fewest possibilities.
        Used as a helper method for solve().
        Returns a tuple to reduce number of times possible_values() is called.
        '''
        cell=None
        possibilities = None
        for curr_cell in self.cells:
            if int(curr_cell) == 0:
                if cell is None:
                    cell = curr_cell
                    possibilities = curr_cell.possible_values()
                else:
                    curr_possibilities=curr_cell.possible_values()
                    if len(curr_possibilities) < len(possibilities):
                        cell = curr_cell
                        possibilities = curr_possibilities

                if len(possibilities)==0:
                    return (cell, possibilities)
    
        return (cell, possibilities)
        
    def check(self, solution:str):
        return ''.join(str(int(x)) for x in self.cells)==solution


