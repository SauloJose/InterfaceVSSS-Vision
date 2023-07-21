import tkinter as tk

def exibir_janela():
    if state.get() == 'aberta':
        # Janela quando o estado é 'aberta'
        window_aberta = tk.Toplevel(root)
        window_aberta.title("Janela Aberta")
        label = tk.Label(window_aberta, text="Janela Aberta")
        label.pack()
    elif state.get() == 'fechada':
        # Janela quando o estado é 'fechada'
        window_fechada = tk.Toplevel(root)
        window_fechada.title("Janela Fechada")
        label = tk.Label(window_fechada, text="Janela Fechada")
        label.pack()

root = tk.Tk()

# Crie a variável state e defina um valor inicial
state = tk.StringVar()
state.set('aberta')

# Botões para alterar o estado
button_abrir = tk.Button(root, text="Abrir Janela", command=lambda: state.set('aberta'))
button_abrir.pack()

button_fechar = tk.Button(root, text="Fechar Janela", command=lambda: state.set('fechada'))
button_fechar.pack()

# Vincule a função exibir_janela() à variável state
state.trace("w", lambda *args: exibir_janela())

root.mainloop()
