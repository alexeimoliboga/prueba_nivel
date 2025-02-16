import argparse

class Parseador(): #Parser de argumentos por linea de comandos
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="""Script que lee cada n segundos 
        los datos obtenidos de un sensor, real o simulado, y almacena los datos en una base de datos. 
        En caso de ser valores simulados, se debe establecer el rango de valores a simularse""")
        #Añadimos los 4 argumentos. El argumento --rango depende de --modo.
        self.parser.add_argument("--modo",type=str, choices=["mockup", "real"],required=True, help="""Modo de extracción de la 
        información del sensor. Los valores disponibles son 'mockup' para valores simulados y 'real' para datos reales""")
        self.parser.add_argument("--periodo", type=int, required=True, help="""Número que representa el periodo de 
        lectura del sensor en segundos""")
        self.parser.add_argument("--rango", type=int, nargs=2, metavar=("MIN", "MAX"),required="--modo" in "mockup", help="""Valor 
        mínimo y máximo del rango de los valores simulados del sensor en modo 'mockup'""")
        self.parser.add_argument("--uri", type=str, required=True, help="""URI de conexión con la base de datos SQL""")
        
    def parsear(self):
        args = self.parser.parse_args()
        if args.modo == "mockup" and not args.rango:
            self.parser.error("El argumento --rango es obligatorio cuando --modo tiene como valor'mockup'.")
        return args

if __name__ == "__main__":
    parsero=Parseador()
    argumentos=parsero.parsear()
    print("Periodo:",argumentos.periodo,", URI:",argumentos.uri,", Modo:",argumentos.modo)
    if argumentos.modo=="mockup":
        print("Rango:",argumentos.rango[0],"-",argumentos.rango[1])