from kivy.app import App # type: ignore
from kivy.uix.boxlayout import BoxLayout # type: ignore
from kivy.uix.label import Label # type: ignore
from kivy.uix.button import Button # type: ignore
from kivy.uix.textinput import TextInput # type: ignore
from kivy.core.window import Window # type: ignore
import random
import os

WIDTH = 600
HEIGHT = 400

class QuizApp(App):
    def __init__(self, **kwargs):
        super(QuizApp, self).__init__(**kwargs)
        self.student_name = ""  # Инициализируем атрибут name
        self.name_label = Label(text="Enter your name:", size_hint=(0.9, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.name_input = TextInput(size_hint=(0.9, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.start_button = Button(text="Start Quiz", size_hint=(0.9, None), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.start_button.bind(on_press=self.start_quiz)
        self.questions = [
    {
        "question": "Что такое психология?",
        "options": ["Наука о душе", "Исследование общества", "Медицинская дисциплина", "Техника программирования"],
        "answer": "Наука о душе"
    },
    {
        "question": "Что такое память?",
        "options": ["Способность удерживать информацию и использовать ее", "Медленная реакция на внешние стимулы", "Отсутствие восприятия", "Противоположность мышления"],
        "answer": "Способность удерживать информацию и использовать ее"
    },
    {
        "question": "Что такое личность?",
        "options": ["Уникальный набор индивидуальных качеств человека", "Базис общественных институтов", "Техническое устройство с идентификатором", "Экономическая категория"],
        "answer": "Уникальный набор индивидуальных качеств человека"
    },
    {
        "question": "Что такое депрессия?",
        "options": ["Психическое расстройство, характеризующееся угнетенным настроением", "Повышенное настроение и недостаток сна", "Состояние бодрости и активности", "Физическое заболевание желудка и кишечника"],
        "answer": "Психическое расстройство, характеризующееся угнетенным настроением"
    }
]

    def build(self):
        Window.size=(WIDTH, HEIGHT)
        layout = BoxLayout(orientation="vertical", size_hint=(1, 1), pos_hint = {'center_x': 0.5, 'center_y': 0.5})
        layout.add_widget(self.name_label)
        layout.add_widget(self.name_input)
        layout.add_widget(self.start_button)
        return layout

    def start_quiz(self, instance):
        self.student_name = self.name_input.text
        self.question_index = 0
        self.score = 0

        self.question_label = Label(text=self.questions[self.question_index]["question"])
        self.answer_label = Label()
        self.score_label = Label(text=f"Score: {self.score}")

        self.option_buttons = []
        for option in self.questions[self.question_index]["options"]:
            button = Button(text=option)
            button.bind(on_press=self.check_answer)
            self.option_buttons.append(button)

        layout = BoxLayout(orientation="vertical")
        layout.add_widget(self.question_label)
        for button in self.option_buttons:
            layout.add_widget(button)
        layout.add_widget(self.answer_label)
        layout.add_widget(self.score_label)

        self.root.clear_widgets()
        self.root.add_widget(layout)

    def check_answer(self, instance):
        current_question = self.questions[self.question_index]
        correct_answer = current_question["answer"]

        if instance.text.lower() == correct_answer.lower():
            self.score += 1
            self.answer_label.text = "Correct!"
        else:
            self.answer_label.text = f"Wrong! Correct answer is {correct_answer}"

        self.question_index += 1
        if self.question_index < len(self.questions):
            self.question_label.text = self.questions[self.question_index]["question"]
            random.shuffle(self.questions[self.question_index]["options"])
            for i, option in enumerate(self.questions[self.question_index]["options"]):
                self.option_buttons[i].text = option
        else:
            self.show_results()
            

        self.score_label.text = f"Score: {self.score}"

    def show_results(self):
        grade = "A" if self.score >= 90 else "B" if self.score >= 80 else "C" if self.score >= 70 else "D" if self.score >= 60 else "F"
        result_label = Label(text=f"Quiz finished, {self.student_name}!\nYour score is {self.score}/{len(self.questions)}\nYour grade is {grade}")
        self.root.clear_widgets()
        self.root.add_widget(result_label)

        file_path = os.path.join(os.path.dirname(__file__), "results.txt")
        with open(file_path, "a") as f:
            f.write(f"{self.student_name}: {self.score}, {grade}\n")
             
if __name__ == "__main__":
    QuizApp().run()