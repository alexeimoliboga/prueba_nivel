import asyncio
import numpy as np
import logging
from nats.aio.client import Client as NATS
import db_manager

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SensorLectorNATS:
    """Clase que lee datos de NATS y los almacena en una base de datos."""

    def __init__(self, periodo=1, uripath="file:sensor_infrarrojo.sqlite?mode=rwc", server="nats://localhost:4222", subject="sensor.infrarrojo"):
        self.periodo = periodo
        self.server = server
        self.subject = subject
        self.nc = NATS()
        self.dataBase = db_manager.Database(uripath=uripath)

    async def connect(self):
        """Conectar al servidor NATS con reintentos en caso de fallo."""
        for _ in range(5):  # Intentar conectar hasta 5 veces
            try:
                await self.nc.connect(self.server)
                logging.info(f"Conectado a NATS en {self.server}")
                return
            except Exception as e:
                logging.warning(f"Error al conectar a NATS: {e}")
                await asyncio.sleep(2)  # Esperar antes de reintentar
        logging.error("No se pudo conectar a NATS después de varios intentos.")
        raise ConnectionError("Error crítico al conectar con NATS.")

    async def message_handler(self, msg):
        """Procesa los mensajes recibidos del servidor NATS."""
        try:
            data = np.frombuffer(msg.data, dtype=np.uint16)
            dataDB = data.tolist()
            logging.info(f"Mensaje recibido: {dataDB}")
            self.dataBase.escritura(dataDB)
        except Exception as e:
            logging.error(f"Error procesando mensaje: {e}")

    async def subscribe(self):
        """Suscribirse al canal de NATS y procesar mensajes indefinidamente."""
        try:
            await self.connect()
            await self.nc.subscribe(self.subject, cb=self.message_handler)
            logging.info(f"Suscrito al tema '{self.subject}'")
            while True:
                await asyncio.sleep(self.periodo)
        except Exception as e:
            logging.error(f"Error en la suscripción: {e}")
        finally:
            await self.nc.close()
            logging.info("Conexión cerrada correctamente.")

# Ejecutar la clase
if __name__ == "__main__":
    try:
        subscriber = SensorLectorNATS(periodo=3)
        asyncio.run(subscriber.subscribe())
    except KeyboardInterrupt:
        logging.info("Proceso interrumpido por el usuario.")
    except Exception as e:
        logging.critical(f"Error fatal: {e}")