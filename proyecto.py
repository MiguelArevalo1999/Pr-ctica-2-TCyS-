import os
import pyaudio
import wave
import numpy as np
import time
import matplotlib.pyplot as plt 
from scipy.io.wavfile import read          
import math as mt
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import tkinter as tk
from sys import platform

raiz = Tk()
raiz.title("Proyecto Final Detección de vocales Eq. Chipocludo")
raiz.resizable(0,0)
raiz.geometry("500x350")
raiz.config(bg="cyan")

myFrame=Frame()
myFrame.pack(side="top")
myFrame.config(bg="white")

#Logo ESCOM
imagen=tk.PhotoImage(file="logoescom.png")
imagen_sub=imagen.subsample(12)
widget=ttk.Label(image=imagen_sub)
widget.place(x=5,y=5)

#Logo IPN
imageni=tk.PhotoImage(file="ipn.png")
imageni_sub=imageni.subsample(15)
widgeti=ttk.Label(image=imageni_sub)
widgeti.place(x=400,y=5)

text = Label(text="Escuela Superior de Cómputo\n\n Arévalo Andrade Miguel Ángel \n Esquivel Salvatti José Luis\n \
            López Morales Miguel Ángel\n Vaca García Jesús Fernando\n Vargas Espino Carlos Hassan")
text.place(x=155,y=7)

opcion_label=Label(raiz, text = "Opción")
opcion_label.place(x=25,y=130)
combo = ttk.Combobox(raiz)
combo.place(x=80,y=130)
combo['values']=('Añadir audio','Detectar vocal')

opcion_vocal=Label(raiz, text = "Vocal")
opcion_vocal.place(x=230,y=130)
combo_vocales = ttk.Combobox(raiz)
combo_vocales.place(x=270,y=130)
combo_vocales['values']=('a','e','i','o','u')

opcion_genero=Label(raiz, text = "Género")
opcion_genero.place(x=230,y=160)
combo_genero = ttk.Combobox(raiz)
combo_genero.place(x=275,y=160)
combo_genero['values']=('Hombre','Mujer')


label_nombre=Label(raiz, text = "Nombre:")
label_nombre.place(x=25,y=160)
nombre = ttk.Entry(raiz)
# Posicionarla en la ventana.
nombre.place(x=80, y=160)



def leerAudio(Nombre="output0.wav",Graficar=False,carpeta="audios"):
    aux = read('./'+carpeta+'/'+Nombre) 
    array_audio = aux[1]
    #print(aux)
    #print(len(array_audio))
    ff = np.array(fft(array_audio),dtype=complex)

    ff = np.split(ff,2)
    if(Graficar):
        plt.title(Nombre)
        plt.plot(array_audio)
        plt.show()
        plt.title(Nombre+" FFT")
        plt.plot(ff[0].real)
        plt.plot(np.abs(ff[0].real))        
        plt.show()

    mayor = np.amax(ff[0])
    #print(mayor)
    frec = int(mayor.real/10000)

    return frec
    #print(frec,"Hz")

    #print("Se trata de la vocal " + identificaVocal(frec))
    #for i in aux[1]:
    #    print(i)

        
        


def crearAudio(segundos=1,nombre="output", Genero="",carpeta="audios"):
    
    CHUNK = 1024*2
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    RECORD_SECONDS = segundos

    numero_archivo = os.listdir('./'+carpeta+'/')
    am = em = im = om = um = output = 0
    ah = eh = ih = oh = uh = 0
    for j in numero_archivo:
        j= j.replace(".wav","")
        if("a" in j and "m" in j):            
            am+=1
        if("e" in j and "m" in j):
            em+=1
        if("i" in j and "m" in j):
            im+=1
        if("o" in j and "m" in j):
            om+=1
        if("u" in j and "m" in j):            
            um+=1
        if("a" in j and "h" in j):            
            ah+=1
        if("e" in j and "h" in j):
            eh+=1
        if("i" in j and "h" in j):
            ih+=1
        if("o" in j and "h" in j):
            oh+=1
        if("u" in j and "h" in j):            
            uh+=1
        if("output"):
            output+=1
    
    if(nombre == "a"):
        if(Genero=="m"):
            numero_archivo = am
        elif Genero=="h":
            numero_archivo = ah
    if(nombre == "e"):
        if(Genero=="m"):
            numero_archivo = em
        elif Genero=="h":
            numero_archivo = eh
    if(nombre == "i"):
        if(Genero=="m"):
            numero_archivo = em
        elif Genero=="h":
            numero_archivo = eh
    if(nombre == "o"):
        if(Genero=="m"):
            numero_archivo = om
        elif Genero=="h":
            numero_archivo = oh
    if(nombre == "u"):
        if(Genero=="m"):
            numero_archivo = um
        elif Genero=="h":
            numero_archivo = uh
    if(nombre == "output"):
        numero_archivo = output

    WAVE_OUTPUT_FILENAME = "./"+carpeta+"/"+nombre+str(numero_archivo)+Genero+".wav"

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    for i in range(3,0,-1):
        print(i)
        time.sleep(1)

    print("* grabando")

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)        
        frames.append(data)

    #print(bytes(0))
    #for i in range(0,21504):
    #    frames.append(bytes("0",encoding="utf-8"))

    print("* grabación terminada")

    frames = frames[:32]
    #print(len(frames))
    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

def clearScreen():
    """Description: Funcion que detecta el sistema operativo y relaciona su comando para borrar la pantalla
    """
    if platform == "win32":
        os.system("cls")
    else:
        os.system("clear")

def fft(funcion):
    """Description: funcion que obtiene la transformada discreta de fourier usando el algoritmo FFT
    
    :param funcion : list
        señal discreta
    
    :return resultado : list
    señal discreta despues de la FFT

    """
    n = len(funcion)
    if n == 1:
        return funcion
    else:
        pares = [ funcion[2*i] for i in range(n//2)]
        impares = [ funcion[2*i+1] for i in range(n//2)]

        pares = fft(pares[:n//2])
        impares = fft(impares[:n//2])        
        resultado = [0 for i in range(n)]        
          
        for i in range(n//2):
            w = complex(mt.cos(2*mt.pi*i/(n)),-mt.sin(2*mt.pi*i/(n)))            
            resultado[i] = pares[i] +w*impares[i]
            resultado[n//2 + i] = pares[i] -w*impares[i]
            
        
        return resultado

def identificaVocal(prom_m, prom_h, frecuencia):

    """
    print("Promedio Hombres:")
    print(prom_h)
    print("Promedio Mujeres:")
    print(prom_m)
    print("Frecuencia:")
    print(frecuencia)
    """

    vocales_h = [0,0,0,0,0]
    vocales_m = [0,0,0,0,0]
    
    #Vocal A
    vocales_h[0] = prom_h[0]-frecuencia
    vocales_m[0] = prom_m[0]-frecuencia  

    #Vocal E
    vocales_h[1] = prom_h[1]-frecuencia
    vocales_m[1] = prom_m[1]-frecuencia

    #Vocal I
    vocales_h[2] = prom_h[2]-frecuencia
    vocales_m[2] = prom_m[2]-frecuencia

    #Vocal O
    vocales_h[3] = prom_h[3]-frecuencia
    vocales_m[3] = prom_m[3]-frecuencia

    #Vocal U
    vocales_h[4] = prom_h[4]-frecuencia
    vocales_m[4] = prom_m[4]-frecuencia
    
    vocal = 100000000
    h = m = 0

    #Obtiene valor absoluto
    for i in range(0,5):
        if(vocales_h[i] < 0):
            vocales_h[i] = vocales_h[i]*-1

    #Obtiene valor absoluto
    for i in range(0,5):
        if(vocales_m[i] < 0):
            vocales_m[i] = vocales_m[i]*-1

    """
    print(vocales_h[0])
    print(vocales_h[1])
    print(vocales_h[2])
    print(vocales_h[3])
    print(vocales_h[4])

    print(vocales_m[0])
    print(vocales_m[1])
    print(vocales_m[2])
    print(vocales_m[3])
    print(vocales_m[4])
    """

    #Obtiene la frecuencia con menor margen a una vocal
    for i in vocales_h:
        if(i < vocal):
            vocal = i
            h = 1
            m = 0

    for i in vocales_m:
        if(i < vocal):
            vocal = i  
            m = 1 
            h = 0


    if(vocal == vocales_h[0] or vocal == vocales_m[0]):
        resul =  "A"
    if(vocal == vocales_h[1] or vocal == vocales_m[1]):
        resul =  "E"
    if(vocal == vocales_h[2] or vocal == vocales_m[2]):
        resul =  "I"
    if(vocal == vocales_h[3] or vocal == vocales_m[3]):
        resul =  "O"    
    if(vocal == vocales_h[4] or vocal == vocales_m[4]):
        resul =  "U"
    if(vocal == 100000000):
        #return "NO SE ENCONTRÓ"
        print("NO SE ENCONTRÓ")

    if(h == 1):
        #return resul + " Hombre"
        print(resul + " Hombre")
    if(m == 1):
        #return resul + " Mujer"
        print(resul + " Mujer")

    input("Presione una tecla...")
    clearScreen()

def leerArchivos(carpeta="audios"):
    archivos = os.listdir('./'+carpeta+'/')
    vocales_mujeres = [0,0,0,0,0] # a e i o u
    vocales_hombres = [0,0,0,0,0]

    m = [0,0,0,0,0] # a e i o u
    h = [0,0,0,0,0]
    for j in archivos:        
        aux = leerAudio(Nombre=j)
        j= j.replace(".wav","")
        if("a" in j and "m" in j):            
            m[0]+=1
            vocales_mujeres[0] += aux
        if("e" in j and "m" in j):
            m[1]+=1
            vocales_mujeres[1] += aux
        if("i" in j and "m" in j):
            m[2]+=1
            vocales_mujeres[2] += aux
        if("o" in j and "m" in j):
            m[3]+=1
            vocales_mujeres[3] += aux
        if("u" in j and "m" in j):            
            m[4]+=1
            vocales_mujeres[4] += aux
        if("a" in j and "h" in j):                        
            h[0]+=1
            vocales_hombres[0] += aux
        if("e" in j and "h" in j):
            h[1]+=1
            vocales_hombres[1] += aux
        if("i" in j and "h" in j):
            h[2]+=1
            vocales_hombres[2] += aux
        if("o" in j and "h" in j):
            h[3]+=1
            vocales_hombres[3] += aux
        if("u" in j and "h" in j):            
            h[4]+=1
            vocales_hombres[4] += aux
    
    v_promedio_m = []
    v_promedio_h = []

    for i in range(5):
        try:
            v_promedio_m.append(vocales_mujeres[i]/m[i])
            v_promedio_h.append(vocales_hombres[i]/h[i])
        except:
            messagebox.showinfo(title= "Información", message="Algunas vocales presentan insuficiencia de datos" )
            

    print(v_promedio_m,v_promedio_h)
    return v_promedio_m,v_promedio_h



print("Iniciando...")
directorio_audio = "./audios/"
directorio_prueba = "./pruebas/"
try:
    os.mkdir(directorio_audio)    
except:
    messagebox.showinfo(title= "Información", message="Directorio de audios listo para funcionar" )


try:
    os.mkdir(directorio_prueba) 
except:
    messagebox.showinfo(title= "Información", message="Directorio de pruebas listo para funcionar" )

pruebas_m,pruebas_h = leerArchivos()
antes_archivo = os.listdir('./audios/')

clearScreen()



def seleccionar_funcion():
    """
    Funcion que dependiendo de las opciones en el combobox ejecuta 
    las operaciones correspondientes
    """
    combo_seleccion = combo.get() #Obtener la seleccion en el combobox
    combo_vocal_seleccion = combo_vocales.get() #Obtiene la vocal seleccionada
    nombre_entrada = nombre.get() #Obtiene el nombre escrito
    combo_genero_seleccion = combo_genero.get() #Obtiene el genero del usuario


    if combo_seleccion == 'Añadir audio':
        gen = ""
        if combo_genero_seleccion == "Hombre":
            gen = 'h'
        elif combo_genero_seleccion == "Mujer":
            gen = 'm'
        crearAudio(nombre=combo_vocal_seleccion,Genero= gen)
    
    elif combo_seleccion == 'Detectar vocal':
        crearAudio(Genero=nombre_entrada,carpeta="pruebas")
        numero_archivo = os.listdir('./pruebas/')
        despues_archivo = os.listdir('./audios/')

        if(antes_archivo != despues_archivo):
            messagebox.showinfo(title= "Información", message="Se detectaron cambios en los archivos de audio\n \
                                                                Calculando frecuencias de nuevo" )
            pruebas_m,pruebas_h = leerArchivos()

        archivo = numero_archivo[-1]
        frec = leerAudio(carpeta='pruebas',Graficar=True,Nombre=archivo)
        identificaVocal(pruebas_m,pruebas_h,frec)# CAMBIAR 
    
    else:
        messagebox.showinfo("Debe seleccionar una opción")


start=Button(raiz, text="Ejecutar",command=seleccionar_funcion)
start.place(x=200,y=300)        

raiz.mainloop()
    