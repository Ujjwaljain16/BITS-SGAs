#!/usr/bin/env bash

ENDPOINT="--endpoint-url http://localhost:8000"

aws dynamodb create-table \
    --table-name Cart \
    --attribute-definitions \
        AttributeName=customer_id,AttributeType=S \
        AttributeName=product_id,AttributeType=S \
    --key-schema \
        AttributeName=customer_id,KeyType=HASH \
        AttributeName=product_id,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    $ENDPOINT

aws dynamodb put-item --table-name Cart --item '{"customer_id": {"S": "C101"}, "product_id": {"S": "P201"}, "product_name": {"S": "Laptop"}, "quantity": {"N": "1"}, "price": {"N": "60000"}}' $ENDPOINT
aws dynamodb put-item --table-name Cart --item '{"customer_id": {"S": "C101"}, "product_id": {"S": "P202"}, "product_name": {"S": "Mouse"}, "quantity": {"N": "2"}, "price": {"N": "1200"}}' $ENDPOINT
aws dynamodb put-item --table-name Cart --item '{"customer_id": {"S": "C102"}, "product_id": {"S": "P201"}, "product_name": {"S": "Laptop"}, "quantity": {"N": "1"}, "price": {"N": "60000"}}' $ENDPOINT
aws dynamodb put-item --table-name Cart --item '{"customer_id": {"S": "C102"}, "product_id": {"S": "P203"}, "product_name": {"S": "Keyboard"}, "quantity": {"N": "1"}, "price": {"N": "2500"}}' $ENDPOINT
aws dynamodb put-item --table-name Cart --item '{"customer_id": {"S": "C103"}, "product_id": {"S": "P204"}, "product_name": {"S": "Monitor"}, "quantity": {"N": "2"}, "price": {"N": "15000"}}' $ENDPOINT

# 1. Retrieve all items in the cart of customer C101
aws dynamodb query \
    --table-name Cart \
    --key-condition-expression "customer_id = :cid" \
    --expression-attribute-values '{":cid": {"S": "C101"}}' \
    $ENDPOINT

# 2. Retrieve product P202 from customer C101's cart
aws dynamodb query \
    --table-name Cart \
    --key-condition-expression "customer_id = :cid AND product_id = :pid" \
    --expression-attribute-values '{":cid": {"S": "C101"}, ":pid": {"S": "P202"}}' \
    $ENDPOINT

# 3. Retrieve all products in customer C102's cart where quantity is greater than 0
aws dynamodb query \
    --table-name Cart \
    --key-condition-expression "customer_id = :cid" \
    --filter-expression "quantity > :zero" \
    --expression-attribute-values '{":cid": {"S": "C102"}, ":zero": {"N": "0"}}' \
    $ENDPOINT

# 4. Retrieve only product_name and quantity for customer C101
aws dynamodb query \
    --table-name Cart \
    --key-condition-expression "customer_id = :cid" \
    --projection-expression "product_name, quantity" \
    --expression-attribute-values '{":cid": {"S": "C101"}}' \
    $ENDPOINT

# 5. Retrieve products from customer C101's cart where quantity is greater than 1
aws dynamodb query \
    --table-name Cart \
    --key-condition-expression "customer_id = :cid" \
    --filter-expression "quantity > :one" \
    --expression-attribute-values '{":cid": {"S": "C101"}, ":one": {"N": "1"}}' \
    $ENDPOINT

# 6. Retrieve products from customer C101's cart where quantity is greater than 1
aws dynamodb query \
    --table-name Cart \
    --key-condition-expression "customer_id = :cid" \
    --filter-expression "quantity > :one" \
    --expression-attribute-values '{":cid": {"S": "C101"}, ":one": {"N": "1"}}' \
    $ENDPOINT
