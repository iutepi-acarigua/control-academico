# control-academico
repositorio para el sistema de control academico del IUTEPI Acarigua 

# 🌟 Guía de Trabajo en Equipo
Este documento explica las normas básicas para trabajar en equipo usando **GitHub Projects** y **GitHub Flow**.  

El objetivo es mantener el proyecto ordenado, evitar confusiones y asegurar que todos puedan contribuir sin miedo.

---

# 👥 1. Normas para trabajar con GitHub Projects

## ✅ 1.1 Toda tarea debe tener un Issue
Antes de comenzar cualquier trabajo, debe existir un **issue** en GitHub.

Un issue representa:
- una tarea  
- un error  
- una mejora  
- una duda importante  

📌 **Regla:** *Si no hay issue, no se trabaja.*

---

## ✅ 1.2 Asignarte tu propia tarea
Cuando tomes una tarea:

1. Ve a **Projects**  
2. Busca tu issue  
3. Asígnate el issue  
4. Cambia el estado a **In Progress**  

Esto hace visible que estás trabajando en esa tarea.

---

## ✅ 1.3 Mantener actualizado el Project
Cada miembro debe mover su tarea según corresponda:

- **To Do** — pendiente  
- **In Progress** — en progreso  
- **Review** — lista para revisar (opcional)  
- **Done** — completada  

Mantener esto al día evita confusiones en el equipo.

---

## ✅ 1.4 Tareas pequeñas y manejables
Si una tarea no se puede completar en un día, se divide en subtareas.

Mantener tareas simples = menos estrés.

---

## ✅ 1.5 Descripción mínima de cada issue
Cada issue debe responder:

- ¿Qué se hará?  
- ¿Dónde se hará? (módulo, archivo, vista, etc.)  
- ¿Cómo sabremos que está listo?  

Ejemplo:

> Crear el modelo Student con campos básicos.  
> Está listo cuando el módulo instala sin errores.

---

# 🔵 2. GitHub Flow Simplificado (con todos los comandos necesarios)

Este flujo es ideal para equipos nuevos.  
Es fácil, seguro y evita romper la rama principal.

---

# 📌 2.1 Regla principal
## ❗ Nunca trabajes en la rama `main`

`main` es la versión estable del proyecto.  
Todas las tareas deben hacerse en ramas separadas.

---

# 🚀 2.2 Antes de comenzar una tarea: actualizar tu repositorio

Si ya tienes el repo clonado:

```bash
git pull origin main



# Tareas:
- Tarea 1: Modelo academia.solicitud. Crear el modelo con los campos necesarios: nombre, apellido, cédula/DNI, correo, teléfono, carrera solicitada (Many2one) y adjuntos (Documentos de identidad/Título).

- Tarea 2: Estados de la Solicitud. Implementar un campo state (Selection) con los estados: borrador, enviado, validado, rechazado.

- Tarea 3: Secuencia Automática. Configurar un ir.sequence para que cada solicitud tenga un número único (ej. INS-2024-001).

- Tarea 4: Controlador Web (controllers/main.py). Crear la ruta /inscripcion que renderice el formulario y el método POST que reciba los datos y cree el registro en academia.solicitud.

- Tarea 5: Validación de Duplicados. Lógica en Python que verifique si ya existe una solicitud con ese mismo número de cédula o correo para evitar spam o registros dobles.
