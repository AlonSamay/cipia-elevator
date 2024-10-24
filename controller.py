from elevator import Elevator, DirectionState
from constants import FLOORS_COUNT


class Controller:
    def __init__(self, elevators: list[Elevator] = None, levels_queue: list[int] = None) -> None:
        self.elevators: list[Elevator] = elevators if elevators else []
        self.levels_queue: list[int] = levels_queue if levels_queue else []
    
    def add_elevators(self, *elevators):
        self.elevators.extend(elevators)
    
    # called from floor when someone push the up or down button at a specific floor
    def call(self, level: int, direction: DirectionState) -> Elevator:
        """call a prioritized elevator

        Args:
            level (int): target level
            direction (DirectionState): target direction

        Returns:
            Elevator: decided elevator
        """
        elevator = self.decide_elevator(level, direction)
        if not elevator:
            self.levels_queue.append(level)
        else:
            elevator.add_floor(level)
        return elevator
    
    def decide_elevator(self, level: int, direction: DirectionState) -> Elevator:
        """decides which elevator to choose by weighting

        Args:
            level (int): target level
            direction (DirectionState): target direction

        Returns:
            Elevator: decided elevator
        """
        priority_elevator: Elevator = None
        priority_distance: int = FLOORS_COUNT
        
        for elevator in self.elevators:
            priority = elevator.priority(level, direction)
            if priority and priority < priority_distance:
                priority_distance = priority
                priority_elevator = elevator
                
        return priority_elevator

    # called when an elevator is changing to idle state
    def decide_from_queue(self, elevator: Elevator) -> None:
        closest = min(self.levels_queue, key= lambda level: elevator.distance(level), default= None)
        if closest:
            elevator.add_floor(closest)
            self.levels_queue.remove(closest)
    
    def add_from_queue(self, elevator: Elevator) -> None:
        for level in self.levels_queue:
            priority = elevator.priority(level)
            if priority:
                elevator.add_floor(level)
                self.levels_queue.remove(level)
    
    def notify_state_change(self, elevator: Elevator) -> None:
        """if the elevator's direction is idle, choose the closest floor for the elevator to go to and add the floors on it's way. otherwise just add the floors on it's way
           this function is the callback for each elevator

        Args:
            elevator (Elevator): target elevator
        """
        match elevator.state:
            case DirectionState.Idle:
                self.decide_from_queue(elevator)
                self.add_from_queue(elevator)
            case _:
                self.add_from_queue(elevator)
                
    # for demo purposes
    def elevators_progress(self, count = 1):
        for elevator in self.elevators:
            elevator.progress(count)
