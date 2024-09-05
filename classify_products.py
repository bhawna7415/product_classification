from typing import List,Dict
import openai
import json
import os
from prompts import SYSTEM_PROMPT_CATAGORY,SYSTEM_PROMPT_FOR_SUBCATAGORY

def call_json_gpt(messages:List):
    try:
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo-1106',
            messages=messages,
            temperature=0,
            response_format={"type": "json_object" }
        )
        response_message = response['choices'][0]['message']['content']
        print("Raw response:", response_message)
        
        try:
            return json.loads(response_message)
        except json.JSONDecodeError:
            print("No valid JSON found in the response.")
    except Exception as e:
        print(f"OpenAI request failed with error: {e}")
        return None

def classify_products_catagories(products:List[str]) -> Dict[str, str]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_CATAGORY},
        {"role": "user", "content": f"Classify the products: \nProducts to classify.Please format your response as a JSON array where each item is an object with the product as the key and its category as the value.: {json.dumps(products)}"},
    ]
    return call_json_gpt(messages=messages)

def classify_subcategories(categorized_products: Dict[str, str]) -> List[Dict[str, str]]:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT_FOR_SUBCATAGORY},
        {"role": "user", "content": f"Classify the products into subcategories: \n{json.dumps(categorized_products)}"},
    ]
    return call_json_gpt(messages=messages)

def transform_items(items_with_category, items_with_subcategory):
    result = []
    for item, category in items_with_category.items():
        subcategory = items_with_subcategory.get(item, "Unknown")
        result.append({
            "item": item,
            "category": category,
            "subcategory": subcategory
        })
    return result

if __name__=="__main__":
    openai.api_key = os.getenv('OPENAI_API_KEY')
    products = [
        "Netflix subscription",
        "Lawn mowing",
        "Printed book",
        "Downloaded app",
        "Massage",
        "Online guitar lessons",
        "Physical CD",
        "Laptop",
        "Website design",
        "Cloud storage"
    ]

    # Step 1: Classify main categories
    categories = classify_products_catagories(products)
    if categories:
        print(f"\nClassified Categories:", categories)
    else:
        print("Failed to classify categories.")
        exit()

    # Step 2: Classify subcategories
    subcategories = classify_subcategories(categories)
    if subcategories:
        print(f"\nClassified Subcategories:", subcategories)
    else:
        print("Failed to classify subcategories.")
        exit()
    
    # Step 3: Transform the data into a more readable format
    final_result = transform_items(categories, subcategories)
    print("\nFinal Result:",final_result)
