def menu():
    while True:
        print("\nMenu:")
        print("0 - Exit App")
        choice = input("Enter your choice: ")
        if choice == "0":
            print("Goodbye!")
            break

if __name__ == "__main__":
    menu()
