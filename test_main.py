from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}

def test_predict_setosa():
    """Tests the /predict endpoint with known setosa data."""
    # This is the sample data we saw in create_model.py
    payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=payload)

    # Check that the API returned a successful status
    assert response.status_code == 200

    # Check that the prediction is correct
    data = response.json()
    assert data["label"] == "Setosa"
    assert data["prediction"] == 0

def test_predict_bad_input():
    """Tests the API's validation. What if we send a string?"""
    payload = {
        "sepal_length": "this-is-not-a-float",
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    response = client.post("/predict", json=payload)

    # Pydantic (via FastAPI) should catch this and return a 422 error
    assert response.status_code == 422