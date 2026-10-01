"""
fastapi_basicapp.py
Social Eagle - CAIE Course Program | Assignment 4 (Basic FastAPI App)

Endpoints:
  GET /                     -> welcome message
  GET /greet/{name}         -> greets the name taken from the URL path
                               optional query parameter: ?language=en|ta|hi
  GET /add?a=5&b=7          -> adds two numbers taken from query parameters

Run:   uvicorn fastapi_basicapp:app --reload
Open:  http://127.0.0.1:8000        (the app)
       http://127.0.0.1:8000/docs   (interactive docs)
"""

from datetime import datetime

from fastapi import FastAPI, HTTPException

# ---------- Create the app ----------
# The title, description and version appear at the top of the /docs page.
app = FastAPI(
    title="Basic FastAPI App",
    description="Social Eagle CAIE Assignment 4 - a first, small API.",
    version="1.0.0",
)

# Greetings in a few languages for the /greet endpoint
GREETINGS = {
    "en": "Hello",
    "ta": "Vanakkam",
    "hi": "Namaste",
}


# ---------- Endpoint 1: root ----------
@app.get("/", tags=["General"])
def read_root():
    """Return a simple welcome message."""
    return {
        "message": "Hello, FastAPI",
        "docs": "Visit /docs to try the endpoints",
    }


# ---------- Endpoint 2: path parameter (+ optional query parameter) ----------
@app.get("/greet/{name}", tags=["Greeting"])
def greet(name: str, language: str = "en"):
    """
    Greet a person by name.

    - **name** (path parameter): the person's name, e.g. /greet/Remya
    - **language** (optional query parameter): en, ta or hi. Defaults to en.
    """
    language = language.lower()
    if language not in GREETINGS:
        # A clear error instead of a crash when the value is not supported
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported language '{language}'. Use one of: {', '.join(GREETINGS)}",
        )
    return {
        "name": name,
        "language": language,
        "greeting": f"{GREETINGS[language]}, {name}!",
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ---------- Endpoint 3: query parameters ----------
@app.get("/add", tags=["Calculator"])
def add(a: float, b: float):
    """
    Add two numbers given as query parameters, e.g. /add?a=5&b=7.

    Both a and b are required. If one is missing or is not a number,
    FastAPI automatically returns a 422 error explaining what is wrong.
    """
    return {"a": a, "b": b, "sum": a + b}
