# ui.py
import tkinter as tk
from tkinter import ttk
from game import Game
from audio import record_audio, stop_recording
from speech import load_model, process_audio_vosk
import threading
import random
import os
import sys
import gc
from PIL import Image, ImageTk
from config import images, loading_image, mainpage_image, end_image, motivational_quotes, relacion  # Importamos end_image
import pygame


class GameUI:
    def __init__(self):
        """Inicializa la interfaz gráfica del juego."""
        self.root = tk.Tk()
        self.root.geometry("1280x800")  # Tamaño inicial
        self.root.configure(bg="#000000")

        # Tamaños de letra: pequeña, mediana y grande
        self.letter_sizes = {"small": 14, "medium": 22, "large": 30}
        self.current_letter_size = "medium"  # Tamaño por defecto

        self.is_recording = False
        self.model = None
        self.recognizer = None
        self.is_correct = False
        self.background_label = tk.Label(self.root)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Para ajustar al tamaño de la ventana
        self.current_level = None
        self.username = tk.StringVar(value="Anonymous")
        self.correct_count = 0
        self.success_quotes = list(motivational_quotes["success"].values())
        self.failure_quotes = list(motivational_quotes["failure"].values())

        self.show_loading_screen()
        threading.Thread(target=self.initialize_model, daemon=True).start()

        # Vincula el evento de redimensionar al método `on_resize`
        self.root.bind("<Configure>", self.on_resize)

    def on_resize(self, event):
        """Ajusta el tamaño de letra y redimensiona las imágenes según el tamaño de la ventana."""
        if event.widget == self.root:  # Verifica que el evento proviene de la ventana principal
            width = self.root.winfo_width()
            height = self.root.winfo_height()

            # Ajustar tamaño de letra dinámicamente
            if width <= 800 or height <= 600:
                self.current_letter_size = "small"
            elif 800 < width <= 1200 or 600 < height <= 900:
                self.current_letter_size = "medium"
            else:
                self.current_letter_size = "large"
            self.update_font_size()

            # Redimensionar la imagen de fondo (asegurar que se cargue correctamente)
            try:
                if hasattr(self, "background_image_path") and self.background_image_path:
                    self.load_background_image(self.background_image_path)
                else:
                    print("[ERROR] No hay imagen de fondo cargada.")
            except Exception as e:
                print(f"[ERROR] Error al redimensionar la imagen: {e}")

    def update_font_size(self):
        """Actualiza el tamaño de letra de todos los widgets según el tamaño seleccionado."""
        font_size = self.letter_sizes[self.current_letter_size]

        # Actualizar widgets con el tamaño de fuente, excepto los que contienen "Voice"
        for widget in self.root.winfo_children():
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)) and "Voice" not in widget.cget("text"):
                widget.config(font=("Helvetica", font_size))
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry)) and "Voice" in widget.cget("text"):
                widget.config(font=("Helvetica", font_size-6))
    
    def show_loading_screen(self):
        """Muestra la pantalla de carga mientras se inicializa el modelo."""
        self.clear_window(exclude_background=True)

        # Aseguramos que la imagen de fondo se cargue correctamente
        self.load_background_image(loading_image)  # Cargar la imagen de fondo
        tk.Label(
            self.root,
            text="Loading model...",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            bg="#000000",
            fg="white",
        ).pack(pady=20)

        self.progress_bar = ttk.Progressbar(self.root, length=300, mode="indeterminate")
        self.progress_bar.pack(pady=20)
        self.progress_bar.start()

    def initialize_model(self):
        """Inicializa el modelo de voz en un hilo separado."""
        try:
            self.model, self.recognizer = load_model()
            # print("[INFO] Modelo cargado correctamente.")
        except Exception as e:
            print(f"[ERROR] No se pudo cargar el modelo: {e}")
    
        self.root.after(0, self.show_level_selection)

    def start_game(self, level):
        """Inicia el juego en el nivel seleccionado."""
        self.current_level = level  # Almacenar el nombre del nivel actual
        self.correct_count = 0  # Reiniciar el contador de respuestas correctas
        self.game = Game(level)
        if level == "Teacher":
            self.current_level_images = images["Challenge"]  # Cargamos las imágenes correspondientes al nivel
        else:
            self.current_level_images = images[level]  # Cargamos las imágenes correspondientes al nivel
    
        pygame.mixer.init()  # Inicializa el módulo de sonido

        self.load_main_screen()

    def instructions(self, level):
        self.clear_window(exclude_background=True)

        # Instrucciones según nivel
        if level == "Challenge":
            predefined_text = (
                f"Welcome to Level {level}\n\n"
                "You will find a section labeled \"Say something:\" where the phrase you need to say will be displayed.\n\n"
                "Start Recording Button\n"
                "You will find the \"Start Recording\" button. Press it to start recording, and press it again to stop.\n"
                "- Green Button: You can start recording.\n"
                "- Red Button: You need to stop recording.\n"
                "- White Button: The button is disabled.\n\n"
                "Next Phrase Button\n"
                "You will find a \"Next Phrase\" button:\n"
                "- Red Button: You cannot proceed to the next level without completing the current one.\n"
                "- Green Button: It indicates that the level is completed successfully.\n\n"
                "Navigation\n" 
                "\"Back Button\": Returns you to the main menu.\n\n"
                "In the top right corner, you will find \"Neutral Voice\" and \"Rick Voice\" buttons to listen to the phrase you must practice."
            )
        elif level == "Teacher":
            predefined_text = (
                f"Welcome to Level {level}\n\n"
                "You will find a section labeled \"Say something:\" where the phrase you need to say will be displayed.\n\n"
                "Start Recording Button\n"
                "You will find the \"Start Recording\" button. Press it to start recording, and press it again to stop.\n"
                "- Green Button: You can start recording.\n"
                "- Red Button: You need to stop recording.\n"
                "- White Button: The button is disabled.\n\n"
                "Next Phrase Button\n"
                "You will find a \"Next Phrase\" button:\n"
                "- Red Button: You cannot proceed to the next level without completing the current one.\n"
                "- Green Button: It indicates that the level is completed successfully.\n\n"
                "Navigation\n" 
                "\"Back Button\": Returns you to the main menu.\n\n"
                "In the top right corner, you will find \"Neutral Voice\" and \"Rick Voice\" buttons to listen to the phrase you must practice.\n\n"
                "To add new levels go into the folder of the app, usually located in:\n"
                "C:\\Program Files (x86)\\Practical Speech\\teacher\\new_levels.txt"
                "- You can add a maximum of 50 levels.\n- Add one level per line, each ending with a period.\n"
                "If needed, add special words that must be capitalized in the special_words.txt file:\n"
                "C:\\Program Files (x86)\\Practical Speech\\teacher\\special_words.txt"
                "- Add one word per line, without punctuation.\n- There is no maximum number of entries.\n"
                "Phrases must always start with a capital letter and end with a period."
            )                                   
        else:
            predefined_text = (
                f"Welcome to Level {level}\n\n"
                "You will find a section labeled \"Say something:\" where the phrase you need to say will be displayed.\n\n"
                "Start Recording Button\n"
                "You will find the \"Start Recording\" button. Press it to start recording, and press it again to stop.\n"
                "- Green button: You can start recording.\n"
                "- Red button: You need to stop recording.\n"
                "- White button: The button is disabled.\n\n"
                "Next Phrase Button\n"
                "You will find a \"Next Phrase\" button:\n"
                "- Red Button: The level hasn't been completed yet.\n"
                "- Green Button: The level is completed successfully.\n\n"
                "Navigation\n" 
                "\"Back Button\": Returns you to the main menu.\n\n"
                "In the top right corner, you’ll find \"Neutral Voice\" and \"Rick Voice\" buttons to listen to the phrase you must practice."
            )

        # ====== CONTENEDOR DE INSTRUCCIONES (80% del tamaño) ======
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5 - 0.6/2, rely=0.05, relwidth=0.6, relheight=0.72)

        canvas = tk.Canvas(container, bg="#000000", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        scroll_frame = tk.Frame(canvas, bg="#000000")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # ====== Etiqueta de texto ======
        label = tk.Label(
            scroll_frame,
            text=predefined_text,
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            justify="left",
            wraplength=700,
            bg="#000000",
            fg="white"
        )
        label.pack(fill="both", expand=True)

        # ====== Botón fuera del frame (centrado debajo) ======
        tk.Button(
            self.root,
            text="Start Game",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#333333",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            command=lambda: self.start_game(level),
        ).place(relx=0.5, rely=0.8, anchor="n")  # Aparece debajo del contenedor

    def show_level_selection(self):
        """Muestra la pantalla de selección de nivel."""
        self.clear_window(exclude_background=True)

        # Aseguramos que la imagen de fondo se cargue correctamente
        self.load_background_image(mainpage_image)  # Cargar la imagen de fondo
        tk.Label(
            self.root,
            text="Select Level",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            bg="#000000",
            fg="white",
        ).pack(pady=20)

        tk.Label(
            self.root,
            text="Enter your name:",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            bg="#000000",
            fg="white",
        ).pack(pady=10)
        tk.Entry(
            self.root,
            textvariable=self.username,
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
        ).pack(pady=10)

        level_frame = tk.Frame(self.root, bg="#000000")  # Contenedor de botones
        level_frame.pack(pady=10)

        button_width = len("Challenge")  # Establece el ancho basado en la palabra más larga

        levels = ["Seventh", "Eighth", "Ninth", "Tenth", "Eleventh", "Challenge"]
        for i, level in enumerate(levels):
            tk.Button(
                level_frame,
                text=level,
                font=("Helvetica", self.letter_sizes[self.current_letter_size]),
                relief="ridge",
                borderwidth=1,
                bg="#000000",
                fg="white",
                width=button_width,  # Se asegura de que todos los botones tengan el mismo ancho
                command=lambda l=level: self.instructions(l),
            ).grid(row=i//2, column=i%2, padx=10, pady=5)

        tk.Button(
            self.root,
            text="Teacher",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#000000",
            fg="white",
            width=button_width,  # Se asegura de que todos los botones tengan el mismo ancho
            command=lambda: self.instructions("Teacher"),
        ).pack(padx=10, pady=5)
        
        # Botón Podium fuera del contenedor de niveles
        tk.Button(
            self.root,
            text="Podium",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#000000",
            fg="white",
            width=button_width,  # Hace que el botón Podium también tenga el mismo ancho
            command=self.show_podium,
        ).pack(pady=10)

        # Botón Podium fuera del contenedor de niveles
        tk.Button(
            self.root,
            text="Credits",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#000000",
            fg="white",
            width=button_width,  # Hace que el botón Podium también tenga el mismo ancho
            command=self.show_credits,
        ).pack(pady=10)

    def load_main_screen(self):
        """Carga la pantalla principal del juego."""
        self.clear_window(exclude_background=True)

        self.set_background_image()  # Establecemos la imagen de fondo

        tk.Label(
            self.root,
            text=f"{self.current_level}",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            bg="#000000",
            fg="white",
        ).pack(pady=10)  # Mostrar el nombre del nivel actual

        self.step_text_label = tk.Label(
            self.root,
            text=f"Say: \"{self.game.get_current_step_text()}\"",
            font=("Helvetica", self.letter_sizes[self.current_letter_size] + 2),
            bg="#000000",
            fg="white",
        )
        self.step_text_label.pack(pady=10)

        self.output_label = tk.Label(
            self.root,
            text="Let's repeat!",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            bg="#000000",
            fg="white",
        )
        self.output_label.pack(pady=20)

        self.progress_bar = ttk.Progressbar(self.root, length=300, mode="indeterminate")
        self.progress_bar.pack(pady=20)

        self.record_button = tk.Button(
            self.root,
            text="Start Recording",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#000000",
            fg="green",
            command=self.toggle_recording,
        )
        self.record_button.pack(pady=20)

        # Por defecto, desactivamos el botón "Next Phrase" en modo Challenge
        self.pass_button = tk.Button(
            self.root,
            text="Next Phrase",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#000000",
            fg="red",
            command=self.pass_to_next,
            state="normal" if self.current_level != "Challenge" else "disabled",  # Desactivado en modo Challenge
        )
        self.pass_button.pack(pady=10)

        self.back_button = tk.Button(
            self.root,
            text="Back",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#000000",
            fg="white",
            command=self.write_score,
        )
        self.back_button.pack(pady=10)

        if self.current_level != "Teacher":
            # Botón para reproducir el primer audio
            self.audio_button_1 = tk.Button(
                self.root,
                text="Neutral_Voice",
                font=("Helvetica", self.letter_sizes[self.current_letter_size]-6),
                relief="ridge",
                borderwidth=1,
                bg="#000000",
                fg="white",
                command=lambda: self.play_audio(1),
            )
            self.audio_button_1.place(relx=0.95, rely=0.05, anchor="ne")  # Posiciona en la esquina superior derecha

            # Botón para reproducir el segundo audio
            self.audio_button_2 = tk.Button(
                self.root,
                text="Rick_Voice",
                font=("Helvetica", self.letter_sizes[self.current_letter_size]-6),
                relief="ridge",
                borderwidth=1,
                bg="#000000",
                fg="white",
                command=lambda: self.play_audio(2),
            )
            self.audio_button_2.place(relx=0.95, rely=0.15, anchor="ne")  # Justo al lado del primero

    def write_score(self):
        if (self.current_level == "Challenge"):
            self.end_game()
        
        self.show_level_selection()

    def play_audio(self, audio_num):
        """Reproduce el audio basado en el nivel y el paso actual."""
        current_step = self.game.get_current_step() + 1
        audio_file = None

        if (self.current_level == "Challenge"):
            if (audio_num == 1):
                audio_file = f"voices/Neutral_Voice/{relacion[current_step]}.mp3"  # Define la ruta del archivo de audio
            elif (audio_num == 2):
                audio_file = f"voices/Rick_Voice/{relacion[current_step]}.wav"  # Define la ruta del archivo de audio
        else:
            if (audio_num == 1):
                audio_file = f"voices/Neutral_Voice/{self.current_level}_{current_step}.mp3"  # Define la ruta del archivo de audio
            elif (audio_num == 2):
                audio_file = f"voices/Rick_Voice/{self.current_level}_{current_step}.wav"  # Define la ruta del archivo de audio

        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Error al reproducir audio: {e}")

    def toggle_recording(self):
        """Inicia o detiene la grabación según el estado actual."""
        if not self.is_recording:
            self.is_recording = True
            self.record_button.config(text="Stop Recording", fg="red")  # Desactivar el botón mientras graba
            self.back_button.config(state="disabled", fg="white")
            self.progress_bar.start()
            threading.Thread(target=record_audio, args=(self.process_audio,), daemon=True).start()  # Grabar en un hilo separado
        else:
            self.is_recording = False
            self.record_button.config(text="Start Recording", state="disabled", fg="white")  # Bloquear hasta que termine de procesar
            self.progress_bar.stop()
            stop_recording()

    def process_audio(self, audio_file):
        """Procesa el audio y actualiza la UI con los resultados."""
        try:
            # Deshabilitar el botón de grabación mientras se analiza el audio
            self.record_button.config(state="disabled", fg="white")
            self.back_button.config(state="disabled", fg="white")
            
            correct, transcribed_text = process_audio_vosk(audio_file, self.recognizer, self.game.get_current_step_text())

            if correct:
                self.correct_count += 1  # Incrementar el contador de respuestas correctas
                self.is_correct = True
                # Bloquear el botón de grabación si la frase es correcta
                self.record_button.config(state="disabled", fg="white")
                self.pass_button.config(fg="green")

            else:
                self.is_correct = False
                # En el modo Challenge, permitir solo el botón "Back" tras fallar
                if self.current_level == "Challenge":
                    self.output_label.config(text="Incorrect! Returning to the main menu.")
                    self.pass_button.config(state="disabled", fg="red")  # Desactivar "Next Phrase"
                    self.record_button.config(state="disabled", fg="white")  # Bloquear grabación
                else:
                    # Rehabilitar el botón de grabación si la frase es incorrecta y no es Challenge
                    self.record_button.config(state="normal", fg="green")
                    self.pass_button.config(fg="red")

            self.back_button.config(state="normal")
            motivational_message = random.choice(self.success_quotes if correct else self.failure_quotes)

            if correct:
                self.output_label.config(text=f"The model correctly understood: \"{transcribed_text}\"\n{motivational_message}")
            else:
                self.output_label.config(text=f"The model understood: \"{transcribed_text}\"\n{motivational_message}")

            self.progress_bar.stop()
            self.record_button.config(text="Start Recording")  # Actualizar texto del botón, pero mantenerlo desactivado si es correcto

            if self.is_correct:
                if self.current_level == "Challenge":
                    self.pass_button.config(state="normal", fg="green")  # Activar el botón "Next Phrase" solo si es correcto
            else:
                if self.current_level == "Challenge":
                    self.pass_button.config(state="disabled", fg="red")  # Mantener el botón desactivado si es incorrecto

            if not self.is_correct and self.current_level == "Challenge":  # Si la respuesta es incorrecta en Challenge
                self.end_game()  # Terminar el juego si la respuesta es incorrecta
        finally:
            # Volver a habilitar el botón de grabación si no es correcto y el procesamiento terminó
            if not self.is_correct and self.current_level != "Challenge":
                self.record_button.config(state="normal", fg="green")

    def pass_to_next(self):
        """Avanza a la siguiente frase en el juego."""
        result = self.game.advance_step(self.is_correct)
        
        if result:  # Si todas las frases del nivel han sido completadas
            # Obtener el total de frases del nivel desde `levels` (asegúrate de importar `levels` desde `config.py`)
            
            accuracy = self.game.get_accuracy()
            # Mostrar los resultados al final del nivel
            self.output_label.config(
                text=f"Level Complete!\nAccuracy: {accuracy:.2f}%\n"
            )
            
            # Desactivar botones al finalizar el nivel
            self.record_button.config(state="disabled", fg="white")
            self.pass_button.config(state="disabled", fg="white")
            self.set_static_background(end_image)  # Cambiar la imagen de fondo a end_image
            
            # Guardar la puntuación
            if self.current_level == "Challenge":
                self.game.save_score(self.username.get())
        else:
            # Actualizamos el texto de la siguiente frase
            self.step_text_label.config(text=f"Say: \"{self.game.get_current_step_text()}\"")
            self.set_background_image()  # Actualizar la imagen de fondo
            self.output_label.config(text="Let's repeat!")  # Reiniciar el mensaje motivacional
            self.record_button.config(state="normal", fg="green")
            self.pass_button.config(fg="red")
            self.is_correct = False
            if self.current_level == "Challenge":
                self.pass_button.config(state="disabled", fg="red")  # Desactivar nuevamente para el siguiente nivel

    def end_game(self):
        """Termina el juego y guarda la puntuación."""
        self.output_label.config(text=f"Game Over! You scored {self.correct_count} correct answers.")
        self.record_button.config(state="disabled", fg="white")
        self.pass_button.config(state="disabled", fg="white")
        self.set_static_background(end_image)  # Cambiar la imagen de fondo a end_image
        # self.game.save_score(self.username.get())  # Guardar la puntuación cuando se complete el juego
        # En Challenge, solo habilitar el botón "Back"
        if self.current_level == "Challenge":
            self.record_button.config(state="disabled")
            self.pass_button.config(state="disabled")

    def clear_window(self, exclude_background=False):
        """Elimina todos los widgets de la ventana, opcionalmente excluyendo la etiqueta de fondo."""
        for widget in self.root.winfo_children():
            if exclude_background and widget == self.background_label:
                continue
            widget.destroy()
            
    def _get_image_path(self, image_path):
        """Obtiene la ruta correcta de la imagen, compatible con PyInstaller."""
        if os.path.isabs(image_path):
            return image_path  # Si ya es absoluta, no modificarla.

        base_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
        return os.path.join(base_dir, image_path)

    def load_background_image(self, image_path):
        """Carga una imagen de fondo ajustada al tamaño de la ventana."""
        if not os.path.exists(image_path):
            print(f"[ERROR] La imagen '{image_path}' no existe.")
            return

        # Guardar la ruta de la imagen para reutilizarla
        self.background_image_path = image_path

        try:
            # Asegurarse de redimensionar al tamaño actual de la ventana
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            image = Image.open(image_path)
            image = image.resize((width, height), Image.LANCZOS)

            self.background_image = ImageTk.PhotoImage(image)
            self.background_label.config(image=self.background_image)
            self.background_label.image = self.background_image  # Evita el garbage collection
        except Exception as e:
            print(f"[ERROR] Error al cargar la imagen: {e}")

    def set_static_background(self, image_path):
        """Establece una imagen de fondo estática."""
        self.load_background_image(image_path)

    def set_background_image(self):
        """Carga la imagen de fondo desde el juego."""
        image_path = self.current_level_images[self.game.current_step]
        self.load_background_image(image_path)
        
    def show_podium(self):
        """Muestra la lista de puntajes desde el archivo de texto."""
        self.clear_window(exclude_background=True)
        self.set_static_background(mainpage_image)  # Establecemos la imagen de fondo para la pantalla de podio
        tk.Label(self.root, text="Podium", font=("Helvetica", self.letter_sizes[self.current_letter_size]), bg="#000000", fg="white").pack(pady=20)
        
        game = Game("null")
        scores = game.load_scores()
        for username, score in scores:
            tk.Label(self.root, text=f"{username}: {score}", font=("Helvetica", self.letter_sizes[self.current_letter_size]), bg="#000000", fg="white").pack(pady=5)

        tk.Button(self.root, text="Back", font=("Helvetica", self.letter_sizes[self.current_letter_size]), relief="ridge", borderwidth=1, bg="#000000", fg="white",
                  command=self.show_level_selection).pack(pady=10)

    def show_credits(self):
        """Muestra los creditos de la aplicación."""
        self.clear_window(exclude_background=True)

        # Instrucciones según nivel
        predefined_text = (
            f"Application developed by computer science student Samuel Ardila Otálora in 2025 for TCU 658: "
            f"Cooperación con el Proceso de Enseñanza-Aprendizaje del Inglés en Educación Secundaria Pública, "
            f"belonging to the School of Modern Languages at the University of Costa RiCa (UCR). "
            f"Carried out under the guidance of Professor Daniela Barrantes Torres, "
            f"Carried out under the guidance of Professor Daniela María Barrantes Torres, Coordinator of TCU-658 and Professor at the School of Modern Languages at UCR."
        )

        # ====== CONTENEDOR DE INSTRUCCIONES (80% del tamaño) ======
        container = tk.Frame(self.root, bg="#000000")
        container.place(relx=0.5 - 0.6/2, rely=0.05, relwidth=0.6, relheight=0.72)

        canvas = tk.Canvas(container, bg="#000000", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        scroll_frame = tk.Frame(canvas, bg="#000000")
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        scroll_frame.bind("<Configure>", on_configure)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Scroll con la rueda del mouse
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))  # Linux
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

        # ====== Etiqueta de texto ======
        label = tk.Label(
            scroll_frame,
            text=predefined_text,
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            justify="left",
            wraplength=700,
            bg="#000000",
            fg="white"
        )
        label.pack(fill="both", expand=True)

        # ====== Botón fuera del frame (centrado debajo) ======
        tk.Button(
            self.root,
            text="Back",
            font=("Helvetica", self.letter_sizes[self.current_letter_size]),
            relief="ridge",
            borderwidth=1,
            bg="#333333",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            command=lambda: self.show_level_selection(),
        ).place(relx=0.5, rely=0.8, anchor="n")  # Aparece debajo del contenedor

    def run(self):
        """Inicia el bucle principal de la interfaz gráfica."""
        self.root.mainloop()
