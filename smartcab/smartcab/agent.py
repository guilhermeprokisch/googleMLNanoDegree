import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator


class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        
        self.possible_actions = [None, 'forward', 'left', 'right']
        self.alpha = 0.5
        self.Q = {}
        self.state_Qvalues = lambda y:map(lambda x: self.Q[(y,x)] if (y,x) in self.Q else 0, self.possible_actions) #Find the Q-Values of a given state.

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # TODO: Update state
        self.state = (('light', inputs['light']), ('next_waypoint', self.next_waypoint), ('oncoming', inputs['oncoming']), ('right',  inputs['right']) ,('left', inputs['left']))

        # TODO: Select action according to your policy
        max_Qvalues = self.state_Qvalues(self.state)
        max_Qvalues_index = max_Qvalues.index(max(max_Qvalues))
        
        i = random.randint(1, 10)
        
        if i != 1 :
            action = self.possible_actions[max_Qvalues_index]
        else:
            action = random.choice(self.possible_actions)
        

        # Execute action and get reward
        reward = self.env.act(self, action)

        # Gather inputs after action
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        # get state'
        after_state = (('light', inputs['light']), ('next_waypoint', self.next_waypoint), ('oncoming', inputs['oncoming']), ('right',  inputs['right'])\
            ,('left', inputs['left']))

        # TODO: Learn policy based on state, action, reward
        self.Q[(self.state,action)] = reward + self.alpha * max(self.state_Qvalues(after_state))

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # specify agent to track
    # NOTE: You can set enforce_deadline=False while debugging to allow longer trials

    # Now simulate it
    sim = Simulator(e, update_delay=0.1, display=True)  # create simulator (uses pygame when display=True, if available)
    # NOTE: To speed up simulation, reduce update_delay and/or set display=False

    sim.run(n_trials=100)  # run for a specified number of trials
    # NOTE: To quit midway, press Esc or close pygame window, or hit Ctrl+C on the command-line


if __name__ == '__main__':
    run()
