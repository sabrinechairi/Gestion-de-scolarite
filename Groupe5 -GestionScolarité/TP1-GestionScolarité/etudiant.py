from tkinter import *
from lxml import etree
import sqlite3
import tkinter as tk
from tkinter import ttk

def vider():
    entree1.delete(0, 'end')
    entree2.delete(0, 'end')
    entree3.delete(0, 'end')
    entree4.delete(0, 'end')
    entree5.set("")

def ajouter_etudiant():
    id_ = entree1.get()
    nom = entree2.get()
    prenom = entree3.get()
    num_apogee = entree4.get()
    master = entree5.get()

    # Base de données
    connexion = sqlite3.connect("Gscolarite.db")
    curseur = connexion.cursor()
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS Etudiant (
            id INTEGER ,
            nom TEXT,
            prenom TEXT,
            num_apogee INTEGER PRIMARY KEY,
            master TEXT
        )
    """)
    curseur.execute("INSERT INTO Etudiant (id, nom, prenom, num_apogee, master) VALUES (?, ?, ?, ?, ?)",
                    (id_, nom, prenom, num_apogee, master))
    connexion.commit()
    connexion.close()

    # XML
    try:
        tree = etree.parse("Gscolarite.xml")
        root = tree.getroot()
    except (etree.XMLSyntaxError, FileNotFoundError):
        root = etree.Element("Gscolarite")
        tree = etree.ElementTree(root)

    etd = etree.SubElement(root, "Etudiant")
    etree.SubElement(etd, "Id").text = id_
    etree.SubElement(etd, "Nom").text = nom
    etree.SubElement(etd, "Prenom").text = prenom
    etree.SubElement(etd, "NumApogee").text = num_apogee
    etree.SubElement(etd, "Master").text = master

    tree.write("Gscolarite.xml", pretty_print=True)

    message_label.config(text="Données ajoutées avec succès.")

# Modifier un étudiant (nouvelle fenêtre)
def ouvrir_fenetre_modifier():
    def chercher_etudiant():
        num_apogee = entree_num_apogee.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Etudiant WHERE num_apogee = ?", (num_apogee,))
        etudiant = curseur.fetchone()
        connexion.close()

        if etudiant:
            fenetre_modifier.destroy()
            afficher_fenetre_modification(etudiant)
        else:
            message_label_modif.config(text="Étudiant non trouvé.", fg="red")

    fenetre_modifier = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_modifier.iconphoto(False, icon)
    fenetre_modifier.title("Modifier un étudiant")
    Label(fenetre_modifier, text="Numéro Apogée :").grid(row=0, column=0, padx=10, pady=5)
    entree_num_apogee = Entry(fenetre_modifier)
    entree_num_apogee.grid(row=0, column=1, padx=10, pady=5)
    Button(fenetre_modifier, text="Rechercher", command=chercher_etudiant).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_modif = Label(fenetre_modifier, text="")
    message_label_modif.grid(row=2, column=0, columnspan=2)

def afficher_fenetre_modification(etudiant):
    def modifier_etudiant():
        nom = entree_nom.get()
        prenom = entree_prenom.get()
        master = entree_master.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("""
            UPDATE Etudiant
            SET nom = ?, prenom = ?, master = ?
            WHERE num_apogee = ?
        """, (nom, prenom, master, etudiant[3]))
        connexion.commit()
        connexion.close()

        # Modifier XML
        try:
            tree = etree.parse("Gscolarite.xml")
            root = tree.getroot()
            for etd in root.findall("Etudiant"):
                if etd.find("NumApogee").text == str(etudiant[3]):
                    etd.find("Nom").text = nom
                    etd.find("Prenom").text = prenom
                    etd.find("Master").text = master
                    break
            tree.write("Gscolarite.xml", pretty_print=True)
        except Exception as e:
            print(f"Erreur XML: {e}")

        message_label_modif_success.config(text="Modification réussie.", fg="green")

    fenetre_modification = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_modification.iconphoto(False, icon)
    fenetre_modification.title("Modifier les informations")
    
    Label(fenetre_modification, text="Nom :").grid(row=0, column=0, padx=10, pady=5)
    entree_nom = Entry(fenetre_modification)
    entree_nom.insert(0, etudiant[1])
    entree_nom.grid(row=0, column=1, padx=10, pady=5)

    Label(fenetre_modification, text="Prenom :").grid(row=1, column=0, padx=10, pady=5)
    entree_prenom = Entry(fenetre_modification)
    entree_prenom.insert(0, etudiant[2])
    entree_prenom.grid(row=1, column=1, padx=10, pady=5)

    Label(fenetre_modification, text="Master :").grid(row=2, column=0, padx=10, pady=5)
    entree_master = ttk.Combobox(
        fenetre_modification, 
        values=[
            "Master B2S", "Master MQSE", "Master MRF", "Master MLAI",
            "Master CARA", "Master IBGE", "Master MM", "Master GPM",
            "Master MQL", "Master M2I", "Master MGEER"
        ]
    )
    entree_master.insert(0, etudiant[4])
    entree_master.grid(row=2, column=1, padx=10, pady=5)

    Button(fenetre_modification, text="Modifier", command=modifier_etudiant).grid(row=3, column=0, columnspan=2, pady=10)
    message_label_modif_success = Label(fenetre_modification, text="")
    message_label_modif_success.grid(row=4, column=0, columnspan=2)

# Supprimer un étudiant (nouvelle fenêtre)
def ouvrir_fenetre_supprimer():
    def supprimer_etudiant():
        num_apogee = entree_num_apogee.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("DELETE FROM Etudiant WHERE num_apogee = ?", (num_apogee,))
        if curseur.rowcount == 0:
            message_label_suppr.config(text="Étudiant non trouvé.", fg="red")
        else:
            connexion.commit()
            # Supprimer dans XML
            try:
                tree = etree.parse("Gscolarite.xml")
                root = tree.getroot()
                for etd in root.findall("Etudiant"):
                    if etd.find("NumApogee").text == num_apogee:
                        root.remove(etd)
                        break
                tree.write("Gscolarite.xml", pretty_print=True)
            except Exception as e:
                print(f"Erreur XML: {e}")
            message_label_suppr.config(text="Étudiant supprimé avec succès.", fg="green")
        connexion.close()

    fenetre_supprimer = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_supprimer.iconphoto(False, icon)
    fenetre_supprimer.title("Supprimer un étudiant")
    Label(fenetre_supprimer, text="Numéro Apogée :").grid(row=0, column=0, padx=10, pady=5)
    entree_num_apogee = Entry(fenetre_supprimer)
    entree_num_apogee.grid(row=0, column=1, padx=10, pady=5)
    Button(fenetre_supprimer, text="Supprimer", command=supprimer_etudiant).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_suppr = Label(fenetre_supprimer, text="")
    message_label_suppr.grid(row=2, column=0, columnspan=2)


# Fonctions d'affichage inchangées
def afficher_bd():
    try:
        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Etudiant")
        rows = curseur.fetchall()
        connexion.close()

        window = tk.Toplevel()
        icon_path = r"Icons\iconUni.png"
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(False, icon)
        treeview = ttk.Treeview(window, columns=("ID", "Nom", "Prenom", "NumApogee", "Master"), show="headings")
        treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        treeview.heading("ID", text="ID")
        treeview.heading("Nom", text="Nom")
        treeview.heading("Prenom", text="Prenom")
        treeview.heading("NumApogee", text="NumApogee")
        treeview.heading("Master", text="Master")

        for row in rows:
            treeview.insert("", "end", values=row)
    except sqlite3.Error as e:
        print(f"Erreur lors de la lecture de la base de données: {e}")

def afficher_xml():
    try:
        tree = etree.parse("Gscolarite.xml")
        root = tree.getroot()

        window = tk.Toplevel()
        icon_path = r"Icons\iconUni.png"
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(False, icon)
        treeview = ttk.Treeview(window, columns=("ID", "Nom", "Prenom", "NumApogee", "Master"), show="headings")
        treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        

        treeview.heading("ID", text="ID")
        treeview.heading("Nom", text="Nom")
        treeview.heading("Prenom", text="Prenom")
        treeview.heading("NumApogee", text="NumApogee")
        treeview.heading("Master", text="Master")

        for etd in root.findall("Etudiant"):
            id_ = etd.find("Id").text
            nom = etd.find("Nom").text
            prenom = etd.find("Prenom").text
            num_apogee = etd.find("NumApogee").text
            master = etd.find("Master").text
            treeview.insert("", "end", values=(id_, nom, prenom, num_apogee, master))
    except Exception as e:
        message_label.config(text=f"Erreur lors de la lecture du fichier XML: {e}", fg="red")

# Interface principale avec menu
fenetre = Tk()
fenetre.title("Gestion des étudiants ")
icon_path = r"Icons\iconUni.png"
icon = tk.PhotoImage(file=icon_path)
fenetre.iconphoto(False, icon)
fenetre.geometry("400x350")
fenetre.resizable(False, False)


menu1 = Menu(fenetre)
menu1.add_cascade(label="Ajouter", command=None)  # Ajouter reste dans la fenêtre principale
menu1.add_cascade(label="Modifier", command=ouvrir_fenetre_modifier)
menu1.add_cascade(label="Supprimer", command=ouvrir_fenetre_supprimer)
fenetre.config(menu=menu1)

# Interface pour Ajouter
Label(fenetre, text="Id :").grid(row=0, column=0, padx=10, pady=5)
entree1 = Entry(fenetre)
entree1.grid(row=0, column=1, padx=10, pady=5)

Label(fenetre, text="Nom :").grid(row=1, column=0, padx=10, pady=5)
entree2 = Entry(fenetre)
entree2.grid(row=1, column=1, padx=10, pady=5)

Label(fenetre, text="Prenom :").grid(row=2, column=0, padx=10, pady=5)
entree3 = Entry(fenetre)
entree3.grid(row=2, column=1, padx=10, pady=5)

Label(fenetre, text="Numéro Apogée :").grid(row=3, column=0, padx=10, pady=5)
entree4 = Entry(fenetre)
entree4.grid(row=3, column=1, padx=10, pady=5)

text5 = Label(fenetre, text="Master :")
entree5 = ttk.Combobox(fenetre, values=["Master B2S", "Master MQSE", "Master MRF", "Master MLAI",
                                         "Master CARA", "Master IBGE", "Master MM", "Master GPM", 
                                         "Master MQL", "Master M2I", "Master MGEER"])
text5.grid(row=4, column=0, padx=10, pady=5)
entree5.grid(row=4, column=1, padx=10, pady=5)

Button(fenetre, text="Ajouter", command=ajouter_etudiant).grid(row=5, column=0, columnspan=2, pady=10)
Button(fenetre, text="Effacer", command=vider).grid(row=5, column=1, padx=10, pady=10)
message_label = Label(fenetre, text="")
message_label.grid(row=6, column=0, columnspan=2)

Button(fenetre, text="Afficher -> BD", command=afficher_bd).grid(row=7, column=0, padx=10, pady=10)
Button(fenetre, text="Afficher -> XML", command=afficher_xml).grid(row=7, column=1, padx=10, pady=10)



fenetre.mainloop()
