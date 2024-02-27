import nltk
from nltk.corpus import treebank
from nltk.corpus import conll2000
from collections import defaultdict

nltk.download('conll2000')
nltk.download('treebank')

train_data = treebank.tagged_sents()

test_data = conll2000.tagged_sents()[:100]

tags = [tag for sentence in train_data for _, tag in sentence]
words = [word for sentence in train_data for word, _ in sentence]

tag_bigrams = list(nltk.bigrams(tags))
tag_freq = nltk.FreqDist(tags)
tag_bigram_freq = nltk.FreqDist(tag_bigrams)
word_tag_freq = nltk.FreqDist([(word, tag) for sentence in train_data for word, tag in sentence])

def transition_probability(t2, t1):
    return tag_bigram_freq[(t1, t2)] / tag_freq[t1]

def wordtag_probability(word, tag):
    k = 0.001
    return (word_tag_freq[(word, tag)] + k) / (tag_freq[tag] + k * len(set(words)))

# Viterbi Algorithm
def viterbi(sentence):
    dp = defaultdict(lambda: defaultdict())
    backpointer = defaultdict(lambda: defaultdict())
    unique_tags = set(tags)
    
    # Initialization
    for tag in unique_tags:
        dp[tag][0] = wordtag_probability(sentence[0], tag) * (tag_freq[tag] / len(tags))
        backpointer[tag][0] = None

    # Recursion
    for t in range(1, len(sentence)):
        for tag in unique_tags:
            max_prob, best_prev_tag = max((dp[prev_tag][t-1] * transition_probability(tag, prev_tag) * wordtag_probability(sentence[t], tag), prev_tag) for prev_tag in unique_tags)
            dp[tag][t] = max_prob
            backpointer[tag][t] = best_prev_tag

    # Termination
    best_last_tag = max((dp[tag][len(sentence)-1], tag) for tag in unique_tags)[1]
    best_path = [best_last_tag]

    for t in range(len(sentence)-1, 0, -1):
        best_path.insert(0, backpointer[best_last_tag][t])
        best_last_tag = backpointer[best_last_tag][t]

    return list(zip(sentence, best_path))

# Test the Viterbi algorithm

output_lists = []
for i in range(9):
    test_sentence = [word for word, _ in test_data[i]]
    output = viterbi(test_sentence)
    output_lists.append(output)

filename = "112003066_Assign1_Output.txt"


with open(filename, 'w') as file:
    for i in output_lists:
        output_text = ""
        for j in i:
            output_text += j[0]+"_"+j[1]+" "
        
        file.write(output_text + '\n')

print(f"Output written to {filename}")
