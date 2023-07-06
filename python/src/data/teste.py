import tkinter as tk
from tkinter import ttk
import colorsys


def update_color(event=None):
    # Obter os valores HSV dos trakebars
    h = int(h_scale.get())
    s = int(s_scale.get())
    v = int(v_scale.get())

    # Converter de 0-360 para 0-179 (padrão do OpenCV)
    h = int(h * 179 / 360)

    # Converter de HSV para RGB
    r, g, b = colorsys.hsv_to_rgb(h / 179, s / 255, v / 255)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    # Atualizar a cor exibida na janela
    color_frame.config(bg='#{:02x}{:02x}{:02x}'.format(r, g, b))

    # Atualizar os valores exibidos
    h_value.config(text=str(h))
    s_value.config(text=str(s))
    v_value.config(text=str(v))

# Criar a janela
window = tk.Tk()
window.title("Seleção de Cor HSV")
window.geometry("300x250")

# Criar estilo para os trakebars
style = ttk.Style()

# Estilizar o widget "Horizontal.TScale"
style.configure("Horizontal.TScale",
                sliderlength=20,
                troughcolor="#E0E0E0",
                slidercolor="#2196F3",
                bordercolor="#E0E0E0",
                gripcount=0,
                gripcolor="",
                troughrelief="flat")

# Estilizar o widget "TLabel"
style.configure("TLabel", background="#E0E0E0")

# Criar as trakebars para H, S e V
h_label = ttk.Label(window, text="H", style="TLabel")
h_label.pack()

h_scale_frame = ttk.Frame(window)
h_scale_frame.pack()
h_scale = ttk.Scale(h_scale_frame, from_=0, to=360, orient=tk.HORIZONTAL, command=update_color, style="Horizontal.TScale")
h_scale.set(0)
h_scale.pack(side=tk.LEFT)
h_value = ttk.Label(h_scale_frame, text="0", style="TLabel")
h_value.pack(side=tk.LEFT, padx=5)

s_label = ttk.Label(window, text="S", style="TLabel")
s_label.pack()

s_scale_frame = ttk.Frame(window)
s_scale_frame.pack()
s_scale = ttk.Scale(s_scale_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=update_color, style="Horizontal.TScale")
s_scale.set(0)
s_scale.pack(side=tk.LEFT)
s_value = ttk.Label(s_scale_frame, text="0", style="TLabel")
s_value.pack(side=tk.LEFT, padx=5)

v_label = ttk.Label(window, text="V", style="TLabel")
v_label.pack()

v_scale_frame = ttk.Frame(window)
v_scale_frame.pack()
v_scale = ttk.Scale(v_scale_frame, from_=0, to=255, orient=tk.HORIZONTAL, command=update_color, style="Horizontal.TScale")
v_scale.set(0)
v_scale.pack(side=tk.LEFT)
v_value = ttk.Label(v_scale_frame, text="0", style="TLabel")
v_value.pack(side=tk.LEFT, padx=5)

# Criar o quadro para exibir a cor selecionada
color_frame = tk.Frame(window, width=100, height=100)
color_frame.pack(pady=10)

#


# Executar a janela
window.mainloop()
