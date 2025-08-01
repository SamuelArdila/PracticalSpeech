# speech.py
import os
import sys
import vosk
import json
import wave
import re

MODEL_PATH = "./vosk-model-en-us-0.22-lgraph"  # Ruta al modelo Vosk
model = None  # Variable global para almacenar el modelo
recognizer = None  # Variable global para almacenar el reconocedor
special_words = {"I", "Internet", "TV", "English", "Costa Rica"}


def get_model_path():
    """Obtiene la ruta absoluta del modelo, compatible con PyInstaller."""
    base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    return os.path.join(base_dir, "vosk-model-en-us-0.22-lgraph")

def load_model():
    """
    Carga el modelo Vosk una sola vez de manera segura.

    Returns:
        model: El modelo Vosk cargado.
        recognizer: El reconocedor Kaldi inicializado.
    """
    global model, recognizer

    if model is None:
        os.environ["VOSK_LOG_LEVEL"] = "-1"
        model_path = get_model_path()
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"[ERROR] No se encontró el modelo en {model_path}")
        
        print(f"[INFO] Cargando modelo de reconocimiento de lenguaje. (Este proceso es normal)")
        model = vosk.Model(model_path)  # Carga el modelo Vosk
        recognizer = vosk.KaldiRecognizer(model, 16000)  # Inicializa el reconocedor Kaldi
        print("[INFO] Modelo cargado exitosamente.")

    return model, recognizer

def load_special_words():
    txt_path = "./teacher/special_words.txt"
    try:
        with open(txt_path, "r", encoding="utf-8") as file:
            words = [line.strip() for line in file if line.strip()]
            return words  # Retorna la lista de palabras, omitiendo líneas vacías
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {txt_path}")
        return []
    except Exception as e:
        print(f"Error: No se pudo cargar el archivo {txt_path}: {e}")
        return []
        
def clean_text(text):
    """Elimina puntuación y convierte a minúsculas."""
    return re.sub(r'[.,!?]', '', text).lower().strip()

def format_text(text):
    """Agrega puntuación y pone mayúsculas según reglas específicas."""
    words = text.strip().split()
    if not words:
        return ""

    # Aplica mayúsculas a palabras especiales (incluyendo compuestas)
    def capitalize_special(word):
        lower_word = word.lower()
        for special in special_words:
            if lower_word == special.lower():
                return special
        
        special_words2 = load_special_words()
        for special in special_words2:
            if lower_word == special.lower():
                return special
            
        return word

    # Formatea cada palabra
    formatted_words = [capitalize_special(word) for word in words]

    # Asegura que la primera letra de la oración esté en mayúscula
    formatted_words[0] = formatted_words[0].capitalize()

    # Une las palabras y agrega un punto si no hay puntuación final
    result = ' '.join(formatted_words)
    if not result.endswith('.'):
        result += '.'

    return result

def process_audio_vosk(audio_file, recognizer, expected_text):
    """
    Procesa el audio usando el modelo Vosk y lo compara con la respuesta esperada.
    """
    try:
        wf = wave.open(audio_file, "rb")
        if wf.getframerate() != 16000:
            raise ValueError("¡El archivo de audio tiene una tasa de muestreo incorrecta!")

        transcribed_text = ""

        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_json = json.loads(result)
                transcribed_text = result_json.get('text', '')

        result = recognizer.FinalResult()
        result_json = json.loads(result)
        transcribed_text = result_json.get('text', '').strip()

        # Aplica el formateo
        formatted_text = format_text(transcribed_text)

        cleaned_expected = clean_text(expected_text)
        correct = transcribed_text.lower() == cleaned_expected.lower()

        return correct, formatted_text

    except Exception as e:
        print(f"[ERROR] Error procesando el audio: {e}")
        return False, "Error processing audio"
