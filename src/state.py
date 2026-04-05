"""Reusable state class for search problems."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


@dataclass(frozen=True)
class RobotState:
    """State representation for warehouse robot."""

    position: tuple[int, int]
    collected: frozenset[tuple[int, int]] = frozenset()

    def __post_init__(self):
        if not (isinstance(self.position, tuple) and len(self.position) == 2):
            raise ValueError("position must be a tuple of (row, col)")

        if not all(isinstance(coord, int) for coord in self.position):
            raise ValueError("position coordinates must be integers")

        if not isinstance(self.collected, frozenset):
            raise ValueError("collected must be a frozenset of positions")

    def is_goal(self, problem) -> bool:
        """Check if state is a goal state."""
        return (
            self.position == problem.delivery_pos
            and len(self.collected) == len(problem.package_positions)
        )

    def get_neighbors(self, problem) -> list[RobotState]:
        """Generate all possible next states from this state."""
        neighbors: list[RobotState] = []

        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in moves:
            new_row = self.position[0] + dr
            new_col = self.position[1] + dc

            if not (0 <= new_row < problem.height and 0 <= new_col < problem.width):
                continue

            if problem.grid[new_row][new_col] == "X":
                continue

            new_collected = set(self.collected)
            if (new_row, new_col) in problem.package_positions:
                new_collected.add((new_row, new_col))

            neighbors.append(
                RobotState((new_row, new_col), frozenset(new_collected))
            )

        return neighbors


__all__ = ["RobotState"]
