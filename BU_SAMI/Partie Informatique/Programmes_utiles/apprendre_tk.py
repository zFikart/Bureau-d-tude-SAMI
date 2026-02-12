## Apprendre tk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def main():
    fen = tk.Tk()
    fen.title("Position du robot")
    style = tk.ttk.Style()
    style.theme_use("xpnative")
    style.configure("Custom.TFrame", background = "lightblue")

    def create_map(root, image_path, positions):
        # Charger l'image de fond
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        root.photo = photo  # Conservation d'une référence à l'image
        # Créer un canvas tkinter et ajouter l'image de fond
        canvas = tk.Canvas(root, width = img.width, height = img.height)
        canvas.pack()
        canvas.create_image(0, 0, image=photo, anchor='nw')

        # Marquer chaque position sur l'image
        for pos in positions:
            x, y = pos
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='red')



    frame_map = tk.Frame(fen)
    frame_map.pack(side = "right")

    # Emplacement de l'image de fond
    image_path = r'O:\Documents\S6\UE_BE_Bureau_detude\TP3_Interface-Graphique\Map.png'

    positions = [(100, 150), (200, 300), (350, 120)]
    create_map(frame_map, image_path, positions)

    bg_choisi = "#B7FFFF"
    fen["background"] = bg_choisi
    # fen.configure(bg = "yellow") # ou config  bg ou back...
    fen.geometry("600x400") # taille de la fenetre
    fen.title("Titre de la fenetre")

    # Placer label dans la fenetre
    # label_title = ttk.Label(fen, text = "Samijotte", bg = bg_choisi, fg = "#080087") # fg = "#080087" couleur de l'ecriture
    label_title = ttk.Label(fen, text = "Samijotte", ) # fg = "#080087" couleur de l'ecriture
    # label_title["fg"] = "#080087"
    style.configure("Custom.TFrame", fg = "#080087")

    label_title["font"] = ("Bauhaus 93", 25)

    label_title.pack()

    ## Etat

    frame_etat = tk.ttk.Frame(fen)
    frame_etat["width"]  = 30*4
    frame_etat["height"] = 30
    # frame_etat["bg"] = "magenta"
    frame_etat.pack()

    canvas_cercle = tk.Canvas(master = frame_etat, width = 30, height = 30) # 40 de base
    canvas_cercle["highlightthickness"] = 0
    # canvas_cercle["bg"] = bg_choisi

    canvas_cercle.pack(side = "left", ipadx = 5)

    # Coordonnées pour le cercle
    # x_center, y_center = 22,12  # Centre du cercle
    # radius = 8  # Rayon du cercle
    x_center, y_center, radius = 15,15, 10  # Centre du cercle, Rayon du cercle
    cercle = canvas_cercle.create_oval(
        x_center - radius, y_center - radius,  # x0, y0
        x_center + radius, y_center + radius,  # x1, y1
        fill = "red"
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


    button_etat = tk.ttk.Button(master = frame_etat, command = etat)
    button_etat["text"] = "A l'arret"
    # button_etat["fg"] = "#080087"
    button_etat.pack(side = "right", ipadx = 5)

    menu_frame = tk.ttk.Frame(fen)
    menu_frame.pack(side = "bottom")

    def transform_to_label():
        changer_button.pack_forget()
        new_text = tk.ttk.Label(frame_etat, text = "Ceci était un bouton")
        new_text.pack()

    changer_button = tk.ttk.Button(frame_etat, text = "Boutton qui se change en texte", command = transform_to_label)
    changer_button.pack()

    def exit_function():
        print("Ferme la fenetre")
        fen.destroy()

    button_exit = tk.ttk.Button(fen, command = exit_function)
    button_exit["text"] = "Exit"
    button_exit.pack()
    # button_exit["bg"] = "red"
    # button_exit.place(relx = 0.95, rely = 0.005)
    # button_exit.grid(padx = 5)

    fen.mainloop()



if __name__ == "__main__":
    main()




