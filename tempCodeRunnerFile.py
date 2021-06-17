print("Iniciando...")
directorio_audio = "./audios/"
directorio_prueba = "./pruebas/"
try:
    os.mkdir(directorio_audio)    
except:
    messagebox.showinfo(title= "Información", message="Directorio de audios listo para funcionar" )
    #os.mkdir(directorio1)

try:
    os.mkdir(directorio_prueba) 
except:
    messagebox.showinfo(title= "Información", message="Directorio de pruebas listo para funcionar" )

pruebas_m,pruebas_h = leerArchivos()
antes_archivo = os.listdir('./audios/')

clearScreen()