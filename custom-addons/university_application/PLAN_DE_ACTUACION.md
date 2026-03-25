# Plan de Actuación: Mejoras Módulo University Application

Este documento detalla la hoja de ruta para la evolución del sistema de inscripciones universitarias tras la auditoría de marzo de 2026.

## 1. Fase de Estabilización y UX (Corto Plazo)
*   **Completar Formulario:** Añadir el campo faltante `user_academic_record` en la vista `enrollment.xml`.
*   **Validación de Identidad (VAT):** Sincronizar el campo `vat` (DNI) del Partner con la solicitud para evitar que un mismo DNI use correos diferentes.
*   **Mejora de Respuestas:** Implementar mensajes de error más amigables que no saquen al usuario del flujo de inscripción (preservar datos mediante `request.params`).

## 2. Fase de Automatización y Notificaciones (Medio Plazo)
*   **Emails Automáticos:**
    *   Confirmación de recepción tras el envío.
    *   Notificación de "Solicitud Validada" con instrucciones de bienvenida.
    *   Notificación de "Solicitud Rechazada" con el motivo (usando el campo `reason` que se añadirá al modelo).
*   **Secuenciación:** Implementar `ir.sequence` para que cada solicitud tenga un código único (ej. `INS-2026-0001`).

## 3. Fase de Experiencia del Aspirante (Portal)
*   **Vista de Portal Estudiante:** 
    *   Desarrollar la ruta `/my/applications` integrada en el portal de Odoo.
    *   Permitir la descarga de los documentos subidos para verificación del alumno.
    *   Chatter habilitado en el portal para comunicación directa Administrador-Aspirante.

## 4. Fase de Administración y Reporting (Largo Plazo)
*   **Reporte PDF de Inscripción:** Crear un reporte `ir.actions.report` (QWeb PDF) que resuma la ficha del estudiante y su selección académica.
*   **Dashboard de Control:**
    *   Vista tipo Pivot para análisis de demanda por carrera.
    *   Vista tipo Graph para medir tiempos de respuesta en validación.
*   **Integración de Pagos:** Conectar con el módulo `payment` para requerir un depósito de reserva de cupo antes de procesar la solicitud.

---
**Elaborado por:** Analista de Sistemas Senior / Gemini CLI
**Fecha:** 25 de marzo de 2026
