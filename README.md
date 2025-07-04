# Setup Automático para Proyecto de Control de Dron con Python

Este archivo explica cómo usar el script `setup_total.sh` para preparar automáticamente el entorno de desarrollo necesario para este proyecto.

---

## ¿Qué hace `setup_total.sh`?

El script automatiza la configuración del entorno y las dependencias:

- Verifica si tienes instalado `pyenv` (para manejar versiones de Python); si no, lo instala automáticamente con Homebrew.
- Instala la versión específica de Python requerida (por defecto, la 3.9.13).
- Configura la versión de Python para usarse localmente en el proyecto.
- Crea y activa un entorno virtual (`venv`).
- Actualiza `pip` e instala todas las dependencias necesarias (`opencv-python`, `cvzone`, `mediapipe`, `djitellopy`, `numpy`).

---

## Cómo usarlo

1. Abre la terminal y navega a la carpeta raíz del proyecto.
2. Dale permisos de ejecución al script (solo la primera vez):

   ```bash
   chmod +x setup_total.sh
   ```

3. Ejecuta el script con:

   ```bash
   ./setup_total.sh
   ```

4. Cuando termine, activa el entorno virtual con:

   ```bash
   source venv/bin/activate
   ```

5. Ya puedes ejecutar tu proyecto normalmente, por ejemplo:

   ```bash
   python drone_hand.py
   ```

---

¡Listo! Así de simple es preparar todo el entorno para que el proyecto funcione sin complicaciones.

---

## Nota

Este script está diseñado para macOS. Para otros sistemas operativos, podrían requerirse adaptaciones.

---

**Autor:** Axel Meyrek  
