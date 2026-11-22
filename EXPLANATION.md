# E-Commerce Product & Customer Retention Analytics
## Complete Project Explanation — What It Is, How It Works, and How to Use It

---

## 1. The Project in One Sentence

This project analyzes an e-commerce business using **customer data, product data, order data, and product-interaction data** to understand business performance, customer behavior, product-funnel performance, and product opportunities.

The final result is an interactive Streamlit application, but **the Streamlit dashboard is only the final layer**.

The actual project is:

```text
Business Problem
      ↓
Business Data
      ↓
Data Understanding
      ↓
SQL Analysis
      ↓
Python Analysis
      ↓
KPIs & Metrics
      ↓
Product Investigation
      ↓
Business Recommendations
      ↓
Interactive Dashboard
```

---

# 2. What Problem Are We Solving?

Imagine you are a Product Analyst at an e-commerce company.

The company has lots of data, but the product team does not simply want a table of numbers.

They want answers.

For example:

### Business questions

- How much revenue are we generating?
- How many orders are being completed?
- What is our average order value?
- Which product categories are performing best?

### Product questions

- How many customers view products?
- How many add products to cart?
- How many reach checkout?
- How many purchase?
- Where are users dropping out?

### Customer questions

- How many customers buy only once?
- How many customers come back?
- What percentage of customers make repeat purchases?

### Product opportunity questions

- Which products get a lot of attention?
- Which products have relatively weak purchase activity?
- Which products should the product team investigate?

### Decision questions

- What should we investigate next?
- What additional data would help us make a stronger decision?
- What product changes could be tested?

That is the purpose of this project.

---

# 3. What Is the Final Output?

There are actually **three outputs**.

## Output 1 — Analytical results

The SQL and Python analysis calculate metrics such as:

- Revenue
- Orders
- Customers
- AOV
- Funnel rates
- Repeat purchase rate
- Product view-to-purchase rate

## Output 2 — Product findings

The analysis identifies things such as:

- high-revenue categories
- funnel drop-off points
- repeat-purchase behavior
- high-traffic / low-purchase products

## Output 3 — Interactive dashboard

The Streamlit application presents these findings in a way that a product manager or business stakeholder can explore.

So:

> **Dashboard = presentation of the analysis, not the entire project.**

---

# 4. Project Architecture

The project has four main analytical layers.

```text
                    ┌────────────────────┐
                    │     DATA LAYER     │
                    │ Customers           │
                    │ Products            │
                    │ Orders              │
                    │ Events              │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │    SQL ANALYSIS     │
                    │ Revenue             │
                    │ Funnel              │
                    │ Category            │
                    │ Retention           │
                    │ Product Opportunity │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │   PYTHON ANALYSIS   │
                    │ Pandas              │
                    │ Cleaning            │
                    │ Aggregation         │
                    │ KPI calculations    │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │ PRODUCT ANALYSIS    │
                    │ Findings            │
                    │ Opportunities       │
                    │ Recommendations     │
                    └─────────┬──────────┘
                              ↓
                    ┌────────────────────┐
                    │ STREAMLIT DASHBOARD │
                    │ Interactive output  │
                    └────────────────────┘
```

---

# 5. Folder Structure

```text
01_Product_Analytics_Ecommerce/
│
├── data/
│   ├── customers.csv
│   ├── products.csv
│   ├── orders.csv
│   └── events.csv
│
├── sql/
│   ├── 01_revenue_analysis.sql
│   ├── 02_funnel_analysis.sql
│   ├── 03_category_analysis.sql
│   ├── 04_retention_analysis.sql
│   └── 05_product_opportunity.sql
│
├── analysis/
│   └── product_analysis.py
│
├── app.py
│
├── README.md
│
├── EXPLANATION.md
│
└── requirements.txt
```

Each part has a different job.

---

# 6. DATA FOLDER — What Is the Data?

The `data/` folder contains the business data.

There are four CSV files.

---

## 6.1 customers.csv

This is the customer table.

Example structure:

```text
customer_id
signup_date
city
age
gender
```

### What does it represent?

Each row represents a customer.

For example:

```text
C001 | 2025-01-10 | Hyderabad | 24 | Female
C002 | 2025-01-12 | Chennai   | 29 | Male
```

### Why do we need it?

It allows us to understand:

- how many customers exist
- customer locations
- customer characteristics
- which customers place orders
- repeat-purchase behavior

---

# 7. products.csv

This is the product catalog.

Important columns:

```text
product_id
product_name
category
price
```

Each row represents a product.

Example:

```text
P001 | Wireless Headphones | Electronics | 2499
P002 | Running Shoes       | Fashion     | 3299
```

### Why do we need it?

Because an order only tells us the product ID.

The product table allows us to understand:

- product name
- product category
- product price
- category performance

---

# 8. orders.csv

This is the transaction table.

Important columns:

```text
order_id
customer_id
product_id
order_date
quantity
unit_price
revenue
status
```

Each row represents an order line.

This is where most revenue analysis comes from.

---

# 9. events.csv

This is the product interaction table.

The main event types are:

```text
Viewed Product
Added to Cart
Checkout
Purchased
```

These events represent actions users take while interacting with products.

This is important because:

> An order tells us what happened after purchase.

But events help us understand:

> What happened before purchase?

That makes the project more useful for Product Analytics.

---

# 10. How the Tables Connect

The tables are connected using IDs.

The main relationship is:

```text
CUSTOMERS
    |
    | customer_id
    ↓
ORDERS
    |
    | product_id
    ↓
PRODUCTS
```

Events also connect through:

```text
product_id
```

So we can move from:

```text
Customer
   ↓
Order
   ↓
Product
   ↓
Product behavior
```

This allows us to combine business and product behavior.

---

# 11. Why Do We Need Four Tables?

Suppose the company says:

> "Revenue from Electronics is high."

That is useful, but incomplete.

With only an orders table, we might know:

```text
Electronics Revenue = ₹X
```

With events, we can ask:

```text
How many times were Electronics products viewed?
How many were added to cart?
How many reached checkout?
How many were purchased?
```

With customers, we can ask:

```text
Do Electronics customers come back?
```

With products, we can ask:

```text
Which individual products are responsible?
```

Therefore, multiple tables allow deeper analysis.

---

# 12. SQL LAYER

The `sql/` folder contains five SQL analyses.

SQL is used because Product Analysts frequently work with structured business data stored in databases.

The SQL files demonstrate the ability to answer business questions using queries.

---

# 13. SQL 1 — Revenue Analysis

File:

```text
01_revenue_analysis.sql
```

This analysis calculates:

- delivered orders
- unique customers
- delivered revenue
- average order value

The core business formula is:

```text
Revenue = Quantity × Unit Price
```

The analysis focuses on delivered orders for the main business KPIs.

---

# 14. What Is AOV?

AOV means:

**Average Order Value**

Formula:

```text
AOV =
Total Delivered Revenue
-----------------------
Number of Delivered Orders
```

Example:

```text
Revenue = ₹10,00,000
Orders  = 5,000

AOV = ₹10,00,000 / 5,000
    = ₹200
```

Why is AOV useful?

Because two companies can have the same revenue but very different order behavior.

---

# 15. SQL 2 — Funnel Analysis

File:

```text
02_funnel_analysis.sql
```

The product funnel is:

```text
Viewed Product
      ↓
Added to Cart
      ↓
Checkout
      ↓
Purchased
```

The analysis counts events at each stage.

Example:

```text
Viewed Product      10,000
Added to Cart        3,000
Checkout             1,800
Purchased            1,000
```

This lets us calculate stage-level rates.

---

# 16. Funnel Conversion

For example:

```text
View → Cart

Cart Events
-----------
View Events
× 100
```

Similarly:

```text
Cart → Checkout

Checkout Events
---------------
Cart Events
× 100
```

And:

```text
Checkout → Purchase

Purchase Events
---------------
Checkout Events
× 100
```

This helps identify where product behavior changes significantly.

---

# 17. Important Funnel Limitation

This project uses event records.

Therefore, the current funnel is an:

> **Event-level diagnostic funnel**

It is NOT a perfect user-level conversion funnel.

For example, one user could generate:

```text
Viewed Product
Viewed Product
Viewed Product
Added to Cart
```

That is four events but one user.

A more advanced production system would track:

```text
user_id
session_id
timestamp
event_type
```

Then we could calculate unique-user or session-level conversion.

This is an important limitation to mention in an interview.

---

# 18. SQL 3 — Category Analysis

File:

```text
03_category_analysis.sql
```

This compares categories.

Metrics include:

- orders
- revenue
- units sold

For example:

```text
Electronics
Fashion
Home
Beauty
Sports
```

The goal is to understand which categories are contributing to business performance.

But the project does not stop at:

> "Electronics has the highest revenue."

We then ask:

> "Why?"

---

# 19. SQL 4 — Retention Analysis

File:

```text
04_retention_analysis.sql
```

This analyzes repeat purchasing.

A customer is classified as a repeat customer when they have:

```text
2 or more delivered orders
```

Formula:

```text
Repeat Purchase Rate
=
Customers with 2+ delivered orders
-----------------------------------
Customers with delivered orders
× 100
```

This tells us whether customers are returning.

---

# 20. Why Repeat Purchase Matters

Imagine:

### Business A

```text
10,000 customers
9,000 purchase once
1,000 purchase again
```

### Business B

```text
7,000 customers
3,000 purchase once
4,000 purchase again
```

The second business may have stronger customer loyalty.

Therefore:

> Revenue alone does not describe customer health.

---

# 21. SQL 5 — Product Opportunity Analysis

File:

```text
05_product_opportunity.sql
```

This combines:

- product views
- product purchases
- product information

One important product signal is:

```text
High Traffic
+
Low Purchase Activity
```

These products are not automatically "bad products."

Instead, they are:

> **Products that deserve investigation.**

---

# 22. Why We Do Not Claim the Cause

Suppose:

```text
Product A
Views = 10,000
Purchases = 100
```

We can say:

> The product receives high traffic relative to purchase activity.

We cannot automatically say:

> The product is too expensive.

There could be many reasons:

- price
- reviews
- rating
- availability
- delivery time
- product images
- description
- competition
- product quality
- checkout friction

A good Product Analyst separates:

```text
WHAT THE DATA SHOWS
```

from:

```text
WHAT WE THINK MIGHT EXPLAIN IT
```

---

# 23. PYTHON ANALYSIS

File:

```text
analysis/product_analysis.py
```

Python is used for additional analysis with Pandas.

The Python layer handles things such as:

- loading CSV files
- filtering data
- joining tables
- grouping data
- calculating KPIs
- analyzing product performance

Run it with:

```bash
python analysis/product_analysis.py
```

The purpose is to keep analytical logic separate from the Streamlit UI.

---

# 24. Why Do We Need Python If We Already Have SQL?

Because SQL and Python are useful for different stages.

### SQL is useful for:

- database querying
- joins
- filtering
- aggregation
- business metrics

### Python is useful for:

- data preparation
- exploratory analysis
- transformations
- custom calculations
- visualization
- reusable analytical workflows

Using both demonstrates practical analyst skills.

---

# 25. STREAMLIT APPLICATION

File:

```text
app.py
```

This is the user-facing application.

The app has five main sections.

---

# 26. TAB 1 — Overview

The Overview page contains:

```text
Revenue
Orders
Customers
AOV
Repeat Purchase Rate
```

It also contains:

- monthly revenue
- category revenue
- business signal

The purpose is to answer:

> "What is happening at a high level?"

---

# 27. TAB 2 — Funnel

The Funnel page shows:

```text
Viewed Product
      ↓
Added to Cart
      ↓
Checkout
      ↓
Purchased
```

It provides stage conversion metrics.

The purpose is to answer:

> "Where might users be losing momentum?"

---

# 28. TAB 3 — Retention

The Retention page shows:

- repeat customers
- one-time customers
- repeat purchase rate
- order distribution

The purpose is to answer:

> "Are customers coming back?"

---

# 29. TAB 4 — Product Analysis

This is one of the most important sections.

It provides:

```text
Product
Category
Views
Purchases
View-to-Purchase %
```

The analyst can look for:

```text
High Views
+
Relatively Low Purchases
```

This becomes a product investigation list.

---

# 30. TAB 5 — Data Explorer

The Data Explorer exposes the underlying data.

You can select:

```text
Orders
Products
Customers
Events
```

This is useful because you can inspect the raw/processed data behind the charts.

You can also download the currently displayed table.

---

# 31. Dashboard Filters

The application has filters for:

### Date

Analyze a selected period.

### Category

Analyze selected product categories.

### City

Analyze selected customer locations.

When the filters change, the order and event analysis updates.

This makes the dashboard interactive.

---

# 32. How the User Should Actually Use the Project

Do not simply open the dashboard and look at the first number.

Use it like an analyst.

### Step 1

Open Overview.

Ask:

> What is happening?

Look at:

- revenue
- orders
- AOV
- category performance

### Step 2

Open Funnel.

Ask:

> Where might users be dropping?

### Step 3

Open Retention.

Ask:

> Are customers returning?

### Step 4

Open Product Analysis.

Ask:

> Which products deserve investigation?

### Step 5

Form a hypothesis.

Example:

> Product X gets strong traffic but weak purchase activity.

### Step 6

Investigate possible explanations.

Look at:

- category
- price
- product information
- ratings/reviews if available
- availability if available

### Step 7

Make a recommendation.

Example:

> Investigate the product page and pricing competitiveness before increasing traffic acquisition.

This is the actual Product Analyst workflow.

---

# 33. Example End-to-End Analysis

Imagine the dashboard shows:

```text
Revenue
₹12.5L

Orders
5,200

AOV
₹2,404

Repeat Purchase Rate
28%
```

Then you inspect the funnel:

```text
Views
100,000

Cart
25,000

Checkout
12,000

Purchase
6,000
```

You notice a large reduction between:

```text
Cart → Checkout
```

That becomes an investigation area.

Then Product Analysis shows:

```text
Product A
Views: 15,000
Purchases: 80

Product B
Views: 12,000
Purchases: 900
```

Product A deserves investigation because it receives substantial traffic but relatively little purchase activity.

The analysis therefore moves from:

```text
Metric
 ↓
Finding
 ↓
Question
 ↓
Investigation
 ↓
Recommendation
```

---

# 34. What Is a Finding?

A finding is something directly supported by the data.

Example:

> Product A has high product views and a relatively low view-to-purchase rate.

This is a finding.

---

# 35. What Is a Hypothesis?

A hypothesis is a possible explanation that needs further investigation.

Example:

> Product A may have a pricing or product-page issue.

This is NOT proven by the current data.

---

# 36. What Is a Recommendation?

A recommendation is the action you propose based on the finding and hypothesis.

Example:

> Compare Product A's price and product-page quality against high-converting products in the same category.

That is a more responsible recommendation than simply saying:

> "Reduce the price."

---

# 37. This Is the Core Product Analytics Skill

The project demonstrates:

```text
Data
 ↓
Metric
 ↓
Finding
 ↓
Hypothesis
 ↓
Investigation
 ↓
Recommendation
```

This is much more valuable than simply creating charts.

---

# 38. How to Run the Project

Open a terminal inside the project folder.

Install the dependencies:

```bash
pip install -r requirements.txt
```

Then start Streamlit:

```bash
streamlit run app.py
```

The browser should open the application.

---

# 39. How to Test the Dashboard

## Test 1 — Application

Confirm:

- application opens
- sidebar appears
- KPI cards appear
- tabs work

---

## Test 2 — Date Filter

Change the date range.

Expected:

- revenue changes
- order count changes
- event analysis changes

---

## Test 3 — Category Filter

Select one category.

Expected:

- relevant product/order metrics change
- category analysis changes

---

## Test 4 — City Filter

Select one city.

Expected:

- customer/order-based metrics change

---

## Test 5 — Funnel

Open Funnel.

Confirm:

```text
Viewed Product
Added to Cart
Checkout
Purchased
```

appear.

---

## Test 6 — Retention

Open Retention.

Confirm:

- repeat customers
- one-time customers
- repeat rate

appear.

---

## Test 7 — Product Analysis

Open Product Analysis.

Check:

- product views
- purchases
- conversion percentage

---

## Test 8 — Data Explorer

Open Data Explorer.

Select:

```text
Orders
Products
Customers
Events
```

Confirm each dataset loads.

---

# 40. How to Test the Python Layer

Run:

```bash
python analysis/product_analysis.py
```

This verifies that the analysis can run independently from the dashboard.

---

# 41. How to Test the SQL Layer

The SQL files are business-analysis queries.

You can run them using a SQL environment such as:

- SQLite
- DuckDB
- PostgreSQL

The important thing is that the SQL answers actual business questions.

For example:

```text
Revenue analysis
       ↓
How much did we make?

Funnel analysis
       ↓
Where are users dropping?

Retention analysis
       ↓
Are customers returning?

Product analysis
       ↓
Which products need attention?
```

---

# 42. Future Version

After the current project is fully understood and working, possible improvements are:

## Version 2

### Cohort Retention

Analyze retention by signup month.

### RFM Segmentation

Classify customers using:

- Recency
- Frequency
- Monetary value

### Customer Lifetime Value

Estimate customer value over time.

### Session-Level Funnel

Track individual journeys.

### A/B Testing

Measure the impact of product changes.

### Automated Reporting

Generate a weekly product-performance report.

These should be added later.

The current version should first be understood properly.

---
# 43. Final Project Summary

This project demonstrates an end-to-end Product Analytics workflow:

```text
                    BUSINESS PROBLEM
                           ↓
                       DATASETS
                           ↓
                 DATA UNDERSTANDING
                           ↓
                      SQL QUERIES
                           ↓
                  PYTHON / PANDAS
                           ↓
                    KPI ANALYSIS
                           ↓
                 PRODUCT FUNNEL
                           ↓
                 CUSTOMER RETENTION
                           ↓
                PRODUCT OPPORTUNITIES
                           ↓
                     FINDINGS
                           ↓
                  RECOMMENDATIONS
                           ↓
                 STREAMLIT DASHBOARD
```

The dashboard is therefore only the final interface.

The real project is the complete analytical process from **business question → data → analysis → product insight → recommendation**.
