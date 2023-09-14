from IPython import get_ipython
from flask import Flask, request, jsonify, render_template
from IPython.core.interactiveshell import InteractiveShell


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/execute-code', methods=['POST'])
def execute_code():
    code = request.json.get('code', '')
    
    # Initialize IPython shell instance
    ipython = InteractiveShell()
    
    try:
        # Execute the code using IPython's run_cell
        result = ipython.run_cell(code)
        
        # Check if there's an error in the result object
        if result.error_in_exec:
            return jsonify({"error": str(result.error_in_exec)})
        
        # Return the result or an empty string if result.result is None
        return jsonify({"output": str(result.result) if result.result else ""})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
