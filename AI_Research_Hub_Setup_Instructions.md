
# AI Research Hub: Development Setup Instructions

## Step 1: Set Up the Conda Environment
1. **Install Conda:**  
   If Conda is not installed, download and install it from [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html).

2. **Create a New Environment:**  
   Open the terminal or command prompt and run:
   ```bash
   conda create --name ai_research_hub python=3.9
   ```

3. **Activate the Environment:**  
   ```bash
   conda activate ai_research_hub
   ```

4. **Install Required Python Libraries:**  
   Install essential libraries for backend development:
   ```bash
   pip install flask fastapi uvicorn sqlalchemy psycopg2-binary
   ```

---

## Step 2: Set Up the Backend
1. **Navigate to Backend Folder:**  
   Create a directory for the backend code and navigate to it:
   ```bash
   mkdir -p AI-Research-Hub/src/backend
   cd AI-Research-Hub/src/backend
   ```

2. **Initialize the Flask App:**  
   Create a file called `app.py`:
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route("/")
   def home():
       return "Welcome to AI Research Hub!"

   if __name__ == "__main__":
       app.run(debug=True)
   ```

3. **Test the Backend:**  
   Run the backend:
   ```bash
   python app.py
   ```

4. **Install FastAPI:**  
   For API endpoints, create a separate `api` folder. Start with an example:
   ```bash
   pip install fastapi uvicorn
   ```

   Example FastAPI code in `src/backend/api/main.py`:
   ```python
   from fastapi import FastAPI

   app = FastAPI()

   @app.get("/")
   async def read_root():
       return {"message": "Hello, FastAPI!"}
   ```

   Run the FastAPI server:
   ```bash
   uvicorn src.backend.api.main:app --reload
   ```

---

## Step 3: Set Up the Frontend
1. **Install Node.js:**  
   Download and install Node.js from [Node.js Official Website](https://nodejs.org/).

2. **Create a Frontend Directory:**  
   Navigate to the `src` folder and create the `frontend` directory:
   ```bash
   mkdir -p AI-Research-Hub/src/frontend
   cd AI-Research-Hub/src/frontend
   ```

3. **Initialize the React App:**  
   Create a React application using:
   ```bash
   npx create-react-app .
   ```

4. **Start the React Server:**  
   Launch the development server:
   ```bash
   npm start
   ```

---

## Step 4: Set Up the PostgreSQL Database
1. **Install PostgreSQL:**  
   Download and install PostgreSQL from [PostgreSQL Downloads](https://www.postgresql.org/download/).

2. **Create a Database:**  
   Log into the PostgreSQL shell and create a new database:
   ```sql
   CREATE DATABASE ai_research_hub;
   ```

3. **Install Database Drivers:**  
   Install `psycopg2` for Python database interaction:
   ```bash
   pip install psycopg2-binary
   ```

4. **Connect to the Database:**  
   Example Python code in `src/backend/models/database.py`:
   ```python
   from sqlalchemy import create_engine

   DATABASE_URL = "postgresql://username:password@localhost/ai_research_hub"
   engine = create_engine(DATABASE_URL)

   # Example: Test Connection
   with engine.connect() as connection:
       result = connection.execute("SELECT 1")
       print("Database connected:", result.scalar())
   ```

---

## Step 5: Integration
1. **Link Frontend and Backend:**  
   Use `axios` or `fetch` in React to make API calls to the backend endpoints.

2. **Run the Application Locally:**  
   Start both the backend and frontend servers:
   - Backend (Flask):  
     ```bash
     python app.py
     ```
   - Backend (FastAPI):  
     ```bash
     uvicorn src.backend.api.main:app --reload
     ```
   - Frontend:  
     ```bash
     npm start
     ```

3. **Test Database Connection:**  
   Ensure the backend successfully connects to PostgreSQL.

---

## Next Steps for Development
- **Add Core Features:**
  - Implement dataset upload functionality in the backend.
  - Develop the ML sandbox for experimentation.
  - Add authentication via OAuth2.

- **Set Up Deployment:**
  - Configure AWS EC2 instance.
  - Use Docker to containerize the app for easier deployment.
