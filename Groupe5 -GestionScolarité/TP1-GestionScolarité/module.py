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

def ajouter_module():
    module_id = entree1.get()
    num_apogee = entree2.get()
    matricule = entree3.get()
    nom = entree4.get()  

    # Base de données
    connexion = sqlite3.connect("Gscolarite.db")
    curseur = connexion.cursor()
    curseur.executescript("""  
        CREATE TABLE IF NOT EXISTS Module (
            module_id INTEGER PRIMARY KEY,
            etudiant_num_apogee INTEGER,
            prof_matricule INTEGER,
            nom TEXT, 
            FOREIGN KEY (etudiant_num_apogee) REFERENCES Etudiant(num_apogee),
            FOREIGN KEY (prof_matricule) REFERENCES Professeur(matricule)
        );
    """)
    curseur.execute(
        "INSERT INTO Module (module_id, etudiant_num_apogee, prof_matricule, nom) VALUES (?, ?, ?, ?)",  
        (module_id, num_apogee, matricule, nom),
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

    module_elem = etree.SubElement(root, "Module")
    etree.SubElement(module_elem, "ModuleId").text = module_id
    etree.SubElement(module_elem, "EtudiantNumApogee").text = num_apogee
    etree.SubElement(module_elem, "ProfMatricule").text = matricule
    etree.SubElement(module_elem, "Nom").text = nom 

    tree.write("Gscolarite.xml", pretty_print=True)

    message_label.config(text="Module ajouté avec succès.")

# Modifier un module
def modifier_module():
    def chercher_module():
        module_id = entree_id_module.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Module WHERE module_id = ?", (module_id,))
        module = curseur.fetchone()
        connexion.close()

        if module:
            fenetre_modifier.destroy()
            afficher_fenetre_modification(module)
        else:
            message_label_modif.config(text="Module non trouvé.", fg="red")

    def afficher_fenetre_modification(module):
        def appliquer_modifications():
            new_etudiant_num_apogee = entree_etudiant_num_apogee.get()  # Numéro d'apogée de l'étudiant
            new_prof_matricule = entree_prof_matricule.get()  # Matricule du professeur
            new_nom = entree_nom.get()  # Nom du module

            # Mise à jour BD
            connexion = sqlite3.connect("Gscolarite.db")
            curseur = connexion.cursor()
            curseur.execute(
                """
                UPDATE Module
                SET etudiant_num_apogee = ?, prof_matricule = ?, nom = ?
                WHERE module_id = ?
                """,
                (new_etudiant_num_apogee, new_prof_matricule, new_nom, module[0]),
            )
            connexion.commit()
            connexion.close()

            # Mise à jour XML
            try:
                tree = etree.parse("Gscolarite.xml")
                root = tree.getroot()
                for elem in root.findall("Module"):
                    if elem.find("ModuleId").text == str(module[0]):
                        elem.find("EtudiantNumApogee").text = str(new_etudiant_num_apogee)
                        elem.find("ProfMatricule").text = str(new_prof_matricule)
                        elem.find("Nom").text = new_nom
                        break
                tree.write("Gscolarite.xml", pretty_print=True)
            except Exception as e:
                print(f"Erreur XML: {e}")

            message_label_modif_success.config(text="Modification réussie.", fg="green")

        fenetre_modification = Toplevel()
        fenetre_modification.title("Modifier un module")
        icon_path = r"Icons\iconUni.png"
        icon = tk.PhotoImage(file=icon_path)
        fenetre_modification.iconphoto(False, icon)

        # Champs pour le nom
        Label(fenetre_modification, text="Nom :").grid(row=1, column=0, padx=10, pady=5)
        entree_nom = Entry(fenetre_modification)
        entree_nom.insert(0, module[3])  # Insérer le nom actuel
        entree_nom.grid(row=1, column=1, padx=10, pady=5)

        # Champs pour le numéro d'apogée de l'étudiant
        Label(fenetre_modification, text="Numéro d'apogée de l'étudiant :").grid(row=2, column=0, padx=10, pady=5)
        entree_etudiant_num_apogee = Entry(fenetre_modification)
        entree_etudiant_num_apogee.insert(0, module[1])  # Insérer le numéro d'apogée actuel
        entree_etudiant_num_apogee.grid(row=2, column=1, padx=10, pady=5)

        # Champs pour le matricule du professeur
        Label(fenetre_modification, text="Matricule du professeur :").grid(row=3, column=0, padx=10, pady=5)
        entree_prof_matricule = Entry(fenetre_modification)
        entree_prof_matricule.insert(0, module[2])  # Insérer le matricule actuel
        entree_prof_matricule.grid(row=3, column=1, padx=10, pady=5)

        Button(fenetre_modification, text="Appliquer", command=appliquer_modifications).grid(row=4, column=0, columnspan=2, pady=10)
        message_label_modif_success = Label(fenetre_modification, text="")
        message_label_modif_success.grid(row=5, column=0, columnspan=2)

    fenetre_modifier = Toplevel()
    fenetre_modifier.title("Modifier un module")
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_modifier.iconphoto(False, icon)
    Label(fenetre_modifier, text="ID du module :").grid(row=0, column=0, padx=10, pady=5)
    entree_id_module = Entry(fenetre_modifier)
    entree_id_module.grid(row=0, column=1, padx=10, pady=5)
    Button(fenetre_modifier, text="Rechercher", command=chercher_module).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_modif = Label(fenetre_modifier, text="")
    message_label_modif.grid(row=2, column=0, columnspan=2)

# Supprimer un module
def supprimer_module():
    def effectuer_suppression():
        module_id = entree_id_module.get()

        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("DELETE FROM Module WHERE module_id = ?", (module_id,))
        if curseur.rowcount == 0:
            message_label_suppr.config(text="Module non trouvé.", fg="red")
        else:
            connexion.commit()
            # Supprimer dans XML
            try:
                tree = etree.parse("Gscolarite.xml")
                root = tree.getroot()
                for elem in root.findall("Module"):
                    if elem.find("ModuleId").text == module_id:
                        root.remove(elem)
                        break
                tree.write("Gscolarite.xml", pretty_print=True)
            except Exception as e:
                print(f"Erreur XML: {e}")
            message_label_suppr.config(text="Module supprimé avec succès.", fg="green")
        connexion.close()

    fenetre_supprimer = Toplevel()
    icon_path = r"Icons\iconUni.png"
    icon = tk.PhotoImage(file=icon_path)
    fenetre_supprimer.iconphoto(False, icon)
    fenetre_supprimer.title("Supprimer un module")
    Label(fenetre_supprimer, text="ID du module :").grid(row=0, column=0, padx=10, pady=5)
    entree_id_module = Entry(fenetre_supprimer)
    entree_id_module.grid(row=0, column=1, padx=10, pady=5)
    Button(fenetre_supprimer, text="Supprimer", command=effectuer_suppression).grid(row=1, column=0, columnspan=2, pady=10)
    message_label_suppr = Label(fenetre_supprimer, text="")
    message_label_suppr.grid(row=2, column=0, columnspan=2)

def afficher_bd_modules():
    try:
        connexion = sqlite3.connect("Gscolarite.db")
        curseur = connexion.cursor()
        curseur.execute("SELECT * FROM Module")
        rows = curseur.fetchall()
        connexion.close()

        window = tk.Toplevel()
        icon_path = r"Icons\iconUni.png"
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(False, icon)
        treeview = ttk.Treeview(window, columns=("ID", "EtudiantNumApogee", "ProfMatricule", "Nom"), show="headings")
        treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        treeview.heading("ID", text="ID")
        treeview.heading("EtudiantNumApogee", text="NumApogee Étudiant")
        treeview.heading("ProfMatricule", text="Matricule Professeur")
        treeview.heading("Nom", text="Nom Module")

        for row in rows:
            treeview.insert("", "end", values=row)
    except sqlite3.Error as e:
        print(f"Erreur lors de la lecture de la base de données: {e}")

def afficher_xml_modules():
    try:
        tree = etree.parse("Gscolarite.xml")
        root = tree.getroot()

        window = tk.Toplevel()
        icon_path = r"Icons\iconUni.png"
        icon = tk.PhotoImage(file=icon_path)
        window.iconphoto(False, icon)
        treeview = ttk.Treeview(window, columns=("ID", "EtudiantNumApogee", "ProfMatricule", "Nom"), show="headings")
        treeview.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        treeview.heading("ID", text="ID")
        treeview.heading("EtudiantNumApogee", text="NumApogee Étudiant")
        treeview.heading("ProfMatricule", text="Matricule Professeur")
        treeview.heading("Nom", text="Nom Module")

        for module in root.findall("Module"):
            # Utilisation de "ModuleId" au lieu de "Id"
            id_module = module.find("ModuleId").text
            etudiant_num_apogee = module.find("EtudiantNumApogee").text
            prof_matricule = module.find("ProfMatricule").text
            nom = module.find("Nom").text
            treeview.insert("", "end", values=(id_module, etudiant_num_apogee, prof_matricule, nom))
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier XML: {e}")


# Interface principale
fenetre = Tk()
fenetre.title("Gestion des Modules")
icon_path = r"Icons\iconUni.png"
icon = tk.PhotoImage(file=icon_path)
fenetre.iconphoto(False, icon)
fenetre.geometry("400x350")
fenetre.resizable(False, False)

menu1 = Menu(fenetre)
menu1.add_cascade(label="Ajouter", command=None)
menu1.add_cascade(label="Modifier", command=modifier_module)
menu1.add_cascade(label="Supprimer", command=supprimer_module)
fenetre.config(menu=menu1)

Label(fenetre, text="ID du module :").grid(row=0, column=0, padx=10, pady=5)
entree1 = Entry(fenetre)
entree1.grid(row=0, column=1, padx=10, pady=5)

Label(fenetre, text="Numéro Apogée :").grid(row=1, column=0, padx=10, pady=5)
entree2 = Entry(fenetre)
entree2.grid(row=1, column=1, padx=10, pady=5)

Label(fenetre, text="Matricule du Professeur :").grid(row=2, column=0, padx=10, pady=5)
entree3 = Entry(fenetre)
entree3.grid(row=2, column=1, padx=10, pady=5)

Label(fenetre, text="Nom du module :").grid(row=3, column=0, padx=10, pady=5)
entree4 = Entry(fenetre)
entree4.grid(row=3, column=1, padx=10, pady=5)

Button(fenetre, text="Ajouter Module", command=ajouter_module).grid(row=4, column=0, columnspan=2, pady=10)
Button(fenetre, text="Effacer", command=vider).grid(row=4, column=1, padx=10, pady=10)
message_label = Label(fenetre, text="")
message_label.grid(row=5, column=0, columnspan=2)

Button(fenetre, text="Afficher Modules -> BD", command=afficher_bd_modules).grid(row=8, column=0, padx=10, pady=10)
Button(fenetre, text="Afficher Modules -> XML", command=afficher_xml_modules).grid(row=8, column=1, padx=10, pady=10)

fenetre.mainloop()
