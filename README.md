# Note-Taking Application API

## Overview
 This application provides a RESTful API for a basic note-taking application. You can interact with it via HTTP requests allowing to create, retrieve, update or delete notes. The API is built in Python, specifically the `http.server` module included in the standard library. Also it uses a MySQL database for persistence.

## Prerequisites
- Docker installed on your machine.
- Basic knowledge of Docker commands and operations.
- Git for version control.

## Setup and Installation
1. **Clone the Repository**
    ```bash
    git clone https://github.com/LuqmanDirie/BTP405
    cd directory-name
    ```

2. **Build and Run with Docker Compose**

    Use Docker Compose to build and run the application and database services:
    ```bash
    docker-compose up --build
    ```

    This command creates the API server image, and starts the services defined in docker-compose.yml.

3. **Stopping the Services**

    To stop the services and remove the containers, use the following command:
    ```bash
    docker-compose down
    ```

## API Endpoints

The API supports the following operations:

### GET /notes - Retrieve All Notes
- **Objective**: Retrieves all the notes.
- **Method**: GET
- **URL**: `http://localhost:8080/notes`
- **Body**: None
- **Instructions**: Set the request method to GET, enter the URL, and send the request.

### POST /notes - Create a New Note
- **Objective**: Creates a new note.
- **Method**: POST
- **URL**: `http://localhost:8080/notes`
- **Body**: (application/json)
    ```json
    {
      "title": "New Note",
      "content": "Content of the new note."
    }
    ```
 – **Instructions**: **POST** – **URL** – **Body**: ‘raw’ – **Type**: JSON – **Send**:

### PUT /notes - Update an Existing Note
- **Objective**: Updates an existing note by ID.
- **Method**: PUT
- **URL**: `http://localhost:8080/notes?id=1` (Replace `1` with the actual note ID)
- **Body**: (application/json)
    ```json
    {
      "title": "Updated Note",
      "content": "Updated content."
    }
    ```
- **Instructions**: Set the request method to PUT, paste the URL, select Body from the tabs, set to 'raw', set the Type to 'JSON', past the JSON to edit the note, and submit the request.

### DELETE /notes - Delete a Note
- **Objective**: Deletes an existing note by ID.
- **Method**: DELETE
- **URL**: `http://localhost:8080/notes?id=1` (Replace `1` with the actual note ID)
- **Body**: None
- **Instructions**: Set the request method to DELETE, enter the URL, and send the request.

## Testing

 You can invoke the API endpoints using a graphics user interface (GUI) such as [Postman](https://www.postman.com/) pretending to be a browser client, or using the `curl` commands similar to those in the examples above.

## Additional Information

- The MySQL database is initialized with a `notes` table, which has the columns `id`, `title`, and `content`.
- The API server runs on port `8080`, and the MySQL service is exposed on the default port `3306`.
- Ensure you have the `.env` file with necessary environment variables if you have sensitive or environment-specific configurations.

## Contributors

- Luqman Dirie (https://github.com/LuqmanDirie/BTP405)