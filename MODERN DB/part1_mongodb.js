use marketplace;

db.customers.drop();

db.customers.insertOne({
  customer_id: 101,
  name: "Praveen",
  city: "Bengaluru",
  orders: [
    {
      order_id: 5001,
      amount: 2500,
      status: "Delivered"
    },
    {
      order_id: 5002,
      amount: 1200,
      status: "Pending"
    }
  ]
});

// 1. Find customers whose city is Bengaluru
print("\n--- Query 1: Customers in Bengaluru ---");
printjson(db.customers.find({ city: "Bengaluru" }).toArray());

// 2. Find customers having at least one Pending order
// Dot notation evaluates array elements to match nested subdocuments
print("\n--- Query 2: Customers with at least one Pending order ---");
printjson(db.customers.find({ "orders.status": "Pending" }).toArray());

// 3. Find customers having an order with amount greater than 2000
print("\n--- Query 3: Customers with order amount > 2000 ---");
printjson(db.customers.find({ "orders.amount": { $gt: 2000 } }).toArray());

// 4. Find customers whose name is "Praveen"
print("\n--- Query 4: Customers named Praveen ---");
printjson(db.customers.find({ name: "Praveen" }).toArray());

// 5. Count the number of customers from Bengaluru
// countDocuments accurately scans current collection state
print("\n--- Query 5: Count of Bengaluru customers ---");
print(db.customers.countDocuments({ city: "Bengaluru" }));
