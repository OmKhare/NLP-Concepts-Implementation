import os

def load_ngrams_from_file(filename):
    with open(filename, 'r') as f:
        ngrams = {}
        for line in f:
            parts = line.strip().split()
            ngram = " ".join(parts[:-1])
            count = int(parts[-1])
            ngrams[ngram] = count
    return ngrams

def predict_next_word(input_words):
    words = input_words.split()
    max_n = min(len(words) + 1, 6)  # We don't want to exceed 5-grams

    best_candidate = None

    for n in range(max_n - 1, 1, -1):
        current_ngram = " ".join(words[-n:])  # Get the last N words from the input for our N-gram
        ngram_file = f"MIS-No_{n+1}-gram-output.txt"

        if os.path.exists(ngram_file):
            ngrams = load_ngrams_from_file(ngram_file)

            # Filter based on current_ngram
            candidates = {k: v for k, v in ngrams.items() if k.startswith(current_ngram)}

            if candidates:
                # Sort the candidates by frequency
                sorted_candidates = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
                
                # If we've not found a best candidate yet or there's a tie in the highest frequency
                if not best_candidate or (best_candidate[1] == sorted_candidates[0][1]):
                    best_candidate = sorted_candidates[0]
                else:
                    break  # If we have a unique high-frequency candidate, we break

    if best_candidate:
        return best_candidate[0].split()[-1]

    return "No prediction available"

if __name__ == "__main__":
    input_words = input("Enter the input words: ").strip()
    predicted_word = predict_next_word(input_words)
    with open("MIS-NO-Part2-Output.txt", 'w') as f:
        f.write(predicted_word)