# -*- coding: utf-8 -*-
"""assignment1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1TMnqZ7LqkXSXc2c15vmt56AQtE1cFayf
"""

import gzip
from collections import defaultdict
import math
import scipy.optimize
from sklearn import svm
import numpy
import string
import random
import string
from sklearn import linear_model
import numpy as np

import warnings
warnings.filterwarnings("ignore")

def readGz(path):
    for l in gzip.open(path, 'rt'):
        yield eval(l)

def readCSV(path):
    f = gzip.open(path, 'rt')
    f.readline()
    for l in f:
        u,b,r = l.strip().split(',')
        r = int(r)
        yield u,b,r

from google.colab import drive
drive.mount('/content/drive')

allRatings = []
for l in readCSV("/content/drive/My Drive/DSC 256R/assignment1/train_Interactions.csv.gz"):
    allRatings.append(l)

len(allRatings)

ratingsTrain = allRatings[:190000]
ratingsValid = allRatings[190000:]
ratingsPerUser = defaultdict(list)
ratingsPerItem = defaultdict(list)
for u,b,r in ratingsTrain:
    ratingsPerUser[u].append((b,r))
    ratingsPerItem[b].append((u,r))

# Build a dictionary to store the sets of users who have read each book in the training set
usersPerBook = defaultdict(set)
for user, book, _ in ratingsTrain:
    usersPerBook[book].add(user)

# Copied from baseline code
bookCount = defaultdict(int)
totalRead = 0

for user,book,_ in readCSV("/content/drive/My Drive/DSC 256R/assignment1/train_Interactions.csv.gz"):
    bookCount[book] += 1
    totalRead += 1

mostPopular = [(bookCount[x], x) for x in bookCount]
mostPopular.sort()
mostPopular.reverse()

# Function to calculate Jaccard similarity between two books
def jaccard_similarity(book1, book2):
    users1 = usersPerBook[book1]
    users2 = usersPerBook[book2]
    intersection = users1.intersection(users2)
    union = users1.union(users2)
    if len(union) == 0:
        return 0
    return len(intersection) / len(union)

# Now use a Jaccard Similarity-based threshold combined with a Popularity-based threshold

def predict_read_hybrid(user, book, jaccard_threshold, popularity_books):
    # Get books read by the user in the training set
    books_read_by_user = [b for b, _ in ratingsPerUser[user]]

    # If the user hasn't read any books in the training set, fall back to popularity check
    if not books_read_by_user:
        return int(book in popularity_books)

    # Calculate the maximum Jaccard similarity for the books the user has read
    max_jaccard = max(jaccard_similarity(book, b) for b in books_read_by_user)

    # First check Jaccard similarity; if it exceeds the threshold, predict 'read'
    if max_jaccard >= jaccard_threshold:
        return 1
    else:
        return int(book in popularity_books)

# Define a fixed popularity threshold based on the top 70% of books by interactions
popularity_threshold = totalRead * 0.7
popular_books = set()
count = 0
for ic, book in mostPopular:
    count += ic
    popular_books.add(book)
    if count >= popularity_threshold:
        break

# define 5% as optimal Jaccard similarity thresholds to test
jaccard_threshold = 0.05

predictions = open("predictions_Read.csv", 'w')
for l in open("/content/drive/My Drive/DSC 256R/assignment1/pairs_Read.csv"):
    if l.startswith("userID"):
        predictions.write(l)
        continue
    u,b = l.strip().split(',')
    predictions.write(u + ',' + b + ',' + str(predict_read_hybrid(u, b, jaccard_threshold, popular_books)) + '\n')

predictions.close()

# Initialize structures to store ratings
ratingsPerUser = defaultdict(list)
ratingsPerItem = defaultdict(list)

for u, b, r in ratingsTrain:
    ratingsPerUser[u].append((b, r))
    ratingsPerItem[b].append((u, r))

# Parameters and constants
N_train = len(ratingsTrain)

# Initialize variables
alpha = np.mean([r for _, _, r in ratingsTrain])  # Global average rating
beta_u = defaultdict(float)
beta_i = defaultdict(float)

# Convergence parameters
max_iterations = 1000
tol = 1e-10

# Optimal lambda regularization value determined through iteration
lambda_reg = 4.5

# Iterative optimization
for iteration in range(max_iterations):
    # Update alpha
    alpha_old = alpha
    alpha = sum(r - (beta_u[u] + beta_i[b]) for u, b, r in ratingsTrain) / N_train

    # Update beta_u (user biases)
    for u in ratingsPerUser:
        beta_u[u] = sum(r - (alpha + beta_i[b]) for b, r in ratingsPerUser[u]) / (lambda_reg + len(ratingsPerUser[u]))

    # Update beta_i (item biases)
    for b in ratingsPerItem:
        beta_i[b] = sum(r - (alpha + beta_u[u]) for u, r in ratingsPerItem[b]) / (lambda_reg + len(ratingsPerItem[b]))

    # Check for convergence
    if abs(alpha - alpha_old) < tol:
        break

predictions = open("predictions_Rating.csv", 'w')
for l in open("/content/drive/My Drive/DSC 256R/assignment1/pairs_Rating.csv"):
    if l.startswith("userID"): # header
        predictions.write(l)
        continue
    u,b = l.strip().split(',') # Read the user and item from the "pairs" file and write out your prediction
    predictions.write(u + ',' + b + ',' + str(alpha + beta_u[u] + beta_i[b]) + '\n')

predictions.close()