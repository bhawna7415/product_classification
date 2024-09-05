from collections import Counter
import json
import requests
from config import OPENAI_API_KEY
import logging
import ssl
import certifi
import tiktoken
import re

class ClassifyProduct:
    def __init__(self):
        # self.model = "ft:gpt-3.5-turbo-0613:kintsugi::8pa5WI2v"
        self.model = "gpt-3.5-turbo"
        # self.model = "gpt-4"
    
    def count_token(self, text: str, enc_str: str="cl100k_base") -> int:
        try:
            encoded = tiktoken.get_encoding(enc_str)
            token_count = len(encoded.encode(text))
            return token_count
        except Exception as e:
            logging.info("Error in count_token:", e)
            return 0

    def run(self, existing_products, new_product, user_pref_category, user_pref_subcategory, user_pref_description):
        existing_products_str = '\n'.join(
            [f"{p.product_name}, {p.product_category}, {p.product_subcategory}" for p in existing_products])
        new_product_str = f"{new_product.product_name} {new_product.product_description}"

        while True:
            tokens_in_request = self.count_token(existing_products_str + new_product_str)
            if tokens_in_request >= 4096:
                existing_products = existing_products[:-2]
                existing_products_str = '\n'.join(
                    [f"{p.product_name}, {p.product_category}, {p.product_subcategory}" for p in existing_products])
            else:
                break

        existing_product_instructions = (
            "You are a powerful AI trained to classify product category and subcategory for the New Product based on the data you have.\n"
            "Return the product title, category, and subcategory:\n\n"
            "- If the category or subcategory has status 'approved', give them priority\n"
            "- If the category or subcategory is 'UNKNOWN', then ignore it\n"
            "**important - if provided name and description are not valid products then provide category and subcategory as 'invalid'\n"
            
            "Below are the definitions and examples for various product categories and their respective subcategories. Use these to classify products into the appropriate category and subcategory.\n\n"

            "Categories and Subcategories\n"
            "1. Services\n"
            "Services refer to non-tangible activities provided by businesses to customers. These can include:\n"
            "- General Services: Broad activities.\n"
            " - Example: House cleaning services, car repair,pet sitting, tutoring.\n"
            "- Professional Services: Specialized skills or knowledge-based services provider.\n"
            " - Example: such as Legal consulting, accounting services.\n"
            "- Services to Tangible Personal Property (TPP): Services performed on physical goods or movable items.\n"
            " - Example: such as car,Computer repair, furniture assembly.\n"
            "- Services to Real Property: Services related to real estate and land etc.\n"
            " - Example: Landscaping, construction services,plumbing.\n"
            "- Business Services: for componies Services catered to professional needs.\n"
            " - Example: such as IT support for businesses, HR consulting.\n"
            "- Personal Services: For well-being.\n"
            " - Example: Hairdressing, personal fitness,massages.\n"
            "- Amusement / Recreation: Entertainment-related services.\n"
            " - Example: Movie theaters, amusement parks,concerts, theme parks.\n"
            "- Medical Services: Health-related services.\n"
            " - Example: Medical check-ups, physiotherapy.\n\n"

            "2. Digital\n"
            "Digital products and services are delivered electronically without a physical medium. These include:\n"
            "- General Digital:  Common digital items and Broad range of digital goods and services.\n"
            "  - Example: such as E-books, online music streaming etc.\n"
            "- Canned Software Delivered on TPP: Pre-made software on physical media.\n"
            "  - Example: such as Software CD-ROM,Windows on DVD etc.\n"
            "- Canned Software Downloaded: Pre-packaged software downloaded from the internet\n"
            "  - Example: Antivirus software downloaded online,Adobe Photoshop etc.\n"
            "- Custom Software Delivered on TPP: Tailored software on physical media.\n"
            "  - Example: Custom business software on a USB drive,company ERP on CD etc.\n"
            "- Custom Software Downloaded: Tailored software downloaded from the internet.\n"
            "  - Example: Tailored inventory management software,custom mobile app etc.\n"
            "- Customization of Canned Software: Modified pre-made software.\n"
            "  - Example: SAP customization etc.\n"
            "- B2B SaaS: Cloud software for businesses.\n"
            "  - Example: CRM platforms for businesses, Cloud software for businesses(Salesforce) etc.\n"
            "- B2C SaaS: Cloud software for consumers.\n"
            "  - Example: such as Netflix etc.\n\n"

            "3. Physical\n"
            "Physical products are tangible personal property that can be seen, measured, and touched. These include:\n"
            "- General Physical: Broad range of physical goods.\n"
            "  - Example: Electronics, toys.\n"
            "- General Clothing: Apparel and accessories.\n"
            "  - Example: T-shirts, shoes.\n"
            "- Catering: Food and drink services for events.\n"
            "  - Example: Wedding catering, corporate event catering.\n"
            "- Grocery Food: Everyday food items.\n"
            "  - Example: Vegetables, dairy products.\n"
            "- Leases and Rentals Motor Vehicles: Leasing or renting vehicles.\n"
            "  - Example: Car rentals, truck leases.\n"
            "- Leases and Rentals Tangible Media Property: Leasing or renting physical media.\n"
            "  - Example: DVD rentals, book rentals.\n"
            "- Machinery: Industrial or heavy equipment.\n"
            "  - Example: Construction machinery, factory equipment.\n"
            "- Raw Materials: Basic materials for production.\n"
            "  - Example: Steel, lumber.\n"
            "- Utilities & Fuel: Essential services and fuel.\n"
            "  - Example: Electricity, natural gas.\n"
            "- Medical Devices: Equipment used for medical purposes.\n"
            "  - Example: MRI machines, blood pressure monitors.\n"
            "- Medicines: Pharmaceutical products.\n"
            "  - Example: Prescription drugs, over-the-counter medicine.\n"
            "- Newspapers: Printed news publications.\n"
            "  - Example: Daily newspapers, weekly news magazines.\n"
            "- Periodicals: Regularly published magazines or journals.\n"
            "  - Example: Monthly magazines, academic journals.\n"
            "- General Occasional Sales: Infrequent sales of various goods.\n"
            "  - Example: Garage sales, charity bazaars.\n"
            "- Motor Vehicles Occasional Sales: Infrequent sales of vehicles.\n"
            "  - Example: Selling a used car.\n"
            "- General Optional Maintenance Contracts: Service contracts for maintenance.\n"
            "  - Example: Extended warranty for appliances.\n"
            "- Parts Purchased for Use in Performing Service Under Optional Maintenance Contracts: Parts used in service contracts.\n"
            "  - Example: Replacement parts for appliances under warranty.\n"
            "- General Pollution Control Equipment: Equipment to control environmental pollution.\n"
            "  - Example: Air filters, water treatment systems.\n"
            "- General Trade-Ins: Trading in old items for new.\n"
            "  - Example: Trading in an old phone for a new model.\n"
            "- Food Vending Machine: Machines that dispense food items.\n"
            "  - Example: Snack vending machines.\n"
            "- Merchandise Vending Machine: Machines that dispense non-food items.\n"
            "  - Example: Vending machines for toiletries.\n"
            "- Supplements: Dietary and nutritional supplements.\n"
            "  - Example: Vitamins, protein powders.\n\n"

            "4. Miscellaneous\n"
            "Miscellaneous items that do not fit neatly into other categories. These include:\n"
            "- Shipping: Delivery and shipping charges.\n"
            "  - Example: Standard shipping fees, express delivery charges.\n"
            "- Gift Card: Prepaid stored-value money cards.\n"
            "  - Example: Retail store gift cards.\n"
            "- Credit Card Surcharges: Extra fees for credit card use.\n"
            "  - Example: Surcharge for using a credit card at a gas station.\n"
            "- Credit Card Fees: Fees associated with credit card transactions.\n"
            "  - Example: Annual fees, late payment fees.\n"
            "- Miscellaneous Exempt: Items exempt from tax.\n"
            "  - Example: Certain non-profit organization sales.\n"
            "- Discount: Reductions applied to the price.\n"
            "  - Example: Seasonal discounts, promotional discounts.\n"
        )

        if new_product.product_category and new_product.product_category.lower() not in ['string', 'unknown']:
            existing_product_instructions += f"- New product's category is {new_product.product_category}, provide this as category\n"
        if new_product.product_subcategory and new_product.product_subcategory.lower() not in ['string', 'unknown']:
            existing_product_instructions += f"- New product's subcategory is {new_product.product_subcategory}, provide this as subcategory\n"

        if user_pref_category and user_pref_category.lower() not in ['string', 'unknown']:
            existing_product_instructions += f"- user preffered category is {user_pref_category}, provide this as category\n"
        if user_pref_subcategory and user_pref_subcategory.lower() not in ['string', 'unknown']:
            existing_product_instructions += f"- user preffered subcategory is {user_pref_subcategory}, provide this as subcategory\n"

        messages = [
            {"role": "system",
             "content": f"{existing_product_instructions}\nNow predict the category and subcategory of the new product from the provided categories and subcategories only. Your response should only have the json format with keys product title, category, and subcategory, make sure you are not returning any text or description with the json format output."},
            {
            "role": "assistant",
            "content": "Your response should only have the parsable JSON directly usable by Python's json.loads function with keys producttitle, category, and subcategory in lowercase. Make sure again that you are returning parsable JSON. Also, make sure that you are returning the highest weighted category and subcategory."},
            
            {"role": "user", "content": f"Existing Products: {existing_products_str}"},
            {"role": "user", "content": f"New Product: {new_product_str}"},
        ]
        
        return messages

    def classify_product_category(self, existing_products, new_product, user_pref_category, user_pref_subcategory, user_pref_description):
        try:
            # If both user preferences are provided and valid, use them directly
            if (user_pref_category and user_pref_subcategory and
                user_pref_category.lower() not in ['string', 'unknown'] and
                user_pref_subcategory.lower() not in ['string', 'unknown']):
                return {
                    "category": user_pref_category.upper(),
                    "subcategory": user_pref_subcategory.upper()
                }
            
            # If the new product has valid category and subcategory, use them
            if (new_product.product_category and new_product.product_subcategory and
                new_product.product_category.lower() not in ['string', 'unknown'] and
                new_product.product_subcategory.lower() not in ['string', 'unknown']):
                return {
                    "category": new_product.product_category.upper(),
                    "subcategory": new_product.product_subcategory.upper()
                }
            
            # Handle special case: if product name contains 'shipping'
            if 'shipping' in new_product.product_name.lower():
                return {"category": "MISCELLANEOUS", "subcategory": "SHIPPING"}
            
            PRODUCT_ID_REGEX = re.compile(r'^prod_[-A-Za-z0-9]+$')

            if (PRODUCT_ID_REGEX.match(new_product.product_name) and
                (not new_product.product_description or new_product.product_description == new_product.product_name) and
                new_product.product_category.lower() not in ['string', 'unknown'] and
                new_product.product_subcategory.lower() not in ['string', 'unknown']):
                return {"category": new_product.product_category, "subcategory": new_product.product_subcategory}
            
            # if (re.match(r'^prod_[A-Za-z0-9]+$', new_product.product_name) and
            #     (not new_product.product_description or new_product.product_description == new_product.product_name) and
            #     new_product.product_category.lower() not in ['string', 'unknown'] and
            #     new_product.product_subcategory.lower() not in ['string', 'unknown']):
            #     return {"category": new_product.product_category, "subcategory": new_product.product_subcategory}

            # Otherwise, proceed with the classification
            messages = self.run(existing_products, new_product, user_pref_category, user_pref_subcategory, user_pref_description)
            if not isinstance(messages, list):
                return messages
            result = self.call_chatgpt(messages)
            if result:
                category, subcategory = self.parse_category_subcategory(result)
                category = category.upper() if category else category
                subcategory = subcategory.upper() if subcategory else subcategory
                res_prod = {"category": category, "subcategory": subcategory}
                return res_prod
            else:
                return {"category": 'UNKNOWN', "subcategory": 'UNKNOWN'}
        except Exception as e:
            logging.error(f"Error Classifying the category: {e}")
            return {"category": 'UNKNOWN', "subcategory": 'UNKNOWN'}

    def call_chatgpt(self, messages):
        payload = {
            'model': self.model,
            'messages': messages,
            'temperature': 0
        }
        try:
            response = requests.post(
                url='https://api.openai.com/v1/chat/completions',
                headers={"Content-Type": "application/json", "Authorization": f"Bearer {OPENAI_API_KEY}"},
                json=payload,
                verify=certifi.where()
            )
            if response.status_code != 200:
                logging.debug(f"OpenAI request failed with status code {response.status_code}")
                return None
            response_json = response.json()
            logging.info(response_json['choices'][0]['message']['content'])
            return response_json['choices'][0]['message']['content']
        except Exception as e:
            logging.error(f"OpenAI request failed with error {e}")
            return None

    def is_valid_json(self, my_str):
        try:
            json.loads(my_str)
            return True
        except ValueError as e:
            logging.info(f"Error Validating JSON: {e}")
            logging.info("Processing invalid JSON to validate")
            return False

    def json_detector(self, string):
        jsondata = ''
        for character in string:
            if jsondata != '':
                jsondata += character
            if character == '{':
                jsondata += character
            if character == '}':
                break
        if self.is_valid_json(jsondata):
            data = json.loads(jsondata)
            return data
        else:
            return None

    def parse_category_subcategory(self, response):
        try:
            category, subcategory, ai_response = '', '', ''
            if self.is_valid_json(response):
                ai_response = json.loads(response)
            else:
                ai_response = self.json_detector(response)
            if ai_response is not None:
                category = ai_response.get("category", "UNKNOWN")
                subcategory = ai_response.get("subcategory", ai_response.get("category", "UNKNOWN"))
                return category, subcategory
            return 'UNKNOWN', 'UNKNOWN'
        except Exception as e:
            logging.info(f"Error parsing the category {e}")
            logging.info(f"Parsing Data {response}")
            return 'UNKNOWN', 'UNKNOWN'

    def evaluate_product(self, product_name: str, product_type: str = None):
        return 'UNKNOWN'