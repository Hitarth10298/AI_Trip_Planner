
class Calculator:
    @staticmethod
    def multiply(a: int, b: int) -> int:
        """Multiplies two numbers."""
        return a * b
    
    @staticmethod
    def calculate_total(*x: float) -> float:
        """Calculates the total expense from a list of expenses."""
        return sum(x)
    
    @staticmethod
    def calculate_daily_budget(total: float, days: int) -> float:
        return total / days if days > 0 else 0