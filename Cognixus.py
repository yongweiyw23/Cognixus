import unittest


class TaskOrdering:
    def __init__(self, tasks):
        self.graph = {}
        self.in_degree = {}
        self.result = []

        # Initialize the graph and in-degree
        for task in tasks:
            name = task["name"]
            depends_on = task.get("depends_on", [])
            self.graph[name] = depends_on
            self.in_degree[name] = self.in_degree.get(name, 0)  # Ensure task is in in_degree

            for dependency in depends_on:
                self.in_degree[dependency] = self.in_degree.get(dependency, 0)

                # Increment in-degree for the dependency
                self.in_degree[dependency] += 1

    def compute_ordering(self):
        # Initialize a queue
        queue = [task for task, degree in self.in_degree.items() if degree == 0]

        while queue:
            current_task = queue.pop(0)
            self.result.append(current_task)

            # Update in-degrees of neighbors
            if current_task in self.graph:
                for neighbor in self.graph[current_task]:
                    self.in_degree[neighbor] -= 1
                    if self.in_degree[neighbor] == 0:
                        queue.append(neighbor)

        # Check for cycles
        if len(self.result) != len(self.in_degree):
            raise ValueError("Dependency cycle detected. Unable to determine task ordering.")

        return self.result[::-1]  # Reverse the result to get the correct order


# Example usage
tasks_config = [
    {"name": "compile", "depends_on": ["check_build_script", "lint"]},
    {"name": "lint", "depends_on": ["check_build_script"]},
    {"name": "package", "depends_on": ["compile"]},
    {"name": "test", "depends_on": ["package"]}
]

task_ordering = TaskOrdering(tasks_config)
ordering_result = task_ordering.compute_ordering()
print(ordering_result)


class TestTaskOrdering(unittest.TestCase):
    def test_compute_ordering(self):
        # Test case with a valid ordering
        tasks_config_valid = [
            {"name": "compile", "depends_on": ["check_build_script", "lint"]},
            {"name": "lint", "depends_on": ["check_build_script"]},
            {"name": "package", "depends_on": ["compile"]},
            {"name": "test", "depends_on": ["package"]}
        ]
        task_ordering_valid = TaskOrdering(tasks_config_valid)
        result_valid = task_ordering_valid.compute_ordering()
        self.assertEqual(result_valid, ['check_build_script', 'lint', 'compile', 'package', 'test'])


if __name__ == '__main__':
    unittest.main()
