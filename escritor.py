import asyncio
import logging
import signal
from nats.aio.client import Client as NATS
from sensor_ficticio import Sensor

# Configuración del logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class SensorEscritorNATS:
    def __init__(self, modo="mockup", min=0, max=(2**16-1), server="nats://localhost:4222", subject="sensor.infrarrojo"):
        self.server = server
        self.subject = subject
        self.nc = NATS()
        self.sensorInfrarrojo = Sensor(modo, min, max)
        self.running = True  # Variable para manejar la ejecución segura

    async def connect(self):
        try:
            await self.nc.connect(self.server)
            logging.info(f"Conectado a {self.server}")
        except Exception as e:
            logging.error(f"Error conectando a NATS: {e}")
            raise

    async def publicar(self):
        await self.connect()
        try:
            while self.running:
                valoresInfrarrojo = self.sensorInfrarrojo.generador()
                await self.nc.publish(self.subject, valoresInfrarrojo.tobytes())
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            logging.warning("Publicación cancelada.")
        finally:
            await self.nc.close()
            logging.info("Conexión cerrada.")

    def stop(self):
        """Método para detener el bucle de publicación de manera segura."""
        self.running = False

async def main():
    sensor = SensorEscritorNATS(modo="real")

    # Manejo de señales para apagar correctamente
    loop = asyncio.get_running_loop()
    for sig in (signal.SIGINT, signal.SIGTERM):
        loop.add_signal_handler(sig, sensor.stop)

    await sensor.publicar()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Interrupción detectada. Saliendo...")

