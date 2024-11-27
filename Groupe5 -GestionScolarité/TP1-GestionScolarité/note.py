from tkinter import *
from lxml import etree
import sqlite3
from tkinter import ttk
import tkinter as tk

def vider():
    entree1.delete(0, 'end')
    entree2.delete(0, 'end')
    entree3.delete(0, 'end')
    entree4.delete(0, 'end')

def ajouter_note():
    id_note = entree1.get()
    num_apogee = entree2.get()
    module_id = entree3.get()
    note_val = entree4.get()

    try:
        # Vérification de la validité de la note
        if not note_val.replace('.', '', 1).isdigit() or float(note_val) < 0 or float(note_val) > 20:
            message_label.config(text="Erreur : La note doit être un nombre entre 0 et 20.", fg="red")
            return

        # Base de données
        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.executescript("""
            CREATE TABLE IF NOT EXISTS Note (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                etudiant_num_apogee INTEGER,
                module_id INTEGER,
                note REAL,
                FOREIGN KEY (etudiant_num_apogee) REFERENCES Etudiant(num_apogee),
                FOREIGN KEY (module_id) REFERENCES Module(id)
            );
        """)
        curseur.execute(
            "INSERT INTO Note (id, etudiant_num_apogee, module_id, note) VALUES (?, ?, ?, ?)",
            (id_note, num_apogee, module_id, float(note_val)),
        )
        connexion.commit()
        connexion.close()

        # XML
        try:
            tree = etree.parse("Gscolarite.xml")
            root = tree.getroot()
        except (etree.XMLSyntaxError, FileNotFoundError):
            root = etree.Element("Gscolarite")
            tree = etree.ElementTree(root)

        note_elem = etree.SubElement(root, "Note")
        etree.SubElement(note_elem, "ID").text = id_note
        etree.SubElement(note_elem, "EtudiantNumApogee").text = num_apogee
        etree.SubElement(note_elem, "Module_ID").text = module_id
        etree.SubElement(note_elem, "Note").text = note_val

        tree.write("Gscolarite.xml", pretty_print=True)

        message_label.config(text="Note ajoutée avec succès.", fg="green")
    except Exception as e:
        message_label.config(text=f"Erreur : {e}", fg="red")

def supprimer_note():
#def supprimer_note():
    def confirmer_suppression():
        id_note = entree_id_suppression.get()

        try:
            # Suppression dans la BD
            connexion = sqlite3.connect("Gscolarite.db")
            curseur = connexion.cursor()
            curseur.execute("DELETE FROM Note WHERE id = ?", (id_note,))
            connexion.commit()
            connexion.close()

            # Suppression dans XML
            try:
                tree = etree.parse("Gscolarite.xml")
                root = tree.getroot()
                for elem in root.findall("Note"):
                    if elem.find("ID").text == id_note:
                        root.remove(elem)
                        break
                tree.write("Gscolarite.xml", pretty_print=True)

                message_label_suppression.config(text="Note supprimée avec succès.", fg="green")
            except Exception as e:
                message_label_suppression.config(text=f"Erreur XML : {e}", fg="red")
        except Exception as e:
            message_label_suppression.config(text=f"Erreur : {e}", fg="red")

    # Fenêtre pour saisir l'ID
    fenetre_suppression = Toplevel()
    fenetre_suppression.title("Supprimer une note")
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_suppression.iconphoto(False, icon)

    Label(fenetre_suppression, text="ID de la note à supprimer :").grid(row=0, column=0, padx=10, pady=5)
    entree_id_suppression = Entry(fenetre_suppression)
    entree_id_suppression.grid(row=0, column=1, padx=10, pady=5)

    Button(fenetre_suppression, text="Supprimer", command=confirmer_suppression).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_suppression = Label(fenetre_suppression, text="")
    message_label_suppression.grid(row=2, column=0, columnspan=2)



def modifier_note():
    def chercher_note():
        num_apogee = entree2_num_apogee.get()
        module_id = entree3_module_id.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Note WHERE etudiant_num_apogee = ? AND module_id = ?", (num_apogee, module_id))
        note = curseur.fetchone()
        connexion.close()

        if note:
            fenetre_modifier.destroy()
            afficher_fenetre_modification(note)
        else:
            message_label_modif.config(text="Note non trouvée.", fg="red")

    def afficher_fenetre_modification(note):
        def appliquer_modifications():
            new_note = entree_note.get()

            # Vérification de la validité de la nouvelle note
            if not new_note.replace('.', '', 1).isdigit() or float(new_note) < 0 or float(new_note) > 20:
                message_label_modif_success.config(text="Erreur : La note doit être un nombre entre 0 et 20.", fg="red")
                return

            # Mise à jour BD
            connexion = sqlite3.connect("Gscolarite.db")
            curseur = connexion.cursor()
            curseur.execute(
                """
                UPDATE Note
                SET note = ?
                WHERE etudiant_num_apogee = ? AND module_id = ?
                """,
                (float(new_note), note[1], note[2]),
            )
            connexion.commit()
            connexion.close()

            # Mise à jour XML
            try:
                tree = etree.parse("Gscolarite.xml")
                root = tree.getroot()
                for elem in root.findall("Note"):
                    if elem.find("EtudiantNumApogee").text == str(note[1]) and elem.find("Module_ID").text == str(note[2]):
                        elem.find("Note").text = new_note
                        break
                tree.write("Gscolarite.xml", pretty_print=True)
            except Exception as e:
                print(f"Erreur XML: {e}")

            message_label_modif_success.config(text="Modification réussie.", fg="green")

        fenetre_modification = Toplevel()
        icon_path = r"Icons\iconUni.png"
        icon = tk.PhotoImage(file=icon_path)
        fenetre_modification.iconphoto(False, icon)
        fenetre_modification.title("Modifier une note")
        Label(fenetre_modification, text="Nouvelle Note :").grid(row=0, column=0, padx=10, pady=5)
        entree_note = Entry(fenetre_modification)
        entree_note.insert(0, str(note[3]))  # Pré-remplir avec la note actuelle
        entree_note.grid(row=0, column=1, padx=10, pady=5)

        Button(fenetre_modification, text="Appliquer", command=appliquer_modifications).grid(row=1, column=0, columnspan=2, pady=10)
        message_label_modif_success = Label(fenetre_modification, text="")
        message_label_modif_success.grid(row=2, column=0, columnspan=2)

    # Fenêtre pour entrer le num_apogee et module_id
    fenetre_modifier = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_modifier.iconphoto(False, icon)
    fenetre_modifier.title("Modifier une note")
    Label(fenetre_modifier, text="Numéro Apogée :").grid(row=0, column=0, padx=10, pady=5)
    entree2_num_apogee = Entry(fenetre_modifier)
    entree2_num_apogee.grid(row=0, column=1, padx=10, pady=5)

    Label(fenetre_modifier, text="ID du module :").grid(row=1, column=0, padx=10, pady=5)
    entree3_module_id = Entry(fenetre_modifier)
    entree3_module_id.grid(row=1, column=1, padx=10, pady=5)

    Button(fenetre_modifier, text="Rechercher", command=chercher_note).grid(row=2, column=0, columnspan=2, pady=10)
    message_label_modif = Label(fenetre_modifier, text="")
    message_label_modif.grid(row=3, column=0, columnspan=2)


# Afficher les données de la BD
def afficher_bd():
    fenetre_bd = Toplevel()
    fenetre_bd.title("Données de la Base de Données")
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_bd.iconphoto(False, icon)

    connexion = sqlite3.connect("Gscolarite.db")
    curseur = connexion.cursor()
    curseur.execute("SELECT * FROM Note")
    donnees = curseur.fetchall()
    connexion.close()

    # Ajouter les en-têtes
    Label(fenetre_bd, text="ID", width=15, borderwidth=1, relief="solid").grid(row=0, column=0)
    Label(fenetre_bd, text="Numéro Apogée", width=15, borderwidth=1, relief="solid").grid(row=0, column=1)
    Label(fenetre_bd, text="Module ID", width=15, borderwidth=1, relief="solid").grid(row=0, column=2)
    Label(fenetre_bd, text="Note", width=15, borderwidth=1, relief="solid").grid(row=0, column=3)

    for i, ligne in enumerate(donnees, start=1):
        for j, val in enumerate(ligne):
            Label(fenetre_bd, text=val, borderwidth=1, relief="solid", width=15).grid(row=i, column=j)

    Button(fenetre_bd, text="Fermer", command=fenetre_bd.destroy).grid(row=len(donnees) + 1, column=0, columnspan=4, pady=10)


# Afficher les données du fichier XML
def afficher_xml():
    fenetre_xml = Toplevel()
    fenetre_xml.title("Données du Fichier XML")
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_xml.iconphoto(False, icon)

    try:
        tree = etree.parse("Gscolarite.xml")
        root = tree.getroot()

        # Ajouter les en-têtes
        Label(fenetre_xml, text="ID", width=15, borderwidth=1, relief="solid").grid(row=0, column=0)
        Label(fenetre_xml, text="Numéro Apogée", width=15, borderwidth=1, relief="solid").grid(row=0, column=1)
        Label(fenetre_xml, text="Module ID", width=15, borderwidth=1, relief="solid").grid(row=0, column=2)
        Label(fenetre_xml, text="Note", width=15, borderwidth=1, relief="solid").grid(row=0, column=3)

        for i, note in enumerate(root.findall("Note"), start=1):
            Label(fenetre_xml, text=note.find("ID").text, borderwidth=1, relief="solid", width=15).grid(row=i, column=0)
            Label(fenetre_xml, text=note.find("EtudiantNumApogee").text, borderwidth=1, relief="solid", width=15).grid(row=i, column=1)
            Label(fenetre_xml, text=note.find("Module_ID").text, borderwidth=1, relief="solid", width=15).grid(row=i, column=2)
            Label(fenetre_xml, text=note.find("Note").text, borderwidth=1, relief="solid", width=15).grid(row=i, column=3)

    except Exception as e:
        Label(fenetre_xml, text=f"Erreur : {e}").pack()

    Button(fenetre_xml, text="Fermer", command=fenetre_xml.destroy).grid(row=i + 1, column=0, columnspan=4, pady=10)


# Interface principale
fenetre = Tk()
fenetre.title("Gestion des Notes")
icon_path = r"Icons\iconUni.png"
icon = tk.PhotoImage(file=icon_path)
fenetre.iconphoto(False, icon)
fenetre.geometry("400x350")
fenetre.resizable(False, False)

menu1 = Menu(fenetre)
menu1.add_cascade(label="Ajouter", command=None)  # Ajouter reste dans la fenêtre principale
menu1.add_cascade(label="Modifier", command=modifier_note)
menu1.add_cascade(label="Supprimer", command=supprimer_note)
fenetre.config(menu=menu1)

Label(fenetre, text="ID de la note :").grid(row=0, column=0, padx=10, pady=5)
Label(fenetre, text="Numéro Apogée :").grid(row=1, column=0, padx=10, pady=5)
Label(fenetre, text="ID du module :").grid(row=2, column=0, padx=10, pady=5)
Label(fenetre, text="Note :").grid(row=3, column=0, padx=10, pady=5)

entree1 = Entry(fenetre)
entree2 = Entry(fenetre)
entree3 = Entry(fenetre)
entree4 = Entry(fenetre)

entree1.grid(row=0, column=1, padx=10, pady=5)
entree2.grid(row=1, column=1, padx=10, pady=5)
entree3.grid(row=2, column=1, padx=10, pady=5)
entree4.grid(row=3, column=1, padx=10, pady=5)

Button(fenetre, text="Ajouter", command=ajouter_note).grid(row=4, column=0, columnspan=2, pady=10)
Button(fenetre, text="Effacer", command=vider).grid(row=4, column=1, padx=10, pady=10)

message_label = Label(fenetre, text="")
message_label.grid(row=5, column=0, columnspan=2)

Button(fenetre, text="Afficher -> BD", command=afficher_bd).grid(row=6, column=0, padx=10, pady=10)
Button(fenetre, text="Afficher -> XML", command=afficher_xml).grid(row=6, column=1, padx=10, pady=10)


fenetre.mainloop()