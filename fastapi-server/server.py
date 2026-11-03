from fastapi import FastAPI, File, UploadFile
from model_helper import predict
import tempfile, os


app = FastAPI()

@app.post("/predict")
async def get_prediction(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
            tmp.write(image_bytes)
            image_path = tmp.name
        try:
            prediction = predict(image_path)
        finally:
            os.remove(image_path)
        return {"prediction": prediction}
    except Exception as e:
        return {"error": str(e)}