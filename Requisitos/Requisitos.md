Este proyecto consistirá en desarrollar un sistema que permita traducir de manera automática textos manuscritos y otra serie de funcionalidades para su digitalización y compartición.

De manera introductoria, se expondrán en este documento una lista de requisitos funcionales para el software, con sus respectivos criterios de validación:

**RF1 – Reconocimiento de Escritura Manual:** El sistema debe ser capaz de reconocer y digitalizar la escritura manual en diversos estilos de escritura.

*Validación:*
- Se debe lograr una tasa de reconocimiento de al menos el 90% en una muestra de escritura manual diversa.
- Debe ser capaz de reconocer diferentes idiomas y estilos de escritura.

**RF2 – Procesamiento de Imágenes:** El sistema debe ser capaz de procesar imágenes de textos manuscritos, ya sea escaneados o capturados con cámaras.

*Validación:*
- Debe admitir una variedad de formatos de imagen, incluyendo JPG, PNG y PDF.

**RF3 – Traducción Automática:** El sistema debe traducir el texto manuscrito a un idioma objetivo específico.

*Validación:*
- La traducción debe tener una precisión de al menos el 90% en una muestra de texto de prueba.
- Debe admitir al menos tres idiomas diferentes como origen y destino.

**RF4 - Captura de texto manuscrito:** Debe tener la capacidad de capturar el texto manuscrito.

*Validación:*
- Captura mediante dispositivos como cámara, escáneres...
- Uso de almacenamiento y gestión de datos para capturar el texto y gestionarlo.

**RF5 – Interfaz de Usuario Intuitiva:** El sistema debe contar con una interfaz de usuario amigable para que los usuarios puedan cargar imágenes y visualizar las respectivas traducciones.

*Validación:*
- Los usuarios deben poder cargar imágenes y obtener traducciones con solo unos pocos clics y sin necesidad de capacitación previa.
- Debe ser compatible con dispositivos móviles y navegadores web.

**RF6 – Privacidad y seguridad:** Se deben implementar medidas de seguridad para proteger la privacidad de los usuarios y garantizar la confidencialidad de los datos que se traducen.

*Validación:*
- Mediante encriptación de datos, accesos autorizados, cumplimiento de normas vigentes, protección contra ataques...

**RF7 - Capacidades de edición y corrección:** Se debe permitir a los usuarios editar y corregir las traducciones generadas.

*Validación:*
- Deben estar disponibles herramientas de edición intuitivas.
- Los cambios realizados por los usuarios deben reflejarse de manera correcta en las traducciones finales.

**RF8 - Documentación y soporte:** Debe contar con documentación detallada y soporte técnico para que los usuarios puedan comprender y utilizar eficazmente el sistema.

*Validación:*
- Creación de guías de usuario, tutoriales, soporte técnico, foros de usuario...

**RF9 - Precisión y velocidad:** Se debe buscar un equilibrio entre la precisión de la traducción y la velocidad de procesamiento, para que el sistema sea útil en situaciones en tiempo real.

*Validación:*
- Creación de guías de usuario, tutoriales, soporte técnico, foros de usuario...

**RF10 - Compatibilidad de idiomas:** Debe ser capaz de manejar una amplia variedad de idiomas. Esto nos permite cierta escalabilidad en el sistema introduciendo más idiomas en un futuro.

*Validación:*
- Soporte de múltiples idiomas, traducciones adaptadas al idioma que se quiera utilizar, escalabilidad...
- Feedback de usuarios que pueden ayudar a corregir errores...

**RF11 - Aprendizaje automático y mejora continua:** El sistema debe tener la capacidad de aprender y mejorar con el tiempo a medida que se utilizan más datos y se reciben retroalimentaciones de los usuarios.

*Validación:*
- Sistema que recopile la información introducida por el usuario y aprenda (IA), feedback de usuario y actualizaciones, uso de modelos de aprendizaje, evaluación de errores...

**RF12 – Compartir Textos y Traducciones:** Se debe permitir a los usuarios compartir los textos originales y las traducciones generadas con otros usuarios o plataformas externas.

*Validación:*
- Los usuarios podrán seleccionar y compartir tanto el texto original como la traducción.
- Se proporciona la opción de compartir a través de enlaces o redes sociales populares, como Facebook y Twitter.
- Los textos y traducciones son accesibles de manera pública o de forma privada, según las preferencias del usuario.

**RF13 - Corrección gramatical y ortográfica:** El sistema incluirá una funcionalidad que permita la corrección de errores gramaticales y ortográficos en el texto introducido para mejorar la calidad del texto del cliente. Dos opciones: corregirlo directamente, lo que podría llevar a cambios que el usuario no desea, o corrección de forma automática que debería incluir una opción de volver atrás por si el usuario no lo desea.

*Validación:*
- Uso de traductor que cambie el texto al idioma que desee el usuario, evaluación de coherencia...
