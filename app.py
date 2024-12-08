from flask import Flask, request, jsonify, render_template  # Importing necessary Flask components for app, request handling, and rendering templates
import pandas as pd  # Importing pandas for data handling
import requests  # Importing requests library to make HTTP requests
from sklearn.feature_extraction.text import TfidfVectorizer  # Importing TF-IDF vectorizer for text feature extraction
from sklearn.metrics.pairwise import cosine_similarity  # Importing cosine similarity for similarity computation
import logging  # Importing logging for debugging purposes

app = Flask(__name__)  # Initializing the Flask app

# Load your dataset
dataset = pd.read_csv('C:\\Users\\roopa\\OneDrive\\Desktop\\MoviesRecommender\\movies.csv')  # Loading dataset from a CSV file path

# Fill missing values and create combined features
dataset['genre'] = dataset['genre'].fillna('unknown')  # Filling missing genre values with 'unknown' to handle NaN
dataset['overview'] = dataset['overview'].fillna('')  # Filling missing overview values with an empty string
dataset['combined_features'] = dataset['genre'] + ' ' + dataset['overview']  # Combining genre and overview columns into a new feature for analysis

# Create TF-IDF Matrix
tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)  # Initializing TF-IDF vectorizer with specified parameters
tfidf_matrix = tfidf.fit_transform(dataset['combined_features'])  # Transforming combined features into a TF-IDF matrix

# Calculate Cosine Similarity
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)  # Calculating cosine similarity matrix from TF-IDF matrix

# Set up logging
logging.basicConfig(level=logging.DEBUG)  # Configuring logging to display debug-level messages

# Define your OMDb API key here
OMDB_API_KEY = "6f5cb803"  # Defining API key for OMDb API for movie data retrieval

def recommend_movies_hierarchical(title_substring, num_recommendations=10):  # Defining function to recommend movies based on input title substring
    title_substring = title_substring.lower().strip()  # Converting input title substring to lowercase and stripping whitespace for consistency
    filtered_titles = dataset[dataset['title'].str.lower().str.contains(title_substring)]  # Filtering dataset for titles containing the substring

    if filtered_titles.empty:  # Checking if no matching titles were found
        words = title_substring.split()  # Splitting substring into individual words
        if len(words) > 1:  # Checking if multiple words are present
            substring_without_last = ' '.join(words[:-1])  # Removing the last word to create a new search substring
            filtered_titles = dataset[dataset['title'].str.lower().str.contains(substring_without_last)]  # Re-filtering dataset with the shortened substring

    if filtered_titles.empty:  # Returning an empty list if still no titles match
        return []

    filtered_indices = filtered_titles.index.tolist()  # Storing indices of matched titles
    filtered_cosine_sim = cosine_sim[filtered_indices, :][:, filtered_indices]  # Creating similarity matrix for matched titles only
    sim_scores = list(enumerate(filtered_cosine_sim.sum(axis=1)))  # Summing similarity scores for each title and enumerating indices
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)  # Sorting similarity scores in descending order
    movie_indices = [filtered_indices[i[0]] for i in sim_scores[:num_recommendations]]  # Selecting top recommendations based on similarity scores

    recommendations = []  # Initializing list to store recommendation results
    for idx in movie_indices:  # Looping through each recommended movie index
        movie_title = dataset['title'].iloc[idx]  # Retrieving movie title for each index
        release_date = dataset['release_date'].iloc[idx]  # Retrieving movie release date for each index

        # Making the API request with the correct URL format
        response = requests.get(f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}")  # Fetching data from OMDb API for each title
        movie_data = response.json()  # Parsing JSON response from the API

        # Logging the response for debugging
        logging.debug(f"OMDb API response for '{movie_title}': {movie_data}")  # Logging API response data for debugging

        if movie_data.get("Response") == "True":  # Checking if API response indicates success
            recommendations.append({  # Appending movie details to recommendations list
                'title': movie_title,
                'overview': movie_data.get("Plot", "Overview not available"),  # Using default text if overview is missing
                'poster_url': movie_data.get("Poster", "https://via.placeholder.com/300x450?text=No+Image+Available"),  # Providing placeholder if no image
                'rating': movie_data.get("imdbRating", "N/A"),  # Adding IMDb rating or 'N/A' if missing
                'popularity': movie_data.get("Metascore", "N/A"),  # Adding Metascore or 'N/A' if missing
                'release_date': release_date  # Adding release date from local dataset
                
            })
        else:  # Handling cases where the API response is unsuccessful
            logging.warning(f"Could not fetch data for '{movie_title}': {movie_data.get('Error')}")  # Logging error for unsuccessful API call

    return recommendations  # Returning list of recommendations

@app.route('/')  # Setting route for homepage
def index():  # Defining index function to render the homepage
    return render_template('index.html')  # Returning HTML template for homepage

@app.route('/recommend', methods=['GET'])  # Setting route for recommendations API endpoint with GET method
def recommend():  # Defining recommend function to handle movie recommendation requests
    title = request.args.get('title', '')  # Retrieving 'title' query parameter from request
    if not title:  # Checking if title parameter is empty
        return jsonify({"error": "Please provide a movie title."}), 400  # Returning error message with status 400 if title is missing

    recommendations = recommend_movies_hierarchical(title)  # Getting recommendations by calling recommendation function
    return jsonify(recommendations)  # Returning recommendations in JSON format

if __name__ == "__main__":  # Checking if this script is being run directly
    app.run(debug=True)  # Running Flask app in debug mode
