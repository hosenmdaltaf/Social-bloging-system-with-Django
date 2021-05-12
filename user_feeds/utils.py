
import random

import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer

from user_feeds.models import Post


# Load Movies Metadata
posts =Post.objects.all().values()
metadata = pd.DataFrame(posts)

#Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
tfidf = TfidfVectorizer(stop_words='english')

#Replace NaN with an empty string
metadata['content'] = metadata['content'].fillna('')

#Construct the required TF-IDF matrix by fitting and transforming the data
tfidf_matrix = tfidf.fit_transform(metadata['content'])

# Compute the cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
# cosine_sim.shape
# cosine_sim[1]
indices = pd.Series(metadata.index, index=metadata['title']).drop_duplicates()
indices[:7]

# Function that takes in movie title as input and outputs most similar movies
def get_recommendations(title='', post_number=5):

    try:
        # Get the index of the movie that matches the title
        idx = indices[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores,key=lambda x: x[1], reverse=True)
        # sim_scores = sorted(sim_scores, reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:5]

        # Get the movie indices
        post_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        similar_posts = metadata['id'].iloc[post_indices].tolist()
    except:
        similar_posts = []

    post_objects = []

    for item in similar_posts:
        if len(post_objects) > post_number:
            break
        post = Post.objects.get(pk=item)
        post_objects.append(post)
    
    if len(post_objects) < post_number:
        all_posts = list(Post.objects.all())
        random_post_number = post_number - len(post_objects)
        random_posts = random.sample(all_posts, random_post_number)
        for random_post in random_posts:
            post_objects.append(random_post)
    
    return post_objects



