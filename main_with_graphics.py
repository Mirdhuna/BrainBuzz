
import json
import uuid
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# Dummy Login class
class Login:
    def login_gui(self, email, password):
        try:
            with open("password.txt", "r") as f:
                for line in f:
                    user, pwd = line.strip().split()
                    if user == email and pwd == password:
                        return True
        except FileNotFoundError:
            return False
        return False

# QuizCreation class
class QuizCreation:
    def __init__(self):
        self.questions = []
        self.batch_size = 50

    def add_question(self):
        question = input("Enter the question:")
        options = []
        for i in range(4):
            option = input(f"Enter option {i + 1}:")
            options.append(option)
        answer = input("Enter the correct answer:")
        self.questions.append({"question": question, "options": options, "answer": answer})
        if len(self.questions) >= self.batch_size:
            self.save_batch()

    def save_batch(self):
        unique_code = str(uuid.uuid4())[:8]
        filename = f"questions_{unique_code}.json"
        with open(filename, "w") as file:
            json.dump(self.questions, file, indent=4)
            print(f"Batch saved as {filename} with {len(self.questions)} questions!")
            self.questions = []

    def force_save(self):
        if self.questions:
            self.save_batch()
        else:
            print("No unsaved questions to write")

    @staticmethod
    def load_questions(file_obj):
        return json.load(file_obj)


# Main GUI App
l = Login()
q = QuizCreation()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Application")
        self.root.geometry("600x400")
        self.build_home()

    def build_home(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Welcome to the Quiz App!", font=("Helvetica", 16)).pack(pady=20)
        tk.Button(self.root, text="Teacher", width=20, command=self.teacher_login).pack(pady=10)
        tk.Button(self.root, text="Student", width=20, command=self.student_login).pack(pady=10)
        tk.Button(self.root, text="Exit", width=20, command=self.root.quit).pack(pady=10)

    def teacher_login(self):
        self.login_screen(role="teacher")

    def student_login(self):
        self.login_screen(role="student")

    def login_screen(self, role):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text=f"{role.capitalize()} Login", font=("Helvetica", 14)).pack(pady=10)
        email = tk.Entry(self.root)
        password = tk.Entry(self.root, show="*")
        email.pack(pady=5)
        password.pack(pady=5)

        def try_login():
            l_input = email.get()
            p_input = password.get()
            if l.login_gui(l_input, p_input):
                if role == "teacher":
                    self.teacher_menu()
                else:
                    self.quiz_screen()
            else:
                messagebox.showerror("Error", "Invalid credentials")

        tk.Button(self.root, text="Login", command=try_login).pack(pady=10)
        tk.Button(self.root, text="Create Account", command=lambda: self.create_account_screen(role)).pack(pady=5)
        tk.Button(self.root, text="Back", command=self.build_home).pack()

    def create_account_screen(self, role):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Create Account", font=("Helvetica", 14)).pack(pady=10)
        email_entry = tk.Entry(self.root)
        password_entry = tk.Entry(self.root, show="*")
        email_entry.pack(pady=5)
        password_entry.pack(pady=5)

        def save_account():
            email = email_entry.get()
            password = password_entry.get()

            if not email or not password:
                messagebox.showerror("Error", "Please enter both email and password")
                return

            try:
                with open("password.txt", "a") as f:
                    f.write(f"{email} {password}\n")
                messagebox.showinfo("Success", "Account created successfully!")
                self.login_screen(role)
            except Exception as e:
                messagebox.showerror("Error", f"Could not create account: {e}")

        tk.Button(self.root, text="Submit", command=save_account).pack(pady=10)
        tk.Button(self.root, text="Back", command=lambda: self.login_screen(role)).pack()

    def teacher_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Teacher Menu", font=("Helvetica", 14)).pack(pady=10)
        tk.Button(self.root, text="Add Question", width=25, command=self.add_question_screen).pack(pady=5)
        tk.Button(self.root, text="Force Save", width=25, command=q.force_save).pack(pady=5)
        tk.Button(self.root, text="Take Quiz", width=25, command=self.quiz_screen).pack(pady=5)
        tk.Button(self.root, text="Back", width=25, command=self.build_home).pack(pady=5)

    def add_question_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        tk.Label(self.root, text="Add Question", font=("Helvetica", 14)).pack(pady=10)

        question = tk.Entry(self.root, width=40)
        options = [tk.Entry(self.root) for _ in range(4)]
        answer = tk.Entry(self.root)

        question.pack(pady=5)
        for o in options:
            o.pack(pady=2)
        answer.pack(pady=5)

        def submit():
            q.questions.append({
                "question": question.get(),
                "options": [o.get() for o in options],
                "answer": answer.get()
            })
            messagebox.showinfo("Success", "Question Added")
            self.teacher_menu()

        tk.Button(self.root, text="Submit", command=submit).pack(pady=10)

    def quiz_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        filename = simpledialog.askstring("Input", "Enter quiz filename:")
        try:
            with open(filename, "r") as f:
                self.quiz_data = QuizCreation.load_questions(f)
        except Exception:
            messagebox.showerror("Error", "File not found or invalid!")
            self.build_home()
            return

        self.current_q = 0
        self.score = 0
        self.show_question()

    def show_question(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        if self.current_q >= len(self.quiz_data):
            self.show_results_graph(self.score, len(self.quiz_data))
            return

        q_data = self.quiz_data[self.current_q]
        tk.Label(self.root, text=q_data["question"], wraplength=350).pack(pady=10)
        var = tk.StringVar()

        for opt in q_data["options"]:
            tk.Radiobutton(self.root, text=opt, variable=var, value=opt).pack(anchor='w')

        def submit_answer():
            if var.get().lower() == q_data["answer"].lower():
                self.score += 1
            self.current_q += 1
            self.show_question()

        tk.Button(self.root, text="Submit", command=submit_answer).pack(pady=10)

    def show_results_graph(self, score, total):
        for widget in self.root.winfo_children():
            widget.destroy()

        missed = total - score

        fig = Figure(figsize=(8, 4), dpi=100)
        ax1 = fig.add_subplot(121)
        ax2 = fig.add_subplot(122)

        ax1.pie([score, missed], labels=['Correct', 'Incorrect'],
                colors=['#4CAF50', '#F44336'], autopct='%1.1f%%', startangle=140)
        ax1.set_title("Quiz Performance (Pie Chart)")

        ax2.bar(['Correct', 'Incorrect'], [score, missed], color=['#4CAF50', '#F44336'])
        ax2.set_title("Quiz Performance (Bar Graph)")
        ax2.set_ylabel("Number of Questions")

        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        canvas.get_tk_widget().pack()

        tk.Label(self.root, text=f"Final Score: {score}/{total}", font=("Helvetica", 12)).pack(pady=10)
        tk.Button(self.root, text="Back to Home", command=self.build_home).pack(pady=10)


# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
