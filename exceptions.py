"""
Exceptions to be thrown when no or multiple start vertices are found
"""


class NoStartVertexException(Exception):
    """Exception when no start vertex is found"""


class MultipleStartVerticesException(Exception):
    """Exception when multiple start vertices are found"""
