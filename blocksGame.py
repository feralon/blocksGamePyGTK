# -*- coding:utf-8 -*-
import gtk
import random 

"""
    BlocksGame with UI in pyGTK
"""

#Alonso, Fernando
#Rodriguez, Raul

#IF WINDOWS IS USED TO RUN THE CODE, SET THIS CONST TO 1
WINDOWS = 1

class Juego():
    def __init__(self):
        
        #Tamaño tablero
        self.numero_filas = 10
        self.numero_columnas = 10
        
        #Juego
        self.toques = 0
        self.jugadas = []
        self.resuelto = False
        self.nivel = 1
        
        #Objetos Glade
        self.glade = gtk.Builder()
        self.glade.add_from_file('blocksGame.glade')
        
        self.ventana = self.glade.get_object('ventana')
        
        self.boton_recomenzar = self.glade.get_object('Recomenzar')
        self.boton_recomenzar.connect("activate",self.clickRecomenzar)
        
        self.boton_deshacer = self.glade.get_object('deshacer')
        self.boton_deshacer.connect("activate",self.clickDeshacer)
        
        self.boton_levelselect = self.glade.get_object('levelsel')
        self.boton_levelselect.connect("activate",self.clickNivel)
        self.selector_nivel = self.glade.get_object('selectorlvl')
        self.submit_lvl = self.glade.get_object('submit_lvl')
        self.submit_lvl.connect("clicked",self.lvlSubmit)
        self.tbox_lvl = self.glade.get_object('tbox_lvl')
        
        self.boton_verpuntos = self.glade.get_object('swpnt')
        self.boton_verpuntos.connect("activate", self.clickPuntuaciones)
        self.dialogo_puntuaciones = self.glade.get_object('dialogpnt')
        self.tview_puntuaciones = self.glade.get_object('textviewpnt')
        self.btn_aceptar_puntuaciones=self.glade.get_object('cerrarpnt')
        self.btn_aceptar_puntuaciones.connect("clicked",self.cerrarDialogo,self.dialogo_puntuaciones)
        self.btn_borrar_puntuaciones=self.glade.get_object('borrarpnt')
        self.btn_borrar_puntuaciones.connect("clicked",self.borrarPuntuaciones)
        
        self.dialogo_ganador = self.glade.get_object('dialogana')
        self.label_ganador = self.glade.get_object('labelganador')
        self.cerrar_dialogo_ganador = self.glade.get_object('closewin')
        self.cerrar_dialogo_ganador.connect("clicked", self.cerrarDialogo, self.dialogo_ganador)
        
        self.label_toques = self.glade.get_object('toques')
        self.label_nivel = self.glade.get_object('nivel')
        
        self.boton_tema1 = self.glade.get_object('tema1')
        self.boton_tema1.connect("activate",self.clickTema,1)
        self.boton_tema2 = self.glade.get_object('tema2')
        self.boton_tema2.connect("activate",self.clickTema,2)
        self.boton_tema3 = self.glade.get_object('tema3')
        self.boton_tema3.connect("activate",self.clickTema,3)
        
        
        self.salir = self.glade.get_object('Salir')
        self.salir.connect("activate",gtk.main_quit)
        
        
        #imagenes para el tablero
        self.imgstocado = ["2.png","2'.png","2''.png"]
        self.imgsnotocado = ["1.png","1'.png","1''.png"]
        
        self.imtocado = self.imgstocado[0]
        self.imnotocado = self.imgsnotocado[0]
        
        
        #Crear Tabla Principal
        self.tabla = self.glade.get_object('tabla1')
        self.images = [] #Array de posiciones de imagenes
        self.crearTabla()
        
        #Ficheros
        self.file_raw = "fraw.txt"
        self.file_texto = "ftex.txt"
        self.crearFichero() #Si no exsite crea el fichero
        
        
        #Arranque del programa
        self.arranque = True
        self.selector_nivel.show()
        
        self.ventana.connect ("destroy", gtk.main_quit)
    def crearTabla(self):
        
        x=0 #Pos X tabla
        y=0 #Pos y tabla
        for i in range (self.numero_filas * self.numero_columnas):
            EventBox = (gtk.EventBox())
            self.tabla.attach(EventBox, x, x+1, y, y+1)
            EventBox.fil = y + 1 #Posicion en la tabla en formato fila columna
                                #de matriz
            EventBox.col = x + 1 
            imagen=gtk.Image()
            imagen.tocada = False
            imagen.set_from_file(self.imnotocado)
            self.images.append(imagen)
            #Enlaza  el evento
            EventBox.add(imagen)
            EventBox.connect("button_press_event",self.clickEventbox)
            x = x + 1
            if(x == self.numero_columnas): 
                x= 0; y+=1
        
    def transCoord(self,fil,col):
        
    #devuelve el numero de elemento en el vector
        if (fil>self.numero_filas or fil<1 or col<1 or col>self.numero_columnas):
            return -1 #Devuelve -1 si la posicion esta fuera de rango
        return (((fil-1)*self.numero_columnas) + col) - 1
    
    def golpe(self,i,j):
    
        casillas = [[i,j],[i,j-1],[i,j-2],[i,j+1],[i,j+2],
        [i+ 1,j],[i+1,j-1],[i+1,j-2],[i+1,j+1],[i+1,j+2],
        [ i- 1,j],[i-1,j-1],[i-1,j-2],[i-1,j+1],[i-1,j+2],
        [i-2,j-1],[i-2,j],[i-2,j+1],
        [i+2,j-1],[i+2,j],[i+2,j+1]]
        for x in casillas:
            array = self.transCoord(x[0],x[1])
            if array != -1:
                
                if (self.images[array].tocada == True):
                    self.images[array].set_from_file(self.imnotocado)
                    self.images[array].tocada = False
                else:
                    self.images[array].set_from_file(self.imtocado)
                    self.images[array].tocada = True
            else:
                continue
                
    def comprobarJuego(self):
        
        for i in self.images:
            if(i.tocada == True):
                self.resuelto = False
                return
        self.resuelto = True
        
    def limpiarTablero(self):
        for x in self.images:
            x.tocada = False
            x.set_from_file(self.imnotocado)
            
    def crearTablero(self):
        self.limpiarTablero()
        self.toques = 0
        
        self.label_toques.set_text("Toques: 0")
        self.label_nivel.set_text("Nivel: " + str(self.nivel))
        
        for x in range(0, self.nivel):
            fila =random.randint(1,self.numero_filas)
            columna = random.randint(1, self.numero_columnas)
            self.golpe(fila, columna)
    
    def clickEventbox(self,ebox,event):  
        #golpe y guarda el golpe para deshacer
        self.golpe(ebox.fil,ebox.col)
        self.toques += 1
        self.label_toques.set_text("Toques: " + str(self.toques))
        self.jugadas.append(str(ebox.fil)+"."+str(ebox.col))
        
        #Comprueba si el juego se resolvio y lo muestra
        self.comprobarJuego()
        if(self.resuelto == True):
            if(self.escribirNivel() == True):
                self.label_ganador.set_text("Ha Ganado\nRECORD")
            else:
                self.label_ganador.set_text("Ha Ganado")
            self.dialogo_ganador.show()                        
        
            
    def clickRecomenzar(self,widget):
        self.crearTablero()
        
    def clickDeshacer(self,widget): 
        try:
            elemento = len(self.jugadas) - 1
            i = (int)(self.jugadas[elemento].split(".")[0])
            j = (int)(self.jugadas[elemento].split(".")[1])
            self.golpe(i, j)
            del self.jugadas[elemento]
        except:
            return
        
    def clickNivel(self,widget):
        self.selector_nivel.show()
        
    def lvlSubmit(self,widget):
      
        try:
            entrada = int (self.tbox_lvl.get_text())
            if (entrada < 1):
                return
        except:
            return
        if (entrada != self.nivel or self.arranque == True):
            self.nivel = entrada
            self.crearTablero()
            
        self.selector_nivel.hide()
        ##Cuando arranca el programa por primera vez
        if(self.arranque == True):
            self.arranque = False
            self.ventana.show_all()
        
    def clickPuntuaciones(self,widget):
        self.crearFicheroTextOrd()
        
        buffer = self.tview_puntuaciones.get_buffer()
        try:
            infile = open(self.file_texto, "r")
        except:
            print("Error de Lectura")
            return
        string = infile.read()
        infile.close() 
        buffer.set_text(string)
        self.dialogo_puntuaciones.show()
    
    def borrarPuntuaciones(self,widget):
        try:
            infile = open(self.file_raw, "w")
            infile.close()
            self.clickPuntuaciones("widget")
        except:
            return
            
    def clickTema(self,widget,tema):
        self.imtocado =self. imgstocado[tema - 1]
        self.imnotocado = self.imgsnotocado[tema - 1]
        for x in self.images:
            if (x.tocada == True):
                x.set_from_file(self.imtocado)
            else:
                 x.set_from_file(self.imnotocado)
      
    def cerrarDialogo(self,widget,dialogo):    
        dialogo.hide() #Cierra cualquier dialogo
        if(dialogo == self.dialogo_ganador):
            self.crearTablero()
            
    def crearFichero(self):
        try:
            fichero = open(self.file_raw, "r")
            fichero.close()
        except:
            try:
                fichero = open(self.file_raw, "w")
            except:
                print("No se pudo crear el fichero")
            finally:
                fichero.close()
        finally:
            fichero.close()
            
    def buscarNivel(self,nivel):
    #Busca el nivel actual en el fichero
        try:
            infile = open(self.file_raw, "r")
        except:
            print("Error al leer el fichero")
            return -1
        pos = 0
        for linea in infile:
            lv = (int)(linea.split(".")[0])

            if(lv == nivel):
                infile.close()
                return pos
            pos += len(linea) + WINDOWS
        infile.close()   
        return -1
    
    def escribirNivel(self):   
     
        posnivelact = self.buscarNivel(self.nivel)#Buscanos si existe el nivel
                                              #en el fichero 
                                              
        ##Si no existe el nivel, aniade en el fichero los puntos directamente
        if(posnivelact == -1):
            try:
                infile = open(self.file_raw, "a")
                infile.write(str(self.nivel) + "." + str(self.toques)+ "." + "\n")
             
            except:
                print("Error al escribir en el fichero 1")
            
            finally:
                infile.close()
                return True
        
        else: ##Si existe ya el nivel, se comprueba si los puntos son mejores
                ## y si lo son los sustituye y deuelve True para indicar record
            try:
                infile = open(self.file_raw, "r+") 
            except:
                print("Error al escribir en el fichero")
                return False
        
            infile.seek(posnivelact)
            linea = infile.read()
            puntos = int(linea.split(".")[1])
        
            if(self.toques < puntos):
                infile.seek(posnivelact)
                infile.write(str(self.nivel) + "." + str(self.toques) + "." + "\n")
                infile.close()
                return True
            else:
                infile.close()
                return False
            
    def crearFicheroTextOrd(self):
        #Buscar lvl max
        max = 1
        try:
            infile = open(self.file_raw, "r")
            auxfile= open(self.file_texto, "w")
        except:
            print("Error al leer el fichero")
            return
        auxfile.write("   ***PUNTUACIONES MAXIMAS***   \n")
        for linea in infile:
            lv = (int)(linea.split(".")[0])
            if(lv > max):
                max = lv
        for x in range(max + 1):
            y = self.buscarNivel(x)
            if(y !=-1):
                infile.seek(y)
                linea = infile.read()
                puntos = int(linea.split(".")[1])
                nivel = int(linea.split(".")[0])
                auxfile.write("Nivel " + str(nivel) + ": "+ str(puntos) + " toques" + "\n")
        
        infile.close()
        auxfile.close()        
hola = Juego()
gtk.main()
