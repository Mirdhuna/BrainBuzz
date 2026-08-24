class Login:
    def main_menu(self):
        while(True):
            print("1.Already Have an account")
            print("2.create Acoount")
            print("3.exit")
            choice=int(input("enter yor choice:"))
            if choice==1:
                return self.login()
            elif choice==2:
                self.createAccount()
            else:
                print("EXiting.....")
                break
        
    def login(self):
        while True:
            user_ip=input("enter the mail id:").strip()
            pwd_ip=input("enter the password:").strip()
            try:
                with open("password.txt","r") as file:
                    for line in file:
                        user,pwd=line.strip().split()
                        if user==user_ip and pwd_ip==pwd:
                            print("you are successfully logged in!")
                            return True
                    print("Invalid username or password")
            except FileNotFoundError:
                    print("No user is found,please create an account")
                    return 
                    
    def createAccount(self):
        print("Enter the following informations to create the account:")
        user_name=input("enter the user name:")
        user_mail=input("enter the user mail id:")
        user_ph=input("enter the phone number:")
        user_pwd=input("enter the password:")
        while(len(user_pwd)<6):
            user_pwd=input("the password is less than six characters,try agin:")
        file1=open("user_details.txt","a")
        file2=open("password.txt","a")
        file1.write(f"{user_name} {user_mail} {user_ph} {user_pwd}\n")
        file2.write(f"{user_mail} {user_pwd}\n")
        file1.close()
        file2.close()
