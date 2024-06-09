import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
from PIL import Image, ImageDraw

# Fungsi untuk algoritma DDA
def dda_line(x1, y1, x2, y2):
    points = []
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    x_increment = dx / steps
    y_increment = dy / steps
    x = x1
    y = y1
    for i in range(steps + 1):
        points.append((round(x), round(y)))
        x += x_increment
        y += y_increment
    return points

# Fungsi untuk algoritma midpoint circle
def midpoint_circle(x0, y0, radius):
    points = []
    x = radius
    y = 0
    p = 1 - radius

    while x >= y:
        points.append((x0 + x, y0 + y))
        points.append((x0 + y, y0 + x))
        points.append((x0 - y, y0 + x))
        points.append((x0 - x, y0 + y))
        points.append((x0 - x, y0 - y))
        points.append((x0 - y, y0 - x))
        points.append((x0 + y, y0 - x))
        points.append((x0 + x, y0 - y))
        y += 1
        if p <= 0:
            p = p + 2 * y + 1
        else:
            x -= 1
            p = p + 2 * y - 2 * x + 1
    return points

# Fungsi untuk algoritma midpoint ellipse
def midpoint_ellipse(rx, ry, xc, yc):
    points = []
    x = 0
    y = ry
    p1 = ry**2 - rx**2 * ry + 0.25 * rx**2
    while 2 * ry**2 * x <= 2 * rx**2 * y:
        points.append((xc + x, yc + y))
        points.append((xc - x, yc + y))
        points.append((xc + x, yc - y))
        points.append((xc - x, yc - y))
        if p1 < 0:
            x += 1
            p1 = p1 + 2 * ry**2 * x + ry**2
        else:
            x += 1
            y -= 1
            p1 = p1 + 2 * ry**2 * x - 2 * rx**2 * y + ry**2

    p2 = ry**2 * (x + 0.5)**2 + rx**2 * (y - 1)**2 - rx**2 * ry**2
    while y >= 0:
        points.append((xc + x, yc + y))
        points.append((xc - x, yc + y))
        points.append((xc + x, yc - y))
        points.append((xc - x, yc - y))
        if p2 > 0:
            y -= 1
            p2 = p2 - 2 * rx**2 * y + rx**2
        else:
            y -= 1
            x += 1
            p2 = p2 + 2 * ry**2 * x - 2 * rx**2 * y + rx**2
    return points

# Fungsi untuk algoritma boundary-fill
def boundary_fill(x, y, fill_color, boundary_color):
    current_color = canvas.gettags(canvas.find_closest(x, y))
    if current_color != boundary_color and current_color != fill_color:
        canvas.create_oval(x, y, x+1, y+1, outline=fill_color, fill=fill_color, tags=fill_color)
        boundary_fill(x + 1, y, fill_color, boundary_color)
        boundary_fill(x - 1, y, fill_color, boundary_color)
        boundary_fill(x, y + 1, fill_color, boundary_color)
        boundary_fill(x, y - 1, fill_color, boundary_color)

# Fungsi untuk menyimpan gambar
def save_image():
    file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
    if file_path:
        canvas.postscript(file="temp.ps", colormode='color')
        img = Image.open("temp.ps")
        img.save(file_path)

# Fungsi untuk menggambar lingkaran
def draw_circle(event):
    x, y = event.x, event.y
    radius = int(radius_entry.get())
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline=color, width=thickness)

# Fungsi untuk menggambar elips
def draw_ellipse(event):
    x, y = event.x, event.y
    rx = int(radius_entry.get())
    ry = int(radius_entry.get()) // 2
    canvas.create_oval(x - rx, y - ry, x + rx, y + ry, outline=color, width=thickness)

# Fungsi untuk menggambar garis saat drag
def start_line(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

def draw_line(event):
    global start_x, start_y
    points = dda_line(start_x, start_y, event.x, event.y)
    for point in points:
        canvas.create_oval(point[0], point[1], point[0] + thickness, point[1] + thickness, fill=color)
    start_x, start_y = event.x, event.y

# Fungsi untuk boundary fill
def fill(event):
    x, y = event.x, event.y
    boundary_fill(x, y, color, boundary_color)

# Fungsi untuk mengubah warna
def change_color():
    global color
    color = colorchooser.askcolor()[1]

# Fungsi untuk mengubah ketebalan
def change_thickness(value):
    global thickness
    thickness = int(value)

# Fungsi untuk menghapus canvas
def clear_canvas():
    canvas.delete("all")

# Fungsi untuk mengubah mode gambar
def set_mode(new_mode):
    global mode
    mode = new_mode
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")
    if mode == "circle":
        canvas.bind("<Button-1>", draw_circle)
    elif mode == "line":
        canvas.bind("<Button-1>", start_line)
        canvas.bind("<B1-Motion>", draw_line)
    elif mode == "ellipse":
        canvas.bind("<Button-1>", draw_ellipse)

# Inisialisasi Tkinter
root = tk.Tk()
root.title("Simple Paint Program")

# Frame untuk kontrol
control_frame = tk.Frame(root)
control_frame.pack(side=tk.TOP, fill=tk.X)

# Tombol untuk mengganti warna
color_button = tk.Button(control_frame, text="Choose Color", command=change_color)
color_button.pack(side=tk.LEFT)

# Entry untuk radius lingkaran dan elips
radius_entry = tk.Entry(control_frame)
radius_entry.pack(side=tk.LEFT)
radius_entry.insert(0, "50")

# Slider untuk ketebalan garis
thickness_slider = tk.Scale(control_frame, from_=1, to_=10, orient=tk.HORIZONTAL, label="Thickness", command=change_thickness)
thickness_slider.pack(side=tk.LEFT)

# Tombol untuk membersihkan canvas
clear_button = tk.Button(control_frame, text="Clear", command=clear_canvas)
clear_button.pack(side=tk.LEFT)

# Tombol untuk menyimpan gambar
save_button = tk.Button(control_frame, text="Save", command=save_image)
save_button.pack(side=tk.LEFT)

# Tombol untuk memilih mode gambar
circle_button = tk.Button(control_frame, text="Draw Circle", command=lambda: set_mode("circle"))
circle_button.pack(side=tk.LEFT)

line_button = tk.Button(control_frame, text="Draw Line", command=lambda: set_mode("line"))
line_button.pack(side=tk.LEFT)

ellipse_button = tk.Button(control_frame, text="Draw Ellipse", command=lambda: set_mode("ellipse"))
ellipse_button.pack(side=tk.LEFT)

# Canvas untuk menggambar
canvas = tk.Canvas(root, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Variabel global
color = "black"
boundary_color = "black"
thickness = 1
mode = "circle"  # Default mode

# Mengatur mode default
set_mode(mode)

# Menjalankan Tkinter
root.mainloop()
