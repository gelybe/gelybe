SELECT
    s.name AS student_name,
    t.teacher_name
FROM students s
JOIN grades g ON s.student_id = g.student_id
JOIN assignments a ON g.assignment_id = a.assignment_id
JOIN teachers t ON a.teacher_id = t.teacher_id
WHERE t.teacher_id = (
    SELECT a2.teacher_id
    FROM assignments a2
    JOIN grades g2 ON a2.assignment_id = g2.assignment_id
    GROUP BY a2.teacher_id
    ORDER BY AVG(g2.grade) DESC
    LIMIT 1
);
