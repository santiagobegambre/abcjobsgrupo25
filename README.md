# Validación del Experimento para ABC Jobs
Este repositorio contiene el código y la documentación relacionada con la validación del experimento realizado para ABC Jobs. El enfoque principal de este experimento es monitorear el componente de servicio de pruebas en un entorno controlado. Además, se busca establecer un sistema asincrónico para notificar las fallas detectadas a través de una plataforma de mensajería.

## Video Semana 5
Para visualizar el video explicativo de click en el siguiente [enlace](https://www.youtube.com/)

## Instrucciones para Realizar la Prueba
Siga estos pasos para realizar la prueba utilizando los servicios creados para el ejemplo (Usuario, pruebas, registro de fallas y administrador):

1. Crear un Entorno Virtual
python -m venv myenv
2. Activar el Entorno Virtual (en Windows)
myenv\Scripts\activate
3. Activar el Entorno Virtual (en macOS/Linux)
source myenv/bin/activate
4. Instalar Flask
pip install Flask

## Configuración del API Gateway
En este ejemplo, utilizamos la configuración proxy del servidor Nginx para implementar el componente API Gateway. Esta configuración permite que todas las solicitudes se hagan al servidor Nginx y este redireccione al servicio correspondiente de acuerdo a la operación y ruta especificada en el URL.

## Dockerización
Todo el entorno de prueba está dockerizado para facilitar la configuración y ejecución. Asegúrese de tener Docker instalado y siga las instrucciones para ejecutar cada uno de los componentes en contenedores Docker.

## Integrantes del Grupo
|Nombre                      | Correo                      |
|----------------------------|-----------------------------|
|  Santiago Begambre Poveda  | s.begambre@uniandes.edu.co  |
|  Carlos Castillo Fuentes   | c.castillof@uniandes.edu.co |
|  Nestor Rodriguez Garcia   | na.rodriguez2@uniandes.edu.co |
