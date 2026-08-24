import json
import uuid
import matplotlib.pyplot as plt
class QuizCreation:
        def __init__(self):
            #list to stor questions and answer
            self.questions=[]
            self.batch_size=50
            
        def add_question(self):
            #allow teachers to input questions and answer
            question=input("Enter the question:")
            options=[]
            #for storing options
            for i in range(4):
                option=input(f"enter the option{i+1}:")
                options.append(option)
            answer=input("Enter the correct answer:")
            self.questions.append({"question":question,"options":options,"answer":answer})
            if len(self.questions)>=self.batch_size:
                self.save_batch()
            
        def save_batch(self):
            unique_code = str(uuid.uuid4())[:8]
            filename=f"questions_{unique_code}.json"
            with open(filename,"w") as file :
                json.dump(self.questions,file,indent=4)
                print(f"batch saved with {filename} with {len(self.questions)} questions!")     
                self.questions=[]
                    
        def force_save(self):
            if self.questions:
                self.save_batch()
            else:
                print("no unsaved questions to write")
                 
        def take_quiz(self):
            #function to attempt quiz
            filename=input("enter the file name for the quiz:")
            try:
                with open(filename,"r") as file:
                    questions=json.load(file)
            except FileNotFoundError:
                print(f"file {filename} not found")
                return             
            
            score=0
            num=0
            for q in questions:
                 num=num+1;
                 print(q["question"])
                 for idx,option in enumerate(q["options"],1):
                     print(f"{idx}.{option}")
                 user_answer=input("Enter the answer:")
                 if user_answer.lower()==q["answer"].lower():
                     score=score+1
                     print("Correct!!\n")
                 else:
                    print(f"Incorrect answer\n the correct answer is:{q['answer']}\n")
            print(f"Quiz completed!!\nyour score {score}/{num}\n")

            obtained = score
            total = num

            if total == 0:
                print("Total score cannot be zero.")
                exit()

            missed = total - obtained

            labels = ['Correct', 'Incorrect']
            sizes = [obtained, missed]
            colors = ['#4CAF50', '#F44336']

            plt.figure(figsize=(10, 5))

            plt.subplot(1, 2, 1)
            plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            plt.title("Quiz Performance (Pie Chart)")

            plt.subplot(1, 2, 2)
            plt.bar(labels, sizes, color=colors)
            plt.title("Quiz Performance (Bar Graph)")
            plt.ylabel("Number of Questions")

            plt.tight_layout()
            plt.show()
 
    
 
            
