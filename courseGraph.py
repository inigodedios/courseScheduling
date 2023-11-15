import time
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


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
        print("Number of colors assigned:", color)
        print("Colors assigned to courses:", result)
        return result

    # Visualization method updated with buttons for interactivity
    def visualize_graph(self):
    
        # Create an undirected graph using the NetworkX library
        G = nx.Graph()

        # Add nodes to the graph to represent each course
        for course in self.courses:
            G.add_node(course)

        # Add edges to the graph to represent conflicts between courses
        for course, conflicts in self.graph.items():
            for conflict in conflicts:
                G.add_edge(course, conflict)

        # Calculate the layout of nodes using the spring_layout algorithm from NetworkX
        pos = nx.spring_layout(G, k=1.5, iterations=50)

        # Color configuration for nodes based on the color assignment of courses
        color_map = plt.cm.get_cmap('viridis', max(self.colors.values()) + 1)
        norm = mcolors.Normalize(vmin=0, vmax=max(self.colors.values()))

        # Create a figure and axes for visualization
        fig, ax = plt.subplots(figsize=(14, 8))
        fig.canvas.manager.set_window_title('Course Conflict Graph')
        fig.tight_layout()
        plt.subplots_adjust(bottom=0.2)

        # Function to update the graph visualization at each step
        def update_graph(index):
            ax.clear()
            ax.set_title(f"Course Conflict Graph - Step {index + 1}" if index >= 0 else "Course Conflict Graph - No Color", fontweight='bold', pad=3)
            
            # Assign colors to nodes based on the current step
            node_colors = [color_map(norm(self.colors.get(node, 0))) if self.colors.get(node) <= index else 'lightgrey' for node in G.nodes()]
            
            # Draw the graph with node labels, colors, and other attributes
            nx.draw(G, pos, ax=ax, with_labels=True, node_color=node_colors, edge_color='gray', node_size=2500, font_size=12, font_color='black')
            fig.canvas.draw_idle()

        # Initial drawing of the graph without colors
        update_graph(-1)

        class IndexTracker(object):
            def __init__(self, course_graph):
                self.index = -1  # Start from -1 to represent the uncolored state
                self.course_graph = course_graph

            def next(self, event):
                if self.index < max(self.course_graph.colors.values()):
                    self.index += 1
                update_graph(self.index)

            def prev(self, event):
                if self.index > -1:  # Allows the index to go back to the uncolored state
                    self.index -= 1
                update_graph(self.index)

        # Buttons callback functions
        tracker = IndexTracker(self) 
        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        bnext = Button(axnext, 'Next')
        bnext.on_clicked(tracker.next)
        bprev = Button(axprev, 'Prev')
        bprev.on_clicked(tracker.prev)
        
        plt.show()
      

# ---------------------------- VISUALIZATION ----------------------------
    # Without colors + with colors -> animation
    # def visualize_graph(self):
        # G = nx.Graph()
        
        # # Añade nodos y aristas al grafo G
        # for course in self.courses:
        #     G.add_node(course)
        # for course, conflicts in self.graph.items():
        #     for conflict in conflicts:
        #         G.add_edge(course, conflict)
        
        # pos = nx.spring_layout(G, k=1.5, iterations=50)

        # # Prepara la figura
        # plt.figure(figsize=(12, 8))
        # plt.title("Course Conflict Graph")

        # # Dibuja el grafo sin colores primero
        # nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2500, font_weight='bold')
        # plt.pause(5)  # Pausa de 2 segundos

        # # Dibuja el grafo con colores
        # color_map = plt.cm.get_cmap('viridis', max(self.colors.values()) + 1)
        # norm = mcolors.Normalize(vmin=0, vmax=max(self.colors.values()))

        # for color in range(max(self.colors.values()) + 1):
        #     # Define los colores de los nodos en este paso
        #     node_colors = [color_map(norm(self.colors[node])) if self.colors[node] <= color else 'lightblue' for node in G.nodes()]

        #     # Actualiza la figura
        #     plt.clf()
        #     plt.title(f"Course Conflict Graph - Coloring Step {color+1}")
        #     nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color='gray', node_size=2500, font_weight='bold')
        #     plt.pause(1)  # Pausa para ver la transición

        # plt.show()

# ---------------------------- INDIVIDUAL VISUALIZATION ----------------------------
    # With colors
    def visualize_graph_with_colors(self):
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

        # Use spring layout for better spacing
        pos = nx.spring_layout(G, k=1.5, iterations=50)  # Ajusta los valores de 'k' y 'iterations' según sea necesario

        # Draw the graph
        plt.figure(figsize=(12, 8))
        nx.draw(G, pos, with_labels=True, node_color=node_colors, cmap=color_map, edge_color='gray', node_size=2500, font_size=10)
        plt.title("Course Conflict Graph")
        plt.show()

    # Without colors
    def visualize_graph_without_colors(self):
        # Create a networkx graph from the course graph
        G = nx.Graph()
        
        # Add nodes
        for course in self.courses:
            G.add_node(course)
        
        # Add edges
        for course, conflicts in self.graph.items():
            for conflict in conflicts:
                G.add_edge(course, conflict)
        
        # Use spring layout for better spacing
        pos = nx.spring_layout(G, k=1.5, iterations=100)  # You can adjust 'k' and 'iterations' for different spacing
        
        # Draw the graph
        plt.figure(figsize=(10, 8))
        nx.draw(G, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=2500, font_size=10)
        plt.title("Course Conflict Graph")
        plt.show()