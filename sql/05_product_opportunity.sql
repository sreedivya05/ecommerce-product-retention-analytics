WITH f AS (
 SELECT product_id,
        SUM(CASE WHEN event_type='Viewed Product' THEN 1 ELSE 0 END) AS views,
        SUM(CASE WHEN event_type='Purchased' THEN 1 ELSE 0 END) AS purchases
 FROM events GROUP BY product_id
)
SELECT p.product_id,p.product_name,p.category,f.views,f.purchases,
       ROUND(100.0*f.purchases/NULLIF(f.views,0),2) AS view_to_purchase_pct
FROM f JOIN products p ON f.product_id=p.product_id
WHERE f.views>=50 ORDER BY view_to_purchase_pct ASC,views DESC;
