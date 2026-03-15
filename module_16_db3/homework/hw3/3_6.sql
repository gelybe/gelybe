SELECT DISTINCT p.maker, l.speed
FROM Product p
JOIN Laptop l ON p.model = l.model
WHERE p.maker IN (
    SELECT DISTINCT maker
    FROM Product
    WHERE type = 'Laptop'
);