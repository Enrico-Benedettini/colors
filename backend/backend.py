from flask import Flask, request, jsonify, abort
import os
import tempfile
from sat_solver import solve_sat_problem
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


port = os.environ.get("PORT", 3000)
SATsolver = os.environ.get("SAT_SOLVER_PATH", "z3")


@app.route("/solve", methods=["POST"])
def solve_from_json():
    print("Received request")
    data = request.get_json()
    print(f"Received data: {data}")

    if not data or 'edges' not in data or 'colors' not in data or 'node_count' not in data:
        abort(400, description="Invalid data in request")

    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        
            temp.write(f"{data['node_count']} {data['colors']}\n")
            for edge in data['edges']:
                temp.write(f"{edge[0]} {edge[1]}\n")
                
            temp.flush()
            temp.seek(0)
            
            print(f"File content:\n{temp.readlines()}")
            
            status, solution = solve_sat_problem(temp.name, SATsolver)

    os.unlink(temp.name)

    return jsonify({"status": status, "solution": solution})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
