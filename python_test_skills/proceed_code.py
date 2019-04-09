"""The module to proceed Python code"""
import sys
import io


def execute_in_process(code, queue):
    std_out, std_err = io.StringIO(), io.StringIO()
    sys.stdout, sys.stderr = std_out, std_err
    try:
        exec(code)
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
    except Exception as err:
        result = err
        queue.put(result)
    else:
        queue.put(std_out.getvalue())

def execute_code(code):
    """
    The functions executes Python code.
    :param code: a string values containts python code in str format.
    :return: results of executions from terminal in str format.
    """
    std_out, std_err = io.StringIO(), io.StringIO()
    sys.stdout, sys.stderr = std_out, std_err
    try:
        exec(code)
    except Exception as err:
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        executed_code = str(err)
    else:
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        executed_code = std_out.getvalue()
    return executed_code


