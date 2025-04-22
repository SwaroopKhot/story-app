# Story App Backend (FastAPI + MongoDB)

A secure backend application built with FastAPI, implementing user authentication via OAuth2.0, complete CRUD functionality for stories, and a background task system for batch updates.

---

## Features

- User Authentication: Secure login with token-based access (OAuth2.0 + JWT)
- Story CRUD: Create, Read, Update, Delete stories
- Background Task: Periodically or manually trigger batch updates for the country field
- Database: MongoDB (via Motor) for asynchronous database access
- Dockerized: Complete setup with Docker Compose for easy deployment
- Periodic Batch Update: To update the Country field automatically (every 1 minute)

---

## Tech Stack

- **Framework**: FastAPI
- **Database**: MongoDB
- **Authentication**: OAuth2.0 with JWT token
- **Task Queue**: FastAPI BackgroundTasks
- **Containerization**: Docker & Docker Compose

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/SwaroopKhot/story-app.git
cd story-app/StoryApp-backend
```

### 2. Choose Setup Option:

### Option 1: Local Setup

#### 1. Setup End to use mongo-db present at your local machine:
```bash
MONGO_URL=mongodb://localhost:27017
```

#### 2. Create Virtual Environment:

- For Windows:
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

- For macOS/Linux:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

#### 3: Install Dependencies:
```bash
pip install -r requirements.txt
```

#### 4. Run the Server:
```bash
uvicorn main:app --reload
```

The backend will typically run at: http://127.0.0.1:8000

### Option 2: Docker Setup (Recommended)

#### 1. Modify .env variable:
Ensure inside .env this variable is set to the name of your mondodb container (in this case it is mongo):
```bash
MONGO_URL=mongodb://mongo:27017
```

#### Run Docker Compose:
```bash
docker-compose up --build -d
```
Once the containers are up, you can access the backend at: http://127.0.0.1:8000

### 3. Accessing Postman API Endpoints

#### 1. Import API Endpoints into Postman:

- Open Postman and click on Import.
- Select File and import the file from: <b>StoryApp-backend/postman_endpoints</b>
- The API collection will be available with valid payloads and authorization headers.


## API Endpoints:

### AUTH Management API's:
<table>
    <tr>
        <th>Method</th>
        <th>Endpoint</th>
        <th>Description</th>
        <th>Auth Required</th>
    </tr>
    <tr>
        <td>POST</td>
        <td>/auth/register</td>
        <td>Register a new user</td>
        <td>No</td>
    </tr>
    <tr>
        <td>POST</td>
        <td>/auth/login</td>
        <td>Obtain JWT token (login)</td>
        <td>No</td>
    </tr>
</table>


### STORY Management API's
<table> 
    <tr> 
        <th>Method</th> 
        <th>Endpoint</th> 
        <th>Description</th> 
        <th>Auth Required</th> 
    </tr> 
    <tr> 
        <td>GET</td> 
        <td>/story/</td> 
        <td>Retrieve all stories</td> 
        <td>No</td> 
    </tr> 
    <tr> 
        <td>GET</td> 
        <td>/story/{story_id}</td> 
        <td>Retrieve a specific story by ID</td> 
        <td>No</td> 
    </tr> 
    <tr> 
        <td>POST</td> 
        <td>/story/create</td> 
        <td>Create a new story</td>
        <td>Yes</td> 
    </tr> 
    <tr> 
        <td>PUT</td> 
        <td>/story/id/{story_id}</td> 
        <td>Update an existing story</td> 
        <td>Yes</td> 
    </tr> 
    <tr> 
        <td>DELETE</td> 
        <td>/story/id/{story_id}</td> 
        <td>Delete a story</td> 
        <td>Yes</td> 
    </tr> 
</table>


### Background Task API:
<table> 
    <tr> 
        <th>Method</th> 
        <th>Endpoint</th> 
        <th>Description</th> 
        <th>Auth Required</th> 
    </tr> 
    <tr> 
        <td>POST</td> 
        <td>/story/batch/update-countries</td> 
        <td>Manually trigger batch update of country field</td> 
        <td>Yes</td> 
    </tr> 
</table>