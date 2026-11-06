"""Modelo abstrato de linhagem celular; NÃO é embriologia humana validada."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Cell:
    identifier: str
    generation: int = 0


def divide(cell: Cell) -> tuple[Cell, Cell]:
    """Divisão binária idealizada, sem dinâmica molecular ou espacial."""
    g = cell.generation + 1
    return (Cell(cell.identifier + "0", g), Cell(cell.identifier + "1", g))


def generations(n: int) -> list[Cell]:
    if n < 0:
        raise ValueError("n must be nonnegative")
    cells = [Cell("z")]
    for _ in range(n):
        cells = [daughter for cell in cells for daughter in divide(cell)]
    return cells
