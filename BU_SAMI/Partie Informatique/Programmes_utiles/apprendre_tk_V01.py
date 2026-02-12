import tkinter as tk


fen = tk.Tk()
bg_choisi = "#B7FFFF"
fen["background"] = bg_choisi
# fen.configure(bg = "yellow") # ou config  bg ou back...
fen.geometry("600x400") # taille de la fenetre
fen.title("Titre de la fenetre")

# Placer label dans la fenetre
label_title = tk.Label(fen, text = "Samijotte", bg = bg_choisi, fg = "#080087") # fg = "#080087" couleur de l'ecriture
label_title["font"] = ("Bauhaus 93", 25)

label_title.pack()

## Etat
frame_etat = tk.Frame(fen, highlightthickness  = 0)
frame_etat["width"]  = 30*4
frame_etat["height"] = 30
frame_etat["bg"] = "magenta"
frame_etat.pack()

canvas_cercle = tk.Canvas(master = frame_etat, width = 30, height = 30) # 40 de base
canvas_cercle["highlightthickness"] = 0
canvas_cercle["bg"] = bg_choisi

canvas_cercle.pack(side = "left", ipadx = 5)

# Coordonnées pour le cercle
# x_center, y_center = 22,12  # Centre du cercle
# radius = 8  # Rayon du cercle
x_center, y_center = 15,15  # Centre du cercle
radius = 10  # Rayon du cercle
cercle = canvas_cercle.create_oval(
    x_center - radius, y_center - radius,  # x0, y0
    x_center + radius, y_center + radius,  # x1, y1
    fill="red"
)
# canvas.itemconfig(circle_id, fill="red")

# change_color = tk.Button(fen)
# change_color.pack()

def etat():
    print("Chnagement d'état et de couleur")
    if button_etat["text"] == "A l'arret":
        button_etat["text"] = "En marche"
        canvas_cercle.itemconfig(cercle, fill="green")

    else:
        button_etat["text"] = "A l'arret"
        canvas_cercle.itemconfig(cercle, fill="red")


button_etat = tk.Button(master = frame_etat, command = etat)
button_etat["text"] = "A l'arret"
button_etat["fg"] = "#080087"
button_etat.pack(side = "right", ipadx = 5)


menu_frame = tk.Frame(fen)
menu_frame.pack(side = "bottom")



def exit_function():
    print("Ferme la fenetre")
    fen.destroy()

button_exit = tk.Button(fen, command = exit_function)
button_exit["text"] = "Exit"
button_exit["bg"] = "red"
# button_exit.place(relx = 0.95, rely = 0.005)
# button_exit.grid(padx = 5)

fen.mainloop()






