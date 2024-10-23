from controller import Controller 
from elevator import Elevator
from constants import *

def main():
    pass
    # con: Controller = Controller()

    # ele1 = Elevator(con)
    # ele2 = Elevator(con)

    # con.add_elevators([ele1, ele2])

    # # User called elevator at 4th floor, we except the first elevator to come
    # assert con.call(4) == ele1
    # # while ele1 going up and coming to 1st floor, another user call at floor 2. we expect the other elevator to get it
    # con.elevators_progress()
    # assert con.call(2) == ele2
    # # the elveators had progressed 2 floors
    # con.elevators_progress(2)
    # # ele2 arrived to it's destination, and the user inside the elevator wants to go to floor 0. at the same time user at floor 1 press down, we except ele2 to get the call
    # ele2.add_floor(0)

if __name__ == "__main__":
    main()
