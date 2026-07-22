import Pyro4

@Pyro4.expose
class Calculator(object):
    def add(self, x, y):
        return x + y

    def subtract(self, x, y):
        return x - y

# Create a Pyro4 daemon
daemon = Pyro4.Daemon()
uri = daemon.register(Calculator)

# Print the URI
print("Server URI:", uri)

# Start the server
print("Calculator server started. Press Ctrl+C to exit.")

try:
    daemon.requestLoop()
except KeyboardInterrupt:
    print("\nExiting Calculator server.")
    daemon.shutdown()
