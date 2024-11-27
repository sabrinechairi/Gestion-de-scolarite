import tkinter as tk
import subprocess
from PIL import Image, ImageTk

def ouvrir_etudiant():
    subprocess.Popen(["python", "etudiant.py"])

def ouvrir_prof():
    subprocess.Popen(["python", "prof.py"])

def ouvrir_module():
    subprocess.Popen(["python", "module.py"])   

def ouvrir_note():
    subprocess.Popen(["python", "note.py"])      

fenetre = tk.Tk()
icon_path = r"Icons\iconUni.png"
fenetre.title("Gestion - Accueil")
icon = tk.PhotoImage(file=icon_path)
fenetre.iconphoto(False, icon)
fenetre.geometry("700x500")
fenetre.resizable(False, False)

titre = tk.Label(fenetre, text="Bienvenue dans la gestion de scolarité", font=("Arial", 16))
titre.pack(pady=20)

image_path = r"Icons\GS.jpg"
image = Image.open(image_path)
image = image.resize((400, 400))
image = ImageTk.PhotoImage(image)

frame_main = tk.Frame(fenetre)
frame_main.pack(pady=10)

image_label = tk.Label(frame_main, image=image)
image_label.pack(side="left", padx=10)

frame_buttons = tk.Frame(frame_main)
frame_buttons.pack(side="left", padx=10)

btn_etudiant = tk.Button(frame_buttons, text="Gérer les Étudiants", font=("Arial", 12), command=ouvrir_etudiant)
btn_etudiant.pack(pady=10)

btn_prof = tk.Button(frame_buttons, text="Gérer les Professeurs", font=("Arial", 12), command=ouvrir_prof)
btn_prof.pack(pady=10)

btn_prof = tk.Button(frame_buttons, text="Gérer les Modules", font=("Arial", 12), command=ouvrir_module)
btn_prof.pack(pady=10)

btn_prof = tk.Button(frame_buttons, text="Gérer les Notes", font=("Arial", 12), command=ouvrir_note)
btn_prof.pack(pady=10)

fenetre.mainloop()
