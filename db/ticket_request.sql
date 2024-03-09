select t.id, 
FROM_UNIXTIME(t.ts_creation, '%d.%m.%Y') AS creation_date,
FROM_UNIXTIME(max(support_tickets_logs.ts), '%d.%m.%Y') as last_log_time,
p.ref, arbo_link.id_arborescence as id_arbo, m.nom as marque, s.id as id_status, tr1.fr as "status",
contrats.nom as contrat, tr4.fr as "type_ticket", a.pseudo as ticket_admin, t.read, 
e1.societe as distributeur, e2.societe as station, 
p.code_barres, date_achat, 
count(tr6.fr) as ticket_total_log_count,
COUNT(CASE WHEN DATE(FROM_UNIXTIME(support_tickets_logs.ts)) = CURDATE() THEN tr6.fr END) AS ticket_log_count_today
from support_tickets t
left join produits p on p.id = t.id_machine 
left join marques m on m.id = p.id_marque
left join support_tickets_statuts s on t.id_statut = s.id
left join translate tr1 on tr1.id = s.tr_nom
left join support_tickets_types ty on ty.id = t.id_type
left join translate tr4 on tr4.id = ty.tr_title
left join admins a on a.id_entite = t.id_admin
left join support_tickets_contrat on support_tickets_contrat.id_ticket = t.id
left join contrats on contrats.id = support_tickets_contrat.id_contrat
left join f_produits_machine arbo_link on arbo_link.id_produit = p.id
left join support_tickets_statuts statuts on t.id_statut = statuts.id
left join translate tr5 on tr5.id = statuts.tr_nom
left join entites e1 on e1.id = t.id_distributeur
left join entites e2 on e2.id = t.id_station
left join support_tickets_logs on support_tickets_logs.id_ticket = t.id
left join support_tickets_logs_types on support_tickets_logs_types.id = support_tickets_logs.id_type
left join translate tr6 on tr6.id = support_tickets_logs_types.tr_nom
where t.ts_creation > 1672527600 and contrats.id not in (3, 46, 51, 64, 71) and support_tickets_logs.id_type not in (50, 81, 84) and statut = 0
group by t.id