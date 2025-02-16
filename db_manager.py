import sqlite3

class Database:
    def __init__(self, nombre="sensor_infrarrojo.db"):
        self.nombre = nombre
        self.conexion = sqlite3.connect(self.nombre)
        self.cursor = self.conexion.cursor()
        self.create_table()
       
    def create_table(self):
        columns = ",\n                ".join([f"num{i} INTEGER CHECK(num{i} BETWEEN 0 AND 65535)" for i in range(1, 65)])
        query = f'''
            CREATE TABLE IF NOT EXISTS valoresInfrarrojo (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                {columns}
            )
        '''
        self.cursor.execute(query)
        self.conexion.commit()

    def escritura(self, valores):
        if len(valores) != 64:
            raise ValueError("Se requieren exactamente 64 valores.")
        placeholders = ", ".join(["?"] * 64)
        query = f"INSERT INTO valoresInfrarrojo ({', '.join([f'num{i}' for i in range(1, 65)])}) VALUES ({placeholders})"
        self.cursor.execute(query, valores)
        self.conexion.commit()

    def lectura(self):
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