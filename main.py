from authentication import register, login, reset_password

# Test code for Iteration One
# Need to rewrite main loop for GUI implementation. Djongo? Flask? Ask Kurgan for Djongo Book

def main():
    while True:
        print("\n=== Academic Forum ===")
        print("1. Register")
        print("2. Login")
        print("3. Reset Password")
        print("4. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            register()
        elif choice == "2":
            if login():
                print("Login in successful")
                # Redirect to other parts of my app here
        elif choice == "3":
            reset_password()
        elif choice == "4":
            print("Exit")
            break
        else:
            print("Invalid choice. Please try again.")

main()



