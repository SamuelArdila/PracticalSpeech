import os

class Game:
    def __init__(self, level):
        from config import levels  # Importar aquí para evitar problemas de dependencia
        
        if level == "Teacher":
            self.steps = self.load_phrases_from_txt()
        elif level in levels:
            self.steps = levels[level]
        
        self.level = level
        self.current_step = 0
        self.correct_answers = 0

        # 📌 Definir la ruta accesible para el archivo de puntajes
        self.scores_file = os.path.join(os.getenv("LOCALAPPDATA"), "Practical_Speech", "tabla.txt")
        os.makedirs(os.path.dirname(self.scores_file), exist_ok=True)  # Crea la carpeta si no existe

    def load_phrases_from_txt(self):
        """Carga las frases desde el archivo TXT en caso de 'Teacher'."""
        txt_path = "./teacher/new_levels.txt"
        try:
            with open(txt_path, "r", encoding="utf-8") as file:
                phrases = [line.strip() for line in file if line.strip()]
                return phrases  # Devuelve la lista de frases, omitiendo líneas vacías
        except FileNotFoundError:
            print(f"[ERROR] No se encontró el archivo {txt_path}")
            return []
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el archivo {txt_path}: {e}")
            return []

    def get_current_step(self):
        return self.current_step

    def get_current_step_text(self):
        return self.steps[self.current_step]

    def advance_step(self, correct):
        if correct:
            self.correct_answers += 1
        self.current_step += 1
        if self.current_step >= len(self.steps):
            return f"Game Over! Accuracy: {self.get_accuracy():.2f}%"
        return None

    def get_accuracy(self):
        return (self.correct_answers / len(self.steps)) * 100

    def load_scores(self):
        """Carga los puntajes desde el archivo, manejando errores si el archivo no existe."""
        scores = []
        if not os.path.exists(self.scores_file):  
            return scores  # Si no existe, retorna una lista vacía

        try:
            with open(self.scores_file, "r", encoding="utf-8") as file:
                for line in file:
                    try:
                        username, score = line.strip().split(": ")
                        scores.append((username, int(score)))  
                    except ValueError:
                        continue  # Ignora líneas mal formateadas
        except Exception as e:
            print(f"[ERROR] No se pudo leer {self.scores_file}: {e}")
        return scores
    
    def insert_score(self, scores, username, correct_answers):
        """Inserta el puntaje del usuario en la lista ordenada correctamente."""
        scores.append((username, correct_answers))  
        scores.sort(key=lambda x: x[1], reverse=True)  # Ordenar de mayor a menor
        return scores[:10]  # Mantiene solo los 10 mejores puntajes

    def save_score(self, username):
        """Guarda la puntuación del usuario en el archivo de ranking."""
        scores = self.load_scores()
        scores = self.insert_score(scores, username, self.correct_answers)

        try:
            with open(self.scores_file, "w", encoding="utf-8") as file:
                for user, score in scores:
                    file.write(f"{user}: {score}\n")
        except Exception as e:
            print(f"[ERROR] No se pudo escribir en {self.scores_file}: {e}")
