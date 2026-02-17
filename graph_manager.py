# import networkx as nx


# class GraphManager:

#     def __init__(self):
#         self.graph = nx.DiGraph()
#         self.process_count = 0
#         self.resource_count = 0

#         # {resource: {"total": x, "available": y}}
#         self.resource_instances = {}

#         # {process: {resource: allocated_count}}
#         self.allocations = {}

#     # ---------------- ADD ---------------- #

#     def add_process(self):
#         process_id = f"P{self.process_count}"
#         self.graph.add_node(process_id)

#         self.allocations[process_id] = {}
#         self.process_count += 1

#         return process_id

#     def add_resource(self, instances):
#         resource_id = f"R{self.resource_count}"
#         self.graph.add_node(resource_id)

#         self.resource_instances[resource_id] = {
#             "total": instances,
#             "available": instances
#         }

#         self.resource_count += 1
#         return resource_id

#     # ---------------- ALLOCATE ---------------- #

#     def allocate_resource(self, process, resource):

#         if resource not in self.resource_instances:
#             return "does not exist"

#         if process not in self.allocations:
#             return "does not exist"

#         # If resource is available → allocate
#         if self.resource_instances[resource]["available"] > 0:
#             self.resource_instances[resource]["available"] -= 1

#             self.allocations[process][resource] = \
#                 self.allocations[process].get(resource, 0) + 1

#             # Add allocation edge (Resource → Process)
#             self.graph.add_edge(resource, process)

#             return "allocated"

#         # If not available → add request edge (Process → Resource)
#         self.graph.add_edge(process, resource, style='dashed')

#         return "not enough instances"

#     # ---------------- RELEASE ---------------- #

#     def release_resource(self, resource, process):

#         if process not in self.allocations:
#             return False

#         if resource not in self.allocations[process]:
#             return False

#         if self.allocations[process][resource] <= 0:
#             return False

#         # Increase available count
#         self.resource_instances[resource]["available"] += 1

#         # Decrease allocation count
#         self.allocations[process][resource] -= 1

#         # Remove allocation record if zero
#         if self.allocations[process][resource] == 0:
#             del self.allocations[process][resource]

#         # Remove allocation edge
#         if self.graph.has_edge(resource, process):
#             self.graph.remove_edge(resource, process)

#         # Check waiting processes (request edges)
#         waiting_processes = [
#             p for p in self.graph.predecessors(resource)
#             if self.graph.edges[p, resource].get('style') == 'dashed'
#         ]

#         # Allocate to first waiting process
#         if waiting_processes:
#             next_process = waiting_processes[0]

#             # Remove request edge
#             self.graph.remove_edge(next_process, resource)

#             # Allocate resource
#             self.allocate_resource(next_process, resource)

#         return True

#     # ---------------- REMOVE ---------------- #

#     def remove_resource(self, resource):

#         if resource not in self.resource_instances:
#             return False

#         del self.resource_instances[resource]

#         if resource in self.graph.nodes:
#             self.graph.remove_node(resource)

#         return True

#     def remove_process(self, process):

#         if process not in self.allocations:
#             return False

#         # Release all allocated resources
#         allocated_resources = list(self.allocations[process].keys())

#         for resource in allocated_resources:
#             self.release_resource(resource, process)

#         # Remove process record
#         del self.allocations[process]

#         if process in self.graph.nodes:
#             self.graph.remove_node(process)

#         return True

import networkx as nx
from bankers import BankersAlgorithm


class GraphManager:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.process_count = 0
        self.resource_count = 0

        self.resource_instances = {}
        self.allocations = {}

        self.bankers = None

    # ---------------- ADD ---------------- #

    def add_process(self):
        pid = f"P{self.process_count}"
        self.graph.add_node(pid)
        self.allocations[pid] = {}
        self.process_count += 1
        return pid

    def add_resource(self, instances):
        rid = f"R{self.resource_count}"
        self.graph.add_node(rid)

        self.resource_instances[rid] = {
            "total": instances,
            "available": instances
        }

        self.resource_count += 1
        return rid

    # ---------------- ALLOCATION ---------------- #

    def allocate_resource(self, process, resource):
        if self.resource_instances[resource]["available"] > 0:
            self.resource_instances[resource]["available"] -= 1
            self.allocations[process][resource] = \
                self.allocations[process].get(resource, 0) + 1

            self.graph.add_edge(resource, process)
            return "allocated"

        self.graph.add_edge(process, resource, style="dashed")
        return "not enough instances"

    # ---------------- DEADLOCK DETECTION ---------------- #

    def detect_deadlock(self):
        return list(nx.simple_cycles(self.graph))

    # ---------------- BANKER ---------------- #

    def initialize_banker(self):
        totals = {
            r: self.resource_instances[r]["total"]
            for r in self.resource_instances
        }
        self.bankers = BankersAlgorithm(totals)

        for p in self.allocations:
            max_demand = {
                r: self.resource_instances[r]["total"]
                for r in self.resource_instances
            }
            self.bankers.add_process(p, max_demand)

    def check_safe_state(self):
        if self.bankers:
            return self.bankers.is_safe_state()
        return None

