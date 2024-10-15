import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    num_links = len(corpus[page])
    num_pages = len(corpus)
    distribution = {}

    if num_links == 0:
        # Current page links to no pages, evenly distribute probability.
        probability = 1 / num_pages
        for key in corpus.keys():
            distribution[key] = probability
        return distribution

    linked_pages = set(corpus[page])
    linked_page_probability = damping_factor / num_links
    random_page_probability = (1 - damping_factor) / num_pages

    # Calculate probability
    for key in corpus.keys():
        distribution[key] = random_page_probability
        if key in linked_pages:
            distribution[key] += linked_page_probability

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    available_pages = list(corpus.keys())

    # Start off on a random page
    page = random.choice(available_pages)
    page_rank = {p: 0 for p in available_pages}

    # Simulate a random surfer clicking on links n - 1 times
    for _ in range(n - 1):
        # Tally up the page rank so far
        page_rank[page] += 1 / n

        probability_distribution = transition_model(corpus, page, damping_factor)
        linked_pages = list(probability_distribution.keys())

        corresponding_probability = [
            probability_distribution[linked_page] for linked_page in linked_pages
        ]

        # The next page the surfer goes to is based on the probability
        # distribution of all links in our corpus
        page = random.choices(
            population=linked_pages, weights=corresponding_probability
        )[0]

    return page_rank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    pages = list(corpus.keys())
    total_pages = len(pages)
    page_rank = {p: 1 / total_pages for p in pages}
    page_rank_diff = {p: float("inf") for p in pages}

    incoming_links = {}

    # Pages that have no links should be interpreted as having one link
    # for every page in the corpus, including itself
    for page in pages:
        if len(corpus[page]) == 0:
            corpus[page] = pages

    # Pre-bake incoming links for each page
    for page in pages:
        # If our `page` is linked to by `p`, add `p` to the `incoming_links`
        # list for our `page`
        incoming_links[page] = [p for p, links in corpus.items() if page in links]

    iterate = True
    while iterate:
        for page in pages:
            # Calculate the probability of choosing `page` from each
            # linking page `i`
            proba_chose_page_from_i = [
                page_rank[linking_page] / len(corpus[linking_page])
                for linking_page in incoming_links[page]
            ]

            # Calculate `page`s new page rank as the probability across
            # all pages + the normalised page rank of all linking pages
            new_rank = (1 - damping_factor) / total_pages + (
                damping_factor * sum(proba_chose_page_from_i)
            )

            # Calculate the difference in new page rank from the previous
            page_rank_diff[page] = abs(new_rank - page_rank[page])
            page_rank[page] = new_rank

        # Keep calculating page ranks until none change by more than 0.001
        iterate = False
        for diff in page_rank_diff.values():
            if diff >= 0.001:
                iterate = True
                break

    return page_rank


if __name__ == "__main__":
    main()
