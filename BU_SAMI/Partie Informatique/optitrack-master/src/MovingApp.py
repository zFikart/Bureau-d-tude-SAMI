import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation
import numpy as np

class MovingPointApp(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.master = master

        self.master.title("Position du robot")
        self.bg_choisi = "#B7FFFF"
        self.fg_choisi = "#080087"
        self.master.configure(background = self.bg_choisi)
        self.master.geometry("1200x700")  # Taille de la fenêtre

        # Liste des coordonnées pour animer le point
        self.coordinates = [(0, 0), (1, 2), (2, 3), (3, 5), (4, 7), (5, 8), (6, 6), (7, 4), (8, 3), (9, 1), (10, 0)]

        self.create_figure()

    def create_figure(self):
        # Configuration du frame pour le graphique
        self.frame_graph = ttk.Frame(self.master)
        self.frame_graph.pack(fill = tk.BOTH, expand = True)

        # Création de la figure et de l'axe
        self.fig = Figure(figsize = (8, 6), dpi = 100)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0, 10)
        self.ax.set_ylim(0, 10)
        self.point, = self.ax.plot([], [], 'ro') # BUG

        # Intégration de la figure dans Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master = self.frame_graph)
        self.canvas.draw() # equivalent de .pack()
        self.canvas.get_tk_widget().pack(fill = tk.BOTH, expand = True)

        self.ani = animation.FuncAnimation(self.fig, self.update_graph, frames = len(self.coordinates), interval = 1000, repeat = False)


    def update_graph(self, i):
        """Met à jour la position du point sur le graphique."""
        x, y = self.coordinates[i]
        self.point.set_data(x, y)
        self.ax.set_title(f"Position: ({x}, {y})")
        self.canvas.draw()

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovingPointApp(root)
    app.run()

    fig = Figure(figsize = (8, 6), dpi = 100)
    ax = fig.add_subplot(111)
    point, = ax.plot([], [], 'ro')
    ax.set
