from dataclasses import dataclass

@dataclass
class Giocatore:
    PlayerID: int
    Name: str

    def __hash__(self):
        return hash(self.PlayerID)

    def __eq__(self, other):
        return self.PlayerID == other.PlayerID

    def __str__(self):
        return f"{self.PlayerID} {self.Name}"