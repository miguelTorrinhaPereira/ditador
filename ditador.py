from string import punctuation
from time import sleep
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# abre o browser vai para o google tradutor
options = Options()
options.add_experimental_option('detach',True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get('https://www.bing.com/translator')
driver.maximize_window()
driver.find_element('xpath','/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[2]/div[1]/div[1]/div').click()
# encontrar os botões
text_box = driver.find_element('xpath', '/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[1]/div[1]/div[3]/div/textarea')
read_button = driver.find_element('xpath','/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[1]/div[1]/div[4]/div/div[1]/div/div')
clear_button = driver.find_element('xpath','/html/body/main/div/div[1]/div[1]/div/table/tbody/tr/td[1]/div[1]/div[3]/div/div[1]/div/div')

# funções para mexer no google tradutor
def por_p(palavra):text_box.send_keys(palavra)
def le_p():read_button.click()
def le_p_event(event):le_p()
def limpa_p():clear_button.click()

# abre a janela do tkinter
janela = tk.Tk()
janela.title('o ditador')
janela.geometry(f'{janela.winfo_screenwidth()}x{janela.winfo_screenheight()}')
janela.config(bg='black')
janela.state('zoomed')
# criar o texto que mostra a quantidade de tentativas
pontuação_palavra_texto = tk.Label(janela, bg='black', fg='white', font=('Arial', 40), text='10')
pontuação_palavra_texto.place(x = 490, y = 200)
# cria o texto que mostra a pontuação
pontuação_texto = tk.Label(janela,bg='black',fg='white',font=('Arial',40),text='0')
pontuação_texto.place(x = janela.winfo_screenwidth()-510, y = 200)
# cria o texto
texto = tk.Label(janela,bg='black',fg='white',font=('Arial',80))
texto.pack(pady=(320,0))
# cria o texto que mostra a palavra correta
correção = tk.Label(janela,bg='black',fg='white',font=('Arial',60))
correção.pack(pady=(80,0))
# cria a entrada de input , .focus_set faz com que o input seja direcionado para a entrada de texto
entrada = tk.Entry(bg='black',bd=0)
entrada.focus_set()
entrada.place(x=janela.winfo_screenwidth(),y=janela.winfo_screenheight())

a_corrigir = False
ditado = '''Era uma vez um pequeno vilarejo escondido nas montanhas'''
ditado = ditado.lower()
for i in punctuation:
    ditado = ditado.replace(i,' ')
palavras = ditado.split()
ditado = [i for i in ditado if i != '']
print(palavras)
index_palavra = 0
palavra = palavras[index_palavra]
pontuação = 0
pontuação_palavra = 10
texto_atual = ''
por_p(palavra)
sleep(1.5)
le_p()

# atualiza o texto mostrado
def atualiza_texto(event):
    global texto_atual
    texto_atual = entrada.get()
    texto.config(text=texto_atual)

def corrigir():
    global a_corrigir
    a_corrigir = True
    correção.config(text=palavra)
    pontuação_palavra_texto.config(text=pontuação_palavra)

def muda_palavra():
    global pontuação,pontuação_palavra,palavras,palavra,index_palavra,a_corrigir

    if index_palavra == len(palavras) - 1:
        janela.unbind('<Key>')
        janela.unbind('<Return>')
        janela.unbind('<Control_L>')
        pontuação_texto.config(text='')
        pontuação_palavra_texto.config(text='')
        texto.config(text='acabaste!')
        correção.config(text=f'pmpp={round(pontuação/len(palavras),1)}')
        janela.focus_set()
        return

    if a_corrigir:
        correção.config(text='')
        a_corrigir = False

    texto.config(text='')
    entrada.delete(first=0,last=len(texto_atual))

    pontuação += pontuação_palavra
    pontuação_palavra = 10

    pontuação_texto.config(text=pontuação)
    pontuação_palavra_texto.config(text=pontuação_palavra)

    index_palavra += 1
    palavra = palavras[index_palavra]

    limpa_p()
    por_p(palavra)
    sleep(0.6  + len(palavra)/50)
    le_p()

def submeter_palavra(event):
    global pontuação_palavra
    if texto_atual == palavra or a_corrigir: muda_palavra()
    elif pontuação_palavra == 10:
        pontuação_palavra -= 5
        pontuação_palavra_texto.config(text=pontuação_palavra)
    elif pontuação_palavra == 5:
        pontuação_palavra -= 3
        pontuação_palavra_texto.config(text=pontuação_palavra)
    else:
        pontuação_palavra = 0
        corrigir()


# faz com que os comandos do teclado funcionem
janela.bind('<Key>',atualiza_texto)
janela.bind('<Return>',submeter_palavra)
janela.bind('<Control_L>',le_p_event)

# inpede a janela de se fechar
janela.mainloop()