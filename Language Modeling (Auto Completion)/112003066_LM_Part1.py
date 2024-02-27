import sys
from collections import defaultdict
from itertools import islice

def generate_ngrams(text, n):
    tokens = text.split()
    ngrams = []

    for i in range(len(tokens) - n + 1):  # Ensuring we don't go beyond the length
        ngram = tokens[i:i+n]  # Slicing the tokens list to get n items
        ngrams.append(" ".join(ngram))

    return ngrams

def ngram_model(input_file):
    ngram_counts = {2: defaultdict(int), 3: defaultdict(int), 4: defaultdict(int), 5: defaultdict(int)}

    with open(input_file, 'r') as f:
        for line in f:
            line = line.strip()
            for n in range(2, 6):
                for ngram in generate_ngrams(line, n):
                    ngram_counts[n][ngram] += 1

    for n, counts in ngram_counts.items():
        output_filename = f"MIS-No_{n}-gram-output.txt"
        with open(output_filename, 'w') as f:
            for ngram, count in counts.items():
                f.write(f"{ngram} {count}\n")

input_file = './input.txt'
ngram_model(input_file)