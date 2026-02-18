# Deadlock Detection & Avoidance Simulator

**Deadlock Detection System** is a **Python desktop application** designed to simulate, visualize, and analyze deadlocks in operating systems. It provides an interactive interface for managing processes and resources, detecting deadlocks, and verifying safe states using classical algorithms.

This project demonstrates a strong understanding of operating system concepts, algorithm design, and GUI development, making it an excellent showcase of applied programming and systems knowledge.

---

## Problem Statement

In multi-process systems, processes compete for limited resources. A **deadlock** occurs when a set of processes waits indefinitely for resources held by each other, resulting in system inefficiency or failure.  

This project addresses the problem by:

- Detecting deadlocks through **Resource Allocation Graph (RAG)** cycle detection.  
- Validating system safety using the **Banker’s Algorithm**.  
- Providing an interactive, user-friendly environment to simulate resource allocation and observe potential deadlocks in real-time.

---

## Key Features

- **Interactive GUI** to add/remove processes and resources.  
- **Dynamic Resource Allocation Graph** visualization using **NetworkX** and **Matplotlib**.  
- Real-time **deadlock detection** based on graph cycles.  
- **Safe state verification** using the Banker’s Algorithm.  
- Alerts and guidance for resource allocation to prevent unsafe states.  

---

## Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| GUI Framework | PyQt6 |
| Graph Management | NetworkX |
| Visualization | Matplotlib |

---

## Architecture & Implementation

- **Graph Manager:** Implements resource allocation graph and cycle detection.  
- **Banker’s Algorithm Module:** Checks system safe state and prevents unsafe allocations.  
- **GUI Layer:** Built with PyQt6 for an intuitive, responsive interface.  
- **Visualization Engine:** Uses NetworkX and Matplotlib to display real-time resource allocation graphs.  

---

## Role & Responsibilities

As the **sole developer**, I was responsible for:

- Designing the project architecture and workflow.  
- Implementing core logic for deadlock detection and safe state verification.  
- Developing the complete GUI and interactive features using PyQt6.  
- Integrating graph visualization and dynamic updates for processes and resources.  
- Testing, debugging, and ensuring correctness for various deadlock scenarios.  
- Documenting the project and preparing it for public use.  

This demonstrates proficiency in **Python programming, algorithm implementation, GUI development, and systems thinking**.

---

## Installation & Usage

1. Clone the repository:
```bash
git clone https://github.com/Gunjan010305/Deadlock-Detection-System.git

pip install pyqt6 networkx matplotlib`  

python main.py
```

References

Banker’s Algorithm — Wikipedia

Deadlock Detection using Resource Allocation Graphs — GeeksforGeeks

Future Enhancements

Support for multi-instance resources.

License

This project is open-source and available for use, modification, and educational purposes.

Highlight

This project reflects a strong ability to develop complete solutions independently, combining algorithmic knowledge, system design, and GUI development.
