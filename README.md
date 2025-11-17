# desarrollo_web_Pablo_Suarez/Tarea-4.
Este es mi proyecto de desarrollo web con HTML CSS y JavaScript, ahora hecho con java y spring boot para el backend.

### Organización.
Esta tarea se encuentra en una carpeta aparte de la carpeta app, donde se encuentra todo el trabajo previo. Esto es así debido a que se usa un lenguaje y framework diferente para el backend, por lo que no era posible compatibilizar los proyectos a partir de esta tarea. Por ende, todo lo anterior funciona sin lo nuevo y, así mismo, lo nuevo funciona sin lo antíguo.

### Templates.
Para los templates se uso Thymelife para hacer los ciclos each de la tabla de avisos. Dado que toda la tarea era desarrollar una sola pantalla con objetos que se iban a usar solo una vez, no fue necesario el uso de fragmentos para los elementos de la página.

### MVC.
Para poder cumplir con lo pedido en la tarea, se implementó el programa según la arquitectura de Modelo Vista Controlador (MVC). Implementé el modelo para nota, aviso de adpoción y comuna, puesto que de estos era de donde provenía la informacion principal a proporcionar; se hizo un archivoRepository para autorizar a acceder a la información que cada uno necesitara; un archivo como servicio para así poder intercambiar la informacion que recogieran los .Repository y mandarla a las url correspondiente. Se implementó las clases de app y api usuales para el manejo de rutas, html y llamadas asincrónicas por parte del JS. Por su puesto existe el HTML y JS encargados de la vista del programa. Se tomó la desición de que todos los links del programa retornen a la misma pantalla de notas por simplicidad, ya que no se pide nada más; con la base de datos de las entregas pasadas ya se cumple el cometido

### Archivos JS.
Par esta entrega solo fué necesario un archivo js (evaluation.js) ya que solo habia que validar la nota que el usuario ingrese del lado del frontend, además de la logica de despliege de intefaz o el manejo de errores generales. Se usaron funciones asincrónicas como fetch para poder comunicarse con el backend y verificar que los datos se hayan guardado de manera correcta.

### Database.
En los archivos de la base de datos hay dos agregados. El primer archivo es el responsable de generar la nueva tabla para las notas, el segundo carga todos los datos necesarios con ordenes SQL, en vez de hacerlo con el __init__ de la app, así se distribuye mejor la responsabilidad y simplifica el código, además de hacerlo todo mucho más rápido.

### Archivo CSS.
Todo el CSS pertienente a la página web se encuentra en un solo arcivo llamado style. En este caso sigue siendo el mismo para las entregas pasadas. Hay que mantener la coherencia visual.

### Dificultades.

Para hacer esta tarea tuve 2 días aproximadamente, esto debido a la fuerte carga académica. Dado que esta tarea era un java y spring boot (un lenguaje y un framework que no habia visto en mi vida), se me hizo mucho más difícil entender el orden lógico de los programas para poder hacer lo que quería. Muchas veces tuve que ver el video del aux 10 una y otra vez; copiando y pegando del archivo del aux en ocaciones; vindo linea por linea para aprender que cosa hace qué. Luego de terminar el backend, pasé al front, y ahí la cosa mejoró un poco, dado a que, por lo menos, algo puedo hacer en JS.
