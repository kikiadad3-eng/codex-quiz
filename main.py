import json
import random
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

DATA_PATH = Path(__file__).with_name("questions.json")


class QuizApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("퀴즈 프로그램")
        self.root.geometry("520x360")

        self.categories = self.load_questions()
        self.current_questions = []
        self.cycle_questions = []
        self.incorrect_questions = []
        self.current_question = None
        self.current_correct_text = None

        self.start_frame = tk.Frame(root)
        self.quiz_frame = tk.Frame(root)

        self.build_start_frame()
        self.build_quiz_frame()

        self.show_start()

    def load_questions(self):
        if not DATA_PATH.exists():
            messagebox.showerror("오류", f"문제 파일을 찾을 수 없습니다: {DATA_PATH}")
            self.root.destroy()
            return []

        with DATA_PATH.open("r", encoding="utf-8") as file:
            payload = json.load(file)

        return payload.get("categories", [])

    def build_start_frame(self):
        title = tk.Label(self.start_frame, text="파트를 선택하세요", font=("Helvetica", 16, "bold"))
        title.pack(pady=20)

        self.category_listbox = tk.Listbox(self.start_frame, height=6, font=("Helvetica", 12))
        for category in self.categories:
            self.category_listbox.insert(tk.END, category["name"])
        self.category_listbox.pack(pady=10, fill=tk.X, padx=40)

        start_button = tk.Button(self.start_frame, text="시작", command=self.start_quiz)
        start_button.pack(pady=10)

    def build_quiz_frame(self):
        self.question_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 14), wraplength=460)
        self.question_label.pack(pady=20)

        self.choice_var = tk.StringVar(value="")
        self.choice_buttons = []
        for _ in range(4):
            button = tk.Radiobutton(
                self.quiz_frame,
                text="",
                variable=self.choice_var,
                value="",
                font=("Helvetica", 12),
                anchor="w",
                justify="left",
            )
            button.pack(fill=tk.X, padx=40, pady=2)
            self.choice_buttons.append(button)

        self.status_label = tk.Label(self.quiz_frame, text="", font=("Helvetica", 10))
        self.status_label.pack(pady=10)

        submit_button = tk.Button(self.quiz_frame, text="정답 제출", command=self.submit_answer)
        submit_button.pack(pady=5)

    def show_start(self):
        self.quiz_frame.pack_forget()
        self.start_frame.pack(fill=tk.BOTH, expand=True)

    def show_quiz(self):
        self.start_frame.pack_forget()
        self.quiz_frame.pack(fill=tk.BOTH, expand=True)

    def start_quiz(self):
        selection = self.category_listbox.curselection()
        if not selection:
            messagebox.showwarning("알림", "파트를 선택하세요.")
            return

        selected_index = selection[0]
        self.current_questions = list(self.categories[selected_index]["questions"])
        if not self.current_questions:
            messagebox.showwarning("알림", "선택한 파트에 문제가 없습니다.")
            return

        self.incorrect_questions = []
        self.start_cycle(self.current_questions)
        self.show_quiz()

    def start_cycle(self, questions):
        self.cycle_questions = list(questions)
        random.shuffle(self.cycle_questions)
        self.next_question()

    def next_question(self):
        if not self.cycle_questions:
            if self.incorrect_questions:
                messagebox.showinfo("오답 복습", "틀린 문제만 다시 풀어봅니다.")
                self.start_cycle(self.incorrect_questions)
                self.incorrect_questions = []
                return

            messagebox.showinfo("완료", "모든 문제를 맞혔습니다!")
            self.show_start()
            return

        self.current_question = self.cycle_questions.pop(0)
        self.render_question()

    def render_question(self):
        question_text = self.current_question["question"]
        options = list(self.current_question["options"])
        correct_index = self.current_question["answer"]
        self.current_correct_text = options[correct_index]

        random.shuffle(options)
        self.question_label.config(text=question_text)
        self.choice_var.set("")

        for idx, option in enumerate(options):
            label = f"{idx + 1}. {option}"
            self.choice_buttons[idx].config(text=label, value=option)

        self.status_label.config(text=f"남은 문제: {len(self.cycle_questions) + 1}")

    def submit_answer(self):
        selected = self.choice_var.get()
        if not selected:
            messagebox.showwarning("알림", "보기를 선택하세요.")
            return

        if selected != self.current_correct_text:
            self.incorrect_questions.append(self.current_question)

        self.next_question()


if __name__ == "__main__":
    app_root = tk.Tk()
    QuizApp(app_root)
    app_root.mainloop()
