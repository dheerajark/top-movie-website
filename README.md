# Movie Collection Manager

This web application allows users to manage a collection of movies. Users can add new movies, edit the details of existing movies, and delete movies from the collection.

## Features

- View a list of all movies in the collection.
- Add new movies to the collection by searching for them using the TMDB API.
- Edit the rating and review of existing movies.
- Delete movies from the collection.

## Technologies Used

- Python
- Flask
- Flask-WTF (for forms)
- Flask-SQLAlchemy (for database management)
- Flask-Bootstrap (for UI styling)
- requests (for making HTTP requests to the TMDB API)
- dotenv (for environment variable management)

## Setup

1. Clone the repository:

```bash
git clone <repository-url>
cd movie-collection-manager
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Set up the environment variables:

   - Create a `.env` file in the project root directory.
   - Add the following environment variables to the `.env` file:

     ```plaintext
     FLASK_KEY=<your-flask-secret-key>
     API_KEY=<your-tmdb-api-key>
     ```

4. Run the application:

```bash
python app.py
```

5. Access the application:

   Open a web browser and navigate to `http://localhost:5000/` to access the application.

## Usage

- Upon accessing the application, you will see a list of movies in the collection.
- You can add a new movie by clicking on the "Add Movie" button and searching for it using the TMDB API.
- To edit the rating and review of a movie, click on the "Edit" button next to the movie.
- To delete a movie, click on the "Delete" button next to the movie.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please fork the repository and submit a pull request.

## License

This project is licensed under the (LICENSE).
```

Feel free to customize the content based on your specific requirements and features of your Flask application.