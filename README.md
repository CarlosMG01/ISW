# Proyecto OCR

Participantes: 

##Dockerfile 

Lo primero será descargarse Docker. Para ello se irá a la página: https://www.docker.com/products/docker-desktop/
y se descargará la versión compatible con el sistema operativo. Luego habrá que abrir el instalador. Una vez terminado el instalador ya se tendrá Docker instalado, pero también habrá que abrir la aplicación y registrarse. Si ya se posee una cuenta Docker solo habrá que darle a sign in y poner los credenciales. Si no se posee una cuenta Docker se creará una dándole a sign up y completando los pasos. También hay la posibilidad de no iniciar sesion, pero esta no se recomienda pues los proyectos no se guardarían en una cuenta.   

Lo siguiente será darle permisos de ejecución a los scripts:
```
chmod +x containerRun.sh
```
Lo siguiente será generar la imagen que usaremos en el contenedor, para ello se hará:
```
docker build -t app-flask .
```

Lo siguiente será ejecutar el primer script:
```
./conteinerRun.sh
``` 

Es importante tener la aplicación Docker encendida, sino no podrá encontrar los contenedores.
