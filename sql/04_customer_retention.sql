WITH x AS (
 SELECT customer_id, COUNT(DISTINCT CASE WHEN status='Delivered' THEN order_id END) AS delivered_orders
 FROM orders GROUP BY customer_id
)
SELECT COUNT(*) AS customers,
       SUM(CASE WHEN delivered_orders>=2 THEN 1 ELSE 0 END) AS repeat_customers,
       ROUND(100.0*SUM(CASE WHEN delivered_orders>=2 THEN 1 ELSE 0 END)/NULLIF(COUNT(*),0),2)
       AS repeat_purchase_rate_pct
FROM x;
