# import sys
# from PyQt6.QtWidgets import (
#     QMainWindow,
#     QWidget,
#     QGridLayout,
#     QPushButton,
#     QMessageBox,
#     QInputDialog,
#     QLabel,
# )
# from PyQt6.QtCore import Qt
# import networkx as nx
# import matplotlib.pyplot as plt

# from graph_manager import GraphManager


# BUTTON_STYLE = """
# QPushButton {
#     background-color: #a677d9;
#     color: white;
#     font-size: 16px;
#     border-radius: 5px;
#     padding: 10px;
# }
# QPushButton:hover {
#     background-color: #472b66;
# }
# QPushButton:pressed {
#     background-color: #3a294d;
# }
# """


# class ResourceAllocationSimulator(QMainWindow):

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Resource Allocation Graph")
#         self.setGeometry(100, 100, 800, 500)

#         self.graph_manager = GraphManager()
#         self.initUI()

#     def initUI(self):
#         central_widget = QWidget()
#         layout = QGridLayout()

#         title = QLabel("Resource Allocation Graph Simulator")
#         title.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         title.setStyleSheet(
#             "font-size: 18px; font-weight: bold; color: white;"
#         )

#         buttons = [
#             ("Add Process", self.add_process),
#             ("Add Resource", self.add_resource),
#             ("Allocate/Request", self.manage_allocation),
#             ("Release Allocation", self.release_resource),
#             ("Remove Resource", self.remove_resource),
#             ("Remove Process", self.remove_process),
#             ("Check Deadlock", self.detect_deadlock),
#         ]

#         row, col = 1, 0
#         for text, handler in buttons:
#             btn = QPushButton(text)
#             btn.setStyleSheet(BUTTON_STYLE)
#             btn.setMinimumHeight(60)
#             btn.clicked.connect(handler)

#             layout.addWidget(btn, row, col)

#             col += 1
#             if col > 2:
#                 col = 0
#                 row += 1

#         layout.addWidget(title, 0, 0, 1, 3)

#         for i in range(3):
#             layout.setColumnStretch(i, 1)

#         central_widget.setStyleSheet("background-color: #2E2E2E;")
#         central_widget.setLayout(layout)
#         self.setCentralWidget(central_widget)

#     # ---------------- PROCESS & RESOURCE ---------------- #

#     def add_process(self):
#         process_id = self.graph_manager.add_process()
#         QMessageBox.information(self, "Process Added", f"Added {process_id}")
#         self.show_graph()

#     def add_resource(self):
#         quantity, ok = QInputDialog.getInt(
#             self, "Resource Instances",
#             "Enter number of instances:", 1, 1, 10, 1
#         )
#         if ok:
#             self.graph_manager.add_resource(quantity)
#             self.show_graph()

#     # ---------------- ALLOCATION ---------------- #

#     def manage_allocation(self):
#         processes = [n for n in self.graph_manager.graph.nodes if n.startswith("P")]
#         resources = [n for n in self.graph_manager.graph.nodes if n.startswith("R")]

#         if not processes or not resources:
#             QMessageBox.warning(self, "Warning", "No processes or resources found!")
#             return

#         process, ok = QInputDialog.getItem(
#             self, "Select Process", "Process:", processes, 0, False
#         )
#         if not ok:
#             return

#         resource, ok = QInputDialog.getItem(
#             self, "Select Resource", "Resource:", resources, 0, False
#         )
#         if not ok:
#             return

#         status = self.graph_manager.allocate_resource(process, resource)

#         if status == "not enough instances":
#             QMessageBox.warning(
#                 self, "Warning",
#                 f"Cannot allocate {resource} to {process}"
#             )
#         else:
#             QMessageBox.information(
#                 self, "Success",
#                 f"{process} allocated {resource}"
#             )

#         self.show_graph()

#     def release_resource(self):
#         allocations = [
#             (u, v) for u, v in self.graph_manager.graph.edges
#             if u.startswith("R") and v.startswith("P")
#         ]

#         if not allocations:
#             QMessageBox.warning(self, "Error", "No resources allocated")
#             return

#         allocation_strs = [f"{u} → {v}" for u, v in allocations]

#         selection, ok = QInputDialog.getItem(
#             self, "Release Resource",
#             "Select allocation:", allocation_strs, 0, False
#         )
#         if not ok:
#             return

#         resource, process = selection.split(" → ")

#         success = self.graph_manager.release_resource(resource, process)

#         if success:
#             QMessageBox.information(
#                 self, "Success",
#                 f"{resource} released from {process}"
#             )
#         else:
#             QMessageBox.warning(
#                 self, "Error",
#                 f"Cannot release {resource} from {process}"
#             )

#         self.show_graph()

#     # ---------------- REMOVE ---------------- #

#     def remove_resource(self):
#         resources = [n for n in self.graph_manager.graph.nodes if n.startswith("R")]

#         if not resources:
#             QMessageBox.warning(self, "Warning", "No resources found!")
#             return

#         resource, ok = QInputDialog.getItem(
#             self, "Remove Resource",
#             "Select Resource:", resources, 0, False
#         )
#         if not ok:
#             return

#         success = self.graph_manager.remove_resource(resource)

#         if success:
#             QMessageBox.information(self, "Success", f"{resource} removed")
#         else:
#             QMessageBox.warning(self, "Error", f"Cannot remove {resource}")

#         self.show_graph()

#     def remove_process(self):
#         processes = [n for n in self.graph_manager.graph.nodes if n.startswith("P")]

#         if not processes:
#             QMessageBox.warning(self, "Error", "No processes available")
#             return

#         process, ok = QInputDialog.getItem(
#             self, "Remove Process",
#             "Select Process:", processes, 0, False
#         )
#         if not ok:
#             return

#         success = self.graph_manager.remove_process(process)

#         if success:
#             QMessageBox.information(self, "Success", f"{process} removed")
#         else:
#             QMessageBox.warning(self, "Error", f"Failed to remove {process}")

#         self.show_graph()

#     # ---------------- DEADLOCK ---------------- #

#     def detect_deadlock(self):
#         try:
#             cycles = list(nx.simple_cycles(self.graph_manager.graph))
#             if cycles:
#                 QMessageBox.critical(
#                     self,
#                     "Deadlock Detected!",
#                     f"Deadlock cycles:\n{cycles}"
#                 )
#             else:
#                 QMessageBox.information(self, "No Deadlock", "System is safe")
#         except nx.NetworkXNoCycle:
#             QMessageBox.information(self, "No Deadlock", "System is safe")

#     # ---------------- GRAPH DISPLAY ---------------- #

#     def show_graph(self):
#         plt.clf()

#         G = self.graph_manager.graph
#         pos = nx.spring_layout(G)

#         color_map = []
#         labels = {}

#         for node in G.nodes:
#             if node.startswith("R"):
#                 available = self.graph_manager.resource_instances[node]["available"]
#                 labels[node] = f"{node} ({available})"
#                 color_map.append("#9370DB")
#             else:
#                 labels[node] = node
#                 color_map.append("#44b0f2")

#         nx.draw(G, pos, with_labels=False,
#                 node_color=color_map,
#                 node_size=2000,
#                 arrows=True)

#         nx.draw_networkx_labels(G, pos, labels)

#         plt.title("Resource Allocation Graph")
#         plt.pause(0.1)
#         plt.draw()

import matplotlib.pyplot as plt
import networkx as nx

from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QPushButton,
    QMessageBox,
    QInputDialog,
    QLabel
)
from PyQt6.QtCore import Qt

from graph_manager import GraphManager


BUTTON_STYLE = """
QPushButton {
    background-color: #a677d9;
    color: white;
    font-size: 15px;
    border-radius: 6px;
    padding: 8px;
}
QPushButton:hover {
    background-color: #472b66;
}
QPushButton:pressed {
    background-color: #3a294d;
}
"""


class ResourceAllocationSimulator(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Deadlock Detection Simulator")
        self.setGeometry(100, 100, 900, 550)

        self.graph_manager = GraphManager()

        self.initUI()

    # ---------------- UI SETUP ---------------- #

    def initUI(self):

        central_widget = QWidget()
        layout = QGridLayout()

        title = QLabel("Deadlock Detection & Avoidance Simulator")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: white;"
        )

        buttons = [
            ("Add Process", self.add_process),
            ("Add Resource", self.add_resource),
            ("Allocate Resource", self.allocate_resource),
            ("Release Resource", self.release_resource),
            ("Remove Process", self.remove_process),
            ("Remove Resource", self.remove_resource),
            ("Check Deadlock (Cycle)", self.detect_deadlock),
            ("Check Safe State (Banker)", self.check_safe_state),
        ]

        row, col = 1, 0

        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet(BUTTON_STYLE)
            btn.setMinimumHeight(50)
            btn.clicked.connect(handler)

            layout.addWidget(btn, row, col)

            col += 1
            if col > 1:
                col = 0
                row += 1

        layout.addWidget(title, 0, 0, 1, 2)

        for i in range(2):
            layout.setColumnStretch(i, 1)

        central_widget.setStyleSheet("background-color: #2E2E2E;")
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    # ---------------- ADD ---------------- #

    def add_process(self):
        pid = self.graph_manager.add_process()
        QMessageBox.information(self, "Process Added", f"{pid} added")
        self.show_graph()

    def add_resource(self):
        instances, ok = QInputDialog.getInt(
            self,
            "Resource Instances",
            "Enter number of instances:",
            1, 1, 10, 1
        )

        if ok:
            rid = self.graph_manager.add_resource(instances)
            QMessageBox.information(self, "Resource Added", f"{rid} added")
            self.show_graph()

    # ---------------- ALLOCATION ---------------- #

    def allocate_resource(self):

        processes = [
            n for n in self.graph_manager.graph.nodes
            if n.startswith("P")
        ]

        resources = [
            n for n in self.graph_manager.graph.nodes
            if n.startswith("R")
        ]

        if not processes or not resources:
            QMessageBox.warning(
                self,
                "Warning",
                "Add processes and resources first!"
            )
            return

        process, ok = QInputDialog.getItem(
            self,
            "Select Process",
            "Process:",
            processes,
            0,
            False
        )
        if not ok:
            return

        resource, ok = QInputDialog.getItem(
            self,
            "Select Resource",
            "Resource:",
            resources,
            0,
            False
        )
        if not ok:
            return

        status = self.graph_manager.allocate_resource(process, resource)

        if status == "allocated":
            QMessageBox.information(
                self,
                "Success",
                f"{resource} allocated to {process}"
            )
        else:
            QMessageBox.warning(
                self,
                "Waiting",
                f"{process} is waiting for {resource}"
            )

        self.show_graph()

    # ---------------- RELEASE ---------------- #

    def release_resource(self):

        allocations = [
            (u, v)
            for u, v in self.graph_manager.graph.edges
            if u.startswith("R") and v.startswith("P")
        ]

        if not allocations:
            QMessageBox.warning(
                self,
                "Error",
                "No active allocations!"
            )
            return

        allocation_strings = [f"{u} → {v}" for u, v in allocations]

        selection, ok = QInputDialog.getItem(
            self,
            "Release Allocation",
            "Select allocation:",
            allocation_strings,
            0,
            False
        )

        if not ok:
            return

        resource, process = selection.split(" → ")

        success = self.graph_manager.release_resource(resource, process)

        if success:
            QMessageBox.information(
                self,
                "Released",
                f"{resource} released from {process}"
            )

        self.show_graph()

    # ---------------- REMOVE ---------------- #

    def remove_process(self):

        processes = [
            n for n in self.graph_manager.graph.nodes
            if n.startswith("P")
        ]

        if not processes:
            QMessageBox.warning(self, "Error", "No processes available")
            return

        process, ok = QInputDialog.getItem(
            self,
            "Remove Process",
            "Select process:",
            processes,
            0,
            False
        )

        if not ok:
            return

        self.graph_manager.remove_process(process)
        self.show_graph()

    def remove_resource(self):

        resources = [
            n for n in self.graph_manager.graph.nodes
            if n.startswith("R")
        ]

        if not resources:
            QMessageBox.warning(self, "Error", "No resources available")
            return

        resource, ok = QInputDialog.getItem(
            self,
            "Remove Resource",
            "Select resource:",
            resources,
            0,
            False
        )

        if not ok:
            return

        self.graph_manager.remove_resource(resource)
        self.show_graph()

    # ---------------- DEADLOCK DETECTION ---------------- #

    def detect_deadlock(self):

        cycles = self.graph_manager.detect_deadlock()

        if cycles:
            QMessageBox.critical(
                self,
                "Deadlock Detected!",
                f"Deadlock cycles:\n{cycles}"
            )
        else:
            QMessageBox.information(
                self,
                "No Deadlock",
                "System is safe"
            )

    # ---------------- BANKER SAFE CHECK ---------------- #

    def check_safe_state(self):

        self.graph_manager.initialize_banker()
        safe = self.graph_manager.check_safe_state()

        if safe:
            QMessageBox.information(
                self,
                "Safe State",
                "System is in SAFE state"
            )
        else:
            QMessageBox.critical(
                self,
                "Unsafe State",
                "System is in UNSAFE state"
            )

    # ---------------- GRAPH VISUALIZATION ---------------- #

    def show_graph(self):

        plt.clf()

        G = self.graph_manager.graph
        pos = nx.spring_layout(G)

        labels = {}
        colors = []

        for node in G.nodes:
            if node.startswith("R"):
                available = self.graph_manager.resource_instances[node]["available"]
                total = self.graph_manager.resource_instances[node]["total"]
                labels[node] = f"{node} ({available}/{total})"
                colors.append("#9370DB")
            else:
                labels[node] = node
                colors.append("#44b0f2")

        nx.draw(
            G,
            pos,
            with_labels=False,
            node_color=colors,
            node_size=2000,
            arrows=True
        )

        nx.draw_networkx_labels(G, pos, labels)

        # Allocation edges
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[
                (u, v) for u, v in G.edges
                if G.edges[u, v].get("style") != "dashed"
            ],
            edge_color="gray",
            arrows=True
        )

        # Request edges
        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[
                (u, v) for u, v in G.edges
                if G.edges[u, v].get("style") == "dashed"
            ],
            edge_color="orange",
            style="dashed",
            arrows=True
        )

        plt.title("Resource Allocation Graph")
        plt.pause(0.1)
        plt.draw()
