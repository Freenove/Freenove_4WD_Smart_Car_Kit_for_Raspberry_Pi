import subprocess

def check_and_install(package):
    try:
        __import__(package)
        return True
    except ImportError:
        install_command = f"sudo pip3 install {package}"
        try:
            subprocess.run(install_command, shell=True, check=True)
            return True
        except subprocess.CalledProcessError:
            print(f"Failed to install {package}.")
            return False

def apt_install(package):
    install_command = f"sudo apt-get install -y {package}"
    try:
        subprocess.run(install_command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to install {package} via apt-get.")
        return False

def custom_install(command):
    try:
        subprocess.run(command, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print(f"Failed to execute custom command: {command}")
        return False

def get_raspberry_pi_version():
    print("Getting Raspberry Pi version...")
    try:
        result = subprocess.run(['cat', '/sys/firmware/devicetree/base/model'], capture_output=True, text=True)
        if result.returncode == 0:
            model = result.stdout.strip()
            if "Raspberry Pi 5" in model:
                print("Detected Raspberry Pi 5")
                return 3
            elif "Raspberry Pi 3" in model:
                print("Detected Raspberry Pi 3")
                return 2
            else:
                print(f"Detected Raspberry Pi {model}")
                return 1
        else:
            print("Failed to get Raspberry Pi model information.")
            return 0
    except Exception as e:
        print(f"Error getting Raspberry Pi version: {e}")
        return 0

def update_config_file(file_path, command, value):
    new_content = []
    command_found = False
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        stripped_line = line.strip()
        if stripped_line.startswith(command) or stripped_line.startswith(f'#{command}'):
            command_found = True
            new_content.append(f'{command}={value}\n')
        else:
            new_content.append(line)
    if not command_found:
        new_content.append(f'\n{command}={value}\n')
    with open(file_path, 'w') as f:
        f.writelines(new_content)
    print(f"Updated {file_path} with '{command}={value}'")

def config_camera_to_config_txt(file_path, command, value=None):
    new_content = []
    command_found = False
    with open(file_path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        stripped_line = line.strip()
        if 'ov5647' in stripped_line or 'imx219' in stripped_line:
            continue
        if stripped_line.startswith(f'dtoverlay={command}') or stripped_line.startswith(f'#dtoverlay={command}'):
            command_found = True
            if value:
                new_content.append(f'dtoverlay={command},{value}\n')
            else:
                new_content.append(f'dtoverlay={command}\n')
        else:
            new_content.append(line)
    if not command_found:
        if value:
            new_content.append(f'\ndtoverlay={command},{value}\n')
        else:
            new_content.append(f'\ndtoverlay={command}\n')
    with open(file_path, 'w') as f:
        f.writelines(new_content)
    value_str = f",{value}" if value else ""
    print(f"Updated {file_path} with 'dtoverlay={command}{value_str}'")

def backup_file(file_path):
    config_path = file_path
    backup_path = config_path + '.bak'
    print("Backing up ", backup_path)
    try:
        with open(config_path, 'rb') as src_file:
            with open(backup_path, 'wb') as dst_file:
                dst_file.write(src_file.read())
        print(f"Backup of {config_path} created at {backup_path}")
    except Exception as e:
        print(f"Error backing up {config_path}: {e}")

def config_file():
    pi_version = get_raspberry_pi_version()
    file_path = '/boot/firmware/config.txt'
    backup_file(file_path)
    update_config_file(file_path, 'dtparam=spi', 'on')
    update_config_file(file_path, 'camera_auto_detect', '0')
    while True:
        camera_model = input("\nEnter the camera model (e.g., ov5647 or imx219): ").strip().lower()
        if camera_model not in ['ov5647', 'imx219']:
            print("Invalid input. Please enter either ov5647 or imx219.")
        else:
            break
    if pi_version == 3:
        print("Setting up for Raspberry Pi 5")
        while True:
            camera_port = input("You have a Raspberry Pi 5. Which camera port is the camera connected to? cam0 or cam1: ").strip().lower()
            if camera_port not in ['cam0', 'cam1']:
                print("Invalid input. Please enter either cam0 or cam1.")
            else:
                break
        config_camera_to_config_txt(file_path, camera_model, camera_port)
    elif pi_version == 2:
        print("Setting up for Raspberry Pi 3")
        update_config_file(file_path, 'dtparam=audio', 'off')
        config_camera_to_config_txt(file_path, camera_model)
    else:
        config_camera_to_config_txt(file_path, camera_model)

def main():
    install_status = {
        "python3-dev python3-pyqt5": False,
        "numpy": False,
        "rpi-ws281x-python (custom install)": False
    }

    subprocess.run("sudo apt-get update", shell=True, check=True)
    install_status["python3-dev python3-pyqt5"] = apt_install("python3-dev python3-pyqt5")
    install_status["gpiozero"] = check_and_install("gpiozero")
    install_status["numpy"] = check_and_install("numpy")
    install_status["rpi-ws281x-python (custom install)"] = custom_install("cd ./Libs/rpi-ws281x-python/library && sudo python3 setup.py install")
    if all(install_status.values()):
        print("\nAll libraries have been installed successfully.")
        config_file()
        print("Please reboot your Raspberry Pi to complete the installation.")
    else:
        missing_libraries = [lib for lib, status in install_status.items() if not status]
        print(f"\nSome libraries have not been installed yet: {', '.join(missing_libraries)}. Please run the script again.")

if __name__ == "__main__":
    main()  