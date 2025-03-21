import pygame #Para hacer la pantalla 
import tkinter as tk 
from tkinter import filedialog #Para poder cargar los archivos
import json # json

class Interfaz_Grafica:
    def __init__(self):
        pass
    
    def cargar_json():
        raiz = tk.Tk() #Carga tkinter para poder cargar el archivo
        raiz.withdraw() #Oculta la ventana emergente
        
        # Abrir el explorador de archivos
        archivo = filedialog.askopenfilename(filetypes=[("Archivos JSON", "*.json")]) #Solo muestra archivos tipo JSON
    
        with open(archivo, "r", encoding="utf-8") as archivo_data: #utf-8 es para evitar complicaciones con caracteres especiales
            data = json.load(archivo_data)
            print(data)
