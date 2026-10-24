"""
Build finaloutput.pdf with authentic user screenshots
Header Details:
Staff Graded Assignment -1
BITS
2024EB02528
UJJWAL JAIN
MODERN DATABASES
"""

import os
import zipfile
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image as RLImage,
    PageBreak, KeepTogether, HRFlowable, Table, TableStyle
)

SCREENSHOTS_DIR = os.path.join(os.getcwd(), "screenshots")


def get_scaled_image(filename, max_w=540, max_h=340):
    filepath = os.path.join(SCREENSHOTS_DIR, filename)
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Missing {filepath}")
    
    with Image.open(filepath) as img:
        orig_w, orig_h = img.size
    
    aspect = orig_w / float(orig_h)
    
    # Target dimensions
    w = min(max_w, orig_w)
    h = w / aspect
    
    if h > max_h:
        h = max_h
        w = h * aspect
        
    return RLImage(filepath, width=w, height=h)


def generate_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    header_title = ParagraphStyle(
        "HeaderTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        alignment=1,
        spaceAfter=3
    )

    header_meta = ParagraphStyle(
        "HeaderMeta",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=16,
        textColor=colors.HexColor("#1e3a8a"),
        alignment=1,
        spaceAfter=2
    )

    section_heading = ParagraphStyle(
        "SectionHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#1e3a8a"),
        spaceBefore=8,
        spaceAfter=4
    )

    question_heading = ParagraphStyle(
        "QuestionHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#0f766e"),
        spaceBefore=6,
        spaceAfter=3
    )

    query_code = ParagraphStyle(
        "QueryCode",
        parent=styles["Normal"],
        fontName="Courier-Bold",
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0369a1"),
        spaceAfter=4
    )

    story = []

    # =========================================================================
    # Header Banner (Strictly no em-dashes)
    # =========================================================================
    story.append(Paragraph("Staff Graded Assignment -1", header_title))
    story.append(Paragraph("BITS", header_meta))
    story.append(Paragraph("2024EB02528", header_meta))
    story.append(Paragraph("UJJWAL JAIN", header_meta))
    story.append(Paragraph("MODERN DATABASES", header_meta))
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e3a8a"), spaceAfter=10))

    # =========================================================================
    # PART 1: MONGODB
    # =========================================================================
    story.append(Paragraph("Part 1: MongoDB (5 Points)", section_heading))
    
    # Document Insertion
    story.append(Paragraph("Dataset Seeding", question_heading))
    story.append(Paragraph("Operation: db.customers.insertOne({...})", query_code))
    story.append(get_scaled_image("mongo_insert.png", max_w=540, max_h=120))
    story.append(Spacer(1, 8))

    # Query 1
    story.append(Paragraph("1. Find customers whose city is Bengaluru", question_heading))
    story.append(Paragraph("Query: db.customers.find({ city: 'Bengaluru' })", query_code))
    story.append(get_scaled_image("mongo_q1.png", max_w=500, max_h=230))
    story.append(PageBreak())

    # Query 2
    story.append(Paragraph("2. Find customers having at least one Pending order", question_heading))
    story.append(Paragraph("Query: db.customers.find({ 'orders.status': 'Pending' })", query_code))
    story.append(get_scaled_image("mongo_q2.png", max_w=500, max_h=240))
    story.append(Spacer(1, 10))

    # Query 3
    story.append(Paragraph("3. Find customers having an order with amount greater than 2000", question_heading))
    story.append(Paragraph("Query: db.customers.find({ 'orders.amount': { $gt: 2000 } })", query_code))
    story.append(get_scaled_image("mongo_q3.png", max_w=500, max_h=240))
    story.append(PageBreak())

    # Query 4
    story.append(Paragraph("4. Find customers whose name is 'Praveen'", question_heading))
    story.append(Paragraph("Query: db.customers.find({ name: 'Praveen' })", query_code))
    story.append(get_scaled_image("mongo_q4.png", max_w=500, max_h=240))
    story.append(Spacer(1, 10))

    # Query 5
    story.append(Paragraph("5. Count the number of customers from Bengaluru", question_heading))
    story.append(Paragraph("Query: db.customers.countDocuments({ city: 'Bengaluru' })", query_code))
    story.append(get_scaled_image("mongo_q5.png", max_w=500, max_h=70))
    story.append(PageBreak())

    # =========================================================================
    # PART 2: NEO4J
    # =========================================================================
    story.append(Paragraph("Part 2: Neo4j (6 Points)", section_heading))
    
    # Graph Seeding
    story.append(Paragraph("Graph Nodes and Relationships Setup", question_heading))
    story.append(Paragraph("Query: CREATE Customer and Product nodes with PURCHASED and FOLLOWS edges", query_code))
    story.append(get_scaled_image("neo4j_seed.png", max_w=540, max_h=260))
    story.append(PageBreak())

    # Query 1
    story.append(Paragraph("1. Find all products purchased by Praveen", question_heading))
    story.append(Paragraph("Query: MATCH (c:Customer {name: 'Praveen'})-[:PURCHASED]->(p:Product) RETURN p;", query_code))
    story.append(get_scaled_image("neo4j_q1.png", max_w=540, max_h=270))
    story.append(PageBreak())

    # Query 2
    story.append(Paragraph("2. Find all customers who follow Praveen", question_heading))
    story.append(Paragraph("Query: MATCH (c:Customer)-[:FOLLOWS]->(target:Customer {name: 'Praveen'}) RETURN c;", query_code))
    story.append(get_scaled_image("neo4j_q2.png", max_w=540, max_h=270))
    story.append(PageBreak())

    # Query 3
    story.append(Paragraph("3. Find the number of products purchased by Praveen", question_heading))
    story.append(Paragraph("Query: MATCH (c:Customer {name: 'Praveen'})-[:PURCHASED]->(p:Product) RETURN count(p) AS number_of_products;", query_code))
    story.append(get_scaled_image("neo4j_q3.png", max_w=540, max_h=270))
    story.append(PageBreak())

    # Query 4
    story.append(Paragraph("4. Find customers who purchased a product named 'Laptop'", question_heading))
    story.append(Paragraph("Query: MATCH (c:Customer)-[:PURCHASED]->(p:Product {name: 'Laptop'}) RETURN c;", query_code))
    story.append(get_scaled_image("neo4j_q4.png", max_w=540, max_h=270))
    story.append(PageBreak())

    # =========================================================================
    # PART 3: DYNAMODB
    # =========================================================================
    story.append(Paragraph("Part 3: DynamoDB (4 Points)", section_heading))

    # Query 1
    story.append(Paragraph("1. Retrieve all items in the cart of customer C101", question_heading))
    story.append(Paragraph("KeyConditionExpression: customer_id = 'C101'", query_code))
    story.append(get_scaled_image("dynamo_q1.png", max_w=460, max_h=250))
    story.append(Spacer(1, 10))

    # Query 2
    story.append(Paragraph("2. Retrieve product P202 from customer C101's cart", question_heading))
    story.append(Paragraph("KeyConditionExpression: customer_id = 'C101' AND product_id = 'P202'", query_code))
    story.append(get_scaled_image("dynamo_q2.png", max_w=460, max_h=180))
    story.append(PageBreak())

    # Query 3
    story.append(Paragraph("3. Retrieve all products in customer C102's cart where the quantity is greater than 0", question_heading))
    story.append(Paragraph("KeyConditionExpression: customer_id = 'C102' | FilterExpression: quantity > 0", query_code))
    story.append(get_scaled_image("dynamo_q3.png", max_w=460, max_h=250))
    story.append(Spacer(1, 10))

    # Query 4
    story.append(Paragraph("4. Retrieve only the product_name and quantity for customer C101", question_heading))
    story.append(Paragraph("KeyConditionExpression: customer_id = 'C101' | ProjectionExpression: product_name, quantity", query_code))
    story.append(get_scaled_image("dynamo_q4.png", max_w=460, max_h=190))
    story.append(PageBreak())

    # Query 5
    story.append(Paragraph("5. Retrieve products from customer C101's cart where the quantity is greater than 1", question_heading))
    story.append(Paragraph("KeyConditionExpression: customer_id = 'C101' | FilterExpression: quantity > 1", query_code))
    story.append(get_scaled_image("dynamo_q5.png", max_w=460, max_h=190))
    story.append(Spacer(1, 10))

    # Query 6
    story.append(Paragraph("6. Retrieve products from customer C101's cart where the quantity is greater than 1", question_heading))
    story.append(Paragraph("KeyConditionExpression: customer_id = 'C101' | FilterExpression: quantity > 1", query_code))
    story.append(get_scaled_image("dynamo_q6.png", max_w=460, max_h=190))

    doc.build(story)
    print(f"PDF built successfully: {output_pdf_path}")


def package_zip(zip_name):
    files = [
        "part1_mongodb.js",
        "part2_neo4j.cql",
        "part3_dynamodb.py",
        "part3_dynamodb_cli.sh",
        "finaloutput.pdf"
    ]
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as z:
        for f in files:
            if os.path.exists(f):
                z.write(f, arcname=f)
                print(f"Packed into zip: {f}")
    print(f"Zip created successfully: {zip_name}")


if __name__ == "__main__":
    pdf_out = os.path.join(os.getcwd(), "finaloutput.pdf")
    generate_pdf(pdf_out)
    package_zip("2024EB02528_MDB_SGA1.zip")
