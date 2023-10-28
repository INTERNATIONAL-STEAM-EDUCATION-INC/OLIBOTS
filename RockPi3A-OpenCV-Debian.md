# Pasos para instalar libmraa y Open CV en RockPi 3A 2GB
# utilizando python 3.9.2
# instalado Debian Bullseye xfce b25 publicado el 28 de agosto 2023
# usando esta imagen del repositorio oficial de Radxa
# https://github.com/radxa-build/rock-3a
# descargamos la imagen para el RockPi 3A 
# https://github.com/radxa-build/rock-3a/releases/download/b25/rock-3a_debian_bullseye_xfce_b25.img.xz
# usando paquetes de debian stable bullseye main
# SoC RK3568
# se instala la libreria mraa para manipulacion de pines
# Se recomienda conectar una memoria usb de por lo menos 4GB y configurarla como memoria SWAP


# Paso 01 - actualizar la librerias

    sudo apt-get update -y && sudo apt-get upgrade -y
#--------------------------------------------------------------------------------------------------------------------------------------

# Paso 02 - Instalacion de paquetes recomendados
# Debemos iniciar sesion en la interfaz grafica con el usuario y contrasena " rock ", y luego en la terminal ejecutar el comando.
    
    sudo apt-get install -y build-essential thonny gcc git wget mlocate curl cheese dpkg cmake pkg-config ccache python2 python3 python3-pip python3-dev libpng-dev libjpeg-dev libeigen3-dev ffmpeg libavcodec-dev libavformat-dev libswscale-dev libavresample-dev libgstreamer1.0-dev libgstreamermm-1.0-dev libgtk-3-dev libgtkglext1-dev libgtkglextmm-x11-1.2-dev apt-utils python3-setuptools python3-opencv python3-numpy virtualenv libxslt1-dev zlib1g zlib1g-dev libglib2.0-0 libsm6 libgl1-mesa-glx libprotobuf-dev libmraa-dev libmraa2 libmraa2-dbgsym mraa-examples mraa-examples mraa-tools mraa-tools-dbgsym python3-mraa python3-mraa-dbgsym 

# Luego de instalados los paquetes vamos a actualizar el manejador " pip " a la version mas reciente
    
    pip3 install --upgrade pip

# Una vez actualizado pip vamos a instalar la libreria " numpy "

    pip3 install numpy

# -------------------------------------------------------------------------------------------------------------------------------------------

# Paso 03 - prueba de OpenCV

    python3  # abre el interprete de python en la terminal

        import cv2 as cv  # importa la libreria
        print( cv.__version__ )   #  para ver la version instalada

# nos aparecera algo como version 4.5.0 
# aqui vamos a descargar el otro codigo del repo " DeteccionDeColoresRojoVerde.py " y guardarlo en le directorio home del rock pi en este caso ~
# 
# -------------------------------------------------------------------------------------------------------------------------------------------

# si funciono estas pruebas, vamos a la interfaz grafica del rockpi, y vamos a la terminal y ejecutar thonny como super usuario

    sudo thonny
# Abrimos el programa " DeteccionDeColoresRojoVerde.py " al abrir deber accionarse la camara web y detectar color rojo y verde.     

# ----------------------------------------------------------------------------------------------------------------------------------------

# Paso 04 - Instalacion de Arduino IDE

    cd ~
    wget https://downloads.arduino.cc/arduino-1.8.19-linuxaarch64.tar.xz
    tar -xf https://downloads.arduino.cc/arduino-1.8.19-linuxaarch64.tar.xz
    cd rduino-1.8.19-linuxaarch64
    sudo sh install.sh
    sudo usermod -a -G dialout rock




