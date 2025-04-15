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
            self.recalculate = False
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
    # Calcular distancias Manhattan
        dist_player = abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X]) + \
                  abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])
    
        # Calcular distancia Manhattan al command center
        dist_cc = abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.COMMAND_CENTER_X]) + \
                abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.COMMAND_CENTER_Y])
        # Elegir la meta más cercana (player=índice 2, command_center=índice 0)
        return self.goals[2] if dist_player < dist_cc else self.goals[0]
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
