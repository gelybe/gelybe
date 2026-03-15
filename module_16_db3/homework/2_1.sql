SELECT c.full_name AS customer_name, m.full_name AS manager_name, o.purchase_amount, o.date
FROM 'order' o
JOIN customer c ON o.customer_id = c.customer_id
JOIN manager m ON o.manager_id = m.manager_id;
