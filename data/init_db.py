import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data.database import initialize_database

# from database import initialize_database

def main():
    print("Initializing the database...")
    initialize_database()

if __name__ == "__main__":
    main()