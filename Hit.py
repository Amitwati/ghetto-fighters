class Hit:
    def __init__(self, title, damage, cost):
        self.title = title
        self.damage = damage
        self.cost = cost

HitsMenu = {
    "sk": Hit("Simple kick", 10, 5),
    "sp": Hit("Simple punch", 15, 10),
    "mk": Hit("Medium kick", 20, 15),
    "mp": Hit("Medium punch", 25, 20),
    "sh": Hit("Super hit", 40, 50),
    "mh": Hit("MEGA HIT", 70, 70)
}