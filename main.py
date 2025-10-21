from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np

class IrisFeatures(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

class Prediction(BaseModel):
    prediction: int
    label: str

CLASS_LABELS = {
    0: "Setosa",
    1: "Versicolor",
    2: "Virginica"
}

class InputMessage(BaseModel):
    message: str
    user_id: int

class OutputMessage(BaseModel):
    message: str
    status_code: int

app = FastAPI(title = "Learning APIs")

model = joblib.load('model.pkl')

@app.post("/hello", response_model=OutputMessage)
def say_hello(payload: InputMessage):
    response_text = f"Hello {payload.user_id}! You said: '{payload.message}'"
    return OutputMessage(message=response_text, status_code=200)

@app.get("/")
def health_check():
    return {"status": "OK"}


@app.post("/predict", response_model=Prediction)
def predict_flower(features: IrisFeatures):
    data_to_predict = np.array([
        [
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]
    ])

    raw_prediction = model.predict(data_to_predict)
    pred_int = int(raw_prediction[0])
    label = CLASS_LABELS[pred_int]

    return Prediction(prediction=pred_int, label=label)