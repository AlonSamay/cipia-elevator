import pytest
from elevator import Elevator, DirectionState
from controller import Controller

# @pytest.mark.parametrize(
#     "x,y,expected",
#     [
#         (,3,4), (1,3,5)
#     ]
# )
# def test_elevator(x, y, expected):
#     assert x + y == expected

# first test: calling elevator
@pytest.mark.parametrize(
    "floor_to_call, expected, controller_lvl_q, ele1_current, ele1_state, ele1_req, ele1_queued, ele2_current, ele2_state, ele2_req, ele2_queued"
    [
        (1, "ele1")
    ]
)
def test_call(floor_to_call, expected, controller_lvl_q = None, ele1_current = 0, ele1_state = DirectionState.Idle, ele1_req = None, ele1_queued = None, ele2_current = 0, ele2_state = DirectionState.Idle, ele2_req = None, ele2_queued = None):
    controller = Controller(levels_queue= controller_lvl_q if controller_lvl_q else [])
    ele1 = Elevator(controller.notify_state_change, ele1_state, ele1_current, ele1_req if ele1_req else [], ele1_queued if ele1_queued else [])
    ele2 = Elevator(controller.notify_state_change, ele2_state, ele2_current, ele2_req if ele2_req else [], ele2_queued if ele2_queued else [])
    dicti = {ele1: "ele1", ele2: "ele2"}
    controller.add_elevators([ele1, ele2])
    
    cur_ele = controller.call(floor_to_call)
    assert cur_ele == expected
    