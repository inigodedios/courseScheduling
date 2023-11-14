import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

class CourseGraph:
    def __init__(self):
        self.graph = {}  # To store graph: course -> list of conflicts
        self.courses = set()  # To store all courses

    def add_course(self, course):
        if course not in self.graph:
            self.graph[course] = []
            self.courses.add(course)

    def add_conflict(self, course1, course2):
        if course1 in self.courses and course2 in self.courses:
            self.graph[course1].append(course2)
            self.graph[course2].append(course1)


    def welsh_powell_algorithm(self):
        # Sort the courses based on the number of conflicts (descending order)
        sorted_courses = sorted(self.graph, key=lambda x: len(self.graph[x]), reverse=True)
        
        result = {}  # To store the color (or time slot) assigned to each course
        color = 0  # Initialize the first color (or time slot)

        # Iterate over each course in the sorted list
        for course in sorted_courses:
            if course not in result:
                # Assign a color to the course if it hasn't been colored yet
                result[course] = color
                
                # Go through all other courses to assign the same color if there's no conflict
                for neighbor in sorted_courses:
                    # Check if neighbor hasn't been colored and doesn't conflict with any other course of the same color
                    if neighbor not in result and all(result.get(conflict) != color for conflict in self.graph[neighbor]):
                        result[neighbor] = color
                # Increment color for the next set of non-conflicting courses
                color += 1

        self.colors = result  # Make sure to assign the result to self.colors
        return result


    # def welsh_powell_algorithm(self):
    #     # Sort the courses based on the number of conflicts
    #     sorted_courses = sorted(self.graph, key=lambda x: len(self.graph[x]), reverse=True)
    #     result = {}  # To store the color assigned to each course
    #     color = 0

    #     for course in sorted_courses:
    #         if course not in result:
    #             # Assign a color to the course
    #             result[course] = color
    #             # Assign the same color to all the courses which do not conflict with this course
    #             for neighbor in self.graph:
    #                 if neighbor not in result and all(result.get(conflict) != color for conflict in self.graph[neighbor]):
    #                     result[neighbor] = color
    #             color += 1  # Increment color for next assignment

    #     return result
    

    def visualize_graph(self):
        # Create a networkx graph from the course graph
        G = nx.Graph()
        
        # Add nodes
        for course in self.courses:
            G.add_node(course)
        
        # Add edges
        for course, conflicts in self.graph.items():
            for conflict in conflicts:
                G.add_edge(course, conflict)
        
        # Define node colors using the colors assigned by Welsh-Powell algorithm
        node_colors = [self.colors[course] for course in self.courses]
        
        # Generate a color map
        color_map = plt.cm.get_cmap('viridis', max(node_colors) + 1)
        
        # Draw the graph
        plt.figure(figsize=(12, 8))
        nx.draw(G, with_labels=True, node_color=node_colors, cmap=color_map, edge_color='gray', node_size=2500, font_size=10)
        plt.title("Course Conflict Graph")
        plt.show()


    
    # def visualize_graph(self):
    #     # Create a networkx graph from the course graph
    #     G = nx.Graph()
        
    #     # Add nodes
    #     for course in self.courses:
    #         G.add_node(course)
        
    #     # Add edges
    #     for course, conflicts in self.graph.items():
    #         for conflict in conflicts:
    #             G.add_edge(course, conflict)
        
    #     # Draw the graph
    #     plt.figure(figsize=(12, 8))
    #     nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2500, font_size=10)
    #     plt.title("Course Conflict Graph")
    #     plt.show()

