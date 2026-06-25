# Konvention für diese Datei:
# - Java-Äquivalent als Kommentarblock über jeder Klasse
# - Darunter der saubere Python-Code ohne Inline-Java-Kommentare
# - Diese Datei enthält ausschließlich Klassendefinitionen, keine direkte
#   Ausführung auf Modulebene (kein Code außerhalb von Klassen/Methoden).
# - Die hier definierten Klassen werden in main.py importiert und dort verwendet.

# Thema: Fehlerbehandlung in Python (try/except)


# Java-Äquivalent:
# import java.util.Scanner;
#
# public class NumberInputHandler {
#     public void readNumber() {
#         Scanner scanner = new Scanner(System.in);
#         String input = scanner.nextLine();
#         try {
#             int num = Integer.parseInt(input);
#             System.out.println("You entered " + num);
#         } catch (NumberFormatException e) {
#             System.out.println("invalid number");
#         } finally {
#             System.out.println("end of operation");
#         }
#     }
# }
# Hinweis: Python's try/except/else hat kein Java-Äquivalent.
#           In Java wird der else-Block in den try-Block verschoben.
class NumberInputHandler:

    def read_number(self):
        user_input = input("Enter a number: ")
        try:
            num = int(user_input)
        except ValueError:
            print("invalid number")
        else:
            print("You entered", num)
        finally:
            print("end of operation")


# Java-Äquivalent:
# import java.util.Scanner;
#
# public class DivisionHandler {
#     public void divideNumbers() {
#         Scanner scanner = new Scanner(System.in);
#         try {
#             System.out.print("Enter numerator: ");
#             int numerator = Integer.parseInt(scanner.nextLine());
#             System.out.print("Enter denominator: ");
#             int denominator = Integer.parseInt(scanner.nextLine());
#             int result = numerator / denominator;
#             System.out.println("Result: " + result);
#         } catch (NumberFormatException e) {
#             System.out.println("invalid number");
#         } catch (ArithmeticException e) {
#             System.out.println("cannot divide by zero");
#         } finally {
#             System.out.println("end of operation");
#         }
#     }
# }
class DivisionHandler:

    def divide_numbers(self):
        try:
            numerator = int(input("Enter numerator: "))
            denominator = int(input("Enter denominator: "))
            result = numerator / denominator
            print("Result: " + str(result))
        except ValueError:
            print("invalid number")
        except ZeroDivisionError:
            print("cannot divide by zero")
        finally:
            print("end of operation")


# Java-Äquivalent:
# import java.util.Scanner;
#
# public class MultiErrorHandler {
#     public void calculate() {
#         Scanner scanner = new Scanner(System.in);
#         try {
#             System.out.print("Enter numerator: ");
#             int numerator = Integer.parseInt(scanner.nextLine());
#             System.out.print("Enter denominator: ");
#             int denominator = Integer.parseInt(scanner.nextLine());
#             int result = numerator / denominator;
#             System.out.println("Result: " + result);
#         } catch (NumberFormatException | ArithmeticException e) {
#             System.out.println("Error: " + e.getMessage());
#         } finally {
#             System.out.println("end of operation");
#         }
#     }
# }
class MultiErrorHandler:

    def calculate(self):
        try:
            numerator = int(input("Enter numerator: "))
            denominator = int(input("Enter denominator: "))
            result = numerator / denominator
            print("Result: " + str(result))
        except (ValueError, ZeroDivisionError) as e:
            print("Error: " + str(e))
        finally:
            print("end of operation")


# Java-Äquivalent:
# import java.util.Scanner;
#
# public class CatchAllHandler {
#     public void calculate() {
#         Scanner scanner = new Scanner(System.in);
#         try {
#             System.out.print("Enter numerator: ");
#             int numerator = Integer.parseInt(scanner.nextLine());
#             System.out.print("Enter denominator: ");
#             int denominator = Integer.parseInt(scanner.nextLine());
#             int result = numerator / denominator;
#             System.out.println("Result: " + result);
#         } catch (Exception e) {
#             System.out.println("An error occurred: " + e.getMessage());
#         } finally {
#             System.out.println("end of operation");
#         }
#     }
# }
class CatchAllHandler:

    def calculate(self):
        try:
            numerator = int(input("Enter numerator: "))
            denominator = int(input("Enter denominator: "))
            result = numerator / denominator
            print("Result: " + str(result))
        except Exception as e:
            print("An error occurred: " + str(e))
        finally:
            print("end of operation")


# Java-Äquivalent:
# import java.util.Scanner;
#
# public class AgeValidator {
#     public void validateAge() {
#         Scanner scanner = new Scanner(System.in);
#         try {
#             System.out.print("Enter your age: ");
#             int age = Integer.parseInt(scanner.nextLine());
#             if (age < 0) {
#                 throw new IllegalArgumentException("Age cannot be negative.");
#             }
#             System.out.println("Your age is: " + age);
#         } catch (NumberFormatException | IllegalArgumentException e) {
#             System.out.println("Invalid input: " + e.getMessage());
#         } finally {
#             System.out.println("end of operation");
#         }
#     }
# }
class AgeValidator:

    def validate_age(self):
        try:
            age = int(input("Enter your age: "))
            if age < 0:
                raise ValueError("Age cannot be negative.")
            print("Your age is: " + str(age))
        except ValueError as e:
            print("Invalid input: " + str(e))
        finally:
            print("end of operation")
