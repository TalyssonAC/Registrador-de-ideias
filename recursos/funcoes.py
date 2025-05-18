import os, time
import speech_recognition as controladorVoz
# inicializar o controlador de voz
recognizer = controladorVoz.Recognizer()

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("base.json","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.json","w")
    
def escreverDados(listaIdeias):
    banco = open("base.json","w")
    for item in listaIdeias:
        banco.write(item + "\n")
    banco.close()

def ouvir():
    
    with controladorVoz.Microphone() as source:
        print("Diga Algo...")
        print("Fique em silêncio para finalizar!")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            texto = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {texto}")
            return texto
        except controladorVoz.UnknownValueError:
            print("Não entendi o que você disse!")
            return ""
        except controladorVoz.RequestError:
            print("Erro ao conectar com o servidor!")
            return ""
    