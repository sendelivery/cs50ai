from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(
    # Rules of the game:
    # We know that A must be either a knight or knave
    Or(AKnight, AKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    # What the players said:
    # We know that knights don't lie, so A would have to be
    # telling the truth
    Implication(AKnight, And(AKnight, AKnave)),
    # We also know that knaves lie, so A would have to be
    # telling a lie
    Implication(AKnave, Not(And(AKnight, AKnave))),
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    # Rules of the game:
    # We know that A and B must each be either a knight
    # or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    # What the players said:
    # If A is a knight, that would imply they're telling
    # the truth
    Implication(AKnight, And(AKnave, BKnave)),
    # If A is a knave, that would imply they're lying
    # Meaning either both are knights (not possible
    # because a knight would never lie and say it's a
    # knave)
    # Or A is lying and is actually a knave, and B is a
    # knight
    Implication(
        AKnave,
        Or(And(AKnight, BKnight), And(AKnave, BKnight)),
    ),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(
    # Rules of the game:
    # We know that A and B must each be either a knight
    # or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    # What the players said:
    # If A were a knight, they would be telling the truth
    Implication(AKnight, And(AKnight, BKnight)),
    # If A were a knave, they would be lying, meaning A and
    # B are different things
    Implication(
        AKnave,
        Or(
            And(AKnave, BKnight),
            And(AKnight, BKnave),
        ),
    ),
    # If B is a knight, they'd be telling the truth
    Implication(
        BKnight,
        Or(
            And(BKnight, AKnave),
            And(BKnave, AKnight),
        ),
    ),
    # If B is a knave, they'd be lying
    Implication(
        BKnave,
        Or(
            And(BKnave, AKnave),
            And(BKnight, AKnight),
        ),
    ),
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(
    # Rules of the game:
    # We know that A, B, and C must each be either a
    # knight or a knave
    Or(AKnight, AKnave),
    Or(BKnight, BKnave),
    Or(CKnight, CKnave),
    # But not both
    Not(And(AKnight, AKnave)),
    Not(And(BKnight, BKnave)),
    Not(And(CKnight, CKnave)),
    # What the players said:
    # Player A...
    Implication(AKnight, AKnight),
    Implication(AKnave, AKnight),
    # Player B - A said I am a Knave
    Implication(BKnight, AKnave),
    Implication(BKnave, AKnight),
    # Player B - C is a Knave
    Implication(BKnight, CKnave),
    Implication(BKnave, CKnight),
    # Player C - A is a knight
    Implication(CKnight, AKnight),
    Implication(CKnave, AKnave),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3),
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
