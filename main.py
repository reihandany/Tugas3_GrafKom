import os
os.environ['TCL_LIBRARY'] = r'C:\Users\LOQ\AppData\Local\Programs\Python\Python313\tcl\tcl8.6'
import tkinter as tk
from tkinter import colorchooser, simpledialog
import math

class SimpleDraw:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple 2D Draw")

        self.canvas = tk.Canvas(root, bg='white', width=700, height=500)
        self.canvas.grid(row=0, column=0, rowspan=20)

        self.shape = tk.StringVar(value="point")
        self.color = "#000000"
        self.thickness = 2
        self.start = None
        self.objects = []

        # Tombol bentuk
        for i, s in enumerate(["point", "line", "rect", "ellipse"]):
            tk.Radiobutton(root, text=s.title(), variable=self.shape, value=s).grid(row=i, column=1, sticky="w")

        # Tombol warna, ketebalan, clear
        tk.Button(root, text="Warna", command=self.pick_color).grid(row=5, column=1, sticky="w")
        tk.Button(root, text="Ketebalan", command=self.set_thickness).grid(row=6, column=1, sticky="w")
        tk.Button(root, text="Clear", command=self.clear_canvas).grid(row=7, column=1, sticky="w")

        # Transformasi
        tk.Button(root, text="Translasi", command=self.translasi).grid(row=9, column=1, sticky="w")
        tk.Button(root, text="Rotasi", command=self.rotasi).grid(row=10, column=1, sticky="w")
        tk.Button(root, text="Scaling", command=self.scaling).grid(row=11, column=1, sticky="w")

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def pick_color(self):
        c = colorchooser.askcolor()[1]
        if c:
            self.color = c

    def set_thickness(self):
        t = simpledialog.askinteger("Ketebalan", "1-10:", minvalue=1, maxvalue=10)
        if t:
            self.thickness = t

    def on_click(self, e):
        self.start = (e.x, e.y)
        if self.shape.get() == "point":
            dot = self.canvas.create_oval(e.x, e.y, e.x+1, e.y+1, fill=self.color, outline=self.color, width=self.thickness)
            self.objects.append((dot, "point", [e.x, e.y], self.color, self.thickness))

    def on_release(self, e):
        sx, sy = self.start
        shape = self.shape.get()
        coords = [sx, sy, e.x, e.y]

        if shape == "line":
            obj = self.canvas.create_line(*coords, fill=self.color, width=self.thickness)
        elif shape == "rect":
            obj = self.canvas.create_rectangle(*coords, outline=self.color, width=self.thickness)
        elif shape == "ellipse":
            obj = self.canvas.create_oval(*coords, outline=self.color, width=self.thickness)
        else:
            return

        self.objects.append((obj, shape, coords, self.color, self.thickness))

    def clear_canvas(self):
        self.canvas.delete("all")
        self.objects.clear()

    def translasi(self):
        dx = simpledialog.askinteger("dx", "Geser X:")
        dy = simpledialog.askinteger("dy", "Geser Y:")
        if dx is None or dy is None: return

        for i, (obj, shape, coords, color, thick) in enumerate(self.objects):
            new_coords = [x + dx if i % 2 == 0 else x + dy for i, x in enumerate(coords)]
            self.canvas.delete(obj)
            new_obj = self.gambar_ulang(shape, new_coords, color, thick)
            self.objects[i] = (new_obj, shape, new_coords, color, thick)

    def rotasi(self):
        sudut = simpledialog.askfloat("Rotasi", "Derajat:")
        if sudut is None: return
        rad = math.radians(sudut)
        cx, cy = 350, 250

        for i, (obj, shape, coords, color, thick) in enumerate(self.objects):
            new = []
            for j in range(0, len(coords), 2):
                x, y = coords[j] - cx, coords[j+1] - cy
                xr = x * math.cos(rad) - y * math.sin(rad) + cx
                yr = x * math.sin(rad) + y * math.cos(rad) + cy
                new += [xr, yr]
            self.canvas.delete(obj)
            new_obj = self.gambar_ulang(shape, new, color, thick)
            self.objects[i] = (new_obj, shape, new, color, thick)

    def scaling(self):
        f = simpledialog.askfloat("Scaling", "Faktor:")
        if f is None: return
        cx, cy = 350, 250

        for i, (obj, shape, coords, color, thick) in enumerate(self.objects):
            new = []
            for j in range(0, len(coords), 2):
                x = cx + (coords[j] - cx) * f
                y = cy + (coords[j+1] - cy) * f
                new += [x, y]
            self.canvas.delete(obj)
            new_obj = self.gambar_ulang(shape, new, color, thick)
            self.objects[i] = (new_obj, shape, new, color, thick)

    def gambar_ulang(self, shape, coords, color, thick):
        if shape == "point":
            return self.canvas.create_oval(coords[0], coords[1], coords[0]+1, coords[1]+1, fill=color, outline=color, width=thick)
        elif shape == "line":
            return self.canvas.create_line(*coords, fill=color, width=thick)
        elif shape == "rect":
            return self.canvas.create_rectangle(*coords, outline=color, width=thick)
        elif shape == "ellipse":
            return self.canvas.create_oval(*coords, outline=color, width=thick)

# Jalankan aplikasi
root = tk.Tk()
app = SimpleDraw(root)
root.mainloop()
