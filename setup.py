import subprocess
import sys

def install_requirements():
    print("Installing required packages...")
    try:
        # Install requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("\nAll packages installed successfully!")
        
    except subprocess.CalledProcessError as e:
        print(f"\nError installing packages: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_requirements() 