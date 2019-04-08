"""The module to proceed Python code"""
import sys
import io
import multiprocessing


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
    # try:
    #     multiprocessing.set_start_method("spawn")
    # except RuntimeError:
    #     pass
    # queue = multiprocessing.Queue()
    # process = multiprocessing.Process(target=execute_in_process, args=(code, queue))
    # process.start()
    # result = queue.get()
    # process.join()
    # return result
    std_out, std_err = io.StringIO(), io.StringIO()
    sys.stdout, sys.stderr = std_out, std_err
    try:
        exec(code)
    except Exception as err:
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        return str(err)
        # return std_err.getvalue()
    else:
        sys.stdout, sys.stderr = sys.__stdout__, sys.__stderr__
        return std_out.getvalue()



