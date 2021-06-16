import os
import pyaudio
import wave
import numpy as np
import time

import math as mt

from sys import platform


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


def leerAudio(Nombre="output0.wav",Graficar=False,carpeta="audios"):
    from scipy.io.wavfile import read   
    aux = read('./'+carpeta+'/'+Nombre) 
    array_audio = aux[1]
    #print(aux)
    #print(len(array_audio))
    ff = np.array(fft(array_audio),dtype=complex)

    ff = np.split(ff,2)
    if(Graficar):
        import matplotlib.pyplot as plt        
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
            print("Algunas vocales presentan insuficiencia de datos")

    print(v_promedio_m,v_promedio_h)
    return v_promedio_m,v_promedio_h
        
        


def crearAudio(segundos=1,nombre="output",Genero="",carpeta="audios"):
    
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

def menu():
    run = True

    print("Iniciando...")
    directorio1 = "./audios/"
    directorio2 = "./pruebas/"
    try:
        os.mkdir(directorio1)    
        print("Creado directorio audios")
    except:
        print("Detectado directorio audios")
        #os.mkdir(directorio1)

    try:
        os.mkdir(directorio2) 
        print("Creado directorio pruebas")
    except:
        print("Detectado directorio pruebas")
        

    pruebas_m,pruebas_h = leerArchivos()
    antes_archivo = os.listdir('./audios/')

    clearScreen()
    while run:
        opcion = int(input("Reconocimiento de Vocales\n1.Agregar audio\n2.Obtener vocal\n3.Salir\nOpcion:"))

        if opcion == 1:
            gen = str(input("Introduce el genero del hablante (h, m o vacio para indistinto): ")).lower()
            vocal = str(input("Introduce que vocal es: "))
            crearAudio(nombre=vocal,Genero=gen)
        if opcion == 2:

            gen = str(input("Introduce tu nombre: ")).lower()
            crearAudio(Genero=gen,carpeta="pruebas")
            numero_archivo = os.listdir('./pruebas/')
            despues_archivo = os.listdir('./audios/')

            if(antes_archivo != despues_archivo):
                print("Se detectaron cambios en los archivos de audio\nCalculando frecuencias de nuevo")
                pruebas_m,pruebas_h = leerArchivos()

            archivo = numero_archivo[-1]
            frec = leerAudio(carpeta='pruebas',Graficar=True,Nombre=archivo)
            identificaVocal(pruebas_m,pruebas_h,frec)# CAMBIAR 
        if opcion == 3:
            print("Bye")
            time.sleep(1)
            run = False
        #input()
        #clearScreen()
        
            
if __name__ == "__main__":
    menu()
    