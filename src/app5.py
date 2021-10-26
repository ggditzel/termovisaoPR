import tkinter
from tkinter import *
from tkinter import filedialog as dlg
from io import StringIO
import os

# importação da biblioteca necessária criar os dataframes
import pandas as pd

pastaApp=os.path.dirname(__file__) # caminho do arquivo do app

# definir funções para os botões que for usar

def semComando():
    pass

def selecionaPasta():
    # filename = dlg.askopenfilename() # retorna caminho para um arquivo; pode já abrir o arquivo, ver opções
    pasta = dlg.askdirectory() # retorna caminho para a pasta
    processar(pasta)

def processar(pasta):

    # lista de caminhos para os 9 arquivos
    caminhos = []
    for i in range(1, 10):
        caminhos.append(f"{pasta}/imagem {i}.csv")

    # lê cada arquivo e coloca numa lista de strings
    file2string = []
    for caminho in caminhos:
        with open(caminho, "r+") as inp:
            string_total = inp.read()  # lê o arquivo inteiro
        string_preparada = string_total.replace("\n", "$")
        string_preparada = string_preparada.replace(";$", "$")  # retirar a anomalia ";"
        string_preparada = string_preparada.replace("$", "\n")
        string_preparada = string_preparada.replace(",", ".")  # para ajudar depois na conversão para float
        file2string.append(string_preparada)

    info_pra = file2string[0].split("\n")
    emissividade = info_pra[2].split(";")[-1].strip().replace(".", ",")

    distancia = info_pra[4].split(";")[-1]
    distancia = distancia[0] if len(distancia) == 3 else distancia[0:2]  # funciona entre 0 e 99 metros

    umidade = info_pra[8].split(";")[-1]
    umidade = umidade[0] if len(umidade) == 3 else umidade[0:2]  # funciona entre 0 e 99%

    temp_atm = info_pra[5].split(";")[-1]
    temp_atm = temp_atm[0:4].replace(".", ",")

    # cria um dataframe para cada string
    lista_df = []
    for s in file2string:
        string_io = StringIO(s)
        lista_df.append(pd.read_csv(string_io, sep=";", skiprows=16, header=None))

    lista_valores = []
    for df in lista_df:
        linha_inicio_bx2 = df[df[0] == 'Bx2'].index[0]

        box1 = df.loc[0:linha_inicio_bx2 - 1]
        box1 = box1.drop(0, axis=1)  # exclui primeira coluna
        box1 = box1.astype("float64")  # converte todas as colunas para número

        box2 = df.loc[linha_inicio_bx2 + 4:]  # pulamos mais algumas linhas
        box2 = box2.drop(box2.columns[[0]], axis=1)
        box2 = box2.astype("float64")

        lista_valores.append(pd.concat([box1, box2]).reset_index(drop=True))

    df_pra = pd.concat([lista_valores[0], lista_valores[1], lista_valores[2]]).reset_index(drop=True)
    df_prb = pd.concat([lista_valores[3], lista_valores[4], lista_valores[5]]).reset_index(drop=True)
    df_prc = pd.concat([lista_valores[6], lista_valores[7], lista_valores[8]]).reset_index(drop=True)

    max_pra = str(round(df_pra.stack().max(),2))
    max_pra = max_pra.replace(".", ",")
    min_pra = str(round(df_pra.stack().min(),2))
    min_pra = min_pra.replace(".", ",")

    max_prb = str(round(df_prb.stack().max(),2))
    max_prb = max_prb.replace(".", ",")
    min_prb = str(round(df_prb.stack().min(),2))
    min_prb = min_prb.replace(".", ",")

    max_prc = str(round(df_prc.stack().max(),2))
    max_prc = max_prc.replace(".", ",")
    min_prc = str(round(df_prc.stack().min(),2))
    min_prc = min_prc.replace(".", ",")

    # inserir cálculo depois
    max_adj_a = 111
    max_adj_b = 222
    max_adj_c = 333

    pra = Label(grupo, text="PR fase A", font=("Arial", 10))
    prb = Label(grupo, text="PR fase B", font=("Arial", 10))
    prc = Label(grupo, text="PR fase C", font=("Arial", 10))

    pra.grid(row=0, column=1)
    prb.grid(row=0, column=2)
    prc.grid(row=0, column=3)

    txt1 = Text(grupo, height=7, width=8)  # número de caracteres em cada direção
    txt1.tag_configure('tag-right', justify='right')
    txt1.insert(END, f"{distancia}\n"
                     f"{umidade}\n"
                     f"{emissividade}\n"
                     f"{min_pra}\n"
                     f"{max_pra}\n"
                     f"{max_adj_a}\n"
                     f"{temp_atm}", "tag-right")
    txt1.configure(font=("Arial", 10))
    txt1.grid(row=1, column=1, padx=10, pady=10)

    txt2 = Text(grupo, height=7, width=8)  # número de caracteres em cada direção
    txt2.tag_configure('tag-right', justify='right')
    txt2.insert(END, f"{distancia}\n"
                     f"{umidade}\n"
                     f"{emissividade}\n"
                     f"{min_prb}\n"
                     f"{max_prb}\n"
                     f"{max_adj_b}\n"
                     f"{temp_atm}", "tag-right")
    txt2.configure(font=("Arial", 10))
    txt2.grid(row=1,column=2, padx= 10, pady=10)

    txt3 = Text(grupo, height=7, width=8)  # número de caracteres em cada direção
    txt3.tag_configure('tag-right', justify='right')
    txt3.insert(END, f"{distancia}\n"
                     f"{umidade}\n"
                     f"{emissividade}\n"
                     f"{min_prc}\n"
                     f"{max_prc}\n"
                     f"{max_adj_c}\n"
                     f"{temp_atm}", "tag-right")
    txt3.configure(font=("Arial", 10))
    txt3.grid(row=1,column=3, padx= 10, pady=10)

    label_linhas = Label(grupo, text="Distância\n"
                                     "Umidade Relativa\n"
                                     "Emissividade\n"
                                     "Temp. mínima\n"
                                     "Temp. máxima\n"
                                     "Máxima Adj.\n"
                                     "Temp. atmosférica", font=("Arial", 10), justify=RIGHT)
    label_linhas.grid(row=1, column=0, padx=10, pady=10)
    grupo.place(anchor="c", relx=.5, rely=.5)

app = Tk()
app.title("Avaliação de Dados Térmicos de PR")
app.geometry("500x310")

grupo=Frame(app)
barraDeMenus=Menu(app) # container

menuArquivo=Menu(barraDeMenus, tearoff=0)
menuArquivo.add_command(label="Selecionar", command=selecionaPasta) # adicionar comandos depois

menuSobre=Menu(barraDeMenus, tearoff=0)
menuSobre.add_command(label="Sobre", command=semComando) # adicionar comandos depois

barraDeMenus.add_cascade(label="Arquivo", menu=menuArquivo)
barraDeMenus.add_cascade(label="Ajuda", menu=menuSobre)

app.config(menu=barraDeMenus)
app.mainloop()
