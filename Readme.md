# Kintsugi Product Classification

This project aims to classify products into various categories using a machine learning model. It leverages Python along with libraries like scikit-learn for model training and FastAPI for API creation. Below, you'll find the instructions on setting up the project and using the FastAPI endpoint to evaluate products.

## Setup

### Creating and Activating a Virtual Environment

To isolate the project dependencies, initiate a virtual environment in the project directory:

~~~bash
python3.11 -m venv venv
~~~

Activate the virtual environment using:

~~~bash
source venv/bin/activate
~~~

### Installing Dependencies

Install the required dependencies with the following command:

~~~bash
pip install -r requirements.txt
~~~

## Usage

### Training the Model

You can train the model by using the `train.sh` script in the `./bin/` directory, which triggers the `train.py` script to train and save the model and vectorizer as `.joblib` files:

~~~bash
./bin/train.sh
~~~

### Utilizing the FastAPI Server

Post the model training, initiate the FastAPI server to begin using the API. Ensure uvicorn is installed in your virtual environment, and execute the following command:

~~~bash
uvicorn main:app --reload
~~~

Access the API documentation at the following URL: 
`http://127.0.0.1:8000/docs`

## API Endpoints

The project hosts a FastAPI endpoint for product evaluation, using the trained model. Test the endpoint using the API documentation interface or through curl commands, as shown:

~~~bash
curl -X 'POST' \
  'http://127.0.0.1:8000/evaluate_product' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "product_name": "sample product",
  "product_type": "recurring"
}'
~~~
