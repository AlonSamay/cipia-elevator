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
    def __init__(self, id, notify_state_change: Callable[['Elevator'], None], state = DirectionState.Idle, current_level: int = 0, required_levels: list[int] = None, queued_levels: list[int] = None) -> None:
        self.id = id
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
        if level == None or self.current_level == level:
            if not self._required_levels:
                self.check_queued_floors()
            return
        
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
    
    def arrived(self):
        """because the queues are ordered by the state (ascending while going down and descending while going up), when arrived to floor we should always pop the last floor.
            when the elevator got to the last floor of the list, check if there are floors waiting at queued_levels
        """
        level = self._required_levels.pop()
        self.input_level(level)
        if not self._required_levels:
            self.check_queued_floors()   
    
    def is_arrived(self):
        return self._required_levels and self._required_levels[-1] == self.current_level
    
    def check_queued_floors(self) -> None:
        """this function is triggred when the elevator reached to minimum or maximum floor, or the required levels queue is empty (no floors left in queue)
        """
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
        for _ in range(count):
            match self.state:
                case DirectionState.Up:                        
                    self.current_level += 1
                    if self.current_level == MAX_FLOOR:
                        self.check_queued_floors()
                case DirectionState.Down:
                    self.current_level -= 1
                    if self.current_level == MIN_FLOOR:
                        self.check_queued_floors()
                case _:
                    pass

            if self.is_arrived():
                self.arrived()

    def input_level(self, arrived_level) -> None:
        print("Elevator " + str(self.id) + " arrived to floor " + str(arrived_level) + "!")
        correct_input = False
        requested_level = None
        while not correct_input:
            requested_level = input("Which floor you want to go? (Max = " + str(MAX_FLOOR) + ", Min = " + str(MIN_FLOOR) + ", empty for nothing): ")
            
            if not requested_level:
                correct_input = True
            
            try:
                requested_level = int(requested_level)
            except ValueError:
                print("Wrong input, try again.")
            
            if MIN_FLOOR <= requested_level <= MAX_FLOOR:
                correct_input = True
            else:
                print("Floor is above max or below min, try again.")
                
        self.add_floor(requested_level)
