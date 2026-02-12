
import tkinter as tk
from PIL import Image, ImageTk

def create_map(root, image_path, positions):
    # Charger l'image de fond
    img = Image.open(image_path)
    photo = ImageTk.PhotoImage(img)
    root.photo = photo  # Conservation d'une référence à l'image
    # Créer un canvas tkinter et ajouter l'image de fond
    canvas = tk.Canvas(root, width=img.width, height=img.height)
    canvas.pack()
    canvas.create_image(0, 0, image=photo, anchor='nw')

    # Marquer chaque position sur l'image
    for pos in positions:
        x, y = pos
        canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='red')

    root.mainloop()

def main():
    # Créer la fenêtre principale
    root = tk.Tk()
    root.title("Carte")

    # Emplacement de l'image de fond
    image_path = 'GGADTkdX0AAdwJN.jpg'

    # Liste des positions à marquer (x, y)
    positions = [(100, 150), (200, 300), (350, 120)]

    # Création de la carte
    create_map(root, image_path, positions)

    # Démarrer la boucle principale de tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
