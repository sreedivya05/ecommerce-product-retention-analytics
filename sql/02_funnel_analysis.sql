SELECT event_type, COUNT(*) AS events, COUNT(DISTINCT customer_id) AS unique_users
FROM events
GROUP BY event_type
ORDER BY CASE event_type WHEN 'Viewed Product' THEN 1 WHEN 'Added to Cart' THEN 2
WHEN 'Checkout' THEN 3 WHEN 'Purchased' THEN 4 END;
