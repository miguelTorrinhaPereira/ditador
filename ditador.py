from random import randint
from string import punctuation
from time import sleep
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# funções para mexer no google tradutor
def por_p(palavra):text_box.send_keys(palavra)
def le_p():read_button.click()
def limpa_p():clear_button.click()

# converte o texto a ditar para uma lista de palavras que podem ser usadas pelo programa
def cria_palavras(ditado,tamanho_palavras):
    ditado = ditado.lower()
    for i in punctuation:ditado = ditado.replace(i,' ')
    proto_palavras,palavras = [i for i in ditado.split() if i != ''], []
    for i in range(0,len(proto_palavras),tamanho_palavras):palavras += [' '.join(proto_palavras[i:i+tamanho_palavras])]
    j = len(proto_palavras)//tamanho_palavras*tamanho_palavras
    if j > 0 and j<len(palavras)-1:palavras += [' '.join(proto_palavras[j:])]
    return palavras

def cria_palavras_random(ditado,tamanho_palavras,numero_palavras):
    ditado = [i for i in ditado.replace('\n',' ').lower().split(' ') if i != '']
    limite,palavras = len(ditado)-1,[]
    for i in range(numero_palavras):
        palavra = []
        for j in range(tamanho_palavras):palavra += [ditado[randint(0,limite)]]
        palavra = ' '.join(palavra)
        palavras += [palavra]
    return palavras

# atualiza o texto mostrado
def atualiza_texto(event):
    global texto_atual
    texto_atual = entrada.get()
    texto.config(text=texto_atual)

# é ativada quando gastas todas as tentativas, mostra a palavras correta
def corrigir():
    global a_corrigir
    a_corrigir = True
    correção.config(text=palavra)
    pontuação_palavra_texto.config(text=pontuação_palavra)

# fecha o programa
def fechar_programa(event):
    driver.close()
    janela.destroy()

# termina o programa quando todas as palavra forem ditadas, mostra algumas informações
def acabar_ditado():
    janela.unbind('<Key>')
    janela.unbind('<Return>')
    janela.unbind('<Control_L>')
    pontuação_texto.config(text='')
    pontuação_palavra_texto.config(text='')
    texto.config(text='acabaste!')
    correção.config(text=f'pmpp={round((pontuação+pontuação_palavra)/len(palavras),1)}')

# mostra a próxima palavra
def muda_palavra():
    global pontuação,pontuação_palavra,palavras,palavra,index_palavra,a_corrigir

    if index_palavra == len(palavras) - 1:
        acabar_ditado()
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

# ativada sempre que se preciona a tecla ENTER, decide o que fazer
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


def começa_ditado():
    '''
    inicia a janela do tradutor
    '''
    global options,driver,text_box,read_button,clear_button
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

    '''
    prepara a janela para começar a ditar
    '''
    global janela,pontuação_palavra_texto,pontuação_texto,texto,correção,entrada
    # criar o texto que mostra a quantidade de tentativas
    pontuação_palavra_texto = tk.Label(janela, bg='black', fg='white', font=('Arial', 40), text='10')
    pontuação_palavra_texto.place(x = 490, y = 200)
    # cria o texto que mostra a pontuação
    pontuação_texto = tk.Label(janela,bg='black',fg='white',font=('Arial',40),text='0')
    pontuação_texto.place(x = janela.winfo_screenwidth()-510, y = 200)
    # cria o texto
    texto = tk.Label(janela,bg='black',fg='white',font=('Arial',70))
    texto.pack(pady=(320,0))
    # cria o texto que mostra a palavra correta
    correção = tk.Label(janela,bg='black',fg='white',font=('Arial',60))
    correção.pack(pady=(80,0))
    # cria a entrada de input , .focus_set faz com que o input seja direcionado para a entrada de texto
    entrada = tk.Entry(janela,bg='black',bd=0)
    entrada.focus_set()
    entrada.place(x=janela.winfo_screenwidth(),y=janela.winfo_screenheight())

    '''
    cria as variavés necessárias para o funcionamento , e prepara a primeira palavra
    '''
    global palavras,a_corrigir,index_palavra,palavra,pontuação,pontuação_palavra,texto_atual
    # cria o ditado
    ditado = entrada_ditado.get(1.0,tk.END)
    número_palavras = random_number_words.get()
    tamanho_palavras = size_number_words.get()
    if tamanho_palavras == '': tamanho_palavras = 1
    else: tamanho_palavras = int(tamanho_palavras)
    if número_palavras == '':palavras = cria_palavras(ditado,tamanho_palavras)
    else:palavras = cria_palavras_random(ditado,tamanho_palavras,int(número_palavras))
    # destroi a UI antiga
    entrada_ditado.destroy()
    frame.destroy()
    # cria outras variáveis
    a_corrigir = False
    index_palavra = 0
    palavra = palavras[index_palavra]
    pontuação = 0
    pontuação_palavra = 10
    texto_atual = ''
    # poem a primeira palavra no tradutor e lê
    por_p(palavra)
    sleep(1.5)
    le_p()


    '''
    cria os bindis necessários
    '''
    janela.bind('<Key>',atualiza_texto)
    janela.bind('<Return>',submeter_palavra)
    janela.bind('<Control_L>',lambda event:le_p)
    janela.bind('<Escape>',fechar_programa)




# abre a janela do tkinter
janela = tk.Tk()
janela.title('o ditador')
janela.geometry(f'{janela.winfo_screenwidth()}x{janela.winfo_screenheight()}')
janela.config(bg='black')
janela.state('zoomed')

frame = tk.Frame(janela,bg='black')
frame.pack(pady=30)

continue_button = tk.Button(frame,bg='black',fg='white',bd=2,width=10,height=2 ,text='Confirmar',command=começa_ditado)
continue_button.grid(row=0,column=0)

random_label = tk.Label(frame,text='Número de palavra aleatórias:',font=('Arial',20),bg='black',fg='white')
random_label.grid(row=0,column=1,padx=20)

random_number_words = tk.Entry(frame,bg='black',fg='white',bd=2,font=('Arial',20),width=5)
random_number_words.grid(row=0,column=2)

size_label = tk.Label(frame,text='Tamanho das palavras:',font=('Arial',20),bg='black',fg='white')
size_label.grid(row=0,column=3,padx=20)

size_number_words = tk.Entry(frame,bg='black',fg='white',bd=2,font=('Arial',20),width=5)
size_number_words.grid(row=0,column=4)

entrada_ditado = tk.Text(janela,bg='gray',fg='white',bd=0,font=('Arial',20),width=85,height=19)
entrada_ditado.pack()

janela.bind('<Escape>',lambda event:janela.destroy)

# inpede a janela de se fechar
janela.mainloop()