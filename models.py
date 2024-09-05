from pydantic import BaseModel
from typing import List
from typing import Union, Optional

class Classification(BaseModel):
    category: str


class ClassificationRequest(BaseModel):
    product_name: str
    product_type: str = None

class Product(BaseModel):
    product_name: str
    product_description: str
    product_status: str
    product_category: str
    product_subcategory: str

class ProductToClassify(BaseModel):
    product_name: str
    product_description: str | None
    product_category: Optional[str] = None
    product_subcategory: Optional[str] = None

class ProductClassificationRequest(BaseModel):
    existing_products: List[Product]
    product_to_classify: ProductToClassify
    user_pref_category: Union[str, None] = None
    user_pref_subcategory: Union[str, None] = None
    user_pref_description: Union[str, None] = None

    
class ProductClassification(BaseModel):
    category: str
    subcategory: str

class ProductClassificationResponse(BaseModel):
    category: str
    subcategory: str

