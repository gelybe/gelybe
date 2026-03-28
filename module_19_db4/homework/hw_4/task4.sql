SELECT
    c.class_name,
    AVG(late_count) AS avg_late,
    MAX(late_count) AS max_late,
    MIN(late_count) AS min_late
FROM classes c
JOIN (
    SELECT
        s.class_id,
        COUNT(CASE WHEN g.is_late = 1 THEN 1 END) AS late_count
    FROM students s
    JOIN grades g ON s.student_id = g.student_id
    GROUP BY s.student_id
) AS student_late ON c.class_id = student_late.class_id
GROUP BY c.class_id, c.class_name;
