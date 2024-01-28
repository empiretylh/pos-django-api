import os
import sys
from django.core.management import execute_from_command_line

if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')

    # Read the domain from the file
    with open('domain.txt', 'r') as file:
        domain = file.read().strip()

    execute_from_command_line([sys.argv[0], 'runserver', domain])