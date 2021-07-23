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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    output = dict()

    if page in corpus:
        if len(corpus[page]) > 0:
            minor = (1 - damping_factor) / len(corpus)
            major = damping_factor / len(corpus[page])
            for every in corpus:
                output[every] = minor
            for link in corpus[page]:
                output[link] += major
        else:
            for page in corpus:
                output[page] = 1 / len(corpus)

        return output


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Creates a dictionary to keep track of number of visits
    visits = dict()
    
    # Creates a list to receive the name of all the pages in corpus
    pages = []
    for page in corpus:
        pages.append(page)
        # And populates the dictionary with pages' names and 0 visits
        visits[page] = 0
    
    # Chooses the first page randomly with equal distribution
    chosen_page = random.choices(pages, k=1)
    # Increments visit counter of chosen page
    visits[chosen_page[0]] = 1
    
    # Starts loop of n cycles to count how many times a page is visited
    for i in range(n-1):
        # Calls transition_model
        transMod = transition_model(corpus, chosen_page[0], damping_factor)

        # Chooses next link or page randomly, but weighted
        population = []
        weights = []
        for key in transMod:
            population.append(key)
        for value in transMod:
            weights.append(transMod[value])
        chosen_page = random.choices(population, weights, k=1)

        # Increments visit counter of chosen page
        visits[chosen_page[0]] += 1

    for page in visits:
        visits[page] /= n

    return visits


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    d = damping_factor
    N = len(corpus)

    # Creates a dictionary to receive pageranks
    PRank = dict()
    PRank_temp = dict()
    flags = 0
    loop = True
    
    # Populates the dictionary with pages' names and initial PRank
    for page in corpus:
        PRank[page] = 1 / N
    
    # Loops until PRank values changes by more than 0.001
    while loop:

        for page in corpus:
            sumPRank = 0
            for link in corpus:
                if page in corpus[link]:
                    sumPRank += (PRank[link] / len(corpus[link]))
                if len(corpus[link]) == 0:
                    sumPRank += (PRank[link] / N)
                PRank_temp[page] = (((1 - d) / N) + (d * sumPRank))

        # Tests for 0.001 precision between iterations
        for page in corpus:
            if PRank[page] - PRank_temp[page] < 0.001:
                flags += 1
        # If all pages converge, quits loop
        if flags == N:
            loop = False
        # Otherwise, updates values
        else:
            flags = 0
            for page in corpus:
                PRank[page] = PRank_temp[page]

    total = 0
    for page in PRank:
        total += PRank[page]
    for page in PRank:
        PRank[page] /= total

    return PRank


if __name__ == "__main__":
    main()
