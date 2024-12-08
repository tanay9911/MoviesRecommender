
# Movies Recommender System

## Authors:
- Md Mudassir Ali (IMT2022054)
- Sparsh Salodkar (IMT2022113)
- Tanay Nagarkar  (IMT2022083)

## Introduction
This is a Flask-based Movies Recommender System that uses a dataset of movies to provide recommendations based on user input. The system also integrates with the OMDb API to fetch additional movie details like posters, ratings, and overviews.

## Folder Structure
MoviesRecommender/
├── app.py            # Main Flask application file
├── movies.csv        # Dataset containing movie details
├── templates/        # Folder for HTML templates
│   └── index.html    # Main homepage template
├── static/           # Folder for static files (e.g., CSS, JS)
└── README.md         # This file

## Prerequisites
- Python 3.7 or higher installed on your system.
- Flask library installed.
- Other necessary Python libraries:
  - pandas
  - requests
  - scikit-learn

## How to Set Up and Run the Project

### 1. Download the Project:
Download or copy the project files into a folder on your local system. Ensure that you have the following files:
- `app.py` (Main application script)
- `movies.csv` (Dataset)
- `templates/` (Folder containing HTML templates)
- `static/` (Folder containing static files like CSS and JS)

### 2. Install Required Libraries:
Ensure you have `pip` installed. Use the following command to install the required libraries:
pip install flask pandas requests scikit-learn

### 3. Place Your Dataset:
Ensure the `movies.csv` file is placed in the root directory (MoviesRecommender/) alongside `app.py`.

### 4. Run the Flask Application:
Navigate to the MoviesRecommender/ folder and run the Flask application using:
python app.py

### 5. Access the Application:
Once the Flask server is running, open your web browser and navigate to:
http://127.0.0.1:5000/

## How to Use
1. Enter a part or full title of a movie in the search bar.
2. The system will display a list of recommended movies along with additional details such as:
    - Overview
    - Poster
    - IMDb rating
    - Release date

## Troubleshooting
- **Flask App Not Running?**
    - Ensure you have Python 3.x installed.
    - Check if all libraries are installed correctly.
    - Verify that the `app.py` file is in the correct folder.

- **Incorrect API Responses?**
    - Ensure your internet connection is active.
    - Confirm that the OMDb API key is valid.

## License
This project is licensed under the MIT License.
