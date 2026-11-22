SELECT p.category,
       COUNT(DISTINCT o.order_id) AS orders,
       SUM(CASE WHEN o.status='Delivered' THEN o.revenue ELSE 0 END) AS revenue,
       SUM(CASE WHEN o.status='Delivered' THEN o.quantity ELSE 0 END) AS units_sold
FROM orders o JOIN products p ON o.product_id=p.product_id
GROUP BY p.category ORDER BY revenue DESC;
