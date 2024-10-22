import sys

from crossword import *


class CrosswordCreator:

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy() for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont

        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size, self.crossword.height * cell_size),
            "black",
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border, i * cell_size + cell_border),
                    (
                        (j + 1) * cell_size - cell_border,
                        (i + 1) * cell_size - cell_border,
                    ),
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (
                                rect[0][0] + ((interior_size - w) / 2),
                                rect[0][1] + ((interior_size - h) / 2) - 10,
                            ),
                            letters[i][j],
                            fill="black",
                            font=font,
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, words in self.domains.items():
            for word in words.copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        overlap = self.crossword.overlaps[x, y]

        # If there's no overlap between our variables, return False
        # i.e. no modification made.
        if not overlap:
            return False

        # Get the overlap indices.
        xindex, yindex = overlap

        modified = False

        # Go through all words in x's domain,
        for xword in self.domains[x].copy():
            remove_x = True
            for yword in self.domains[y]:
                # For each word in x, if it has a corresponding value in y's
                # domain, we don't remove it from x's domain.
                if xword[xindex] == yword[yindex]:
                    remove_x = False
                    break
            if remove_x:
                self.domains[x].remove(xword)
                modified = True

        return modified

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if arcs is None:
            # Set arcs to all arcs in the csp
            arcs = [
                arc
                for arc, overlaps in self.crossword.overlaps.items()
                if overlaps is not None
            ]

        i = 0
        while i < len(arcs):
            x, y = arcs[i]
            if self.revise(x, y):
                if len(self.domains[x]) == 0:
                    return False
                arcs.extend([(n, x) for n in self.crossword.neighbors(x) if n != y])
            i += 1

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.crossword.variables:
            if variable not in assignment:
                return False
            word = assignment[variable]
            if word is None or word == "" or len(word) == 0:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for x, xword in assignment.items():
            # If length of word does not match variable length return False
            if x.length != len(xword):
                return False

            # For each pair
            for y, yword in assignment.items():
                if x == y:
                    continue

                # If the words are not distinct return False
                if xword == yword:
                    return False

                overlap = self.crossword.overlaps[x, y]

                if overlap is None:
                    continue

                # Return False if the overlapping characters are not equal
                xindex, yindex = overlap
                if xword[xindex] != yword[yindex]:
                    return False

        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        word_freq = {word: 0 for word in self.domains[var]}
        for n in self.crossword.neighbors(var):
            for word in self.domains[var]:
                if word in self.domains[n]:
                    word_freq[word] += 1

        domain_values = list(self.domains[var])
        domain_values.sort(key=lambda w: word_freq[w])
        return domain_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        unassigned = list(self.crossword.variables - set(assignment.keys()))
        unassigned.sort(key=lambda x: len(self.domains[x]))  # sort by size of domain

        ties = []
        smallest = len(self.domains[unassigned[0]])
        for var in unassigned:
            if len(self.domains[var]) > smallest:
                break
            ties.append(var)

        if len(ties) > 1:
            ties.sort(key=lambda x: len(self.crossword.neighbors(x)))

        return ties[-1]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment

        variable = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                consistent_assignment = assignment.copy()
                inference = self.ac3()
                result = None
                if inference:
                    result = self.backtrack(assignment)
                else:
                    result = self.backtrack(consistent_assignment)

                if result:
                    return result

            else:
                del assignment[variable]

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
