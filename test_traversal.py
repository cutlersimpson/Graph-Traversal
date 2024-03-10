import time
import json
import unittest
from io import StringIO
from unittest.mock import patch
from app import traverse_graph, print_vertices
from exceptions import NoStartVertexException, MultipleStartVerticesException


class TestWorkflow(unittest.TestCase):
    def test_empty_json(self):
        graph_json = """ { } """
        graph = json.loads(graph_json)

        self.assertRaises(NoStartVertexException, traverse_graph, graph)

    def test_multiple_start_vertices(self):
        graph_json = """
        {
            "A": {"start": true, "edges": {}},
            "B": {"start": true, "edges": {}},
            "C": {"edges": {}}
        }
        """
        graph = json.loads(graph_json)

        self.assertRaises(MultipleStartVerticesException, traverse_graph, graph)

    def test_no_start_vertex(self):
        graph_json = """
        {
            "A": {"start": false, "edges": {}},
            "B": {"edges": {}},
            "C": {"edges": {}}
        }
        """

        graph = json.loads(graph_json)

        self.assertRaises(NoStartVertexException, traverse_graph, graph)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("app.time.sleep")  # Used to mock sleep to avoid waiting for delay
    def test_single_vertex(self, mock_sleep, mock_stdout):
        graph_json = """
        {
            "A": {"start": true, "edges": {}}
        }
        """
        expected_output = "A\n"

        graph = json.loads(graph_json)
        vertices = traverse_graph(graph)
        print_vertices(vertices)

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("app.time.sleep")  # Used to mock sleep to avoid waiting for delay
    def test_example(self, mock_sleep, mock_stdout):
        graph_json = """
        {
            "A": {"start": true, "edges": {"B": 5, "C": 7}},
            "B": {"edges": {}},
            "C": {"edges": {}}
        }
        """
        expected_output = "A\nB\nC\n"

        graph = json.loads(graph_json)
        vertices = traverse_graph(graph)
        print_vertices(vertices)

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("app.time.sleep")  # Used to mock sleep to avoid waiting for delay
    def test_extended_example(self, mock_sleep, mock_stdout):
        graph_json = """
        {
            "A": {"start": true, "edges": {"B": 2, "C": 4}},
            "B": {"edges": {"D": 1}},
            "C": {"edges": {}},
            "D": {"edges": {}}
        }
        """
        expected_output = "A\nB\nD\nC\n"

        graph = json.loads(graph_json)
        vertices = traverse_graph(graph)
        print_vertices(vertices)

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("app.time.sleep")  # Used to mock sleep to avoid waiting for delay
    def test_extended_empty(self, mock_sleep, mock_stdout):
        # D vertex not in json but is connected to B
        graph_json = """
        {
            "A": {"start": true, "edges": {"B": 2, "C": 4}},
            "B": {"edges": {"D": 1}},
            "C": {"edges": {}}
        }
        """
        expected_output = "A\nB\nD\nC\n"

        graph = json.loads(graph_json)
        vertices = traverse_graph(graph)
        print_vertices(vertices)

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("app.time.sleep")  # Used to mock sleep to avoid waiting for delay
    def test_chain(self, mock_sleep, mock_stdout):
        graph_json = """
        {
            "A": {"start": true, "edges": {"B": 1, "E": 4}},
            "B": {"edges": {"C": 1}},
            "C": {"edges": {"D": 1}},
            "D": {"edges": {}}
        }

        """

        expected_output = "A\nB\nC\nD\nE\n"

        graph = json.loads(graph_json)
        vertices = traverse_graph(graph)
        print_vertices(vertices)

        self.assertEqual(mock_stdout.getvalue(), expected_output)

    @patch("sys.stdout", new_callable=StringIO)
    @patch("app.time.sleep")  # Used to mock sleep to avoid waiting for delay
    def test_timing_ties_across_multiple_vertices(self, mock_sleep, mock_stdout):
        graph_json = """
        {
            "A": {"start": true, "edges": {"B": 2, "C": 2, "D": 2}},
            "B": {"edges": {}},
            "C": {"edges": {}},
            "D": {"edges": {}}
        }
        """
        expected_outputs = [
            "A\nB\nC\nD\n",
            "A\nB\nD\nC\n",
            "A\nC\nB\nD\n",
            "A\nC\nD\nB\n",
            "A\nD\nB\nC\n",
            "A\nD\nC\nB\n",
        ]

        graph = json.loads(graph_json)
        vertices = traverse_graph(graph)
        print_vertices(vertices)

        self.assertIn(mock_stdout.getvalue(), expected_outputs)

    def test_expected_delay(self):
        graph_json = """
        {
            "A": {"start": true, "edges": {"B": 5, "C": 7}},
            "B": {"edges": {}},
            "C": {"edges": {}}
        }
        """
        start_time = time.time()

        graph = json.loads(graph_json)
        vertices = traverse_graph(graph)
        print_vertices(vertices)

        execution_time = round(time.time() - start_time, 2)

        self.assertAlmostEqual(execution_time, 7, delta=0.05)


if __name__ == "__main__":
    unittest.main(buffer=True)
