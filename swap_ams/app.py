from flask import Flask, flash, redirect, render_template, request, session
import pandas as pd

# Configure application
app = Flask(__name__)

@app.route("/")
def index():

    # read the morning file
    # dfMorning = pd.read_csv("D:/Code/CS50_Final/swap_ams/db/morning.csv", sep=",")
    dfMorning = pd.read_csv("/home/gamz/Code/SWAP/cs50_final/swap_ams/db/morning.csv", sep=",")

    # read the evening file
    # dfEvening = pd.read_csv("D:/Code/CS50_Final/swap_ams/db/evening.csv", sep=",")
    dfEvening = pd.read_csv("/home/gamz/Code/SWAP/cs50_final/swap_ams/db/evening.csv", sep=",")

    # show all tickets that are not admin closure and not removed
    total_tickets_morning = len(dfMorning)
    total_tickets_evening = len(dfEvening)

    # agents verif
    verif_feider_morning = len(dfMorning[(dfMorning["pseudo"]=="03 - Agent Vérification SWAP") 
                          & (dfMorning["marque"] == "FEIDER")])
    
    verif_all_morning = len(dfMorning[(dfMorning["pseudo"]=="03 - Agent Vérification SWAP")])
    
    verif_others_morning = verif_all_morning - verif_feider_morning

    verif_feider_evening = len(dfEvening[(dfEvening["pseudo"]=="03 - Agent Vérification SWAP") 
                          & (dfEvening["marque"] == "FEIDER")])
    
    verif_all_evening = len(dfEvening[(dfEvening["pseudo"]=="03 - Agent Vérification SWAP")])
    
    verif_others_evening = verif_all_evening - verif_feider_evening


    # agents admin
    admin_feider_morning = len(dfMorning[(dfMorning["pseudo"]=="02 - Agent Administratif SWAP") 
                          & (dfMorning["marque"] == "FEIDER")])
    
    admin_all_morning = len(dfMorning[(dfMorning["pseudo"]=="02 - Agent Administratif SWAP")])
    
    admin_others_morning = admin_all_morning - admin_feider_morning

    admin_feider_evening = len(dfEvening[(dfEvening["pseudo"]=="02 - Agent Administratif SWAP") 
                          & (dfEvening["marque"] == "FEIDER")])
    
    admin_all_evening = len(dfEvening[(dfEvening["pseudo"]=="02 - Agent Administratif SWAP")])
    
    admin_others_evening = admin_all_evening - admin_feider_evening


    # agents tech
    tech_feider_morning  = len(dfMorning[(dfMorning["pseudo"]=="01 - Agent Technique SWAP") 
                         & (dfMorning["marque"] == "FEIDER")])
    
    tech_all_morning = len(dfMorning[(dfMorning["pseudo"]=="01 - Agent Technique SWAP")])
    
    tech_others_morning = tech_all_morning - tech_feider_morning

    tech_feider_evening  = len(dfEvening[(dfEvening["pseudo"]=="01 - Agent Technique SWAP") 
                         & (dfEvening["marque"] == "FEIDER")])
    
    tech_all_evening = len(dfEvening[(dfEvening["pseudo"]=="01 - Agent Technique SWAP")])
    
    tech_others_evening = tech_all_evening - tech_feider_evening


    # agent pieces
    pieces_feider_morning = len(dfMorning[(dfMorning["pseudo"]=="04 - Agent Pièces SWAP") 
                           & (dfMorning["marque"] == "FEIDER")])
    
    pieces_all_morning = len(dfMorning[(dfMorning["pseudo"]=="04 - Agent Pièces SWAP")])
    
    pieces_others = pieces_all_morning - pieces_feider_morning

    pieces_feider_evening = len(dfEvening[(dfEvening["pseudo"]=="04 - Agent Pièces SWAP") 
                           & (dfEvening["marque"] == "FEIDER")])
    
    pieces_all_evening = len(dfEvening[(dfEvening["pseudo"]=="04 - Agent Pièces SWAP")])
    
    pieces_others_evening = pieces_all_evening - pieces_feider_evening

    return render_template("index.html", 
                           pieces_others=pieces_others, pieces_feider_morning=pieces_feider_morning, 
                           pieces_others_evening=pieces_others_evening, pieces_feider_evening=pieces_feider_evening, 
                           tech_feider_morning=tech_feider_morning,tech_others_morning=tech_others_morning, 
                           tech_feider_evening=tech_feider_evening,tech_others_evening=tech_others_evening, 
                           total_tickets_morning=total_tickets_morning,
                           total_tickets_evening=total_tickets_evening,
                           verif_feider_morning=verif_feider_morning, verif_others_morning=verif_others_morning, 
                           verif_feider_evening=verif_feider_evening, verif_others_evening=verif_others_evening,
                           admin_others_morning=admin_others_morning, admin_feider_morning=admin_feider_morning, 
                           admin_feider_evening=admin_feider_evening, admin_others_evening=admin_others_evening)


# следить за изменениями в количестве обработанных и необработанных тикетов на ежедневной основе с разрезом по контрактам

# скачать базу данных для отслеживания, нужны : номер тикета, админ, контракт, закрыто или нет (админ + другое)
# статусы, логи

# сколько тикетов не закрытых было и сколько стало
