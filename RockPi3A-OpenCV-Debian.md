# Pasos para instalar libmraa y Open CV en RockPi 3A 2GB
# utilizando python 3.8.10
# instalado Debian Bullseye xfce b25 publicado el 28 de agosto 2023
# usando esta imagen del repositorio oficial de Radxa
# https://github.com/radxa-build/rock-3a
# descargamos la imagen para el RockPi 3A 
# https://github.com/radxa-build/rock-3a/releases/download/b25/rock-3a_debian_bullseye_xfce_b25.img.xz
# usando paquetes de debian stable bullseye main
# SoC RK3568
# se instala la libreria mraa para manipulacion de pines
# Se recomienda conectar una memoria usb de por lo menos 4GB y configurarla como memoria SWAP


# Paso 01 - OMITIR


#--------------------------------------------------------------------------------------------------------------------------------------

# Paso 02 - actualizar la librerias

    sudo apt-get update -y && sudo apt-get upgrade -y
#--------------------------------------------------------------------------------------------------------------------------------------

# Paso 03 - Instalacion de Interfaz Grafica - OMITIR

    sudo apt-get install -y xfce4 xubuntu-desktop
#--------------------------------------------------------------------------------------------------------------------------------------


# Paso 04 - Instalacion de paquetes recomendados
# Debemos iniciar sesion en la interfaz grafica con el usuario y contrasena " rock ", y luego en la terminal ejecutar el comando.
    
    sudo apt-get install -y build-essential thonny gcc git wget mlocate curl cheese dpkg cmake pkg-config ccache python2 python3 python3-pip python3-dev libpng-dev libjpeg-dev libeigen3-dev ffmpeg libavcodec-dev libavformat-dev libswscale-dev libavresample-dev libgstreamer1.0-dev libgstreamermm-1.0-dev libgtk-3-dev libgtkglext1-dev libgtkglextmm-x11-1.2-dev apt-utils python3-setuptools python3-opencv python3-numpy virtualenv libxslt1-dev zlib1g zlib1g-dev libglib2.0-0 libsm6 libgl1-mesa-glx libprotobuf-dev libmraa-dev libmraa2 libmraa2-dbgsym mraa-examples mraa-examples mraa-tools mraa-tools-dbgsym python3-mraa python3-mraa-dbgsym

# Luego de instalados los paquetes vamos a actualizar el manejador " pip " a la version mas reciente
    
    pip3 install --upgrade pip

# Una vez actualizado pip vamos a instalar la libreria " numpy "

    pip3 install numpy

# -------------------------------------------------------------------------------------------------------------------------------------------

# Paso 05 - aumentar la memoria swap a por el tamano de la memoria USB

    lsblk   # esto nos dara la identificacion de la memoria usb algo como por ejemplo: /dev/sda
    
    sudo blkid   # esto nos dara la indentificacion unica de todos los volumenes de memoria

    # se enlistara todos los volumenes de memoria, prestar atencion al conectado en /dev/sda debemos guardar el valor UUID de la memoria 
    # esta tendra una forma="XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"

    sudo umount /dev/XXX # aqui nos aseguramos que la memoria no este en uso, ejemplo que /dev/sda no este montada ni en uso
    sudo mkswap /dev/XXX # aqui formateamos la memoria en configuracion SWAP
    sudo nano /etc/fstab # editaremos el archivo fstab que nos permite especificar la memoria SWAP

    # debemos agregar la linea  " UUID=XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX none swap sw,pri=5 0 0  " donde remplazamos las X por el valor obtenido anteriormente.

    sudo swapon -a  # activa la memoria SWAP ahora dentro de la memoria USB

    free -m   # para comprobar que la memoria SWAP esta configurada y habilitada.

# ----------------------------------------------------------------------------------------------------------------------------------------

# Paso 06 - descargar e instalar biblioteca OpenBLAS

    cd ~
    get -O openblas.zip https://github.com/xianyi/OpenBLAS/releases/download/v0.3.23/OpenBLAS-0.3.23.zip
    unzip openblas.zip
    cd OpenBLAS-0.3.23
    make all -j4    # esperar un momento en que compila, esto utlizara los 4 cpu del rockpi
    sudo make install  #esperar a que termine


# ----------------------------------------------------------------------------------------------------------------------------------------

# Paso 07 - descargar e instalar biblioteca OpenCV

    `cd ~`
    `wget -O opencv.zip https://github.com/opencv/opencv/archive/refs/tags/4.8.0.zip`
    `unzip opencv.zip`
    `cd opencv`
    `mkdir -p build && cd build`
    `cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_VERBOSE_MAKEFILE=ON -DCMAKE_INSTALL_PREFIX=/opt/opencv -DWITH_OPENGL=ON -DOPENCV_ENABLE_NONFREE=ON -DWITH_QT=ON -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF -DOPENCV_GENERATE_PKGCONFIG=ON  -DWITH_1394=OFF -DBUILD_opencv_python2=OFF -DBUILD_opencv_python3=ON -DPYTHON3_LIBRARY=$(python3 -c "from distutils.sysconfig import get_config_var;from os.path import dirname,join ; print(join(dirname(get_config_var('LIBPC')),get_config_var('LDLIBRARY')))") -DPYTHON3_NUMPY_INCLUDE_DIRS=$(python3 -c "import numpy; print(numpy.get_include())") -DPYTHON3_PACKAGES_PATH=$(python3 -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")`

    # Esperar a que termine

    `make all -j4`
    # Esperar a que termine

    `make install`
    # Esperar a que termine

# ----------------------------------------------------------------------------------------------------------------------------------------

# Paso 08 - prueba de OpenCV

    `python3`  # abre el interprete de python en la terminal

        `import cv2 as cv`    # importa la libreria
        `print( cv.__version__ )`   #  para ver la version instalada

# nos aparecera algo como version 4.2.0 
# aqui vamos a descargar el otro codigo del repo " DeteccionDeColoresRojoVerde.py " y guardarlo en le directorio home del rock pi en este caso ~
# 

# ----------------------------------------------------------------------------------------------------------------------------------------

# Paso 09 - Instalacion y prueba de libmraa

#Copia de ejemplos de codigos
    
    `sudo cp -av /usr/local/share/mraa/examples/ /home/rock/mraa-examples`

# Verificacion de libreria
    
    `mraa-gpio list`

# realizacion de pruebas de puertos
# importante senalar que estamos usando el usuario rock y para esta prueba debemos ser super usuario con el comando

    `sudo mraa-gpio set 40 1` // esto deberia encender un led conectado al pin
    `sudo mraa-gpio set 40 0` // esto deberia apagar un led conectado al pin

# si funciono estas pruebas, vamos a la interfaz grafica del rockpi, y vamos a la terminal y ejecutar thonny como super usuario

    `sudo thonny`

#una vez abierto vamos a buscar los ejemplos en la carpeta "/home/rock/mraa-examples" donde vamos a abir el archivo gpio.py
#vamos a hacer la prueba de circuito y coloquemos play.


