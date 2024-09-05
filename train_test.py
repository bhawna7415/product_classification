from service import ClassifyProduct
from constants import ProductType

def test_evaluate_product():
    product_name = "Team Users"
    product_type = ProductType.SUBSCRIPTION
    category_prediction = ClassifyProduct().evaluate_product(product_name, product_type)
    assert category_prediction == "UNKNOWN", "Product categorization failed."

    product_type = "CHARGE"
    category_prediction = ClassifyProduct().evaluate_product(product_name, product_type)
    assert category_prediction != "PHYSICAL", "Product categorization failed."
