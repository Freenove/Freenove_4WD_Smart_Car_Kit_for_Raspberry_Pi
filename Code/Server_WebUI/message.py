import queue

class Message_Parse:
    def __init__(self):
        """Initialize the Message_Parse class with empty parameters."""
        self.input_string = None    # The raw input string
        self.string_parameter = []  # List to store string parameters
        self.int_parameter = []     # List to store integer parameters
        self.command_string = None  # The command string extracted from the input

    def clear_parameters(self):
        """Clear all parsed parameters."""
        self.input_string = None       # Reset the input string
        self.string_parameter.clear()  # Clear the list of string parameters
        self.int_parameter.clear()     # Clear the list of integer parameters
        self.command_string = None     # Reset the command string

    def parse(self, msg: str) -> bool:
        """
        Parse the input message and extract command and parameters.
        Parameters:
        msg (str): The input message to parse.
        Returns:
        bool: True if parsing is successful, False otherwise.
        """
        try:
            self.clear_parameters()                              # Clear any existing parameters
            self.input_string = msg.strip()                      # Remove leading and trailing whitespace from the input message
            self.string_parameter = self.input_string.split("#")  # Split the input string by '#' to get parameters
            self.command_string = self.string_parameter[0]        # The first element is the command string
            buf_string_parameter = self.string_parameter[1:]      # Remaining elements are parameters
            if len(buf_string_parameter) > 0:
                for x in buf_string_parameter:
                    if x != "" and x != '':                        # Ensure the parameter is not an empty string
                        try:
                            self.int_parameter.append(round(float(x)))  # Convert the parameter to an integer and append to the list
                        except:
                            if x == 'one':
                                self.int_parameter.append(0)
                            elif x == 'two':
                                self.int_parameter.append(1)
                            elif x == 'three':
                                self.int_parameter.append(3)
                            elif x == 'four':
                                self.int_parameter.append(2)
                            else:
                                self.int_parameter.append(0)
            return True
        except Exception as e:
            print("Error: Invalid command or parameter.")       # Print an error message if parsing fails
            print("msg:{}".format(msg))                         # Print the original message
            self.clear_parameters()                              # Clear parameters in case of error
            print("Error:", e)                                  # Print the exception details
            return False

if __name__ == '__main__':
    print('Program is starting ... ')  # Print a message indicating the start of the program
    msg_parse = Message_Parse()       # Create an instance of the Message_Parse class
    my_queue = queue.Queue()           # Create a queue to hold messages

    print("Message Parse Test")        # Print a test start message
    print("Put message to queue")      # Indicate that a message is being added to the queue
    my_queue.put("CMD_LED#0#255#0#0#15#")  # Add a test message to the queue

    print("Get message from queue\n")  # Indicate that messages are being processed from the queue
    while not my_queue.empty():        # Process messages until the queue is empty
        print("Queue size: " + str(my_queue.qsize()))  # Print the current size of the queue
        if msg_parse.parse(my_queue.get()):  # Parse the message from the queue
            if len(msg_parse.int_parameter) > 0 and len(msg_parse.string_parameter) > 0:
                print("msg.input_string: {}".format(msg_parse.input_string))          # Print the raw input string
                print("msg.string_parameter: {}".format(msg_parse.string_parameter))  # Print the list of string parameters
                print("msg.command_string: {}".format(msg_parse.command_string))      # Print the command string
                print("msg.int_parameter:{}\n".format(msg_parse.int_parameter))       # Print the list of integer parameters
            elif len(msg_parse.string_parameter) > 0 and len(msg_parse.int_parameter) == 0:
                print("msg.input_string: {}".format(msg_parse.input_string))          # Print the raw input string
                print("msg.command_string: {}\n".format(msg_parse.command_string))    # Print the command string
            else:
                print("msg.input_string: {}".format(msg_parse.input_string))          # Print the raw input string

    print("Test end")  # Indicate the end of the test