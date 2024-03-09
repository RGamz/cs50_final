SELECT
    t.id,
    FROM_UNIXTIME(last_message.ts_creation, '%d.%m.%Y') AS last_message_time,
    last_message.message,
    COUNT(CASE WHEN m.id_entite != '' THEN m.id END) AS message_count
FROM
    support_tickets t
LEFT JOIN (
    SELECT
        id_discussion,
        MAX(ts_creation) AS max_ts_creation
    FROM
        discussions_messages
    WHERE
        id_entite != ''
    GROUP BY
        id_discussion
) AS latest_message_time ON t.id_discussion = latest_message_time.id_discussion
LEFT JOIN
    discussions_messages last_message ON last_message.id_discussion = latest_message_time.id_discussion
                                        AND last_message.ts_creation = latest_message_time.max_ts_creation
LEFT JOIN
    discussions_messages m ON m.id_discussion = t.id_discussion
LEFT JOIN
    support_tickets_contrat ON support_tickets_contrat.id_ticket = t.id
LEFT JOIN
    contrats ON contrats.id = support_tickets_contrat.id_contrat
WHERE
    t.statut = 0
    AND t.ts_creation > 1672527600
    AND contrats.id NOT IN (3, 46, 51, 64, 71)
    AND last_message.id_entite != ''
GROUP BY
    t.id, last_message.ts_creation, last_message.message;
