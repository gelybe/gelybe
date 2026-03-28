SELECT
    t.teacher_name,
    AVG(g.grade) AS avg_grade
FROM teachers t
JOIN assignments a ON t.teacher_id = a.teacher_id
JOIN grades g ON a.assignment_id = g.assignment_id
GROUP BY t.teacher_id, t.teacher_name
ORDER BY avg_grade ASC
LIMIT 1;
