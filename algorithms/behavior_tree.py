from enum import Enum

class BTState(Enum):
    SUCCESS = 1
    FAILURE = 2
    RUNNING = 3

class BTNode:
    def tick(self, enemy, dt):
        raise NotImplementedError

class Selector(BTNode):
    def __init__(self, children):
        self.children = children

    def tick(self, enemy, dt):
        for child in self.children:
            result = child.tick(enemy, dt)
            if result != BTState.FAILURE:
                return result
        return BTState.FAILURE

class Sequence(BTNode):
    def __init__(self, children):
        self.children = children

    def tick(self, enemy, dt):
        for child in self.children:
            result = child.tick(enemy, dt)
            if result != BTState.SUCCESS:
                return result
        return BTState.SUCCESS

class Condition(BTNode):
    def __init__(self, condition_func):
        self.condition_func = condition_func

    def tick(self, enemy, dt):
        if self.condition_func(enemy):
            return BTState.SUCCESS
        return BTState.FAILURE

class Action(BTNode):
    def __init__(self, action_func):
        self.action_func = action_func

    def tick(self, enemy, dt):
        return self.action_func(enemy, dt)