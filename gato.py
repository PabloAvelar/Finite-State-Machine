from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import random
import numpy as np

#Mi propia librería
from maquina import *


class Gato:
    def __init__(self, raiz, maquina):
        self.raiz = raiz
        self.raiz.config(bg="green")
        self.maquina = maquina
        self.contador = 0
        self.turno = 2
        self.salidas = ""
        self.mostrar_resultado = False
        fondo = PhotoImage(file="assets/fondo.png")
        l_fondo =Label(self.raiz, image=fondo)
        l_fondo.place(x=0, y=0, relwidth=1, relheight=1)
        l_fondo.image=fondo

        self.varEstado = StringVar(self.raiz, self.maquina.s)
        self.varOutput = StringVar(self.raiz, "***")
        
        mostrar_estado = Label(
            self.raiz, textvariable=self.varEstado
        )
        mostrar_estado.config(bg="red", font=("Arial", 13))
        mostrar_estado.place(x=80, y=0)

        mostrar_salida = Label(
            self.raiz, textvariable=self.varOutput
        )
        mostrar_salida.config(bg="green", font=("Arial", 13))
        mostrar_salida.place(x=110, y=30)

        Label(self.raiz, text="Estado: ", bg="red", font=("Arial", 13)).place(x=0, y=0)
        Label(self.raiz, text="Ultima Salida: ", bg="green", font=("Arial", 13)).place(x=0, y=30)

        self.posiciones =  [[None, None, None],
                            [None, None, None],
                            [None, None, None]]

    def fin(self):
        for i in self.posiciones:
            print("fila: ", i)
        #Checa si hay un ganador#
            #tres en fila

        def verificar(lista):
            # print("lista: ", tipo)
            cont = 0
            for i in lista:
                final = all(str(elemento) == i[cont] for elemento in i)
                if final:
                    if self.turno == 1:
                        print("GANADOR JUGADOR")
                    elif self.turno == 0:
                        print("GANADOR MAQUINA")
                    return final
                cont+=1
        
        if verificar(self.posiciones):
            return True
            #Tres en columna
        #Matriz transpuesta para checar las columnas como filas#
        transpuesta = np.transpose(self.posiciones)
        if verificar(transpuesta):
            return True

        #Tres en diagonales
        diagonal_principal = []
        diagonal_secundaria = []

        #Diagonal principal
        for i in range(3):
            for j in range(3):
                if i == j: 
                    diagonal_principal.append(self.posiciones[i][j])

        #Diagonal secundaria
        for i in range(3):
            for j in reversed(range(3)):
                if i + j == 2:
                    diagonal_secundaria.append(self.posiciones[i][j])

        print("DIAGONAL: ", diagonal_principal)
        if verificar([diagonal_principal]):
            return True
        if verificar([diagonal_secundaria]):
            return True
            
        #Checa si la matriz está llena
        if self.contador == 9:
            print("La matriz está llena")
            print("CONTADOR: ", self.contador)
            self.turno = 2
            self.mostrar_resultado = True
            return True
        return False

    def bot(self, botones, tablero):
        print("BOT")
        if not self.fin():
            
            self.turno = 0
            x = random.choice([0, 1, 2])
            y = random.choice([0, 1, 2])
            while self.posiciones[x][y] != None:
                x = random.choice([0, 1, 2])
                y = random.choice([0, 1, 2])
            self.contador += 1
            self.posiciones[x][y] = "X"
            print("(x, y) = ({}, {})".format(x, y))
            o = self.maquina.g("0")
            self.salidas+=o
            self.varOutput.set(o)
            self.maquina.f("0")
            
            btn = botones[x][y]
            txt = StringVar(tablero, o)
            btn.config(textvariable=txt, fg="red")
            self.varEstado.set(self.maquina.s)
            #checa nada más
        if self.fin():
            print("Juego terminado BOT XD")
            o = self.maquina.g("full")
            self.salidas+=o
            self.varOutput.set(o)
            self.maquina.f("full")
            print(o)

            self.resultado(tablero)

    def resultado(self, tablero):
        #self.varEstado.set(self.maquina.s)
        print("ver Salida: ", self.varOutput.get())
        ganador = None
        if self.turno == 0:
            txt = "¡Ganador: Máquina!"+"\n\n¿Desea jugar de nuevo?"
            ganador = "0"
        elif self.turno == 1:
            txt = "¡Ganador: Usuario!"+"\n\n¿Desea jugar de nuevo?"
            ganador = "1"
        else:
            txt = "¡Empate!"+"\n\n¿Desea jugar de nuevo?"
            ganador = "e"

        jugar = messagebox.askquestion("Resultado", txt)
        if jugar == 'yes':
            o = self.maquina.g(ganador)
            self.salidas+=o
            self.varOutput.set(o)
            print(o)
            self.maquina.f(ganador)

            for cosas in tablero.winfo_children():
                cosas.destroy()
            
            tablero.destroy()
            for i in range(3):
                for j in range(3):
                    self.posiciones[i][j] = None
            self.contador = 0
            for i in self.posiciones:
                print("fila RESULTADO: ", i)
            self.inicio()
        else:
            raiz.quit()
        

    def evaluar(self, x, y, botones, txt, tablero):
        print("TURNO JUGADOR")
        
        if not self.fin():
            self.turno = 1
            print("botones text: ", botones[x][y]["text"])
            # turno = " "
            # if self.maquina.s == "q1": turno = "0"
            # elif self.maquina.s == "q2": turno = "1"

            if botones[x][y]["text"] == "":
                self.contador += 1
                o = self.maquina.g("1")
                self.salidas+=o
                self.varOutput.set(o)
                self.maquina.f("1")
                self.posiciones[x][y] = o
                #Se actualiza el tablero
                txt.set(o)
                self.varEstado.set(self.maquina.s)

            if self.maquina.s == "q1":
                self.bot(botones, tablero)
            # for i in self.posiciones:
            #     print(i)
        else:
            print("Juego terminado")
            o = self.maquina.g("full")
            self.salidas+=o
            self.varOutput.set(o)
            self.maquina.f("full")
            print(o)

            self.resultado(tablero)
            

        print("CONTADOR: ", self.contador)

        for i in self.posiciones:
            print("fila: ", i)

    def mostrar_tablero(self):
        for i in self.posiciones:
            print("fila TABLERO: ", i)
        
        try:
            for boton in botones:
                for txt in boton:
                    txt.text = None
        except:
            pass

        b_w = 17
        i=0
        botones = [[], [], []]

        tablero = Frame(raiz, width=500, height=500,
                        highlightbackground="white", highlightthickness=5)
        tablero.place(anchor='center', rely=0.5, relx=0.5)

        tablero.config(bg="#444444")

        for x in range(3):
            j=0
            for pos in self.posiciones[i]:
                #print(pos)
                txt = StringVar(tablero, pos)
                b = Button(tablero,
                        textvariable=txt,
                        command=lambda x=x,
                                        j=j,
                                        btn=botones,
                                        txtvar = txt,
                                        tab = tablero: self.evaluar(x, j, btn, txtvar, tab), 
                        width=b_w, height=int(b_w/2))
                b.grid(row=i, column=j, padx=5, pady=2)

                botones[x].append(b)
                j+=1
            i+=1
        if self.maquina.s == "q1":
            self.bot(botones, tablero)

    def ver_salidas(self):
        w = Toplevel()
        w.wm_geometry("400x400")

        Label(w, text="Todas las salidas hasta ahora").pack()
        print(self.salidas)
        Label(w, text=self.salidas).pack()


        w.mainloop()

    def inicio(self):
        self.varEstado.set(self.maquina.s)
        def click_btn(x):
            o = self.maquina.g(x)
            self.salidas+=o
            self.maquina.f(x)

            #Eliminando widgets
            l.destroy()
            btn_m.destroy()
            btn_u.destroy()
            minombre.destroy()
            l_maquina.destroy()
            self.mostrar_tablero()

        img_maquina = Image.open("assets/maquina.png")
        img_maquina = img_maquina.resize((200,200), Image.Resampling.LANCZOS)
        img_maquina = ImageTk.PhotoImage(img_maquina)

        img_usuario = Image.open("assets/usuario.png")
        img_usuario = img_usuario.resize((200,200), Image.Resampling.LANCZOS)
        img_usuario = ImageTk.PhotoImage(img_usuario)

        minombre = Label(raiz,
            text="Pablo Avelar Armenta",
            font=("Arial", 15),
            bg="#e5bd8a"
            )
        minombre.pack()

        l_maquina = Label(raiz,
            text="Maquina de Estado Finito",
            font=("Arial", 13),
            bg="#e5bd8a"
            )
        l_maquina.pack()


        l = Label(self.raiz, text="¿Quién inicia?",
                    font=("Arial", 17, "bold"), bg="#e5bd8a")
        l.place(y=-150, relx=0.5, rely=0.5, anchor=CENTER)

        btn_m = Button(self.raiz, image=img_maquina, command=lambda x="0":click_btn(x))
        btn_m.place(x=-120, y=30, relx=0.5, rely=0.5, anchor=CENTER)
        btn_m.image = img_maquina

        btn_u = Button(self.raiz, image=img_usuario, bg="#cdefff", command=lambda x="1":click_btn(x))
        btn_u.place(x=120, y=30, relx=0.5, rely=0.5, anchor=CENTER)
        btn_u.image = img_usuario

        btn_salidas = Button(self.raiz, text="Todas las salidas", command=lambda:self.ver_salidas())
        btn_salidas.config(bg="#CAA678", fg="#ccc", font=("Arial", 11, "bold"))
        btn_salidas.place(x=0, y=570)


        #juego.mostrar_tablero()

if __name__ == '__main__':
    global raiz
    inicial = "q0"
    s = inicial
    maquina = Maquina()

    raiz = Tk()
    raiz.title("Gato")
    raiz.geometry("600x600")
    raiz.resizable(False, False)
    raiz.iconbitmap("gato.ico")
    
    juego = Gato(raiz, maquina)

    if maquina.s == "q0":
        #Limpiando el tablero
        for i in range(3):
            for j in range(3):
                juego.posiciones[i][j] = None

        juego.inicio()

    print("HOLA XD")
    for i in juego.posiciones:
        print(i)

    raiz.mainloop()