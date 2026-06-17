# Konvention für diese Datei:
# - Jede Python-Zeile/jeder Python-Block wird direkt darüber als Kommentar
#   mit dem äquivalenten Java-Code versehen.
# - Diese Datei enthält ausschließlich Klassendefinitionen, keine direkte
#   Ausführung auf Modulebene (kein Code außerhalb von Klassen/Methoden).
# - Die hier definierten Klassen werden in main.py importiert und dort verwendet.

# Thema: Fehlerbehandlung in Python (try/except)


# import java.util.Scanner;
#
# public class NumberInputHandler {
class NumberInputHandler:

    #     public void readNumber() {
    def read_number(self):
        #         Scanner scanner = new Scanner(System.in);
        #         String input = scanner.nextLine();
        user_input = input("Enter a number: ")

        #         try {
        try:
            #             int num = Integer.parseInt(input);
            num = int(user_input)
            #             System.out.println("you entered: " + num);
            print("you entered: " + str(num))
        #         } catch (NumberFormatException e) {
        except ValueError:
            #             System.out.println("invalid number");
            print("invalid number")
        #     }
        # }
# }


# import java.util.Scanner;
#
# public class DivisionHandler {
class DivisionHandler:

    #     public void divideNumbers() {
    def divide_numbers(self):
        #         Scanner scanner = new Scanner(System.in);
        #         try {
        try:
            #             System.out.print("Enter numerator: ");
            #             int numerator = Integer.parseInt(scanner.nextLine());
            numerator = int(input("Enter numerator: "))
            #             System.out.print("Enter denominator: ");
            #             int denominator = Integer.parseInt(scanner.nextLine());
            denominator = int(input("Enter denominator: "))
            #             int result = numerator / denominator;
            #             System.out.println("Result: " + result);
            result = numerator / denominator
            print("Result: " + str(result))
        #         } catch (NumberFormatException e) {
        except ValueError:
            #             System.out.println("invalid number");
            print("invalid number")
        #         } catch (ArithmeticException e) {
        except ZeroDivisionError:
            #             System.out.println("cannot divide by zero");
            print("cannot divide by zero")
        #     }
        # }
# }
# import java.util.Scanner;
#
# public class MultiErrorHandler {
class MultiErrorHandler:

    #     public void calculate() {
    def calculate(self):
        #         Scanner scanner = new Scanner(System.in);
        #         try {
        try:
            #             System.out.print("Enter numerator: ");
            #             int numerator = Integer.parseInt(scanner.nextLine());
            numerator = int(input("Enter numerator: "))
            #             System.out.print("Enter denominator: ");
            #             int denominator = Integer.parseInt(scanner.nextLine());
            denominator = int(input("Enter denominator: "))
            #             int result = numerator / denominator;
            #             System.out.println("Result: " + result);
            result = numerator / denominator
            print("Result: " + str(result))
        #         } catch (NumberFormatException | ArithmeticException e) {
        except (ValueError, ZeroDivisionError) as e:
            #             System.out.println("Error: " + e.getMessage());
            print("Error: " + str(e))
        #     }
        # }
# }


# import java.util.Scanner;
#
# public class CatchAllHandler {
class CatchAllHandler:

    #     public void calculate() {
    def calculate(self):
        #         Scanner scanner = new Scanner(System.in);
        #         try {
        try:
            #             System.out.print("Enter numerator: ");
            #             int numerator = Integer.parseInt(scanner.nextLine());
            numerator = int(input("Enter numerator: "))
            #             System.out.print("Enter denominator: ");
            #             int denominator = Integer.parseInt(scanner.nextLine());
            denominator = int(input("Enter denominator: "))
            #             int result = numerator / denominator;
            #             System.out.println("Result: " + result);
            result = numerator / denominator
            print("Result: " + str(result))
        #         } catch (Exception e) {
        except Exception as e:
            #             System.out.println("An error occurred: " + e.getMessage());
            print("An error occurred: " + str(e))
        #     }
        # }
# }


# import java.util.Scanner;
#
# public class AgeValidator {
class AgeValidator:

    #     public void validateAge() {
    def validate_age(self):
        #         Scanner scanner = new Scanner(System.in);
        #         try {
        try:
            #             System.out.print("Enter your age: ");
            #             int age = Integer.parseInt(scanner.nextLine());
            age = int(input("Enter your age: "))
            #             if (age < 0) {
            #                 throw new IllegalArgumentException("Age cannot be negative.");
            #             }
            if age < 0:
                raise ValueError("Age cannot be negative.")
            #             System.out.println("Your age is: " + age);
            print("Your age is: " + str(age))
        #         } catch (NumberFormatException e) {
        except ValueError as e:
            #             System.out.println("Invalid input: " + e.getMessage());
            print("Invalid input: " + str(e))
        #     }
        # }
# }
