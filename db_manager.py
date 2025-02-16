import sqlite3

class Database: #Clase de creación, escritura y lectura de base de datos asociada
    def __init__(self, uripath="file:sensor_infrarrojo.sqlite?mode=rwc"):
        self.conexion = sqlite3.connect(uripath,uri=True)
        self.cursor = self.conexion.cursor()
        self.create_table()
       
    def create_table(self): #Creación de tabla con ID y los 64 numeros con valores entre 0 y 65535
        columns = ",\n                ".join([f"num{i} INTEGER CHECK(num{i} BETWEEN 0 AND 65535)" for i in range(1, 65)])
        query = f'''
            CREATE TABLE IF NOT EXISTS valoresInfrarrojo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns}
            )
        '''
        self.cursor.execute(query)
        self.conexion.commit()

    def escritura(self, valores): #Escritura en la base de datos
        if len(valores) != 64:
            raise ValueError("Se requieren exactamente 64 valores.")
        placeholders = ", ".join(["?"] * 64)
        query = f"INSERT INTO valoresInfrarrojo ({', '.join([f'num{i}' for i in range(1, 65)])}) VALUES ({placeholders})"
        self.cursor.execute(query, valores)
        self.conexion.commit()

    def lectura(self): #Lectura de la base de datos
        self.cursor.execute("SELECT * FROM valoresInfrarrojo")
        rows = self.cursor.fetchall()
        for row in rows:
            print(row)


    def close(self):
        self.conexion.close()
        print("Conexión cerrada.")

if __name__ == "__main__":
    db = Database()
    db.escritura([i for i in range(64)])
    db.lectura()
    db.close()