## Position du robot
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

def main():
    bg_choisi, fg_choisi = "#B7FFFF", "#080087"
    fen = tk.Tk()
    fen.title("Interface robot")
    fen["background"] = bg_choisi
    fen.geometry("1400x700") # taille de la fenetre
    fen.title("Titre de la fenetre")

    style = ttk.Style()
    style.theme_use("xpnative")
    style.configure("Custom.TLabel", background = bg_choisi, fg = fg_choisi)
    style.configure("Custom.TButton", background = bg_choisi, fg = fg_choisi)
    # style.configure("Custom.TButton1", background = bg_choisi, foreground  = "purple")
    style.configure("C.TButton", bg = "red", fg = "green")

    style.configure("Custom.TFrame", background = bg_choisi, fg = fg_choisi)

    frame_left = ttk.Frame(fen, width = 700, style = "Custom.TFrame")
    # frame_left = tk.Frame(fen, bg = "orange", width = 600)
    frame_right = ttk.Frame(fen, style = "Custom.TFrame")
    frame_left.pack(side = "left", fill = "both")
    frame_right.pack(side = "right", fill = "both", expand = True)
    frame_left.pack_propagate(False)

    # Placer label dans la fenetre
    label_title = ttk.Label(frame_left, text = "Samijote", style = "Custom.TLabel") # fg = "#080087" couleur de l'ecriture
    label_title["font"] = ("Bauhaus 93", 25)
    label_title.pack(side = "top")

    def create_map(root, image_path, positions):
        # Charger l'image de fond
        img = Image.open(image_path)
        photo = ImageTk.PhotoImage(img)
        root.photo = photo  # Conservation d'une référence à l'image
        # Créer un canvas tkinter et ajouter l'image de fond
        canvas = tk.Canvas(root, width = img.width, height = img.height, bg = bg_choisi)
        canvas.pack(side = "bottom")
        canvas.create_image(0, 0, image = photo, anchor = 'nw')

        # Marquer chaque position sur l'image
        for pos in positions:
            x, y = pos
            canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill = 'red')

    label_map = tk.Label(frame_right, text = "Position du robot sur la carte")
    # label_map = tk.Label(frame_right, bg = "orange", text = "Position du robot sur la carte")
    label_map["font"] = 25
    label_map["bg"] = bg_choisi
    label_map.pack(fill = tk.X, expand = True, side = "top")

    # Emplacement de l'image de fond
    image_path = "Map.png"
    positions = [(100, 150), (200, 300), (350, 120)]
    create_map(frame_right, image_path, positions)


    ## Etat
    frame_etat = ttk.Frame(frame_left, style = "Custom.TFrame")
    frame_etat["width"]  = 30*4
    frame_etat["height"] = 30
    # frame_etat["bg"] = "magenta"

    canvas_cercle = tk.Canvas(master = frame_etat, width = 30, height = 30) # 40 de base
    canvas_cercle["highlightthickness"] = 0
    canvas_cercle["bg"] = bg_choisi
    frame_etat.pack()
    canvas_cercle.pack(side = "left", ipadx = 5)

    # Coordonnées pour le cercle
    x_center, y_center, radius = 15,15,10  # Centre du cercle, Rayon du cercle
    cercle = canvas_cercle.create_oval(
        x_center - radius, y_center - radius,  # x0, y0
        x_center + radius, y_center + radius,  # x1, y1
        fill = "red"
    )
    # canvas.itemconfig(circle_id, fill = "red")
    # change_color = tk.Button(fen)
    # change_color.pack()

    def change_light():
        print("Chnagement d'état et de couleur")
        if button_light["text"] == "A l'arret":
            button_light["text"] = "En marche"
            canvas_cercle.itemconfig(cercle, fill = "green")
        else:
            button_light["text"] = "A l'arret"
            canvas_cercle.itemconfig(cercle, fill = "red")


    # button_light = ttk.Button(master = frame_etat, style = "Custom.TButton", command = change_light)
    button_light = ttk.Button(master = frame_etat, style = "C.TButton", command = change_light)
    button_light["text"] = "A l'arret"
    button_light.pack(side = "right", ipadx = 5)

    menu_frame = ttk.Frame(frame_left, style = "Custom.TFrame")
    menu_frame.pack(side = "bottom")

    def transform_to_label():
        changer_button.pack_forget()
        new_text = ttk.Label(frame_left, text = "Ceci était un bouton", style = "Custom.TLabel")
        new_text.pack()

    changer_button = ttk.Button(frame_left, text = "Boutton qui se change en texte", style = "Custom.TButton", command = transform_to_label)
    changer_button.pack()

    def exit_function():
        print("Fermeture de la fenêtre")
        fen.destroy()

    button_exit = ttk.Button(frame_left, command = exit_function)
    button_exit["style"] = "C.TButton"
    button_exit["text"] = "Exit"
    button_exit.pack(side = "bottom")
    # button_exit["bg"] = "red"
    # button_exit.place(relx = 0.95, rely = 0.005)
    # button_exit.grid(padx = 5)

    fen.mainloop()


if __name__ == "__main__":
    main()




