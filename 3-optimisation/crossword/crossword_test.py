from crossword import Crossword, Variable
from generate import CrosswordCreator

crossword = Crossword(
    structure_file="3-optimisation/crossword/testdata/structure.txt",
    words_file="3-optimisation/crossword/testdata/words.txt",
)

creator = CrosswordCreator(crossword)
creator.domains
creator.enforce_node_consistency()
creator.ac3()
creator.domains

"""
{
    A: Variable(4, 1, 'across', 4): {'FOUR', 'FIVE', 'NINE'}, - final character overlaps with C
    B: Variable(0, 1, 'across', 3): {'SIX', 'ONE', 'TWO', 'TEN'},
    C: Variable(1, 4, 'down', 4): {'FOUR', 'FIVE', 'NINE'}, - final character overlaps with A
    D: Variable(0, 1, 'down', 5): {'THREE', 'EIGHT', 'SEVEN'}
}
{
    Variable(4, 1, 'across', 4): {'NINE'}, 
    Variable(0, 1, 'across', 3): {'SIX'}, 
    Variable(1, 4, 'down', 4): {'FIVE', 'NINE'}, 
    Variable(0, 1, 'down', 5): {'SEVEN'}
}
"""
"""
{
    Variable(4, 1, 'across', 4): {'NINE'},
    Variable(0, 1, 'across', 3): {'SIX', 'TEN', 'TWO'},
    Variable(1, 4, 'down', 4): {'NINE', 'FIVE'},
    Variable(0, 1, 'down', 5): {'SEVEN'}
}
"""
"""
{
    Variable(4, 1, 'across', 4): {'NINE'},
    Variable(0, 1, 'across', 3): {'SIX', 'TWO', 'TEN'},
    Variable(1, 4, 'down', 4): {'FIVE', 'NINE'},
    Variable(0, 1, 'down', 5): {'SEVEN'}
}
"""
