SELECT
    a.pseudo as log_admin,
    COUNT(id_ticket) AS logs_qty
FROM
    support_tickets_logs l
LEFT JOIN
    support_tickets_logs_types lt ON lt.id = l.id_type
LEFT JOIN
    translate tr ON tr.id = lt.tr_nom
LEFT JOIN
    admins a ON a.id_entite = l.id_entite
WHERE
    a.pseudo != ''
    AND DATE(FROM_UNIXTIME(l.ts)) = CURRENT_DATE
    AND l.id_type not in (50, 81, 84)
GROUP BY
    a.pseudo
ORDER BY
	logs_qty
    DESC;
