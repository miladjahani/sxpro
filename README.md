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

## 4. Deployment (Production Build)

To deploy the frontend to a static hosting service like GitHub Pages, Netlify, or Vercel, you need to create a production-ready build. This process compiles and optimizes the React code and generates static HTML, CSS, and JavaScript files, including the necessary `index.html`.

From the `frontend` directory, run the following command:

```bash
# Navigate to the frontend directory if you are not already there
cd frontend

# Create the production build
npm run build
```

This command creates a `build` directory inside the `frontend` folder. The contents of this `build` directory are all you need to deploy the application. You can upload this folder to your hosting provider.