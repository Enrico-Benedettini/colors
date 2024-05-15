from flask import Flask, request, jsonify, abort
import os
import tempfile
from sat_solver import solve_sat_problem

app = Flask(__name__)

port = os.environ.get("PORT", 3000)
SATsolver = os.environ.get("SAT_SOLVER_PATH", "z3")


@app.route("/solve", methods=["POST"])
def solve_from_json():
    data = request.get_json()
    if not data or 'edges' not in data or 'colors' not in data:
        abort(400, description="Invalid data in request")
    
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp:
        
        temp.write(f"{len(data['edges'])} {data['colors']}\n")
        for edge in data['edges']:
            temp.write(f"{edge[0]} {edge[1]}\n")
        temp.flush()
        status, solution = solve_sat_problem(temp.name, SATsolver)
    
    # Clean up the temporary file
    os.unlink(temp.name)
    
    return jsonify({"status": status, "solution": solution})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
