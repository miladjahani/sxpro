# SimSXCu Web Application

This project transforms a Python-based copper solvent extraction simulation into a modern, interactive web application.

The application is built with a FastAPI backend and a React frontend.

## Technology Stack

- **Backend**: Python, FastAPI, NumPy, SciPy
- **Frontend**: React.js, Ant Design, Plotly.js, Axios
- **API**: RESTful API with JSON

## Features

- **Two Simulation Modes**:
  1.  **Designer Mode**: Solves for the optimal extractant concentration (`v/v%`).
  2.  **Plant Metallurgist Mode**: Solves for key operating parameters based on plant performance targets.
- **Dynamic UI**: Input forms adjust based on the selected mode.
- **Interactive Visualizations**:
    - Dynamic flowsheet diagram that updates with simulation results.
    - Interactive McCabe-Thiele plots for extraction and stripping stages.
- **Data Export**: Simulation results can be exported to CSV.
- **Responsive Design**: Usable on desktop, tablet, and mobile devices.

---

## Getting Started

### Prerequisites

-   Python 3.8+ and `pip`
-   Node.js 16+ and `npm`

### 1. Backend Setup

First, navigate to the `backend` directory and set up a virtual environment.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Start the backend server
# The server will run on http://127.0.0.1:8000
uvicorn app.main:app --reload
```

### 2. Frontend Setup

Open a **new terminal window**, navigate to the `frontend` directory, and install the dependencies.

```bash
# Navigate to the frontend directory
cd frontend

# Install the required npm packages
npm install

# Start the React development server
# The application will open in your browser at http://localhost:3000
npm start
```

### 3. Usage

Once both the backend and frontend servers are running, you can access the application at `http://localhost:3000`.

-   Use the **Input Panel** on the left to select a configuration and simulation mode.
-   Fill in the required parameters for the chosen mode.
-   Click the **"Run Simulation"** button.
-   View the results, including key metrics, the flowsheet diagram, and McCabe-Thiele plots, in the **Output Panel** on the right.

---

## 4. Deployment Guide

Deploying this full-stack application involves two separate components: the **Backend API** and the **Frontend Application**.

### A. Deploying the Backend

The FastAPI backend must be deployed to a hosting service that can run a Python web server (e.g., Vercel, Heroku, AWS, Google Cloud).

1.  **Choose a Hosting Provider**: Select a platform that supports Python/WSGI applications.
2.  **Deploy**: Follow your chosen provider's instructions for deploying a FastAPI application. They will typically involve pointing the service to your `backend` directory and specifying how to run the server (e.g., using `uvicorn app.main:app`).
3.  **Get the Public URL**: Once deployed, the service will provide you with a public URL for your API (e.g., `https://your-simsxcu-api.onrender.com`). You will need this URL for the next step.

### B. Deploying the Frontend to GitHub Pages

The React frontend can be deployed to any static hosting service. Here are the instructions for deploying to **GitHub Pages**.

1.  **Set the Backend API URL**:
    The frontend needs to know the public URL of your deployed backend. You provide this using an environment variable named `REACT_APP_API_URL`.

2.  **Build the Application**:
    Run the build command from the `frontend` directory, prefixing it with your public API URL.

    ```bash
    # From the frontend directory
    cd frontend

    # Replace the URL with your actual deployed backend URL
    REACT_APP_API_URL=https://your-simsxcu-api.onrender.com npm run build
    ```
    This command creates an optimized, production-ready build in the `frontend/build` directory. The `homepage` property in `package.json` is set to `.` to ensure all asset links are relative, which is required for GitHub Pages.

3.  **Deploy to GitHub Pages**:
    The easiest way to deploy the `build` folder is to use the `gh-pages` package.

    ```bash
    # Install the gh-pages package if you haven't already
    npm install --save-dev gh-pages

    # Add a "deploy" script to your package.json scripts section:
    # "deploy": "gh-pages -d build"

    # Run the deploy script
    npm run deploy
    ```
    This will push the contents of your `build` directory to a new `gh-pages` branch on your GitHub repository, which will be automatically hosted by GitHub Pages.