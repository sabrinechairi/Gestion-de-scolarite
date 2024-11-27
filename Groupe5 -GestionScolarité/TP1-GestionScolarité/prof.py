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

def ajouter_prof():
    id_ = entree1.get()
    nom = entree2.get()
    prenom = entree3.get()
    immatriculation = entree4.get()
    departement = entree5.get()

    # Base de données
    connexion = sqlite3.connect("Gscolarite.db")
    curseur = connexion.cursor()
    curseur.execute("""
        CREATE TABLE IF NOT EXISTS Prof (
            id INTEGER,
            nom TEXT,
            prenom TEXT,
            immatriculation INTEGER PRIMARY KEY,
            departement TEXT
        )
    """)
    curseur.execute("INSERT INTO Prof (id, nom, prenom, immatriculation, departement) VALUES (?, ?, ?, ?, ?)",
                    (id_, nom, prenom, immatriculation, departement))
    connexion.commit()
    connexion.close()

    # XML
    try:
        tree = etree.parse("Gscolarite.xml")
        root = tree.getroot()
    except (etree.XMLSyntaxError, FileNotFoundError):
        root = etree.Element("Gprofesseur")
        tree = etree.ElementTree(root)

    prof = etree.SubElement(root, "Prof")
    etree.SubElement(prof, "Id").text = id_
    etree.SubElement(prof, "Nom").text = nom
    etree.SubElement(prof, "Prenom").text = prenom
    etree.SubElement(prof, "Immatriculation").text = immatriculation
    etree.SubElement(prof, "Departement").text = departement

    tree.write("Gscolarite.xml", pretty_print=True)

    message_label.config(text="Données ajoutées avec succès.")

# Modifier un professeur (nouvelle fenêtre)
def ouvrir_fenetre_modifier():
    def chercher_prof():
        immatriculation = entree_immatriculation.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Prof WHERE immatriculation = ?", (immatriculation,))
        professeur = curseur.fetchone()
        connexion.close()

        if professeur:
            fenetre_modifier.destroy()
            afficher_fenetre_modification(professeur)
        else:
            message_label_modif.config(text="Professeur non trouvé.", fg="red")

    fenetre_modifier = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_modifier.iconphoto(False, icon)
    fenetre_modifier.title("Modifier un professeur")
    Label(fenetre_modifier, text="Immatriculation :").grid(row=0, column=0, padx=10, pady=5)
    entree_immatriculation = Entry(fenetre_modifier)
    entree_immatriculation.grid(row=0, column=1, padx=10, pady=5)
    Button(fenetre_modifier, text="Rechercher", command=chercher_prof).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_modif = Label(fenetre_modifier, text="")
    message_label_modif.grid(row=2, column=0, columnspan=2)

def afficher_fenetre_modification(professeur):
    def modifier_prof():
        nom = entree_nom.get()
        prenom = entree_prenom.get()
        departement = entree_departement.get()
        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("""
            UPDATE Prof
            SET nom = ?, prenom = ?, departement = ?
            WHERE immatriculation = ?
        """, (nom, prenom, departement, professeur[3]))
        connexion.commit()
        connexion.close()

        # Modifier XML
        try:
            tree = etree.parse("Gscolarite.xml")
            root = tree.getroot()
            for prof in root.findall("Prof"):
                if prof.find("Immatriculation").text == str(professeur[3]):
                    prof.find("Nom").text = nom
                    prof.find("Prenom").text = prenom
                    prof.find("Departement").text = departement
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
    entree_nom.insert(0, professeur[1])
    entree_nom.grid(row=0, column=1, padx=10, pady=5)

    Label(fenetre_modification, text="Prenom :").grid(row=1, column=0, padx=10, pady=5)
    entree_prenom = Entry(fenetre_modification)
    entree_prenom.insert(0, professeur[2])
    entree_prenom.grid(row=1, column=1, padx=10, pady=5)

    Label(fenetre_modification, text="Departement :").grid(row=2, column=0, padx=10, pady=5)
    entree_departement = ttk.Combobox(
        fenetre_modification, 
        values=["Biologie","Chimie","Géologie","Informatique","Mathématiques","Physique"]
    )
    entree_departement.insert(0, professeur[4])
    entree_departement.grid(row=2, column=1, padx=10, pady=5)

    Button(fenetre_modification, text="Modifier", command=modifier_prof).grid(row=3, column=0, columnspan=2, pady=10)
    message_label_modif_success = Label(fenetre_modification, text="")
    message_label_modif_success.grid(row=4, column=0, columnspan=2)

def ouvrir_fenetre_modifier_prof():
    def chercher_prof():
        immatriculation = entree_immatriculation.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Prof WHERE immatriculation = ?", (immatriculation,))
        professeur = curseur.fetchone()
        connexion.close()

        if professeur:
            fenetre_modifier.destroy()
            afficher_fenetre_modification(professeur)
        else:
            message_label_modif.config(text="Professeur non trouvé.", fg="red")

    fenetre_modifier = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_modifier.iconphoto(False, icon)
    fenetre_modifier.title("Modifier un professeur")

    Label(fenetre_modifier, text="Immatriculation :").grid(row=0, column=0, padx=10, pady=5)
    entree_immatriculation = Entry(fenetre_modifier)
    entree_immatriculation.grid(row=0, column=1, padx=10, pady=5)

    Button(fenetre_modifier, text="Rechercher", command=chercher_prof).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_modif = Label(fenetre_modifier, text="")
    message_label_modif.grid(row=2, column=0, columnspan=2)


# Supprimer un professeur (nouvelle fenêtre)
def ouvrir_fenetre_supprimer():
    def supprimer_prof():
        immatriculation = entree_immatriculation.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("DELETE FROM Prof WHERE immatriculation = ?", (immatriculation,))
        if curseur.rowcount == 0:
            message_label_suppr.config(text="Professeur non trouvé.", fg="red")
        else:
            connexion.commit()
            # Supprimer dans XML
            try:
                tree = etree.parse("Gscolarite.xml")
                root = tree.getroot()
                for prof in root.findall("Prof"):
                    if prof.find("Immatriculation").text == immatriculation:
                        root.remove(prof)
                        break
                tree.write("Gscolarite.xml", pretty_print=True)
            except Exception as e:
                print(f"Erreur XML: {e}")
            message_label_suppr.config(text="Professeur supprimé avec succès.", fg="green")
        connexion.close()

    fenetre_supprimer = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_supprimer.iconphoto(False, icon)
    fenetre_supprimer.title("Supprimer un professeur")
    Label(fenetre_supprimer, text="Immatriculation :").grid(row=0, column=0, padx=10, pady=5)
    entree_immatriculation = Entry(fenetre_supprimer)
    entree_immatriculation.grid(row=0, column=1, padx=10, pady=5)
    Button(fenetre_supprimer, text="Supprimer", command=supprimer_prof).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_suppr = Label(fenetre_supprimer, text="")
    message_label_suppr.grid(row=2, column=0, columnspan=2)


# Fonctions d'affichage inchangées
def afficher_bd():
    try:
        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Prof")
        rows = curseur.fetchall()
        connexion.close()

        window = tk.Toplevel()
        icon_path = r"Icons\iconUni.png"
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(False, icon)
        treeview = ttk.Treeview(window, columns=("ID", "Nom", "Prenom", "Immatriculation", "Departement"), show="headings")
        treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        treeview.heading("ID", text="ID")
        treeview.heading("Nom", text="Nom")
        treeview.heading("Prenom", text="Prenom")
        treeview.heading("Immatriculation", text="Immatriculation")
        treeview.heading("Departement", text="Departement")

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
        treeview = ttk.Treeview(window, columns=("ID", "Nom", "Prenom", "Immatriculation", "Departement"), show="headings")
        treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        treeview.heading("ID", text="ID")
        treeview.heading("Nom", text="Nom")
        treeview.heading("Prenom", text="Prenom")
        treeview.heading("Immatriculation", text="Immatriculation")
        treeview.heading("Departement", text="Departement")

        for prof in root.findall("Prof"):
            id_ = prof.find("Id").text
            nom = prof.find("Nom").text
            prenom = prof.find("Prenom").text
            immatriculation = prof.find("Immatriculation").text
            departement = prof.find("Departement").text
            treeview.insert("", "end", values=(id_, nom, prenom, immatriculation, departement))
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier XML: {e}")

# Interface principale
fenetre = Tk()
fenetre.title("Gestion des Professeurs")
icon_path = r"Icons\iconUni.png"
icon = tk.PhotoImage(file=icon_path)
fenetre.iconphoto(False, icon)
fenetre.geometry("400x350")
fenetre.resizable(False, False)


menu1 = Menu(fenetre)
menu1.add_cascade(label="Ajouter", command=None)  # Ajouter reste dans la fenêtre principale
menu1.add_cascade(label="Modifier", command=ouvrir_fenetre_modifier_prof)
menu1.add_cascade(label="Supprimer", command=ouvrir_fenetre_supprimer)
fenetre.config(menu=menu1)

Label(fenetre, text="ID :").grid(row=0, column=0, padx=10, pady=5)
entree1 = Entry(fenetre)
entree1.grid(row=0, column=1, padx=10, pady=5)

Label(fenetre, text="Nom :").grid(row=1, column=0, padx=10, pady=5)
entree2 = Entry(fenetre)
entree2.grid(row=1, column=1, padx=10, pady=5)

Label(fenetre, text="Prenom :").grid(row=2, column=0, padx=10, pady=5)
entree3 = Entry(fenetre)
entree3.grid(row=2, column=1, padx=10, pady=5)

Label(fenetre, text="Immatriculation :").grid(row=3, column=0, padx=10, pady=5)
entree4 = Entry(fenetre)
entree4.grid(row=3, column=1, padx=10, pady=5)

text5 = Label(fenetre, text="Departement :")
entree5 = ttk.Combobox(fenetre, values=["Biologie","Chimie","Géologie","Informatique","Mathématiques","Physique"])
text5.grid(row=4, column=0, padx=10, pady=5)
entree5.grid(row=4, column=1, padx=10, pady=5)

Button(fenetre, text="Ajouter", command=ajouter_prof).grid(row=5, column=0, columnspan=2, pady=10)
Button(fenetre, text="Effacer", command=vider).grid(row=5, column=1, padx=10, pady=10)

message_label = Label(fenetre, text="")
message_label.grid(row=6, column=0, columnspan=2)

Button(fenetre, text="Afficher -> BD", command=afficher_bd).grid(row=7, column=0, padx=10, pady=10)
Button(fenetre, text="Afficher -> XML", command=afficher_xml).grid(row=7, column=1, padx=10, pady=10)

fenetre.mainloop()
