import os
import json
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr

# Helper to serialize DynamoDB Decimal types for clean JSON output
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return super().default(o)


def get_table():
    endpoint = os.environ.get("DYNAMODB_ENDPOINT", "http://localhost:8000")
    dynamodb = boto3.resource(
        "dynamodb",
        endpoint_url=endpoint,
        region_name="us-east-1",
        aws_access_key_id="dummy",
        aws_secret_access_key="dummy"
    )

    # Recreate table on each run to guarantee reproducible test state
    existing = [t.name for t in dynamodb.tables.all()]
    if "Cart" in existing:
        dynamodb.Table("Cart").delete()
        dynamodb.Table("Cart").wait_until_not_exists()

    table = dynamodb.create_table(
        TableName="Cart",
        KeySchema=[
            {"AttributeName": "customer_id", "KeyType": "HASH"},
            {"AttributeName": "product_id", "KeyType": "RANGE"}
        ],
        AttributeDefinitions=[
            {"AttributeName": "customer_id", "AttributeType": "S"},
            {"AttributeName": "product_id", "AttributeType": "S"}
        ],
        BillingMode="PAY_PER_REQUEST"
    )
    table.wait_until_exists()
    return table


def seed_cart(table):
    items = [
        {"customer_id": "C101", "product_id": "P201", "product_name": "Laptop", "quantity": 1, "price": 60000},
        {"customer_id": "C101", "product_id": "P202", "product_name": "Mouse", "quantity": 2, "price": 1200},
        {"customer_id": "C102", "product_id": "P201", "product_name": "Laptop", "quantity": 1, "price": 60000},
        {"customer_id": "C102", "product_id": "P203", "product_name": "Keyboard", "quantity": 1, "price": 2500},
        {"customer_id": "C103", "product_id": "P204", "product_name": "Monitor", "quantity": 2, "price": 15000}
    ]
    with table.batch_writer() as batch:
        for item in items:
            batch.put_item(Item=item)


def print_result(label, items):
    print(f"\n--- {label} ---")
    print(json.dumps(items, indent=2, cls=DecimalEncoder))


def run_queries(table):
    # 1. Retrieve all items in the cart of customer C101
    q1 = table.query(KeyConditionExpression=Key("customer_id").eq("C101"))
    print_result("Query 1: All items for customer C101", q1.get("Items", []))

    # 2. Retrieve product P202 from customer C101's cart
    # Uses composite primary key (partition + sort key)
    q2 = table.query(KeyConditionExpression=Key("customer_id").eq("C101") & Key("product_id").eq("P202"))
    print_result("Query 2: Product P202 for customer C101", q2.get("Items", []))

    # 3. Retrieve all products in customer C102's cart where quantity is greater than 0
    # FilterExpression is evaluated after partition retrieval
    q3 = table.query(
        KeyConditionExpression=Key("customer_id").eq("C102"),
        FilterExpression=Attr("quantity").gt(0)
    )
    print_result("Query 3: Products for C102 with quantity > 0", q3.get("Items", []))

    # 4. Retrieve only product_name and quantity for customer C101
    # ProjectionExpression minimizes network payload
    q4 = table.query(
        KeyConditionExpression=Key("customer_id").eq("C101"),
        ProjectionExpression="product_name, quantity"
    )
    print_result("Query 4: Project product_name and quantity for C101", q4.get("Items", []))

    # 5. Retrieve products from customer C101's cart where quantity is greater than 1
    q5 = table.query(
        KeyConditionExpression=Key("customer_id").eq("C101"),
        FilterExpression=Attr("quantity").gt(1)
    )
    print_result("Query 5: Products for C101 with quantity > 1", q5.get("Items", []))

    # 6. Retrieve products from customer C101's cart where quantity is greater than 1
    q6 = table.query(
        KeyConditionExpression=Key("customer_id").eq("C101"),
        FilterExpression=Attr("quantity").gt(1)
    )
    print_result("Query 6: Products for C101 with quantity > 1", q6.get("Items", []))


if __name__ == "__main__":
    cart_table = get_table()
    seed_cart(cart_table)
    run_queries(cart_table)
