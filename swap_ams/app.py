from flask import Flask, flash, redirect, render_template, request, session
import pandas as pd

# Configure application
app = Flask(__name__)

@app.route("/")
def index():

    # read the file
    df = pd.read_csv("D:/Code/CS50_Final/swap_ams/db/orders.csv", sep=",")

    # show all tickets that are not admin closure and not removed
    total_tickets = len(df[(df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])

    verif_feider = len(df[(df["pseudo"]=="03 - Agent Vérification SWAP") & (df["contrat"] == "BUILDER / TCK") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    verif_all = len(df[(df["pseudo"]=="03 - Agent Vérification SWAP") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    verif_others = verif_all - verif_feider

    admin_feider = len(df[(df["pseudo"]=="02 - Agent Administratif SWAP") & (df["contrat"] == "BUILDER / TCK") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    admin_all = len(df[(df["pseudo"]=="02 - Agent Administratif SWAP") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    admin_others = admin_all - admin_feider

    tech_feider = len(df[(df["pseudo"]=="01 - Agent Technique SWAP") & (df["contrat"] == "BUILDER / TCK") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    tech_all = len(df[(df["pseudo"]=="01 - Agent Technique SWAP") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    tech_others = tech_all - tech_feider

    pieces_feider = len(df[(df["pseudo"]=="01 - Agent Technique SWAP") & (df["contrat"] == "BUILDER / TCK") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    pieces_all = len(df[(df["pseudo"]=="01 - Agent Technique SWAP") & (df["is_admin_closure"] == 0) & (df["is_removed"] == 0)])
    pieces_others = pieces_all - pieces_feider

    return render_template("index.html", tech_feider=tech_feider,tech_others=tech_others, total_tickets = total_tickets,verif_feider=verif_feider, verif_others=verif_others, admin_others=admin_others, admin_feider=admin_feider )


# следить за изменениями в количестве обработанных и необработанных тикетов на ежедневной основе с разрезом по контрактам

# скачать базу данных для отслеживания, нужны : номер тикета, админ, контракт, закрыто или нет (админ + другое)
# статусы, логи

# сколько тикетов не закрытых было и сколько стало
