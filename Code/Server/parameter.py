# Import necessary modules
import os
import json
import subprocess

class ParameterManager:
    # Define the default parameter file name
    PARAM_FILE = 'params.json'

    def __init__(self):
        # Initialize the file path to the default parameter file
        self.file_path = self.PARAM_FILE
        if self.file_exists() == False or self.validate_params() == False:
            self.deal_with_param()

    def file_exists(self, file_path=None):
        # Check if the specified file exists
        file_path = file_path or self.file_path
        return os.path.exists(file_path)

    def validate_params(self, file_path=None):
        # Validate that the parameter file exists and contains valid parameters
        file_path = file_path or self.file_path
        if not self.file_exists(file_path):
            return False
        try:
            with open(file_path, 'r') as file:
                params = json.load(file)
                # Check if required parameters are present and valid
                return ('Pcb_Version' in params and params['Pcb_Version'] in [1, 2]) and \
                       ('Pi_Version' in params and params['Pi_Version'] in [1, 2])
        except json.JSONDecodeError:
            print("Error decoding JSON file.")
            return False
        except Exception as e:
            print(f"Error reading file: {e}")
            return False

    def get_param(self, param_name, file_path=None):
        # Get the value of a specified parameter from the parameter file
        file_path = file_path or self.file_path
        if self.validate_params(file_path):
            with open(file_path, 'r') as file:
                params = json.load(file)
                return params.get(param_name)
        return None

    def set_param(self, param_name, value, file_path=None):
        # Set the value of a specified parameter in the parameter file
        file_path = file_path or self.file_path
        params = {}
        if self.file_exists(file_path):
            with open(file_path, 'r') as file:
                params = json.load(file)
        params[param_name] = value
        with open(file_path, 'w') as file:
            json.dump(params, file, indent=4)
        # print(f"{param_name} set to {value}")

    def delete_param_file(self, file_path=None):
        # Delete the specified parameter file
        file_path = file_path or self.file_path
        if self.file_exists(file_path):
            os.remove(file_path)
            print(f"Deleted {file_path}")
        else:
            print(f"File {file_path} does not exist")

    def create_param_file(self, file_path=None):
        # Create a parameter file and set default parameters
        file_path = file_path or self.file_path
        default_params = {
            'Pcb_Version': 2,
            'Pi_Version': self.get_raspberry_pi_version()
        }
        with open(file_path, 'w') as file:
            json.dump(default_params, file, indent=4)
        # print(f"Created {file_path} with default values")

    def get_raspberry_pi_version(self):
        # Get the version of the Raspberry Pi
        try:
            result = subprocess.run(['cat', '/sys/firmware/devicetree/base/model'], capture_output=True, text=True)
            if result.returncode == 0:
                model = result.stdout.strip()
                if "Raspberry Pi 5" in model:
                    return 2
                else:
                    return 1
            else:
                print("Failed to get Raspberry Pi model information.")
                return 1
        except Exception as e:
            print(f"Error getting Raspberry Pi version: {e}")
            return 1

    def deal_with_param(self):
        # Main function to manage parameter file
        if not self.file_exists() or not self.validate_params():
            print(f"Parameter file {self.PARAM_FILE} does not exist or contains invalid parameters.")
            user_input_required = True
        else:
            user_choice = input("Do you want to re-enter the hardware versions? (yes/no): ").strip().lower()
            user_input_required = user_choice == 'yes'

        if user_input_required:
            print("Please enter the hardware versions.")
            while True:
                try:
                    pcb_version = int(input("Enter PCB Version (1 or 2): "))
                    if pcb_version in [1, 2]:
                        break
                    else:
                        print("Invalid PCB Version. Please enter 1 or 2.")
                except ValueError:
                    print("Invalid input. Please enter a number.")
            pi_version = self.get_raspberry_pi_version()
            self.create_param_file()
            self.set_param('Pcb_Version', pcb_version)
            self.set_param('Pi_Version', pi_version)
        else:
            print("Do not modify the hardware version. Skipping...")

    def get_pcb_version(self):
        # Get the PCB version from the parameter file
        return self.get_param('Pcb_Version')

    def get_pi_version(self):
        # Get the Raspberry Pi version from the parameter file
        return self.get_param('Pi_Version')

if __name__ == '__main__':
    # Entry point of the script
    manager = ParameterManager()
    manager.deal_with_param()
    if manager.file_exists("params.json") and manager.validate_params("params.json"):
        pcb_version = manager.get_pcb_version()
        print(f"PCB Version: {pcb_version}.0")
        pi_version = manager.get_raspberry_pi_version()
        print(f"Raspberry PI version is {'less than 5' if pi_version == 1 else '5'}.")