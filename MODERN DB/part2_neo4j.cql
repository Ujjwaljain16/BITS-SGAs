MATCH (n) DETACH DELETE n;

// Seed graph nodes and relationships
CREATE (c1:Customer {id: 101, name: "Praveen"})
CREATE (c2:Customer {id: 102, name: "kumar"})
CREATE (p1:Product {id: 201, name: "Laptop"})
CREATE (p2:Product {id: 202, name: "Phone"})

CREATE (c1)-[:PURCHASED]->(p1)
CREATE (c1)-[:PURCHASED]->(p2)
CREATE (c2)-[:FOLLOWS]->(c1)
CREATE (c2)-[:PURCHASED]->(p1);

// 1. Find all products purchased by Praveen
MATCH (c:Customer {name: "Praveen"})-[:PURCHASED]->(p:Product)
RETURN p;

// 2. Find all customers who follow Praveen
MATCH (c:Customer)-[:FOLLOWS]->(target:Customer {name: "Praveen"})
RETURN c;

// 3. Find the number of products purchased by Praveen
MATCH (c:Customer {name: "Praveen"})-[:PURCHASED]->(p:Product)
RETURN count(p) AS number_of_products;

// 4. Find customers who purchased a product named "Laptop"
MATCH (c:Customer)-[:PURCHASED]->(p:Product {name: "Laptop"})
RETURN c;
