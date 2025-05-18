import tkinter as tk
from tkinter import simpledialog, messagebox
from threading import Thread
from recursos.funcoes import inicializarBancoDeDados, escreverDados
import speech_recognition as sr

inicializarBancoDeDados()
listaIdeias = []
with open("base.json", "r") as banco:
    listaIdeias = banco.readlines()

def ouvir_com_janela():
    janela = tk.Toplevel()
    janela.title("Microfone Ativo")
    janela.geometry("200x200")
    canvas = tk.Canvas(janela, width=100, height=100)
    canvas.pack(pady=10)
    canvas.create_oval(10, 10, 90, 90, fill="red")
    texto_var = tk.StringVar()
    texto_var.set("Fale algo...")
    label = tk.Label(janela, textvariable=texto_var, font=("Arial", 14))
    label.pack(pady=10)

    def reconhecer():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            try:
                audio = recognizer.listen(source, timeout=5)
                texto_var.set("Reconhecendo...")
                texto = recognizer.recognize_google(audio, language="pt-BR")
                texto_var.set(texto)
                janela.after(1500, janela.destroy)
                return texto
            except Exception as e:
                texto_var.set("Não entendi. Tente novamente.")
                janela.after(1500, janela.destroy)
                return ""

    resultado = {"texto": ""}
    def thread_func():
        resultado["texto"] = reconhecer()
    t = Thread(target=thread_func)
    t.start()
    janela.grab_set()
    janela.wait_window()
    return resultado["texto"]

def cadastrar_ideia():
    ideia = ouvir_com_janela()
    if ideia and len(ideia) > 0:
        listaIdeias.append(ideia)
        escreverDados(listaIdeias)
        messagebox.showinfo("Sucesso", "Ideia cadastrada com sucesso!")
    else:
        messagebox.showwarning("Erro", "Ideia inválida!")

def listar_ideias():
    ideias = "".join(f"- {item}" for item in listaIdeias)
    messagebox.showinfo("Ideias", ideias if ideias else "Nenhuma ideia cadastrada.")

def excluir_ideia():
    if not listaIdeias:
        messagebox.showinfo("Excluir Ideia", "Nenhuma ideia cadastrada.")
        return
    ideias_com_id = "\n".join([f"{idx}: {item.strip()}" for idx, item in enumerate(listaIdeias)])
    id_str = simpledialog.askstring(
        "Excluir Ideia",
        f"Escolha o ID para excluir:\n\n{ideias_com_id}\n\nDigite o ID:"
    )
    try:
        idDeletar = int(id_str)
        del listaIdeias[idDeletar]
        escreverDados(listaIdeias)
        messagebox.showinfo("Sucesso", "Ideia excluída com sucesso!")
    except:
        messagebox.showerror("Erro", "ID inválido!")

root = tk.Tk()
root.title("Registro de Ideias")
root.geometry("500x100")

tk.Button(root, text="Cadastrar Ideia", command=cadastrar_ideia).pack(fill='x')
tk.Button(root, text="Listar Ideias", command=listar_ideias).pack(fill='x')
tk.Button(root, text="Excluir Ideia", command=excluir_ideia).pack(fill='x')
tk.Button(root, text="Sair", command=root.quit).pack(fill='x')

root.mainloop()