# BhaskarAcharya MathsSolver

A web-based math solver that provides step-by-step solutions, graphs, and explanations for a variety of mathematical problems, including simple calculations, functions, quadratic equations, and linear equations (one, two, and three variables).

  
**[View Live Demo](https://mathssolver.vercel.app/)**

## Features

- **Simple Calculator:** Evaluate arithmetic and complex expressions.
- **Function Solver:** Supports trigonometric and logarithmic functions with arguments.
- **Quadratic Equation Solver:** Finds roots, shows steps, and plots the graph.
- **Linear Equation Solver:** Handles equations in one, two, or three variables, with step-by-step solutions and graphing.
- **Step-by-Step Explanations:** Detailed breakdown of each calculation.
- **Graph Visualization:** Visual representation of results and equations.
- **Calculation History:** View and reuse previous calculations.
- **Theme Toggle:** Switch between light and dark modes.
- **Responsive UI:** Works on desktop and mobile devices.

## Project Structure

```
.
├── app.py                  # Main Flask application
├── Simple.py               # Simple calculator logic
├── Functionswitharg.py     # Function with argument logic
├── Quadratic.py            # Quadratic equation logic
├── Linearequation.py       # Linear equation logic
├── requirements.txt        # Python dependencies
├── package.json            # JS dependencies (for MathLive, etc.)
├── static/
│   ├── css/
│   ├── images/
│   └── script/
├── templates/
│   ├── home.html
│   ├── solver.html
│   ├── bot.html
│   ├── optionlink.html
│   ├── explaination.html
│   └── contact.html
└── vercel.json             # Vercel deployment config
```

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js (for frontend dependencies, optional)
- [Vercel CLI](https://vercel.com/docs/cli) (for deployment, optional)

### Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd 189-master
   ```

2. **Install Python dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **(Optional) Install frontend dependencies:**
   ```sh
   npm install
   ```

### Running Locally

```sh
python app.py
```
Visit [http://localhost:5000](http://localhost:5000) in your browser.

### Deployment

This project is ready to deploy on [Vercel](https://vercel.com/):

```sh
vercel
```
See [vercel.json](vercel.json) for configuration.

## Usage

- Go to the homepage and select "BhaskarAcharya MathsSolver".
- Enter your math problem and select the appropriate solver type.
- View the answer, step-by-step solution, and graph.
- Use the history sidebar to review or reuse previous calculations.

## Technologies Used

- **Backend:** Python, Flask, matplotlib
- **Frontend:** HTML, CSS, JavaScript, [MathLive](https://mathlive.io/)
- **Deployment:** Vercel

## Credits

Developed by [Ashutosh Shukla](https://github.com/panditashushukl).

## License

MIT License
