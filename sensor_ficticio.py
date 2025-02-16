import random

class Sensor():
    def __init__(self,min,max):
        self.min=min
        self.max=max

    def generador(self):
        datosSensor=[]
        for __ in range(64):
            datosSensor.append(random.randint(self.min, self.max))
        return datosSensor
    
if __name__ == "__main__":
    sensor=Sensor(50,78)
    valores=sensor.generador()
    print(valores)