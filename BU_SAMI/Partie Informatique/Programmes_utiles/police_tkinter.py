import tkinter as tk
import tkinter.font as font

root = tk.Tk()  # Créer la fenêtre principale

# Récupérer et afficher les familles de polices disponibles
available_fonts = font.families()
L_police = []
for family in available_fonts:
    # print(family)
    L_police.append(family)
root.mainloop()
