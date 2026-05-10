# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)


# STEP 1
df_boston = pd.read_sql("""
SELECT firstName, lastName, jobTitle
FROM employees
JOIN offices
ON employees.officeCode = offices.officeCode
WHERE city = 'Boston';
""", conn)


# STEP 2
df_zero_emp = pd.read_sql("""
SELECT offices.officeCode, offices.city
FROM offices
LEFT JOIN employees
ON offices.officeCode = employees.officeCode
WHERE employees.employeeNumber IS NULL;
""", conn)


# STEP 3
df_employee = pd.read_sql("""
SELECT employees.firstName,
       employees.lastName,
       offices.city,
       offices.state
FROM employees
LEFT JOIN offices
ON employees.officeCode = offices.officeCode
ORDER BY employees.firstName, employees.lastName;
""", conn)


# STEP 4
df_contacts = pd.read_sql("""
SELECT contactFirstName,
       contactLastName,
       phone,
       salesRepEmployeeNumber
FROM customers
LEFT JOIN orders
ON customers.customerNumber = orders.customerNumber
WHERE orders.orderNumber IS NULL
ORDER BY contactLastName;
""", conn)


# STEP 5
df_payment = pd.read_sql("""
SELECT customers.contactFirstName,
       customers.contactLastName,
       payments.amount,
       payments.paymentDate
FROM customers
JOIN payments
ON customers.customerNumber = payments.customerNumber
ORDER BY CAST(payments.amount AS REAL) DESC;
""", conn)


# STEP 6
df_credit = pd.read_sql("""
SELECT employees.employeeNumber,
       employees.firstName,
       employees.lastName,
       COUNT(customers.customerNumber) AS numCustomers
FROM employees
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY employees.employeeNumber
HAVING AVG(customers.creditLimit) > 90000
ORDER BY numCustomers DESC
LIMIT 4;
""", conn)


# STEP 7
df_product_sold = pd.read_sql("""
SELECT products.productName,
       COUNT(orderdetails.orderNumber) AS numorders,
       SUM(orderdetails.quantityOrdered) AS totalunits
FROM products
JOIN orderdetails
ON products.productCode = orderdetails.productCode
GROUP BY products.productCode
ORDER BY totalunits DESC;
""", conn)


# STEP 8
df_total_customers = pd.read_sql("""
SELECT products.productName,
       products.productCode,
       COUNT(DISTINCT orders.customerNumber) AS numpurchasers
FROM products
JOIN orderdetails
ON products.productCode = orderdetails.productCode
JOIN orders
ON orderdetails.orderNumber = orders.orderNumber
GROUP BY products.productCode
ORDER BY numpurchasers DESC;
""", conn)


# STEP 9
df_customers = pd.read_sql("""
SELECT offices.officeCode,
       offices.city,
       COUNT(customers.customerNumber) AS n_customers
FROM offices
LEFT JOIN employees
ON offices.officeCode = employees.officeCode
LEFT JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
GROUP BY offices.officeCode
ORDER BY n_customers DESC;
""", conn)


# STEP 10
df_under_20 = pd.read_sql("""
WITH low_products AS (
    SELECT products.productCode
    FROM products
    JOIN orderdetails
    ON products.productCode = orderdetails.productCode
    JOIN orders
    ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY products.productCode
    HAVING COUNT(DISTINCT orders.customerNumber) < 20
)

SELECT DISTINCT employees.employeeNumber,
       employees.firstName,
       employees.lastName,
       offices.city,
       offices.officeCode
FROM employees
JOIN customers
ON employees.employeeNumber = customers.salesRepEmployeeNumber
JOIN orders
ON customers.customerNumber = orders.customerNumber
JOIN orderdetails
ON orders.orderNumber = orderdetails.orderNumber
JOIN offices
ON employees.officeCode = offices.officeCode
WHERE orderdetails.productCode IN (
    SELECT productCode FROM low_products
);
""", conn)


conn.close()