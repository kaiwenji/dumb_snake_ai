from snake import snake
import random
class agent:
    s = snake()
    valid_actions = ["up","down","right","left"]
    def __init__(self, epsilon = 1, alpha = 0.6, tolerance = 0.001, learning = False):
        self.Q = dict()
        self.epsilon = epsilon
        self.alpha = alpha
        self.tolerance = tolerance
        self.learning = learning
        self.t = 0.0
        if not learning:
            self.load_memory()
        return 
    def reset(self):
        self.t += 1
        self.epsilon=0.99**(1.5*self.t-1)
        if self.epsilon < self.tolerance:
            print "training over"
            return False
        return True
    def build_state(self):
        return self.s.get_state()
    def get_max_Q(self, state):
        return max(self.Q[state].values())
    def create_Q(self, state):
        if state not in self.Q:
            self.Q[state] = dict()
            for action in self.valid_actions:
                self.Q[state][action] = 0.0
        return 
    def choose_action(self, state):
        if self.epsilon > random.random() and self.learning: 
            action = random.choice(self.valid_actions)
        else:                                                   
            valid_actions = []
            maxQ = self.get_max_Q(state)  
            for act in self.Q[state]:   
                if maxQ == self.Q[state][act]:
                    valid_actions.append(act)
            action = random.choice(valid_actions)
        return action
    def learn(self, state, action, reward):
        if self.learning:
            self.Q[state][action] = self.Q[state][action] + self.alpha * (reward - self.Q[state][action])
        return
    def get_reward(self,action):
        reward = 0
        food = self.s.food
        old_dist = abs(food[0] - self.s.queue[0][0]) + abs(food[1] - self.s.queue[0][1])
        res = self.s.run(action)
        if res == False:
            self.s.reset()
            reward -= 10
        elif res[1] == True:
            reward += 30
            if self.reset() == False:
                return False
        else:
            reward += 2
            if old_dist > abs(food[0] - self.s.queue[0][0]) + abs(food[1] - self.s.queue[0][1]):
                reward += 10
            else:
                reward -= 20
        return reward
    def update(self):
        state = self.build_state()          # Get current state
        self.create_Q(state)                 # Create 'state' in Q-table
        action = self.choose_action(state)  # Choose an action
        reward = self.get_reward(action) # Receive a reward
        if reward == False:
            return False
        self.learn(state, action, reward)
        return True
    def load_memory(self):
        try:
            file_object = open('test.txt')
            try:
                all_the_text = file_object.read( )
                self.Q = eval(all_the_text)
            finally:
                file_object.close()
        except IOError:
            self.Q = dict()
    def output(self):
        file_object = open('test.txt', 'w')
        file_object.write(str(self.Q))
        file_object.close()

def run():
    my_agent = agent(learning = True)
    my_agent.load_memory()
    for i in range(200000):
        my_agent.update()
    my_agent.output()
if __name__ == '__main__':
    run()