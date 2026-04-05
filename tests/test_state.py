"""Tests for RobotState."""
import pytest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.state import RobotState
from src.problem import WarehouseProblem


def test_state_equality():
    """Test state equality check."""
    state1 = RobotState((0, 0), frozenset([(1, 1)]))
    state2 = RobotState((0, 0), frozenset([(1, 1)]))
    state3 = RobotState((0, 1), frozenset([(1, 1)]))
    
    assert state1 == state2
    assert state1 != state3


def test_state_hash():
    """Test state hashing."""
    state1 = RobotState((0, 0), frozenset([(1, 1)]))
    state2 = RobotState((0, 0), frozenset([(1, 1)]))
    
    assert hash(state1) == hash(state2)


def test_neighbors_basic():
    """Test neighbor generation."""
    grid = [['S', '.'], ['.', 'D']]
    problem = WarehouseProblem(grid, [], (1, 1))
    state = RobotState((0, 0))
    neighbors = state.get_neighbors(problem)
    
    assert len(neighbors) == 2  # Down and Right


def test_package_collection():
    """Test package collection works."""
    grid = [['S', 'P'], ['.', 'D']]
    problem = WarehouseProblem(grid, [(0, 1)], (1, 1))
    state = RobotState((0, 0))
    neighbors = state.get_neighbors(problem)
    
    # Moving to package should collect it
    for neighbor in neighbors:
        if neighbor.position == (0, 1):
            assert (0, 1) in neighbor.collected


def test_is_goal_state():
    """Test goal state detection."""
    grid = [['S', 'P'], ['.', 'D']]
    problem = WarehouseProblem(grid, [(0, 1)], (1, 1))
    
    # Not at goal yet
    state1 = RobotState((0, 0), frozenset())
    assert not state1.is_goal(problem)
    
    # At delivery but no packages collected
    state2 = RobotState((1, 1), frozenset())
    assert not state2.is_goal(problem)
    
    # At delivery with all packages
    state3 = RobotState((1, 1), frozenset([(0, 1)]))
    assert state3.is_goal(problem)


def test_state_immutability():
    """Test that states are immutable."""
    state = RobotState((0, 0), frozenset([(1, 1)]))
    
    # Should not be able to modify
    with pytest.raises(AttributeError):
        state.position = (1, 1)


def test_state_validation():
    """Test invalid state creation."""
    # Position must be a tuple
    with pytest.raises(ValueError):
        RobotState([0, 0])
    
    # Position must have 2 coordinates
    with pytest.raises(ValueError):
        RobotState((0,))
    
    # Coordinates must be integers
    with pytest.raises(ValueError):
        RobotState(("0", "1"))


def test_obstacle_avoidance():
    """Test that robot cannot move through obstacles."""
    grid = [
        ['S', 'X', '.'],
        ['X', '.', '.'],
        ['.', '.', 'D']
    ]
    problem = WarehouseProblem(grid, [], (2, 2))
    state = RobotState((0, 0))
    neighbors = state.get_neighbors(problem)
    
    # Should not be able to move through obstacles
    neighbor_positions = [n.position for n in neighbors]
    assert (0, 1) not in neighbor_positions  # X obstacle
    assert (1, 0) not in neighbor_positions  # X obstacle
