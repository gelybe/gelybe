SELECT
    s.name,
    AVG(g.grade) AS avg_grade
FROM students s
JOIN grades g ON s.student_id = g.student_id
GROUP BY s.student_id, s.name
ORDER BY avg_grade DESC
LIMIT 10;
