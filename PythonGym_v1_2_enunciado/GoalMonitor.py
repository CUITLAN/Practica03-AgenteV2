import random
from States.AgentConsts import AgentConsts

class GoalMonitor:

    GOAL_COMMAND_CENTRER = 0
    GOAL_LIFE = 1
    GOAL_PLAYER = 2
    def __init__(self, problem, goals):
        self.goals = goals
        self.problem = problem
        self.lastTime = -1
        self.recalculate = False

    def ForceToRecalculate(self):
        self.recalculate = True

    #determina si necesitamos replanificar
    def NeedReplaning(self, perception, map, agent):
        currentTime = perception[AgentConsts.TIME]
        if self.recalculate:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        if perception[AgentConsts.LIFE] < 2:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        if currentTime - self.lastTime > 10:
            self.lastTime = perception[AgentConsts.TIME]
            return True
        
        return False
    
    #selecciona la meta mas adecuada al estado actual
    def SelectGoal(self, perception, map, agent):
        #TODO definir la estrategia del cambio de meta
        print("TODO aqui faltan cosas :)")
        return self.goals[random.randint(0,len(self.goals))]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
