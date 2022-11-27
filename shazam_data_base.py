import sqlite3 as sql
#si vous voulez visualiser la base de données: téléchargez le logiciel DB Browser for SQlite

#connection à la base de données
connexion=sql.connect("shazam_data_base.db")

#création curseur (outil qui permet de faire des requêtes)
cursor=connexion.cursor()

#création de la base de données à 7 champs si elle n'existe pas déjà
cursor.execute('''create table if not exists Data_base(
id integer primary key autoincrement,
title text,
author text,
frequency_1 real,
frequency_2 real,
delta_time real,
time_1 real
)''')

#on se déconnecte de la base de données
connexion.close()