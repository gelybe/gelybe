SELECT full_name
FROM customer
WHERE customer_id NOT IN (
    SELECT DISTINCT customer_id
    FROM 'order'
);
