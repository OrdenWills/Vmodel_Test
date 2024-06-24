# Video Recommendation System
This repository contains a basic video recommendation system implemented in Python. The system uses user watch history and video metadata to suggest relevant videos.
### Features:
* Data Parsing: Parses a JSON file containing user and video data into appropriate data structures.
* Similarity Calculation: Implements cosine similarity to measure the similarity between videos based on their categories and tags.
* Recommendation Algorithm: Utilizes a hybrid approach combining user-based collaborative filtering and content-based filtering for generating recommendations.
* Top-N Recommendations: Returns the top N recommended video IDs for a given user.(
### Requirements:
Python 3.9+
scipy (installed via pip install scipy)
