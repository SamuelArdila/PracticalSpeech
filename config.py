# config.py
import threading

MODEL_PATH = "./vosk-model-en-us-0.22"
is_listening = False
stop_recording = threading.Event()
model = None
recognizer = None

letter_size = {
    14, 22, 30
}

levels = {
    "Seventh": [
        "Good morning!",
        "I like playing soccer.",
        "My family is very big.",
        "My favorite color is blue.",
        "Let's go to the park to have fun.",
        "We love learning English.",
        "I love going to school.",
        "It is time to have fun.",
        "I have a big family who loves me.",
        "She is my best friend.",
        "See you tomorrow at school.",
        "It is sunny outside today.",
        "I like reading interesting books.",
        "Let's eat fruit for breakfast.",
        "I wake up early every morning."
    ],
    "Eighth": [
        "School is fun and interesting.",
        "I follow my daily routine.",
        "We celebrate special occasions together.",
        "I love living in Costa Rica.",
        "Shopping is fun for me.",
        "My town is very pretty.",
        "We play outside every afternoon.",
        "Music makes me happy every day.",
        "My favorite song inspires me.",
        "We go to the beach on weekends.",
        "I need groceries for my family.",
        "Traveling is fun and exciting.",
        "Let’s practice English together.",
        "I like hanging out with my friends.",
        "My backpack is full of books."
    ],
    "Ninth": [
        "Technology is everywhere in our lives.",
        "Let's watch a movie together.",
        "I use my phone to stay connected.",
        "Reading is fun and educational.",
        "The Internet is useful for learning.",
        "My laptop helps me with homework.",
        "Cooking is fun and creative.",
        "I go to the gym to stay healthy.",
        "Let's play a game after school.",
        "This book is good for learning new things.",
        "I listen to music while studying.",
        "Watching TV is relaxing at night.",
        "This person is an actor I admire.",
        "Social media is popular among teens.",
        "I keep a journal about my day."
    ],
    "Tenth": [
        "Finding a job is important for the future.",
        "I want to learn a new skill.",
        "Books are powerful tools for knowledge.",
        "We should take care of nature every day.",
        "Sustainability matters for our planet.",
        "Recycling is necessary to reduce waste.",
        "Digital safety is important for everyone.",
        "Technology helps us solve problems.",
        "My future is in my hands.",
        "Hard work pays off in the long run.",
        "I enjoy volunteering in my community.",
        "Creativity is important for innovation.",
        "Time management is key to success.",
        "This app is helpful for studying.",
        "Studying abroad is fun and educational."
    ],
    "Eleventh": [
        "Healthy habits matter for a good life.",
        "Innovation changes the world every day.",
        "The future is bright for those who work hard.",
        "Positivity leads to success in life.",
        "We learn from mistakes to grow better.",
        "Dream big and work hard to achieve goals.",
        "A balanced life is important for happiness.",
        "Hard work leads to success and fulfillment.",
        "Education opens doors to great opportunities.",
        "Leadership skills are valuable in life.",
        "Stay focused and determined to reach your goals.",
        "Community service is rewarding and fulfilling.",
        "New technology shapes the world around us.",
        "Protecting the environment is crucial for survival.",
        "Respect and kindness matter in every situation."
    ],
    "Challenge": [
        "I like playing soccer.",
        "Let's go to the park to have fun.",
        "We love learning English.",
        "It is sunny outside today.",
        "I wake up early every morning.",
        "My family is very big.",
        "She is my best friend.",
        "I like reading interesting books.",
        "Let's eat fruit for breakfast.",
        "School is fun and interesting.",
        "I follow my daily routine.",
        "We celebrate special occasions together.",
        "Traveling is fun and exciting.",
        "Let’s practice English together.",
        "I love living in Costa Rica.",
        "My backpack is full of books.",
        "Shopping is fun for me.",
        "Music makes me happy every day.",
        "My town is very pretty.",
        "We play outside every afternoon.",
        "Technology is everywhere in our lives.",
        "Let's watch a movie together.",
        "The Internet is useful for learning.",
        "Cooking is fun and creative.",
        "I go to the gym to stay healthy.",
        "Social media is popular among teens.",
        "My laptop helps me with homework.",
        "I keep a journal about my day.",
        "Books are powerful tools for knowledge.",
        "Sustainability matters for our planet.",
        "Hard work pays off in the long run.",
        "Recycling is necessary to reduce waste.",
        "Creativity is important for innovation.",
        "Digital safety is important for everyone.",
        "Studying abroad is fun and educational.",
        "Healthy habits matter for a good life.",
        "Innovation changes the world every day.",
        "Dream big and work hard to achieve goals.",
        "Education opens doors to great opportunities.",
        "Leadership skills are valuable in life.",
        "Community service is rewarding and fulfilling.",
        "Protecting the environment is crucial for survival.",
        "Positivity leads to success in life.",
        "We learn from mistakes to grow better.",
        "Hard work leads to success and fulfillment.",
        "New technology shapes the world around us.",
        "Respect and kindness matter in every situation.",
        "Time management is key to success.",
        "My future is in my hands.",
        "A balanced life is important for happiness.",
        "Finding a job is important for the future."
    ]
}

images = {
    "Seventh": [
        "img/Wireframe_1.jpg", "img/Wireframe_3.jpg", "img/Wireframe_5.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_6.jpg", "img/Wireframe_4.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_5.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_4.jpg", "img/Wireframe_3.jpg",
        "img/Wireframe_5.jpg", "img/Wireframe_2.jpg", "img/Wireframe_6.jpg"
    ],
    "Eighth": [
        "img/Wireframe_1.jpg", "img/Wireframe_2.jpg", "img/Wireframe_4.jpg",
        "img/Wireframe_6.jpg", "img/Wireframe_5.jpg", "img/Wireframe_3.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_6.jpg", "img/Wireframe_4.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_5.jpg", "img/Wireframe_2.jpg",
        "img/Wireframe_6.jpg", "img/Wireframe_3.jpg", "img/Wireframe_4.jpg"
    ],
    "Ninth": [
        "img/Wireframe_1.jpg", "img/Wireframe_5.jpg", "img/Wireframe_3.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_6.jpg", "img/Wireframe_4.jpg",
        "img/Wireframe_5.jpg", "img/Wireframe_3.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_4.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_5.jpg", "img/Wireframe_2.jpg"
    ],
    "Tenth": [
        "img/Wireframe_1.jpg", "img/Wireframe_4.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_5.jpg", "img/Wireframe_3.jpg",
        "img/Wireframe_6.jpg", "img/Wireframe_4.jpg", "img/Wireframe_2.jpg",
        "img/Wireframe_5.jpg", "img/Wireframe_3.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_4.jpg", "img/Wireframe_3.jpg", "img/Wireframe_2.jpg"
    ],
    "Eleventh": [
        "img/Wireframe_1.jpg", "img/Wireframe_3.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_4.jpg", "img/Wireframe_5.jpg", "img/Wireframe_2.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_5.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_4.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_5.jpg", "img/Wireframe_3.jpg", "img/Wireframe_2.jpg"
    ],
    "Challenge": [
        "img/Wireframe_1.jpg", "img/Wireframe_4.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_2.jpg", "img/Wireframe_5.jpg",
        "img/Wireframe_4.jpg", "img/Wireframe_3.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_5.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_4.jpg", "img/Wireframe_5.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_6.jpg", "img/Wireframe_3.jpg",
        "img/Wireframe_4.jpg", "img/Wireframe_5.jpg", "img/Wireframe_2.jpg",
        "img/Wireframe_6.jpg", "img/Wireframe_4.jpg", "img/Wireframe_3.jpg",
        "img/Wireframe_5.jpg", "img/Wireframe_2.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_4.jpg", "img/Wireframe_3.jpg", "img/Wireframe_5.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_6.jpg", "img/Wireframe_4.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_5.jpg", "img/Wireframe_2.jpg",
        "img/Wireframe_6.jpg", "img/Wireframe_4.jpg", "img/Wireframe_3.jpg",
        "img/Wireframe_5.jpg", "img/Wireframe_2.jpg", "img/Wireframe_6.jpg",
        "img/Wireframe_4.jpg", "img/Wireframe_3.jpg", "img/Wireframe_5.jpg",
        "img/Wireframe_2.jpg", "img/Wireframe_6.jpg", "img/Wireframe_4.jpg",
        "img/Wireframe_3.jpg", "img/Wireframe_5.jpg"
    ]
}


motivational_quotes = {
    "failure": {
        1: "Don't give up! Every failure is a step closer to success",
        2: "Keep pushing forward. Your effort will pay off!",
        3: "Mistakes are proof that you are trying. Keep going!",
        4: "Believe in yourself! You've got this!",
        5: "Every challenge is an opportunity to grow. Keep striving!",
        6: "Success is not final, failure is not fatal: It is the courage to continue that counts",
        7: "You are stronger than you think. Keep pushing!",
        8: "Keep your head up and keep moving forward. You can do it!",
        9: "Your perseverance will lead you to greatness. Don't stop now!",
        10: "Failure is a detour, not a dead-end. Keep going!"
    },
    "success": {
        1: "Congratulations! Your hard work has paid off!",
        2: "Well done! Keep up the great work!",
        3: "You did it! Celebrate your success!",
        4: "Great job! You should be proud of yourself!",
        5: "Fantastic! Your dedication is truly inspiring!",
        6: "Bravo! Your effort and commitment have led to this success!",
        7: "Amazing! Your hard work and determination made this possible!",
        8: "Wonderful! Keep shining and reaching new heights!",
        9: "Outstanding! You've shown great skill and perseverance!",
        10: "Excellent! Keep pushing the boundaries and achieving greatness!"
    }
}

relacion = {
    1: "Seventh_2",
    2: "Seventh_5",
    3: "Seventh_6",
    4: "Seventh_12",
    5: "Seventh_15",
    6: "Seventh_3",
    7: "Seventh_10",
    8: "Seventh_13",
    9: "Seventh_14",
    10: "Eighth_1",
    11: "Eighth_2",
    12: "Eighth_3",
    13: "Eighth_12",
    14: "Eighth_13",
    15: "Eighth_4",
    16: "Eighth_15",
    17: "Eighth_5",
    18: "Eighth_8",
    19: "Eighth_6",
    20: "Eighth_7",
    21: "Ninth_1",
    22: "Ninth_2",
    23: "Ninth_5",
    24: "Ninth_7",
    25: "Ninth_8",
    26: "Ninth_14",
    27: "Ninth_6",
    28: "Ninth_15",
    29: "Tenth_3",
    30: "Tenth_5",
    31: "Tenth_10",
    32: "Tenth_6",
    33: "Tenth_12",
    34: "Tenth_7",
    35: "Tenth_15",
    36: "Eleventh_1",
    37: "Eleventh_2",
    38: "Eleventh_6",
    39: "Eleventh_9",
    40: "Eleventh_10",
    41: "Eleventh_12",
    42: "Eleventh_14",
    43: "Eleventh_4",
    44: "Eleventh_5",
    45: "Eleventh_8",
    46: "Eleventh_13",
    47: "Eleventh_15",
    48: "Tenth_13",
    49: "Tenth_9",
    50: "Eleventh_7",
    51: "Tenth_1"
}

loading_image = "img/mainpage.jpg"
mainpage_image = "img/mainpage.jpg"
end_image = "img/Wireframe_end.jpg"
