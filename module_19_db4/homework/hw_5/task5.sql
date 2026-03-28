SELECT
    c.class_name,
    COUNT(DISTINCT s.student_id) AS total_students,
    AVG(g.grade) AS average_grade,
    SUM(CASE WHEN g.grade IS NULL THEN 1 ELSE 0 END) AS not_submitted,
    SUM(CASE WHEN g.is_late = 1 THEN 1 ELSE 0 END) AS late_submissions,
    SUM(g.retry_count) AS retry_attempts
FROM classes c
LEFT JOIN students s ON c.class_id = s.class_id
LEFT JOIN grades g ON s.student_id = g.student_id
GROUP BY c.class_id, c.class_name;
