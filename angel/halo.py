import os


class HaloSystem:
    def __init__(self, config):
        self.max_cost = config['halo']['max_daily_cost_usd']
        self.stop_file = config['halo']['emergency_stop_file']
        self.current_spend = 0.0

    def check_safety(self):
        """Returns (False, Reason) if safety is breached."""
        if os.path.exists(self.stop_file):
            return False, "Emergency Stop File Detected!"

        if self.current_spend >= self.max_cost:
            return False, "Mana Pool Depleted (Budget Limit Reached)"

        return True, "Systems Normal"

    def record_spend(self, cost):
        self.current_spend += cost
