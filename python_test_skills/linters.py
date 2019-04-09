import subprocess
import io
from pprint import pprint

FILE_NAME = 'tmp.py'

def linter_stream(string_value):
    with open(FILE_NAME, 'w') as file:
        file.write(string_value)
        process = subprocess.Popen(["flake8", FILE_NAME], stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT)
    result = ''
    for line in io.TextIOWrapper(process.stdout, encoding="utf-8"):
        result += line
    return result


if __name__ == '__main__':
    print(linter_stream('print("New Hello world")'))