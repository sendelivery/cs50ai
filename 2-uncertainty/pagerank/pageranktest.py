from pagerank import transition_model, sample_pagerank, iterate_pagerank


# TRANSITION MODEL TESTS ==================================
print("TEST - transition_model")
print("test case 1", end="")

corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
page = "1.html"
damping_factor = 0.85

result = transition_model(corpus, page, damping_factor)
expected = {"1.html": 0.05, "2.html": 0.475, "3.html": 0.475}

assert len(result) == 3
for page, value in result.items():
    assert f"{value:.4f}" == f"{expected[page]:.4f}"

print(" - PASS")

print("test case 2", end="")

corpus = {
    "1.html": {},
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
page = "1.html"
damping_factor = 0.85

result = transition_model(corpus, page, damping_factor)
expected = {"1.html": 0.33, "2.html": 0.33, "3.html": 0.33}

assert len(result) == 3
for page, value in result.items():
    assert f"{value:.2f}" == f"{expected[page]:.2f}"

print(" - PASS")

print("test case 3", end="")

corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
page = "2.html"
damping_factor = 0.85

result = transition_model(corpus, page, damping_factor)
expected = {"1.html": 0.05, "2.html": 0.05, "3.html": 0.9}

assert len(result) == 3
for page, value in result.items():
    assert f"{value:.4f}" == f"{expected[page]:.4f}"

print(" - PASS")

# SAMPLE PAGERANK TESTS ===================================
print()
print("TEST - sample_pagerank")
print("test case 1")

corpus = {
    "1.html": {"2.html", "3.html"},
    "2.html": {"3.html"},
    "3.html": {"2.html"},
}
damping_factor = 0.85

result = sample_pagerank(corpus, damping_factor, 10000)

for page, value in result.items():
    print(f"{page}: {value:.4f}")

print("test case 2")

corpus = {
    "1.html": ["2.html"],
    "2.html": ["1.html", "3.html"],
    "3.html": ["2.html", "4.html"],
    "4.html": ["2.html"],
}
damping_factor = 0.85

result = sample_pagerank(corpus, damping_factor, 10000)

for page, value in result.items():
    print(f"{page}: {value:.4f}")

# ITERATE PAGERANK TESTS ===================================
print()
print("TEST - iterate_pagerank")
print("test case 1")

corpus = {
    "1.html": ["2.html"],
    "2.html": ["1.html", "3.html"],
    "3.html": ["2.html", "4.html"],
    "4.html": ["2.html"],
}
damping_factor = 0.85

result = iterate_pagerank(corpus, damping_factor)

for page, value in result.items():
    print(f"{page}: {value:.4f}")
