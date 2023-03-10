from tkinter import Button, Label, messagebox
import random
import settings
import sys


class Cell:
    all = []
    cell_count = settings.CELL_COUNT
    cell_count_label_object = None
    # Define a class cell

    def __init__(self, x, y, is_mine=False):
        # Initialization of the class Cell
        self.is_mine = is_mine
        self.cell_btn_object = None
        self.is_opened = False
        self.is_mine_candidate = False
        self.x = x
        self.y = y

        #Append the object to the cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        # define a function create_btn_object
        btn = Button(
            location,
            width = 12,
            height = 4,
        )
        btn.bind('<Button-1>', self.left_click_actions ) # left Click
        btn.bind('<Button-3>', self.right_click_actions ) # Right Click
        self.cell_btn_object = btn

    @staticmethod   
    def create_cell_count_label(location):
        lbl = Label(
            location,
            bg = 'black',
            fg = 'white',
            text=f"Cells Left:{Cell.cell_count}",
            width = 12,
            height = 4,
            font =("", 25)
        )
        Cell.cell_count_label_object = lbl


    def left_click_actions(self, event):
        # Define the class left_click_actions
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
            self.show_cell()
            #If Mines count is equal to the cells left count PLAYER WON THE GAME
            if Cell.cell_count == settings.MINES_COUNT:
                messagebox.showinfo("CONGRATULATIONS", "You Won")

        #Cancel left and right click events if cell already clicked. To prevent code running behind the hood
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-3>')

    def get_cell_by_axis(self, x, y):
        #Return a cell object based on the value of x and y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        #Count mines in surrounded cells
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1

        return counter

         

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            #Replace the text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text = f"Cells.left:{Cell.cell_count}"
                )


        #If this was a mine candidate then for safety, we should configure the bg color to "gray58"
        self.cell_btn_object.configure(
            bg = "gray85"
        )


        #Mark the cell as opened(Use it as the last line of this method)
        self.is_opened = True

    def show_mine(self):
        # A logic to interupt the game and display player lost
        self.cell_btn_object.configure(bg='red')
        messagebox.showinfo("BUSTED", "Game Over")
        sys.exit()

    def right_click_actions(self, event):
        # Define the class right_click_actions
        if not self.is_mine_candidate:
            self.cell_btn_object.configure(
                bg='Blue'
            )
            self.is_mine_candidate = True
        else:
            self.cell_btn_object.configure(
                bg = "gray85"
            )
            self.is_mine_candidate = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(
            Cell.all, 9
        )
        for picked_cells in picked_cells:
            picked_cells.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
