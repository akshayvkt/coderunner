from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute-code', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')

    output_dict = {"output": ""}

    def capture_print(*args, **kwargs):
        output_dict["output"] += " ".join(map(str, args)) + "\n"

    try:
        # Temporarily override the built-in print function
        original_print = __builtins__.print
        __builtins__.print = capture_print

        # First, try to evaluate the code as an expression
        try:
            result = eval(code)
            if result is not None:  # Only capture if there's a result
                output_dict["output"] += str(result) + "\n"
        except SyntaxError:
            # If it's not an expression, execute it as a statement
            exec(code)

        return jsonify(output_dict)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        # Restore the original print function
        __builtins__.print = original_print


if __name__ == '__main__':
    app.run(debug=True)
