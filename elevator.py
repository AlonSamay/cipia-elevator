import bisect
from enum import Enum
from typing import Callable

from constants import MAX_FLOOR, MIN_FLOOR


class DirectionState(Enum):
    Idle = "Idle"
    Up = "Up"
    Down = "Down"
    
    def reverse(self):
        match self:
            case DirectionState.Up:
                return DirectionState.Down
            case DirectionState.Down:
                return DirectionState.Up
            case _:
                return DirectionState.Idle

class Elevator:
    
    def __init__(self, notify_state_change: Callable[['Elevator'], None], state = DirectionState.Idle, current_level: int = 0, required_levels: list[int] = None, queued_levels: list[int] = None) -> None:
        self.notify_state_change = notify_state_change
        self.state = state
        self.current_level = current_level
        self._required_levels = required_levels if required_levels else []
        self._queued_levels = queued_levels if queued_levels else []

    def priority(self, level: int, direction: DirectionState) -> int:
        """return this elevator priority (distance), lower is prefered

        Args:
            level (int): target level
            direction (DirectionState): target direction (up or down)

        Returns:
            int: distance or none if there is no prefered priority
        """
        if self.state == DirectionState.Idle or (direction == self.state and self.is_floor_in_way(level)):
            return self.distance(level)
        else:
            return None
    
    def distance(self, level: int) -> int:
        return abs(self.current_level - level)
    
    def is_floor_in_way(self, level: int) -> bool:
        return (self.state == DirectionState.Up and level >= self.current_level) or (self.state == DirectionState.Down and level <= self.current_level)
     
    def add_floor(self, level: int) -> None:
        """add floor to selected queue.
           can be called within controller, or within the elevator itself (from the numbers pad inside the elevator)

        Args:
            level (int): target level
        """
        if self.state == DirectionState.Idle:
            self._required_levels.append(level)
            self.state = self.choose_state(level)
            self.notify_state_change(self)
        else:
            if self.is_floor_in_way(level):
                if self.state == DirectionState.Up:   
                    bisect.insort(self._required_levels, level, key=lambda x: -x) # reverse insort for efficient poping
                if self.state == DirectionState.Down:
                    bisect.insort(self._required_levels, level)
            else:
                bisect.insort(self._queued_levels, level)

    def choose_state(self, level) -> DirectionState:
            if self.current_level > level:
                return DirectionState.Down
            elif self.current_level < level:
                return DirectionState.Up
            else:
                return DirectionState.Idle
    
    def arrived(self) -> None:
        """
        because the queues are ordered by the state (ascending while going down and descending while going up), when arrived to floor we should always pop the last floor.
        when the elevator got to the last floor of the list, check if there are floors waiting at queued_levels
        """
        self._required_levels.pop()
        if not self._required_levels:
            if self._queued_levels:
                self.state.reverse() # reverse the state from up to down or vice versa
                if self.state == DirectionState.Up:
                    self._queued_levels.reverse()
                self._required_levels = self._queued_levels
                self._queued_levels = []
            else:
                self.state = DirectionState.Idle
            
            self.notify_state_change(self)
               
    # for demo purposes 
    def progress(self, count):
        if self.state == DirectionState.Up:
            self.level_up(count)
        elif self.state == DirectionState.Down:
            self.level_down(count)
    
    def level_up(self, count = 1):
        if self.current_level + count < MAX_FLOOR:
            self.current_level += count
        else:
            self.current_level = MAX_FLOOR
            
        if self._required_levels[-1] == self.current_level:
            self.arrived()
        
    def level_down(self, count = 1):
        if self.current_level - count > MIN_FLOOR:
            self.current_level -= count
        else:
            self.current_level = MIN_FLOOR
            
        if self._required_levels[-1] == self.current_level:
            self.arrived()
