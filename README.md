# joswig
Temporal Joswig algorithm implementation in Python for Parametric Shortest Path Algorithms. Based on https://arxiv.org/pdf/1904.01082.pdf

Files in /src are current.
/src/t_joswig.py contains the main code that implements the joswig algorithm.
/src/joswig_example.py contains an example script that solves a parametric path problem.
/src/auto_interp.py solves the temporal parametric problem for a simulated lunar gateway scenario and pulls data from /src/gatewayDistances.csv

Files in /old are obsolete but may still be useful in the future.
/old/joswig.py contains the old unfinished implementation of the joswig algorithm.
/old/joswig_binary.py contains the alternative code that implements the binary method for approximating solutions to the parametric shortest path problem.
/old/joswig_dijkstra.py contains an implementation of Dijkstra's algorithm and is a dependency for both /old/joswig.py and /old/joswig_binary.py

Any questions should be sent to jacob.cleveland@colostate.edu or jacleveland@unomaha.edu
