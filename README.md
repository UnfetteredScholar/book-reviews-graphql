# Book Reviews Service API

This is a Book Reviews Service API built with FastAPI for the REST endpoints and Strawberry for the GraphQL endpoints. It allows users to manage book reviews, including adding, updating, retrieving, and deleting reviews.

## Features

- **REST API** built with FastAPI
- **GraphQL API** built with Strawberry
- CRUD operations for book reviews
- JSON Web Token (JWT) authentication
- Pagination and filtering for retrieving reviews
- Input validation using Pydantic
- Async support for improved performance

## Table of Contents

- [Installation](#installation)
- [Running the App](#running-the-app)
- [API Documentation](#api-documentation)
- [GraphQL Queries and Mutations](#graphql-queries-and-mutations)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install and run the application, follow these steps:

1. Clone the repository:

   ```bash
   https://github.com/UnfetteredScholar/book-reviews-graphql.git

2. Navigate to the project directory:

    ```bash
    cd book-reviews-graphql

3. Create a virtual environment:

    ```bash
    python -m venv venv

4. Activate the virtual environment:

On macOS/Linux:
    
    ```bash
    source venv/bin/activate

On Windows:

    ```bash
    venv\Scripts\activate
    

5. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    
    
6. Set up environment variables in a .env file (optional, if needed):

    ```bash
    SECRET_KEY=<your_secret_key>
    DATABASE_URL=<your_database_url>


## Running the App
1. Start the FastAPI development server:

    ```bash
    uvicorn main:app --reload

2. The API will be available at:
    * REST API: http://localhost:8000
    * GraphQL API: http://localhost:8000/graphql


## API Documentation
FastAPI automatically generates API documentation:

* Swagger UI: http://localhost:8000/docs
* Redoc: http://localhost:8000/redoc
These provide interactive interfaces for testing REST API endpoints.

### Example Endpoints
* POST /reviews/: Create a new review
* GET /reviews/: Retrieve all reviews with pagination
* GET /reviews/{id}: Retrieve a review by ID
* PUT /reviews/{id}: Update a review
* DELETE /reviews/{id}: Delete a review


## GraphQL Queries and Mutations
You can access the GraphQL playground at http://localhost:8000/graphql to test queries and mutations.

### Example Queries:
    ```graphql
    query GetReviews {
    reviews {
        id
        bookTitle
        reviewText
        rating
        reviewer {
        name
        }
    }
    }

### Example Mutations:
    ```graphql
    mutation CreateReview {
    createReview(input: {
        bookTitle: "1984",
        reviewText: "A masterpiece of dystopian fiction.",
        rating: 5,
        reviewerId: 1
    }) {
        id
        bookTitle
    }
    }


## Running Tests
1. Install the development dependencies:

    ```bash
    pip install -r requirements-dev.txt

2. Run the tests:

    ```bash
    pytest


## Contributing
We welcome contributions! 

Please see the CONTRIBUTING.md file for guidelines on how to contribute.

## License
This project is licensed under the MIT License - see the LICENSE file for details.