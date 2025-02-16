import numpy as np

class Sensor(): #Clase de generación de datos del sensor
    def __init__(self,modo,min=0,max=(2**16)-1):
        self.modo=modo
        self.min=min
        self.max=max
        self.orden=0

    def generador(self): #Generador de los 64 valores del sensor, a falta de un sensor real.
        if self.modo == "mockup": #Generamos los datos de manera aleatoria
            datosSensor=np.random.randint(self.min, self.max+1,size=64,dtype=np.uint16)
        else:#Esto sustituiría al caso de un sensor real. Dado que no disponemos de un sensor real, ponemos valores que incrementan.
            datosSensor=np.full(64,self.orden,dtype=np.uint16)
            self.orden = (self.orden +1) % (2**16)
        return datosSensor
    
if __name__ == "__main__":
    sensor=Sensor("mockup",0,1000)
    valores=sensor.generador()
    print(valores)