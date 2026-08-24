
import Login
import QuizCreation

l = Login.Login()
q = QuizCreation.QuizCreation()

v = True
while v:
    print("\n----------------Welcome to the quiz-----------------")
    print("1. Teacher")
    print("2. Student")
    print("3. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Please enter a valid number.")
        continue

    if choice == 1:
        print("Welcome, Teacher!")
        val = l.main_menu()
        if val:
            while True:
                print("\n--- Teacher Menu ---")
                print("1. Add Questions")
                print("2. Save Remaining Questions")
                print("3. Take Quiz")
                print("4. Exit")
                ch = input("Enter your choice: ")

                if ch == "1":
                    q.add_question()
                elif ch == "2":
                    q.force_save()
                elif ch == "3":
                    q.take_quiz()
                elif ch == "4":
                    q.force_save()
                    print("Exiting teacher menu...")
                    break
                else:
                    print("Invalid choice. Please try again.\n")

    elif choice == 2:
        print("Welcome, Student!")
        val = l.main_menu()
        if val:
            q.take_quiz()

    elif choice == 3:
        print("Thank you for using the quiz system!")
        v = False
    else:
        print("Invalid choice. Please try again.\n")
