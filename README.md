Claro, Samuel. Aquí tienes el README actualizado con una descripción más precisa y técnica de las responsabilidades reales de cada archivo, según tu sistema modular y el contenido de `speech.py` y `ui.py`:

---

# Practical Speech – Sistema de Entrenamiento de Pronunciación para Educación Secundaria

**Practical Speech** es una aplicación interactiva diseñada para apoyar el desarrollo de la competencia oral en inglés de estudiantes de educación secundaria. Mediante una interfaz gráfica responsiva, niveles estructurados y reconocimiento de voz automático, la aplicación facilita la práctica autónoma y guiada de frases clave alineadas con el currículo oficial.

El sistema fue desarrollado en el marco del Trabajo Comunal Universitario TCU-658 de la Universidad de Costa Rica, orientado a fortalecer el proceso de enseñanza-aprendizaje del inglés en la educación secundaria pública.

## Características Técnicas

- **Interfaz adaptativa:** Implementada en `Tkinter`, ajusta dinámicamente el tamaño de fuente e imágenes según la resolución del dispositivo.
- **Reconocimiento de voz local:** Integración con el motor [Vosk](https://alphacephei.com/vosk/), lo que permite transcripción de audio en tiempo real sin requerir conexión a internet.
- **Retroalimentación motivacional:** El sistema evalúa la precisión fonética y muestra mensajes motivacionales acordes al desempeño del usuario.
- **Gestión de niveles:** Incluye niveles progresivos (“Seventh” a “Eleventh”), un modo de reto (“Challenge”) y un modo docente (“Teacher”) para expansión de contenidos.
- **Referencias auditivas:** Reproducción de frases modelo con dos variantes vocales, facilitando la comparación y práctica.
- **Registro de puntajes:** Visualización de resultados acumulados por usuario.
- **Modularidad del sistema:** Separación clara entre lógica del juego, interfaz gráfica, grabación y procesamiento de audio.

## Dependencias

Instalar mediante pip:

```bash
pip install vosk pygame pillow pyaudio
```

Además, se requiere descargar y ubicar el modelo de reconocimiento de voz de Vosk en el directorio `vosk-model-en-us-0.22-lgraph`.

## Estructura de Archivos

- `ui.py` – Interfaz principal. Maneja la lógica de flujo del juego, visualización de instrucciones, botones de interacción, redimensionamiento dinámico, y muestra de resultados. Encapsula la clase `GameUI`.
- `game.py` – Control de niveles, frases por paso, cálculo de precisión y gestión de puntajes. Se comunica con la interfaz mediante métodos de avance y recuperación de estado.
- `audio.py` – Módulo de grabación de voz. Utiliza `PyAudio` para capturar entrada del micrófono, guardar el archivo WAV temporal y ejecutar un callback para procesamiento posterior.
- `speech.py` – Procesamiento de audio. Encargado de cargar el modelo Vosk, aplicar el reconocedor Kaldi, limpiar y comparar transcripciones, formatear texto y aplicar capitalización contextual. También gestiona la carga de vocabulario especial desde archivo externo.
- `config.py` – Repositorio central de recursos. Define rutas de imágenes, frases motivacionales, relaciones entre índices y audios, y los recursos gráficos de fondo.
- Carpeta `voices/` – Audios de referencia organizados por voz (`Neutral_Voice`, `Rick_Voice`), nivel y número de paso.
- Carpeta `images/` – Imágenes ilustrativas por paso en cada nivel, utilizadas como fondo motivacional.
- Carpeta `teacher/` – Archivos de texto para personalización (`new_levels.txt`, `special_words.txt`).

## Personalización de Contenidos (Modo Teacher)

- **Niveles personalizados:**  
  Agregar frases en `new_levels.txt`, ubicado en:  
  `C:\Program Files (x86)\Practical Speech\teacher\new_levels.txt`  
  - Máximo: 50 niveles  
  - Formato: Una frase por línea, cada una iniciando en mayúscula y terminando con punto.

- **Palabras especiales:**  
  Añadir vocablos que deben conservar su capitalización en:  
  `C:\Program Files (x86)\Practical Speech\teacher\special_words.txt`  
  - Sin límite de entradas  
  - Formato: Una palabra por línea, sin puntuación.

## Créditos

Este proyecto fue desarrollado por **Samuel Ardila Otálora**, estudiante de Informática, durante el año 2025, como parte del Trabajo Comunal Universitario TCU-658: *“Cooperación con el Proceso de Enseñanza-Aprendizaje del Inglés en Educación Secundaria Pública”*, perteneciente a la Escuela de Lenguas Modernas de la Universidad de Costa Rica.

La dirección académica estuvo a cargo de la profesora **Daniela María Barrantes Torres**, Coordinadora del TCU-658 y docente de la Escuela de Lenguas Modernas de la UCR.

El sistema de reconocimiento de voz se basa en **Vosk**, motor de código abierto disponible en:  
[https://alphacephei.com/vosk/](https://alphacephei.com/vosk/)

