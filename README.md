# Project Overview
This project explores a hybrid recommendation approach for a book recommendation system. It focuses on predicting two critical aspects:

1. Whether a user would read a given book.
2. The star rating a user would assign to a book.

The system combines Jaccard similarity-based personalized recommendations with popularity-based methods for book prediction. It also employs collaborative filtering techniques to predict star ratings, incorporating user and item biases.

# Methodology
1. Predicting Book Read Status
- Jaccard Similarity:
  - Measures the overlap between users who have read the current book and those who have interacted with other books in the user's history.
  - Predictions are based on a similarity threshold (5%), determined iteratively for optimal performance.
- Popularity-Based Fallback:
  - Books in the top 70% of the most-read list among all users are prioritized when Jaccard similarity is insufficient.

This hybrid approach ensures a balance between personalized recommendations and global popularity trends.

2. Predicting Star Ratings
- Bias-Based Collaborative Filtering:
  - Initializes global averages, user biases, and item biases.
  - Uses gradient descent to iteratively optimize these biases.
  - Regularization is applied to prevent overfitting (lambda term tuned via validation).
  - Final predictions combine global averages, user biases, and item biases:
      - Prediction = Global Average + User Bias + Item Bias

# Tools and Libraries
- NumPy & Pandas: Data manipulation and numerical computations.

# Results
## Book Read Prediction
- High accuracy in identifying whether a user would read a given book.
- Hybrid approach ensures a good balance between personalization and general trends.
## Star Rating Prediction
- Bias-based collaborative filtering effectively captures user-specific tendencies and item-specific popularity.
- Regularization prevents overfitting, ensuring robust predictions.

# Future Enhancements
- Extend the hybrid model with content-based filtering for improved personalization.
- Implement matrix factorization techniques like SVD for star rating predictions.
- Explore neural network-based approaches for capturing complex user-item interactions.
