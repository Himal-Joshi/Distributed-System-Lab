import Pyro4

# Prompt the user to enter the URI of the server
uri = input("Enter the URI of the server: ")

# Connect to the server
calc = Pyro4.Proxy(uri)

# Function to perform addition
def perform_addition():
    x = float(input("Enter the first number: "))
    y = float(input("Enter the second number: "))
    result = calc.add(x, y)
    print("Result of addition:", result)

# Function to perform subtraction
def perform_subtraction():
    x = float(input("Enter the first number: "))
    y = float(input("Enter the second number: "))
    result = calc.subtract(x, y)
    print("Result of subtraction:", result)

# Interactive menu
while True:
    print("\nChoose an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Exit")

    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        perform_addition()
    elif choice == "2":
        perform_subtraction()
    elif choice == "3":
        print("Exiting client.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
