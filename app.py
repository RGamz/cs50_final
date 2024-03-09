from datetime import datetime
from flask import Flask, render_template, g
import logging
import sqlite3
# from database import engine

# Configure application
app = Flask(__name__)

DATABASE = '/workspaces/gamzat-python/db/support_tickets.db'

# sqlite3 connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.cursor = g.db.cursor()
    return g.db, g.cursor

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def calculate_days_since(date_str):
    """Calculate the number of days since the given date."""
    date = datetime.strptime(date_str, '%d.%m.%Y')
    today = datetime.today()
    return (today - date).days

def tickets_to_list(ticket_list, rows):
    """Populate a list with ticket data from the given rows."""
    for row in rows:
                days_since_last_log = calculate_days_since(row[6])
                days_since_creation = calculate_days_since(row[7])

                ticket_data = {'id': row[0], 'ref': row[1], 'contrat': row[2], 'distributeur': row[3], 'station': row[4], 'read': row[5], 'days_since_last_log': days_since_last_log, 'days_since_creation': days_since_creation}
                ticket_list.append(ticket_data)
    return ticket_list

@app.before_request
def before_request():
    get_db()

@app.teardown_request
def teardown_request(exception=None):
    close_db()

# create index route
@app.route('/')
def index():

    try:
        # connect to the db
        db, cursor = get_db()

        cursor.execute("SELECT ticket_admin, COUNT(id) as total_tickets, COUNT(CASE WHEN read = 1 THEN id END) AS lu, COUNT(CASE WHEN read = 0 THEN id END) AS non_lu, SUM(id) as ticket_qty_sum, SUM(CASE WHEN read = 1 THEN id END) AS sum_lu, SUM(CASE WHEN read = 0 THEN id END) AS sum_non_lu FROM tickets GROUP BY ticket_admin")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []
        total_sum = 0
        total_lu = 0
        total_non_lu = 0

        for row in rows:
            total_sum += row[1]
            total_lu += row[2]
            total_non_lu += row[3]
            ticket_data = {'ticket_admin': row[0], 'total_tickets': row[1], 'lu': row[2], 'non_lu': row[3]}
            openTicketList.append(ticket_data)


        # select for the admin log qty table
        # ---------------------
        cursor.execute("SELECT log_admin, logs_qty FROM logs")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList2 = []
        logs_sum = 0

        for row in rows:
            logs_sum += row[1]
            ticket_data = {'log_admin': row[0], 'logs_qty': row[1]}
            openTicketList2.append(ticket_data)

        return render_template('index.html',
                            openTicketList=openTicketList,
                            openTicketList2=openTicketList2,
                            total_sum=total_sum,total_lu=total_lu,total_non_lu=total_non_lu,
                            logs_sum=logs_sum)
    
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'index' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.route('/agent_v')
def agent_v():

    try: 
        # connect to the db
        db, cursor = get_db()

        # get today's ticket qty for agent verif
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '03 - Agent Vérification SWAP' AND type_ticket != 'Prise en charge Hors Garantie'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []
        tickets_to_list(openTicketList, rows)

        openTicketCounter = len(openTicketList)

        return render_template('agent_v.html', 
                            openTicketList=openTicketList, openTicketCounter=openTicketCounter)
    
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'agent_v' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.route('/agent_a')
def agent_a():

    try: 
        # connect to the db
        db, cursor = get_db()

        # tous tickets type demande de garantie et agent admin => organiser transport aller et attribuer la station
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '02 - Agent Administratif SWAP' AND type_ticket == 'Demande de Garantie'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []
        tickets_to_list(openTicketList, rows)

        openTicketCounter = len(openTicketList)

        # tickets en attente de validation par tech mais admin != tech
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin != '01 - Agent Technique SWAP' AND id_status IN (2, 4)")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList2 = []

        tickets_to_list(openTicketList2, rows)
        openTicketCounter2 = len(openTicketList2)

        # tickets reparation reussie ou anr et donc en attente de transport retour
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '02 - Agent Administratif SWAP' AND id_status IN (7, 14)")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries 
        openTicketList3 = []
        tickets_to_list(openTicketList3, rows)

        openTicketCounter3 = len(openTicketList3)

        # tous les tickets admin
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '02 - Agent Administratif SWAP' AND type_ticket != 'Prise en charge Hors Garantie'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries 
        openTicketList30 = []
        tickets_to_list(openTicketList30, rows)

        openTicketCounter30 = len(openTicketList30)

        return render_template('agent_a.html',
                            openTicketList=openTicketList,openTicketCounter=openTicketCounter,
                            openTicketList2=openTicketList2,openTicketCounter2=openTicketCounter2,
                            openTicketList3=openTicketList3,openTicketCounter3=openTicketCounter3,
                            openTicketList30=openTicketList30,openTicketCounter30=openTicketCounter30)
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'agent_a' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.route('/agent_t')
def agent_t():

    try: 
        # connect to the db
        db, cursor = get_db()

        # Envoi pièces (contrat Bronze)
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('BCM Better Choice','BCM BURGAIN','BCM JIWEI','BCM Le Fun', 'Carrefour Barbecues','FOXTER ASPIRATEUR -LECLERC','JHS CLIM -LECLERC','LECLERC - MONO Batterie','NHP FOXTER - LECLERC')")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []
        tickets_to_list(openTicketList, rows)

        openTicketCounter = len(openTicketList)

        # REUSED
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat == 'SWAP REUSED'")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList2 = []
        tickets_to_list(openTicketList2, rows)

        openTicketCounter2 = len(openTicketList2)

        # MTD
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('MTD - assist. dom.','MTD - standard')")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList3 = []
        tickets_to_list(openTicketList3, rows)

        openTicketCounter3 = len(openTicketList3)

        # Réparation sans faible valeur
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('BCM ZHONGJIAN / TOPSUN','RYOBI','YAT - Robots','SIPLEC - LITTAN')")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList4 = []
        tickets_to_list(openTicketList4, rows)

        openTicketCounter4 = len(openTicketList4)

        # Kingfisher et Leclerc Ext
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('KINGFISHER','LECLERC Externe (Hors Garantie)')")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList5 = []
        tickets_to_list(openTicketList5, rows)

        openTicketCounter5 = len(openTicketList5)

        # Kingfisher riders
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('KINGFISHER') and id_arbo in (1251,217)")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList6 = []
        tickets_to_list(openTicketList6, rows)

        openTicketCounter6 = len(openTicketList6)

        # Leroy Merlin
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('LEROY MERLIN FR - STERWINS','BUILDER / TCK') AND distributeur LIKE '%LEROY MERLIN%' ")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList7 = []
        tickets_to_list(openTicketList7, rows)

        openTicketCounter7 = len(openTicketList7)

        # Faible valeur 50
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('BCM Dunsch','BCM HIGH HOPE','BCM Johnwin','BCM Kingxxel','BCM POWFIT','BCM Sunray','BCM Sunseeker','BCM YAT automne 2017','BCM YAT printemps 2015')")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList8 = []
        tickets_to_list(openTicketList8, rows)

        openTicketCounter8 = len(openTicketList8)

        # Faible valeur 80
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('BUILDER / TCK') AND distributeur NOT LIKE '%LEROY MERLIN%' ")

        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList11 = []
        tickets_to_list(openTicketList11, rows)

        openTicketCounter11 = len(openTicketList11)

        # Kaufland
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('Kaufland')")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList9 = []
        tickets_to_list(openTicketList9, rows)

        openTicketCounter9 = len(openTicketList9)

        # Pannes au deballage?
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie' AND contrat IN ('BUILDER / TCK','BCM Dunsch','BCM HIGH HOPE','BCM Johnwin','BCM Kingxxel','BCM POWFIT','BCM Sunray','BCM Sunseeker','BCM YAT automne 2017','BCM YAT printemps 2015','SWAP REUSED') AND julianday(creation_date) - julianday(date_achat) < 10")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList10 = []
        tickets_to_list(openTicketList10, rows)

        openTicketCounter10 = len(openTicketList10)

        # tous tickets confondus
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '01 - Agent Technique SWAP' AND type_ticket !='Prise en charge Hors Garantie'")
        
        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList12 = []
        tickets_to_list(openTicketList12, rows)

        openTicketCounter12 = len(openTicketList12)

        return render_template('agent_t.html', 
                            openTicketList=openTicketList,openTicketCounter=openTicketCounter,
                            openTicketList2=openTicketList2,openTicketCounter2=openTicketCounter2,
                            openTicketList3=openTicketList3,openTicketCounter3=openTicketCounter3,
                            openTicketList4=openTicketList4,openTicketCounter4=openTicketCounter4,
                            openTicketList5=openTicketList5,openTicketCounter5=openTicketCounter5,
                            openTicketList6=openTicketList6,openTicketCounter6=openTicketCounter6,
                            openTicketList7=openTicketList7,openTicketCounter7=openTicketCounter7,
                            openTicketList8=openTicketList8,openTicketCounter8=openTicketCounter8,
                            openTicketList9=openTicketList9,openTicketCounter9=openTicketCounter9,
                            openTicketList10=openTicketList10,openTicketCounter10=openTicketCounter10,
                            openTicketList11=openTicketList11,openTicketCounter11=openTicketCounter11,
                            openTicketList12=openTicketList12,openTicketCounter12=openTicketCounter12)
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'agent_t' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.route('/agent_hg')
def agent_hg():

    try:
        # connect to the db
        db, cursor = get_db()

        # tous tickets HG en attente de diagnostic ou devis station
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND id_status IN (1,16,34)")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []
        tickets_to_list(openTicketList, rows)

        openTicketCounter = len(openTicketList)

        # tous tickets HG en attente de la modération par un administrateur du devis proposé par la station
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND status == 'Modération par un administrateur du devis proposé par la station'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList2 = []
        tickets_to_list(openTicketList2, rows)

        openTicketCounter2 = len(openTicketList2)

        # tous tickets HG en attente de devis pour client
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND status == 'L''administrateur SWAP doit établir un devis pour le client'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList3 = []
        tickets_to_list(openTicketList3, rows)

        openTicketCounter3 = len(openTicketList3)

        # attente acceptation devis par le client
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND status == 'Le client doit indiquer s''il accepte ou non le devis SWAP'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList4 = []
        tickets_to_list(openTicketList4, rows)

        openTicketCounter4 = len(openTicketList4)

        # Le client a accepté le devis, la station peut commencer la réparation
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND id_status == 39")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList5 = []
        tickets_to_list(openTicketList5, rows)

        openTicketCounter5 = len(openTicketList5)

        # En attente de paiement du panier par le client
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND id_status == 62")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList6 = []
        tickets_to_list(openTicketList6, rows)

        openTicketCounter6 = len(openTicketList6)

        # La prestation n'a pas pu aboutir
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND id_status == 37")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList7 = []
        tickets_to_list(openTicketList7, rows)

        openTicketCounter7 = len(openTicketList7)

        # La réparation a été effectuée avec succès
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND id_status IN (14,40)")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList8 = []
        tickets_to_list(openTicketList8, rows)

        openTicketCounter8 = len(openTicketList8)
        
        # Le transport retour a besoin d'être modéré par un admin
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie' AND id_status == 60")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList9 = []
        tickets_to_list(openTicketList9, rows)

        openTicketCounter9 = len(openTicketList9)

        # all tickets hg
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE type_ticket =='Prise en charge Hors Garantie'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList40 = []
        tickets_to_list(openTicketList40, rows)

        openTicketCounter40 = len(openTicketList40)

        return render_template('agent_hg.html',
                            openTicketList=openTicketList,openTicketCounter=openTicketCounter,
                            openTicketList2=openTicketList2,openTicketCounter2=openTicketCounter2,
                            openTicketList3=openTicketList3,openTicketCounter3=openTicketCounter3,
                            openTicketList4=openTicketList4,openTicketCounter4=openTicketCounter4,
                            openTicketList5=openTicketList5,openTicketCounter5=openTicketCounter5,
                            openTicketList6=openTicketList6,openTicketCounter6=openTicketCounter6,
                            openTicketList7=openTicketList7,openTicketCounter7=openTicketCounter7,
                            openTicketList8=openTicketList8,openTicketCounter8=openTicketCounter8,
                            openTicketList9=openTicketList9,openTicketCounter9=openTicketCounter9,
                            openTicketList40=openTicketList40,openTicketCounter40=openTicketCounter40)
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'agent_hg' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.route('/agent_m')
def agent_m():

    try:
        # connect to the db
        db, cursor = get_db()

        # tous tickets HG en attente de devis station
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '05 - Agent Moteur BS/Honda' AND type_ticket !='Prise en charge Hors Garantie'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []
        tickets_to_list(openTicketList, rows)

        openTicketCounter = len(openTicketList)

        return render_template('agent_m.html',
                            openTicketList=openTicketList,openTicketCounter=openTicketCounter)
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'agent_m' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.route('/agent_p')
def agent_p():

    try:
        # connect to the db
        db, cursor = get_db()

        # tous tickets HG en attente de devis station
        # get selection
        cursor.execute("SELECT id, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin == '04 - Agent Pièces SWAP' AND type_ticket !='Prise en charge Hors Garantie'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []
        tickets_to_list(openTicketList, rows)

        openTicketCounter = len(openTicketList)

        return render_template('agent_p.html',
                            openTicketList=openTicketList,openTicketCounter=openTicketCounter)
    
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'agent_p' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.route('/autres_agents')
def autres_agents():

    try:
        # connect to the db
        db, cursor = get_db()

        # tous tickets HG en attente de devis station
        # get selection
        cursor.execute("SELECT id, ticket_admin, ref, contrat, distributeur, station, read, last_log_time, creation_date FROM tickets WHERE ticket_admin NOT IN ('01 - Agent Technique SWAP', '02 - Agent Administratif SWAP', '03 - Agent Vérification SWAP', '04 - Agent Pièces SWAP', '05 - Agent Moteur BS/Honda') AND type_ticket !='Prise en charge Hors Garantie'")

        # Fetch all rows from the result set
        rows = cursor.fetchall()

        # Create a list of dictionaries with days_since_creation
        openTicketList = []

        for row in rows:

            days_since_creation = calculate_days_since(row[8])

            days_since_last_log = calculate_days_since(row[7])

            ticket_data = {'id': row[0], 'ticket_admin': row[1], 'ref': row[2], 'contrat': row[3], 'distributeur': row[4], 'station': row[5], 'read': row[6], 'days_since_last_log': days_since_last_log, 'days_since_creation': days_since_creation}
            openTicketList.append(ticket_data)

        openTicketCounter = len(openTicketList)

        return render_template('autres_agents.html',
                            openTicketList=openTicketList, openTicketCounter=openTicketCounter)
    
    except Exception as e:
        # Handle exceptions (log or return an error page)
        logging.exception("An error occurred in the 'autres_agents' route: %s", str(e))
        return render_template('error.html', error_message=str(e))

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('page404.html')

if __name__=='__main__':
    app.run(debug=True)