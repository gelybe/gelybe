SELECT AVG(price) AS avg_price
FROM (
    SELECT pc.price
    FROM PC pc
    JOIN Product p ON pc.model = p.model
    WHERE p.maker = 'A'

    UNION ALL

    SELECT l.price
    FROM Laptop l
    JOIN Product p ON l.model = p.model
    WHERE p.maker = 'A'
) AS combined_prices;