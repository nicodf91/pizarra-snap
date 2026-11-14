---
name: orquestador-pizarra-snap
description: 'Coordinar cambios que abarcan varios módulos de Pizarra Snap o requieren elegir procedimientos para requerimientos, PDF y secretos.'
---

# Orquestar una tarea en Pizarra Snap

1. Delimitá el resultado solicitado, qué archivos podés tocar y qué acciones fueron autorizadas. Identificá los RF y consumidores en el [catálogo](../../../docs/REQUERIMIENTOS.md) y contrastalos con el código.
2. Elegí los procedimientos según el impacto. Leé únicamente las guías que vayas a aplicar y abrí las referencias del PDF cuando sean necesarias.

| Tarea | Procedimiento |
|---|---|
| Incorporar o modificar comportamiento | [agregar-requerimiento](../agregar-requerimiento/SKILL.md) para delimitar impacto y pruebas |
| Cambiar el PDF, sus categorías, temas o adjunto | [informe-pdf](../informe-pdf/SKILL.md) para revisar el contrato o el diseño afectado |
| Revisar credenciales, configuración o transporte de correo | [manejo-de-secretos](../manejo-de-secretos/SKILL.md) para preparar una comprobación simulada |
| Corregir documentación | Contrastar la afirmación con su fuente y validar enlaces. Consultar una skill solo si el área requiere una regla especializada. |

3. Si aplican varias guías, empezá por alcance y contratos, luego revisá el módulo especializado y finalmente validá el recorrido afectado. Por ejemplo, cambiar la maqueta requiere la guía de PDF. Cambiar los destinatarios puede requerir revisar impacto, adjunto y transporte. Trabajar con la configuración de Gmail se resuelve con la guía de secretos.
4. Resolvé las diferencias entre instrucciones y evidencia antes de editar. Si una decisión modifica un contrato fuera del alcance autorizado, preservá el trabajo y explicá qué decisión falta.
5. Cerrá con los cambios, el resultado de las comprobaciones ejecutadas y los pendientes. En tareas de solo lectura, devolvé el plan y las referencias sin editar archivos.

Este procedimiento se aplica en la sesión del asistente. Las operaciones Git y externas siguen el alcance autorizado por el usuario.
