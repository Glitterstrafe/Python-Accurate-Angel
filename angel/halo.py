import json
import os


class HaloSystem:
    def __init__(self, config):
        self.max_cost = config['halo']['max_daily_cost_usd']
        self.stop_file = config['halo']['emergency_stop_file']
        self.usage_file = config.get('halo', {}).get('usage_file', 'angel_usage.json')
        self.current_spend = self._load_spend()

    def _load_spend(self) -> float:
        if not os.path.exists(self.usage_file):
            return 0.0
        try:
            with open(self.usage_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            value = float(data.get("current_spend", 0.0))
            return value if value >= 0 else 0.0
        except Exception:
            return 0.0

    def _save_spend(self) -> None:
        data = {"current_spend": self.current_spend}
        with open(self.usage_file, "w", encoding="utf-8") as f:
            json.dump(data, f)

    def check_safety(self):
        """Returns (False, Reason) if safety is breached."""
        if os.path.exists(self.stop_file):
            return False, "Emergency Stop File Detected!"

        if self.current_spend >= self.max_cost:
            return False, "Mana Pool Depleted (Budget Limit Reached)"

        return True, "Systems Normal"

    def record_spend(self, cost):
        self.current_spend += cost
        self._save_spend()
