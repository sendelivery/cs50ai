import csv
import itertools
import sys

PROBS = {
    # Unconditional probabilities for having gene
    "gene": {2: 0.01, 1: 0.03, 0: 0.96},
    "trait": {
        # Probability of trait given two copies of gene
        2: {True: 0.65, False: 0.35},
        # Probability of trait given one copy of gene
        1: {True: 0.56, False: 0.44},
        # Probability of trait given no gene
        0: {True: 0.01, False: 0.99},
    },
    # Mutation probability
    "mutation": 0.01,
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {"gene": {2: 0, 1: 0, 0: 0}, "trait": {True: 0, False: 0}}
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (
                people[person]["trait"] is not None
                and people[person]["trait"] != (person in have_trait)
            )
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (
                    True
                    if row["trait"] == "1"
                    else False if row["trait"] == "0" else None
                ),
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s)
        for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    probability = 1
    names = set(people.keys())

    for person in names:
        num_genes = -1
        m = people[person]["mother"]
        f = people[person]["father"]

        if person in one_gene:
            # person has one gene
            num_genes = 1

            if m is not None and f is not None:
                # gets the gene from mother and not father
                mnf = 0
                if m in one_gene:
                    mnf = 0.5
                elif m in two_genes:
                    mnf = 1 - PROBS["mutation"]
                else:
                    mnf = PROBS["mutation"]
                if f in one_gene:
                    mnf *= 0.5
                elif f in two_genes:
                    mnf *= PROBS["mutation"]
                else:
                    mnf *= 1 - PROBS["mutation"]

                # gets the gene from father and not mother
                fnm = 0
                if f in one_gene:
                    fnm = 0.5
                elif f in two_genes:
                    fnm = 1 - PROBS["mutation"]
                else:
                    fnm = PROBS["mutation"]
                if m in one_gene:
                    fnm *= 0.5
                elif m in two_genes:
                    fnm *= PROBS["mutation"]
                else:
                    fnm *= 1 - PROBS["mutation"]

                probability *= mnf + fnm
            else:
                probability *= PROBS["gene"][1]

        elif person in two_genes:
            # person has two genes
            num_genes = 2

            if m is not None and f is not None:
                # gets the gene from mother and father
                maf = 0
                if m in one_gene:
                    maf = 0.5
                elif m in two_genes:
                    maf = 1 - PROBS["mutation"]
                else:
                    maf = PROBS["mutation"]
                if f in one_gene:
                    maf *= 0.5
                elif f in two_genes:
                    maf *= 1 - PROBS["mutation"]
                else:
                    maf *= PROBS["mutation"]

                probability *= maf
            else:
                probability *= PROBS["gene"][2]
        else:
            # person does not have the gene
            num_genes = 0

            if m is not None and f is not None:
                # does not get the gene from either mother or father
                maf = 0
                if m in one_gene:
                    maf = 0.5
                elif m in two_genes:
                    maf = PROBS["mutation"]
                else:
                    maf = 1 - PROBS["mutation"]
                if f in one_gene:
                    maf *= 0.5
                elif f in two_genes:
                    maf *= PROBS["mutation"]
                else:
                    maf *= 1 - PROBS["mutation"]

                probability *= maf
            else:
                probability *= PROBS["gene"][0]

        if person in have_trait:
            # person has the trait
            probability *= PROBS["trait"][num_genes][True]
        else:
            # person does not have the trait
            probability *= PROBS["trait"][num_genes][False]

    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    names = set(probabilities.keys())
    for person in names:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p

        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    names = set(probabilities.keys())
    for person in names:
        # map gene distributions
        zero = probabilities[person]["gene"][0]
        one = probabilities[person]["gene"][1]
        two = probabilities[person]["gene"][2]

        total = zero + one + two

        probabilities[person]["gene"][0] = zero / total
        probabilities[person]["gene"][1] = one / total
        probabilities[person]["gene"][2] = two / total

        # map trait distributions
        has_trait = probabilities[person]["trait"][True]
        doesnt_have_trait = probabilities[person]["trait"][False]

        total = has_trait + doesnt_have_trait

        probabilities[person]["trait"][True] = has_trait / total
        probabilities[person]["trait"][False] = doesnt_have_trait / total


if __name__ == "__main__":
    main()
