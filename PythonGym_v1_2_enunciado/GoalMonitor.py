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
        #TODO
        # Replanificar si se ha forzado manualmente

        # Replanificar cada cierto tiempo (por ejemplo, cada 5000 unidades de tiempo)
        if self.recalculate:
            self.lastTime = perception[AgentConsts.TIME]
            self.recalculate = False
            return True

        # Replanificar cada cierto tiempo (por ejemplo, cada 5000 unidades de tiempo)
        current_time = perception[AgentConsts.TIME]
        if current_time - self.lastTime > 5000:
            self.lastTime = current_time
            return True

        # Replanificar si la salud del agente es baja (por ejemplo, menos de 3)
        if perception[AgentConsts.HEALTH] < 2:
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
