SELECT COUNT(DISTINCT order_id) AS orders,
       COUNT(DISTINCT customer_id) AS customers,
       SUM(CASE WHEN status='Delivered' THEN revenue ELSE 0 END) AS delivered_revenue,
       ROUND(SUM(CASE WHEN status='Delivered' THEN revenue ELSE 0 END) /
             NULLIF(COUNT(DISTINCT CASE WHEN status='Delivered' THEN order_id END),0),2) AS average_order_value
FROM orders;
