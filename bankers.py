class BankersAlgorithm:

    def __init__(self, total_resources):
        """
        total_resources: dict {R0: total_instances}
        """
        self.total = total_resources
        self.available = total_resources.copy()
        self.max_demand = {}      # {process: {resource: max}}
        self.allocation = {}      # {process: {resource: allocated}}

    def add_process(self, process, max_demand):
        self.max_demand[process] = max_demand
        self.allocation[process] = {r: 0 for r in self.total}

    def allocate(self, process, resource):
        if self.available[resource] <= 0:
            return False

        if self.allocation[process][resource] < self.max_demand[process][resource]:
            self.available[resource] -= 1
            self.allocation[process][resource] += 1
            return True

        return False

    def release(self, process, resource):
        if self.allocation[process][resource] > 0:
            self.available[resource] += 1
            self.allocation[process][resource] -= 1

    def is_safe_state(self):
        work = self.available.copy()
        finish = {p: False for p in self.max_demand}

        while True:
            allocated = False
            for p in self.max_demand:
                if not finish[p]:
                    need = {
                        r: self.max_demand[p][r] - self.allocation[p][r]
                        for r in self.total
                    }

                    if all(need[r] <= work[r] for r in self.total):
                        for r in self.total:
                            work[r] += self.allocation[p][r]
                        finish[p] = True
                        allocated = True

            if not allocated:
                break

        return all(finish.values())
