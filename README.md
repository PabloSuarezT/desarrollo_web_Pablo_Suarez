# desarrollo_web_Pablo_Suarez.
Este es mi proyecto de desarrollo web con HTML CSS y JavaScript. A continuación algunas consideraciones.

### Organización.
Para esta tarea se organizó todo de tal forma que el framework de trabajo flask pueda interpretar el proyecto. Se tiene una carpeta central llamada app con todas las carpetas que, a su vez, contienen todos los archivos.

### Templates.
Aqui se encuentran todos los archivos html del programa. El programa base.html corresponde a una futura refactorizacion de la página para mejorar el funcionamiento. 


### Archivos JS.
Decidí separa los archivos JS en tres: 
- region_comuna.JS, que contiene el código pertinente para la pestaña de formulario de adopción (se actualizan las comunas segun la region y validaciones).
- Listado.JS, que contiene todo lo necesario para poder ver el listado de adpción con la pestaña de información detallada. También maneja la lógica para agregar comentarios del lado del frontend.
- Graficos.JS, que contiene todo lo necesario para mostrar los graficos en la seccion de estadisticas.  Se usó fetch para modelar los gráficos según los datos de la base de datos 
- adopcion.js: este fue ana adicion que por ahora no hace nada. responde a una funcionalidad futura que no pude implementar.

### Database.
Aqui se encuentra todo lo relacionado a la comunicación con la base de datos y la página, así como la correcta configuración del server. host y la base misma. Tambien están los archivos sql necesarios para crear las tablas y rellenar las comunas y regiones, parte clave del formulario de adpoción.

### utils.
Aquí se encuentra el archivo que hace las validaciones del lado del servisor para evitar que  malos datos (inyecciones código o ataques) ingresen.

### Archivo CSS.
Todo el CSS pertienente a la página web se encuentra en un solo arcivo llamado style.

### Dificultades.

La dificultad en esta entrega fué agregar La funcionalidad de comentario y arreglar errores de funcionamiento anteriores. En un principio intenté complejizar el programa, pero decidí dar marcha atras y agregar todos los cambios necesarios en los arcivos que ya tenía.
