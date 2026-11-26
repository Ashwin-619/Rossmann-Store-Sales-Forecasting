from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from src.pipeline.data_pipeline import FeaturePipeline
from src.schema.input_data import InputFeatures, InsertData
from src.inference.predictor import TwoStageModelPipeline
from src.database.storing_data import save_inference_data
from src.database.inference_to_main import inference_to_main

app = FastAPI()

feature_pipeline = FeaturePipeline()

model_pipeline = TwoStageModelPipeline(
    customer_model_path=r"models\customer_final_model.pkl",
    sales_model_path=r"models\sales_final_model.pkl",
    customer_col_name="predicted_customers"  # Match column name used during training
)

@app.get('/')
def home():
    return {'message': 'Two-stage sales prediction service online.'}

@app.post('/predict')
def predict(data: InputFeatures):
    # Step A: Transform raw payload into 1-row feature DataFrame
    features_df = feature_pipeline.transform(data)

    # Step B: Run sequential inference (Customer Model -> Sales Model)
    results = model_pipeline.predict(features_df)

    # Step C: Save inference data
    save_inference_data(
        inference_data=features_df.to_dict(orient="records")[0],
        db_path=r"DB\Sales_data.db",
        predicted_customers=results['predicted_customers'],
        predicted_sales=results['predicted_sales'],
        date=data.Date.isoformat()
    )

    # Step C: Return clean JSON payload
    return {
        "predictions_for_Sales": results['predicted_sales'],
        "predictions_for_Customers": results['predicted_customers'],
        "input" : features_df.to_dict(orient="records")[0]  # Return the input features for reference
    }

@app.post('/insert_data')
def insert_sales_data(data: InsertData):
    # Insert data into the database 
    data_dict = data.model_dump(mode="python")
    message=inference_to_main(data_dict)
    return message

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(exc: StarletteHTTPException):
    return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = {
        "detail": "Validation error",
        "errors": exc.errors(),
        "body": exc.body
    }
    return JSONResponse(status_code=422, content=content)
