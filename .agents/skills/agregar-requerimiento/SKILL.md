---
name: agregar-requerimiento
description: 'Incorporar o modificar una funcionalidad de Pizarra Snap, revisar los RF afectados, sus contratos y las pruebas necesarias para un PR.'
---

# Agregar o modificar un requerimiento

1. Precisá el resultado observable, el alcance y los casos de error. Identificá los RF que ya cubren el pedido en el [catálogo](../../../docs/REQUERIMIENTOS.md). Usá un nuevo número solo cuando el equipo lo acuerde.
2. Leé la implementación y los antecedentes pertinentes del [plan](../../../PLAN_TRABAJO_PIZARRA_SNAP.md). Localizá entradas, salidas, dependencias y consumidores antes de cambiar código. Si difieren las fuentes, registrá el comportamiento que verifica el código y la decisión que necesita el equipo.
3. Identificá riesgos para los resultados previos, la memoria de RF09, los temporales y la sesión. Para cambios de informe o envío, aplicá los procedimientos especializados que correspondan.
4. Implementá el cambio mínimo en el punto que controla ese comportamiento. Conservá el manejo de errores y los contratos compartidos dentro del alcance acordado.
5. Validá desde el punto de entrada que usará el usuario. Elegí casos sintéticos para el contrato y una comparación con el MP4 oficial cuando cambie el flujo completo. Para una corrección exclusivamente documental, comprobá rutas y coherencia con el código.
6. Actualizá solo la documentación afectada y revisá el diff, incluidos los archivos nuevos. Prepará el PR con los RF afectados, decisiones de compatibilidad, resultados de prueba y límites de la validación.
