from IPython import display
from flask import Flask, request, jsonify, render_template
from IPython.core.interactiveshell import InteractiveShell
import io,sys


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute-code', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')

    # Initialize a new IPython shell instance
    ipython = InteractiveShell()

    # Redirect stdout to capture the output
    original_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        result = ipython.run_cell(code)

        # Restore original stdout
        sys.stdout = original_stdout

        # Get captured output
        stdout_output = buffer.getvalue()

        if result.error_in_exec:
            return jsonify({"error": str(result.error_in_exec)})

        # Combine stdout output with the result of the last expression
        combined_output = stdout_output + (str(result.result) if result.result else "")
        return jsonify({"output": combined_output})

    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        # Ensure the original stdout is always restored
        sys.stdout = original_stdout



if __name__ == '__main__':
    app.run(debug=True)
