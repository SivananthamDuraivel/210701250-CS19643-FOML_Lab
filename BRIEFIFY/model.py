import nltk
from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import spacy
from collections import Counter

# Ensure necessary downloads
nltk.download("stopwords")

# Load spaCy's English model
nlp = spacy.load('en_core_web_sm')

# Function to read the article
def read_article(text):
    article = text.split(". ")
    sentences = []

    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    if sentences[-1] == ['']:  # Remove any empty strings
        sentences.pop() 
    
    return sentences

# Function to calculate sentence similarity
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vector1, vector2)

# Function to build similarity matrix
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)

    return similarity_matrix

# Function to generate summary
def generate_summary(text, top_n=5):
    stop_words = stopwords.words('english')
    summarize_text = []

    # Read text and split it
    sentences =  read_article(text)

    # Generate Similarity Matrix across sentences
    sentence_similarity_matrix = build_similarity_matrix(sentences, stop_words)

    # Rank sentences in similarity matrix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    # Sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)    

    for i in range(top_n):
        summarize_text.append(" ".join(ranked_sentence[i][1]))

    # Output the summarized text
    return ". ".join(summarize_text)

# Function to read the input file
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Function to extract keywords
def extract_keywords(text, top_n=10):
    doc = nlp(text)
    
    # Extract named entities and noun chunks
    entities = [ent.text for ent in doc.ents if ent.label_ in ['PERSON', 'ORG', 'GPE', 'LOC', 'EVENT']]
    noun_chunks = [chunk.text for chunk in doc.noun_chunks if len(chunk) > 1]
    
    # Combine and count the frequency of entities and noun chunks
    all_phrases = entities + noun_chunks
    frequency = Counter(all_phrases)
    
    # Get the most common phrases
    most_common_phrases = frequency.most_common(top_n)
    keywords = [phrase for phrase, count in most_common_phrases]
    
    return keywords
