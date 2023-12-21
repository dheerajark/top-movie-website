import subprocess


def uninstall_packages():
    with open('requirements.txt', 'r') as file:
        packages = file.readlines()
        for package in packages:
            package = package.strip()  # Remove leading/trailing whitespaces and newlines
            if package:  # Check if the line is not empty
                try:
                    subprocess.check_call(['pip', 'uninstall', '-y', package])
                except subprocess.CalledProcessError as e:
                    print(f"Failed to uninstall {package}: {e}")


if __name__ == '__main__':
    uninstall_packages()
