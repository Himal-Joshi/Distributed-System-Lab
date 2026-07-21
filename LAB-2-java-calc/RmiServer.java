import java.rmi.Naming;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.server.UnicastRemoteObject;

public class RmiServer extends UnicastRemoteObject implements RmiServerIntf {

    public RmiServer() throws RemoteException {
        super();
    }

    public int add(int a, int b) throws RemoteException {
        return a + b;
    }

    public int subtract(int a, int b) throws RemoteException {
        return a - b;
    }

    public int multiply(int a, int b) throws RemoteException {
        return a * b;
    }

    public int divide(int a, int b) throws RemoteException {
        if (b == 0) {
            throw new RemoteException("Cannot divide by zero");
        }
        return a / b;
    }

    public static void main(String args[]) {
        try {
            System.out.println("RMI server started");

            LocateRegistry.createRegistry(1099);
            System.out.println("Java RMI registry created.");

            RmiServer obj = new RmiServer();
            Naming.rebind("//localhost/CalculatorService", obj);
            System.out.println("Calculator service bound in registry");
        } catch (Exception e) {
            System.err.println("RMI server exception: " + e.getMessage());
            e.printStackTrace();
        }
    }
}
