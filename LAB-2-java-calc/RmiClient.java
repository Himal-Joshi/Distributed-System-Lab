import java.rmi.Naming;
import java.util.Scanner;

public class RmiClient {
    public static void main(String args[]) {
        try {
            RmiServerIntf obj = (RmiServerIntf) Naming.lookup("//localhost/CalculatorService");

            Scanner scanner = new Scanner(System.in);

            System.out.print("Enter the first number: ");
            int a = scanner.nextInt();

            System.out.print("Enter the second number: ");
            int b = scanner.nextInt();

            System.out.println("Addition result: " + obj.add(a, b));
            System.out.println("Subtraction result: " + obj.subtract(a, b));
            System.out.println("Multiplication result: " + obj.multiply(a, b));

            try {
                System.out.println("Division result: " + obj.divide(a, b));
            } catch (Exception e) {
                System.out.println("Division error: " + e.getMessage());
            }
        } catch (Exception e) {
            System.err.println("RMI client exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
