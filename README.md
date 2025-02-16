# prueba_nivel
Prueba de nivel desarrollo Python asociada a la Tarea 1 que se muestra en el PDF adjunto.

# Clonar repositorio
Para clonar el repositorio, ejecutar este código en terminal.

```bash
git clone https://github.com/alexeimoliboga/prueba_nivel.git
```

# Ejecución
Para su ejecución, es necesario disponer de las librerías numpy, nats y nats-server instalado en el equipo.

Para ejecutar el código, es obligatorio utilizar los siguientes argumentos:
--periodo : que va seguido de un número que señala cada cuantos segundos se lee y escribe en la base de datos del sensor.
--uri : que va seguido de la URI de la base de datos que se vaya a utilizar.
--modo : que va seguido del valor "mockup" o "real", dependiendo del origen de los datos.

En caso de que --modo tome el valor "mockup" es obligatorio que exista el siguiente argumento tambien:
--rango : que va seguido de dos números, que son el valor mínimo y máximo que tomaran los valores generados aleatoriamente por el mockup.

Así, obtendremos dos posibles estilos de comando por terminal:

MOCKUP:
```bash
python3 main.py --modo mockup --rango 123 4567 --periodo 4 --uri "file:sensor_infrarrojo.sqlite?mode=rwc"
```
REAL:
```bash
python3 main.py --modo real --periodo 4 --uri "file:sensor_infrarrojo.sqlite?mode=rwc"
```

Con ambos comandos se evaluará los argumentos proporcionados y se lanzarán dos hilos, uno que escribirá los valores del sensor (mockup o real serán ficticios, ya que no disponemos de sensor), y otro hilo de lectura de dichos datos y escritura en la base de datos. El hilo de lectura cuenta a su vez con un hilo que comprueba la pulsación de teclas para pausar o finalizar la aplicación.

Como se dijo antes, tanto mockup como real son ficticios, por lo que mockup genera valores aleatorios dentro del rango establecido en los argumentos, y real genera los 64 numeros del sensor identicos y aumentando a razón de 1 por segundo.

# Funcionamiento

Una vez ejecutado, la aplicación generará la base de datos si no existe e irá añadiendo el último dato leído cada --periodo segundos. Si se pulsa p, se pausará dicha lectura y escritura en la base de datos. Si se vuelve a pausar, se reanudará dicha lectura y escritura.
Para finalizar su ejecución, es necesario pulsar la tecla q.