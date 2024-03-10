# Graph Traversal

[app.py](app.py) is a script to traverse a directed acyclic graph where
letters are assigned to the vertices and numbers (times) are assigned to the edges.
The script traverses the graph and prints the vertices in increasing order of times.

This is accomplished using a breadth first search to visit all children vertices and
sum the total delay at the given vertex. Each vertex and total delay is added, as a
tuple, to a list that is sorted by time.

This sorted list is then iterated to print each vertex letter after waiting the delay
time seconds.


## Execution
  * Main script: `python app.py`
  * Test script: `python test_traversal.py`
