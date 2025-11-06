from calculator import sqrt, factorial, ln, power, DomainError

def menu():
    print("Scientific Calculator")
    print("1) sqrt(x)")
    print("2) factorial(n)")
    print("3) ln(x)")
    print("4) power(a, b)")
    print("5) exit")

while True:
    menu()
    choice = input("Choose: ").strip()
    try:
        if choice == "1":
            x = float(input("x = "))
            print("=", sqrt(x))
        elif choice == "2":
            n = int(input("n = "))
            print("=", factorial(n))
        elif choice == "3":
            x = float(input("x = "))
            print("=", ln(x))
        elif choice == "4":
            a = float(input("a = "))
            b = float(input("b = "))
            print("=", power(a, b))
        elif choice == "5":
            break
        else:
            print("Invalid option")
    except DomainError as e:
        print("Error:", e)
    except ValueError:
        print("Error: invalid number")


# IMT2022100