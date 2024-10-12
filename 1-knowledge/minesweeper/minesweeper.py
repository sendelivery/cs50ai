import itertools
import random
from typing import List


class Minesweeper:
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence:
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # We can only be absolutely sure that a cell is a mine
        # if the number of mines matches the number of cells
        # at which point we can return the whole set
        if len(self.cells) == self.count:
            return self.cells

        # Otherwise, we'll have to return an empty set
        # because we can't be sure of which cell is a mine
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # We only know our cells are safe if the count of
        # mines within is 0
        if self.count == 0:
            return self.cells

        # Otherwise, we can't be sure and have to return
        # an empty set.
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            # Remove the cell from our set of cells
            self.cells.remove(cell)

            # Decrement our count of mines
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells and self.count != 0:
            # Remove the cell from our set of cells
            self.cells.remove(cell)


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge: List[Sentence] = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        self.moves_made.add(cell)  # Mark the cell as a move that has been made
        self.mark_safe(cell)  # Mark the cell as a safe move

        # Add a new sentence to the AI's knowledge base by:
        #   1. Get all neighbouring cells

        neighbours = set()

        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                undetermined_cell = (i, j)

                # Ignore the cell itself
                if undetermined_cell == cell:
                    continue

                # If we already know it's a mine, decrement the count, continue
                if undetermined_cell in self.mines:
                    count -= 1
                    continue

                # Add to `neighbours` if in bounds
                # AND we're not sure if it's a safe cell
                if (
                    0 <= i < self.height
                    and 0 <= j < self.width
                    and undetermined_cell not in self.safes
                ):
                    neighbours.add(undetermined_cell)

        #   2. Add the new sentence to our knowledge base
        if len(neighbours) > 0:
            self.knowledge.append(Sentence(neighbours, count))

        # Next, mark any additional cells as safe or as mines if it can be
        # concluded from our current knowledge base
        for sentence in reversed(self.knowledge.copy()):
            known_safes = sentence.known_safes()
            known_mines = sentence.known_mines()

            if known_safes:
                for safe_cell in known_safes.copy():
                    self.mark_safe(safe_cell)

            if known_mines:
                for mine_cell in known_mines.copy():
                    self.mark_mine(mine_cell)

            if len(sentence.cells) == 0 or sentence.count == 0:
                self.knowledge.remove(sentence)

        # Finally, infer new sentences based on our existing knowledge
        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence1 == sentence2:
                    continue

                if sentence1.cells.issubset(sentence2.cells):
                    sentence2.cells -= sentence1.cells
                    sentence2.count -= sentence1.count
                elif sentence2.cells.issubset(sentence1.cells):
                    sentence1.cells -= sentence2.cells
                    sentence1.count -= sentence2.count

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe in self.safes:
            if safe not in self.mines and safe not in self.moves_made:
                return safe

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        cell = None

        while cell is None:
            i = random.randint(0, self.height - 1)
            j = random.randint(0, self.width - 1)
            if (i, j) not in self.moves_made and (i, j) not in self.mines:
                cell = (i, j)

        return cell
