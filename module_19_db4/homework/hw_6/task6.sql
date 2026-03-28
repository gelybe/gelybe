SELECT
    AVG(g.grade) AS avg_reading_grade
FROM grades g
JOIN assignments a ON g.assignment_id = a.assignment_id
WHERE a.type = 'reading';
