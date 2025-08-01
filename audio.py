import pyaudio
import wave
import threading
import os

# 📌 Definir la ruta accesible donde se guardará el archivo de audio
output_dir = os.path.join(os.getenv("LOCALAPPDATA"), "Practical_Speech")
os.makedirs(output_dir, exist_ok=True)  # Crea la carpeta si no existe
AUDIO_FILE = os.path.join(output_dir, "temp.wav")  # Ruta completa del archivo

stop_event = threading.Event()  # Evento para detener la grabación

def record_audio(callback):
    """
    Graba audio en un archivo WAV y luego ejecuta la función callback.

    Args:
        callback (function): Función a ejecutar después de grabar el audio.
    """
    def listen():
        """
        Función interna que realiza la grabación del audio.
        """
        global stop_event
        stop_event.clear()  # Limpia cualquier señal de detener la grabación
        # print("[INFO] Iniciando grabación...")

        p = pyaudio.PyAudio()  # Inicializa PyAudio

        try:
            stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                            input=True, frames_per_buffer=1024)  # Abre el stream de audio
        except OSError as e:
            print(f"[ERROR] No se pudo acceder al micrófono: {e}")
            p.terminate()
            return

        frames = []  # Lista para almacenar los frames de audio

        while not stop_event.is_set():  # Mientras no se haya solicitado detener la grabación
            try:
                data = stream.read(1024, exception_on_overflow=False)  # Lee 1024 frames del stream de audio
                frames.append(data)  # Añade los frames leídos a la lista
            except IOError as e:
                print(f"[ERROR] Error al leer el micrófono: {e}")
                break

        stream.stop_stream()  # Detiene el stream de audio
        stream.close()  # Cierra el stream de audio
        p.terminate()  # Termina la instancia de PyAudio

        # Escribe los frames de audio en un archivo WAV
        try:
            with wave.open(AUDIO_FILE, "wb") as audio_file:
                audio_file.setnchannels(1)  # Establece el número de canales a 1
                audio_file.setsampwidth(p.get_sample_size(pyaudio.paInt16))  # Establece el tamaño de muestra
                audio_file.setframerate(16000)  # Establece la frecuencia de muestreo
                audio_file.writeframes(b''.join(frames))  # Escribe los frames de audio en el archivo
            # print(f"[INFO] Grabación finalizada. Archivo guardado: {AUDIO_FILE}")
            callback(AUDIO_FILE)  # Llama a la función callback con el archivo de audio
        except Exception as e:
            print(f"[ERROR] No se pudo guardar el archivo de audio: {e}")

    threading.Thread(target=listen, daemon=True).start()  # Inicia la grabación en un hilo separado

def stop_recording():
    """
    Detiene la grabación.
    """
    global stop_event
    stop_event.set()  # Señala el evento para detener la grabación
