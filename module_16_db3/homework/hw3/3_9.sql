SELECT p.maker, MAX(pc.price) AS max_price
FROM Product p
JOIN PC pc ON p.model = pc.model
GROUP BY p.maker;