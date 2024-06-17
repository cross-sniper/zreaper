import sys
import os
import traceback
import time


def excepthook(exctype, value, tb):
    # Extract the traceback summary
    tb_summary = traceback.extract_tb(tb)

    if tb_summary:
        # Get the most relevant (last) traceback call
        last_call = tb_summary[-1]
        filename = os.path.basename(last_call.filename)
        lineno = last_call.lineno
        name = last_call.name
        line = last_call.line

        # Timestamp
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

        # Get context lines
        context_lines = 3
        try:
            with open(last_call.filename, "r") as f:
                file_lines = f.readlines()
                start = max(0, lineno - context_lines - 1)
                end = min(len(file_lines), lineno + context_lines)
                context = "".join(file_lines[start:end])
        except Exception as e:
            context = "Error reading file context."

        # Function name
        function_name = f"  Function: {name}\n" if name != "<module>" else ""

        # Print a concise error message
        error_message = (
            f"{timestamp}\n"
            f"Exception: {exctype.__name__}: {value}\n"
            f"  Line: {lineno}\n"
            f"  File: {filename}\n"
            f"{function_name}"
            f"  Code:\n{indent_code(line.strip())}\n"
            f"  Context:\n{context}\n"
        )
        print(error_message)

    else:
        print(f"{exctype.__name__}: {value}")

    # Optional full traceback (uncomment to enable)
    # traceback.print_exception(exctype, value, tb)

    exit(1)


def indent_code(code):
    return "\n".join(["\t" + line for line in code.split("\n")])


def safeEval(code="", functions={}, variables={}):
    exec(code, functions, variables)


# Set the custom excepthook
sys.excepthook = excepthook

if __name__ == "__main__":
    # To test the error message
    print(1 / 0)
