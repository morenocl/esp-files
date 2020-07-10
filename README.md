## Modulos y scripts para ejecutar en esp8266 con Micropython


[Micropython](https://micropython.org/) es una eficiente implementacion de Python3 que incluye uno pequeño subconjunto de la libreria estandar de Python y esta optimizado para ejecutarse en microcontroladores.


El [ESP8266](https://es.wikipedia.org/wiki/ESP8266) es un chip de bajo costo Wi-Fi con un stack TCP/IP completo y un microcontrolador, fabricado por Espressif.  
Posee un Xtensa LX106 a 80 MHz, RAM de instrucción de 64 KiB, RAM de datos de 96 KiB, flash de 4MiB, IEEE 802.11 b/g/n Wi-Fi, y mas.


Contiene:
+ myhttp:  
 - Implementacion ultrapequeña del protocolo http. Este unicamnete implementa metodos GET y POST, con los codigos de respuesta 200 y 404.  
 - Ejecutar `import myhttp` y ya esta corriendo un servidor!
+ ftp-server:
 - Pequeño servidor ftp. Permite listar archivos, obtener su tamaño y descarga total o parcial.
 - Primero `from ftpserver import Server` luego `ftp = Server()` y finalmente `ftp.serve()` y ya tiene su server ftp ejecutando!
 + wlan:
  - Una simple funcion para conectar al wifi.



-------------


## Modules and scripts to run on esp8266 with Micropython


[Micropython](https://micropython.org/) is a lean and efficient implementation of the Python 3 programming language that includes a small subset of the Python standard library and is optimised to run on microcontrollers and in constrained environments.  


The [ESP8266](https://es.wikipedia.org/wiki/ESP8266) is a low-cost Wi-Fi microchip, with a full TCP/IP stack and microcontroller capability, produced by Espressif.  
Processor Xtensa LX106 @ 80 MHz, 64 KiB instruction RAM, 96 KiB data RAM, 4MiB flash memory, IEEE 802.11 b/g/n Wi-Fi, and more.


Content:
+ myhttp:  
 - Ultra small implementation of http protocol. This only implement GET and POST methods, with 200 and 404 responde codes.  
 - Run `import myhttp` and a server is already running!
+ ftp-server:
 - Little server ftp. Allows listing file, obtain size and full or partial download.
 - First `from ftpserver import Server` then `ftp = Server()` finally `ftp.serve()` and a ftp server is already running!
+ wlan:
 - A simple function to connect to wifi.
