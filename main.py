import logging
import threading
import signal
import os
import asyncio
from lector import SensorLectorNATS, key_listener
from parser import Parseador
from escritor import SensorEscritorNATS

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_sensor_lector(sensor):
    """Ejecuta el lector de NATS en un hilo separado con su propio bucle de eventos."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(sensor.subscribe())

def run_publicador(publicador):
    """Ejecuta el publicador en un hilo separado con su propio bucle de eventos."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(publicador.publicar())

if __name__ == "__main__":
    # Parsear argumentos
    parsero = Parseador()
    args = parsero.parsear()

    # Crear el lector de NATS
    lector = SensorLectorNATS(periodo=args.periodo, uripath=args.uri)

    # Crear el publicador con los parámetros de línea de comandos
    if args.modo == "mockup":
        publicador = SensorEscritorNATS(modo=args.modo, min=args.rango[0], max=args.rango[1])
    else:
        publicador = SensorEscritorNATS(modo=args.modo)

    # Lanzar el lector en un hilo separado
    thread_lector = threading.Thread(target=run_sensor_lector, args=(lector,), daemon=True)
    thread_lector.start()

    # Lanzar el publicador en otro hilo separado
    thread_publicador = threading.Thread(target=run_publicador, args=(publicador,), daemon=True)
    thread_publicador.start()

    # Capturar señales para apagado seguro
    def shutdown_handler(signum, frame):
        logging.info("Señal de apagado recibida. Cerrando procesos...")
        lector.stop()
        publicador.stop()  # Agregamos el método stop en la clase del publicador
        thread_lector.join()
        thread_publicador.join()
        logging.info("Todos los procesos han finalizado correctamente.")
        os._exit(0)

    # Manejar señales
    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    # Iniciar detección de teclas (pausa con 'p', salida con 'q')
    key_listener(lector)

