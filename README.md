# Colors
## Description
Companies printing maps are always trying to save money by buying the smallest amount of ink cartridge: given a map, they want to know if it is possible to print the map with k colors.
Given an undirected graph G = (V, E) and an integer k, is there a way to color the vertices with k colors such that adjacent vertices are colored differently?
## Task
Task: write an encoder for the Colors problem:
 - Input: a text file containing the graph and an integer k
 - Encode the problem into SAT
 - If unsatisfiable, output UNSATISFIABLE
 - If satisfiable, output the color associated with each node of the graph
 ## Setup and Run
 To run the project we'll need to setup the two main parts composing it:
 - Backend: to run the backend we use two scripts to start and stop the backend server. To ensure these work properly, ensure you have the needed python version (3.7+) and the required packages, such as flask, flask-cors and the z3 solver. Once these are installed, go to the root folder of the backend (`cd backend`) and run the `start_backend.sh` script (`bash start_backend.sh` on Linux machines). This will run the project on port 3000. To stop it, run the `stop_backend.sh` script (`bash stop_backend.sh` on Linux).
 - Frontend: to run the frontend, all we need to do is to move to the root folder for the frontend (`cd graph-project`) and run two commands:
 - 1. `npm install` to get all the dependencies
 - 2. `npm run serve` to run the project, that will then be available on _http://localhost:8080/_. You can stop this by simply pressing `Ctrl + C` from the terminal from which it's been launched.
----------------------------------------------------------------------------------------------------------------------------------
Project developed as Homework 6 of the course **Theory of Computation** at USI (Università della Svizzera italiana)
