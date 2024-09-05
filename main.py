from fastapi import FastAPI, HTTPException
from service import ClassifyProduct
from typing import Union
# from mangum import Mangum
from models import (
    Classification,
    ClassificationRequest,
    ProductClassificationResponse,
    ProductClassificationRequest
)
from config import init_sentry
import logging

init_sentry()
app = FastAPI()
# handler = Mangum(app)

@app.get("/")
async def health():
    return "OK"


@app.post("/evaluate-product", response_model=Classification)
def evaluate_endpoint(request: ClassificationRequest):
    classification = {"category": "UNKNOWN"}
    return classification


@app.post("/classification", response_model=ProductClassificationResponse)
def classify_product(request: ProductClassificationRequest):
    # Assuming you have some classification logic here
    # For simplicity, let's just return the first existing product's category and subcategory
    if request.existing_products:
        existing_products = request.existing_products
        new_product = request.product_to_classify  
        user_pref_category = request.user_pref_category
        user_pref_subcategory = request.user_pref_subcategory
        user_pref_description = request.user_pref_description
        classify = ClassifyProduct()
        classified_response = classify.classify_product_category(existing_products,new_product,user_pref_category,user_pref_subcategory,user_pref_description)
        logging.info(f"INFO: printing classified_response: {classified_response}")
        return classified_response
    else:
        raise HTTPException(status_code=400, detail="No existing products provided for classification")
