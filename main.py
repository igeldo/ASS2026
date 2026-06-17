from informatik4_oop_java_zu_python import NumberInputHandler, DivisionHandler, MultiErrorHandler, CatchAllHandler, AgeValidator

if __name__ == "__main__":
    print("Wähle eine Klasse:")
    print("1 - NumberInputHandler")
    print("2 - DivisionHandler")
    print("3 - MultiErrorHandler")
    print("4 - CatchAllHandler")
    print("5 - AgeValidator")

    choice = input("Eingabe (1-5): ")

    if choice == "1":
        NumberInputHandler().read_number()
    elif choice == "2":
        DivisionHandler().divide_numbers()
    elif choice == "3":
        MultiErrorHandler().calculate()
    elif choice == "4":
        CatchAllHandler().calculate()
    elif choice == "5":
        AgeValidator().validate_age()
    else:
        print("Ungültige Auswahl.")
