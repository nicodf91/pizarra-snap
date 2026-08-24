Las convenciones de desarrollo y documentación establecidas para el proyecto **Pizarra Snap** se estructuran en tres ejes principales para asegurar la legibilidad, consistencia y reproducibilidad del sistema:

### 1. Convenciones de Escritura de Código y Comentarios
* **Código didáctico:** El código del notebook debe mantenerse **simple, breve, comentado, didáctico y reproducible**.
* **Estilo de comentarios:** Los comentarios deben escribirse estrictamente como notas de carácter técnico propias del desarrollo, **evitando expresiones conversacionales** o informales dentro de las celdas de código.
* **Preservación de datos:** Para evitar efectos colaterales en el pipeline, se deben conservar las variables y nombres acordados en los contratos y trabajar sobre **copias de los datos** en lugar de modificar los originales.

### 2. Criterios de Integración y Pruebas
* **Desarrollo incremental:** Cada nuevo módulo debe partir obligatoriamente del resultado validado del módulo anterior.
* **Contratos claros:** Es obligatorio dejar documentado con precisión qué datos de **entrada** recibe el módulo y qué datos de **salida** entrega al siguiente.
* **Validación interna:** Cada entrega debe incluir al menos **una prueba** que permita verificar su correcto funcionamiento antes de avanzar.
* **Revisión cruzada:** Ningún cambio de código se incorpora a la rama principal (`main`) sin haber superado una revisión cruzada por parte de otro integrante del equipo.

### 3. Convenciones de Lenguaje y Documentación
* **Vocabulario consistente:** En toda la documentación se utiliza el término **"pizarra"** de forma homogénea.
* **Terminología de ejecución:** Se denomina formalmente **Run All** a la acción de ejecutar de forma completa todas las celdas del notebook.
* **Actualización del Plan de Trabajo:** Al realizar cambios funcionales, se debe actualizar primero el estado técnico del módulo en la matriz maestra. En caso de agregar registros al historial de integración, estos deben enfocarse en explicar **decisiones y aprendizajes prácticos**, evitando repetir rutinariamente el estado actual.
