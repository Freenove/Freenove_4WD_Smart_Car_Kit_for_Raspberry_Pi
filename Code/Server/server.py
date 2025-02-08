import socket  # Import the socket module for network communication
import fcntl   # Import the fcntl module for I/O control
import struct  # Import the struct module for packing and unpacking data
from tcp_server import TCPServer  # Import the TCPServer class from the tcp_server module

class Server:
    def __init__(self):
        """Initialize the TankServer class."""
        self.ip_address = self.get_interface_ip()  # Get the IP address of the network interface
        self.command_server = TCPServer()          # Initialize the command server
        self.video_server = TCPServer()            # Initialize the video server
        self.command_server_is_busy = False        # Flag to indicate whether the command server is busy
        self.video_server_is_busy = False          # Flag to indicate whether the video server is busy

    def get_interface_ip(self) -> str:
        """Get the IP address of the wlan0 interface."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Create a UDP socket
            ip = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', b'wlan0'[:15])
            )[20:24])
            return ip
        except Exception as e:
            print(f"Error getting IP address: {e}")
            return "127.0.0.1"  # Default to localhost if an error occurs

    def start_tcp_servers(self, command_port: int = 5000, video_port: int = 8000, max_clients: int = 1, listen_count: int = 1) -> None:
        """Start the TCP servers on specified ports."""
        try:
            self.command_server.start(self.ip_address, command_port, max_clients, listen_count)  # Start the command server
            self.video_server.start(self.ip_address, video_port, max_clients, listen_count)      # Start the video server
        except Exception as e:
            print(f"Error starting TCP servers: {e}")

    def stop_tcp_servers(self) -> None:
        """Stop the TCP servers."""
        try:
            self.command_server.close()  # Close the command server
            self.video_server.close()    # Close the video server
        except Exception as e:
            print(f"Error stopping TCP servers: {e}")

    def set_command_server_busy(self, state: bool) -> None:
        """Set the busy state of the command server."""
        self.command_server_is_busy = state

    def set_video_server_busy(self, state: bool) -> None:
        """Set the busy state of the video server."""
        self.video_server_is_busy = state

    def get_command_server_busy(self) -> bool:
        """Get the busy state of the command server."""
        return self.command_server_is_busy

    def get_video_server_busy(self) -> bool:
        """Get the busy state of the video server."""
        return self.video_server_is_busy

    def send_data_to_command_client(self, data: bytes, ip_address: str = None) -> None:
        """Send data to the command server client(s)."""
        self.set_command_server_busy(True)
        try:
            if ip_address is not None:
                self.command_server.send_to_client(ip_address, data)  # Send data to a specific client
            else:
                self.command_server.send_to_all_client(data)         # Send data to all connected clients of the command server
        except Exception as e:
            print(e)
        finally:
            self.set_command_server_busy(False)

    def send_data_to_video_client(self, data: bytes, ip_address: str = None) -> None:
        """Send data to the video server client(s)."""
        self.set_video_server_busy(True)
        try:
            if ip_address is not None:
                self.video_server.send_to_client(ip_address, data)  # Send data to a specific client
            else:
                self.video_server.send_to_all_client(data)         # Send data to all connected clients of the video server
        finally:
            self.set_video_server_busy(False)

    def read_data_from_command_server(self) -> 'queue.Queue':
        """Read data from the command server's message queue."""
        return self.command_server.message_queue

    def read_data_from_video_server(self) -> 'queue.Queue':
        """Read data from the video server's message queue."""
        return self.video_server.message_queue

    def is_command_server_connected(self) -> bool:
        """Check if the command server has any active connections."""
        return self.command_server.active_connections > 0

    def is_video_server_connected(self) -> bool:
        """Check if the video server has any active connections."""
        return self.video_server.active_connections > 0

    def get_command_server_client_ips(self) -> list:
        """Get the list of client IP addresses connected to the command server."""
        return self.command_server.get_client_ips()

    def get_video_server_client_ips(self) -> list:
        """Get the list of client IP addresses connected to the video server."""
        return self.video_server.get_client_ips()

if __name__ == '__main__':
    print('Program is starting ... ')  # Print a message indicating the start of the program
    server = Server()              # Create an instance of the TankServer class
    server.start_tcp_servers(5003, 8003)  # Start the TCP servers on specified ports

    try:
        while True:
            cmd_queue = server.read_data_from_command_server()  # Get the command server's message queue
            if cmd_queue.qsize() > 0:  # Check if there are messages in the queue
                client_address, message = cmd_queue.get()  # Get a message from the queue
                print(client_address, message)  # Print the client address and message
                server.send_data_to_command_client(message, client_address)  # Send the message back to the client

            video_queue = server.read_data_from_video_server()  # Get the video server's message queue
            if video_queue.qsize() > 0:  # Check if there are messages in the queue
                client_address, message = video_queue.get()  # Get a message from the queue
                print(client_address, message)  # Print the client address and message
                server.send_data_to_video_client(message, client_address)  # Send the message back to the client

    except KeyboardInterrupt:  # Catch keyboard interrupt
        print("Received interrupt signal, stopping server...")  # Print interrupt information
        server.stop_tcp_servers()  # Stop the TCP servers