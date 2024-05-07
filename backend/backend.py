import os
from z3 import Solver, Bool, Or, And, Not, sat
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

port = os.environ.get("PORT", 3000) 

# def encode_sat(edges, colors):
#     solver = Solver()

#     return solver

# def decode_sat():

#     return graph

@app.route("/solve", methods=["POST"])
def solve():
    data = request.get_json()
    if not data:
        abort(400, description="No data in request")

    edges = data['edges']
    colors = data['colors']

    # solver, variables = encode_sat(n, edges, colors)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
