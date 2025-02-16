import asyncio
import numpy as np
import logging
import threading
import sys
import tty
import termios
from nats.aio.client import Client as NATS
import db_manager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SensorLectorNATS:
    def __init__(self, periodo=1, uripath="file:sensor_infrarrojo.sqlite?mode=rwc", server="nats://localhost:4222", subject="sensor.infrarrojo"):
        self.periodo = periodo
        self.server = server
        self.subject = subject
        self.nc = NATS()
        self.dataBase = db_manager.Database(uripath=uripath)
        self.ultima_lectura = None  # Último mensaje recibido
        self.paused = False  # Estado de pausa
        self.running = True  # Controlar el cierre seguro

    async def connect(self):
        """Conectar a NATS con reintentos."""
        for _ in range(5):
            try:
                await self.nc.connect(self.server)
                logging.info(f"Conectado a NATS en {self.server}")
                return
            except Exception as e:
                logging.warning(f"Error conectando a NATS: {e}")
                await asyncio.sleep(2)
        logging.error("No se pudo conectar a NATS después de varios intentos.")
        raise ConnectionError("Error crítico al conectar con NATS.")

    async def message_handler(self, msg):
        """Almacenar el último mensaje recibido."""
        self.ultima_lectura = msg

    async def subscribe(self):
        """Suscribirse al tema y procesar datos cada 'periodo' segundos."""
        try:
            await self.connect()
            await self.nc.subscribe(self.subject, cb=self.message_handler)

            while self.running:
                await asyncio.sleep(self.periodo)  # Esperar el tiempo definido
                
                if not self.paused and self.ultima_lectura:  # Solo escribir si no está pausado
                    try:
                        data = np.frombuffer(self.ultima_lectura.data, dtype=np.uint16).tolist()
                        logging.info(f"Procesando mensaje: {data}")
                        self.dataBase.escritura(data)
                    except Exception as e:
                        logging.error(f"Error procesando mensaje: {e}")
                    
                    self.ultima_lectura = None  # Limpiar para esperar el siguiente

        except Exception as e:
            logging.error(f"Error en la suscripción: {e}")
        finally:
            await self.nc.close()
            logging.info("Conexión cerrada correctamente.")

    def toggle_pause(self):
        """Alternar entre pausa y reanudación."""
        self.paused = not self.paused
        if self.paused:
            logging.info("Escritura en base de datos pausada. Pulsa 'p' para reanudar.")
        else:
            logging.info("Escritura en base de datos reanudada.")

    def stop(self):
        """Detener la ejecución del programa."""
        self.running = False
        logging.info("Deteniendo el sistema...")

def key_listener(sensor):
    """Escuchar la tecla 'p' para pausar/reanudar y 'q' para salir."""
    def get_key():
        """Leer un solo carácter sin necesidad de presionar Enter."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            return sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    while sensor.running:
        key = get_key()
        if key == 'p':
            sensor.toggle_pause()
        elif key == 'q':  # Permitir cerrar con 'q'
            sensor.stop()
            break

# Ejecutar
if __name__ == "__main__":
    lector = SensorLectorNATS(periodo=3)
    
    # Iniciar la detección de teclas en un hilo separado
    thread = threading.Thread(target=key_listener, args=(lector,), daemon=True)
    thread.start()
    
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(lector.subscribe())
    except KeyboardInterrupt:
        logging.info("Interrupción detectada (Ctrl + C). Cerrando el sistema...")
        lector.stop()
    finally:
        loop.run_until_complete(lector.nc.close())
        loop.close()
        logging.info("Programa cerrado correctamente.")
