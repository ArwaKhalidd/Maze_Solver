# Maze Solver: Search vs Optimization

## Overview
This project is a visual maze-solving simulator built using Python and Pygame.  
It demonstrates and compares different pathfinding algorithms including:

- Breadth First Search (BFS)
- Depth First Search (DFS)
- A* Search Algorithm

The project also applies a simple optimization technique inspired by Genetic Algorithms to improve the generated path.

---

## Features

- Random maze generation
- Real-time visualization
- BFS, DFS, and A* implementation
- Path optimization using mutation
- Execution time tracking
- Visited nodes counter
- Interactive keyboard controls

---

## Algorithms Used

### BFS (Breadth First Search)
- Finds the shortest path
- Explores nodes level by level

### DFS (Depth First Search)
- Explores deeply before backtracking
- Faster in some cases but not optimal

### A* Search
- Uses heuristic function
- Faster and more efficient pathfinding

---

## Controls

| Key | Action |
|-----|--------|
| B | Run BFS |
| D | Run DFS |
| A | Run A* |
| R | Generate New Maze |

---

## Installation

### Install Python
Download Python from the official website:

https://www.python.org

### Install Pygame

```bash
pip install pygame
```

---

## Run the Project

```bash
python maze_solver.py
```

---

## Project Structure

```text
Maze.py
Maze Solver.pdf
README.md
```

---

## How It Works

1. A random maze is generated
2. The selected algorithm searches for a path
3. The search process is visualized in real time
4. Statistics are displayed:
   - Execution Time
   - Visited Nodes
5. The final path is optimized using mutation

---

## Technologies Used

- Python
- Pygame
- Heap Queue
- Deque

---

## Educational Purpose

This project helps in understanding:
- Search Algorithms
- Pathfinding Techniques
- Basic AI Concepts
- Optimization Methods
