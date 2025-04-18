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

        self.currentGoal = -1
        self.lifeExists = True

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
        map = self.problem.map

        self.lifeExist = (perception[AgentConsts.LIFE_X] != -1 and perception[AgentConsts.LIFE_Y] != -1)

        #Goals
        #Ir a por la vida si tiene vida baja y existe
        #Ir a por el jugador si tiene toda la vida
        #Goal predeterminado de ir al command center
        goals = [ (self.GOAL_LIFE, perception[AgentConsts.HEALTH] < 2 and self.lifeExists),
            (self.GOAL_PLAYER, perception[AgentConsts.HEALTH] == 3),
            (self.GOAL_COMMAND_CENTER, True) ]
        
        if self.currentGoal == -1 or (self.currentGoal == 1 and not self.lifeExist):
            #Si no hay goal seleccionado o si el goal es ir a por la vida pero ya no esta la vida
            for goal, cond in goals:
                newGoal = self.goals[goal]
                x, y = newGoal.x, newGoal.y
                pos = map[x][y]
                if cond and self.problem.getCost(pos) < sys.maxsize:
                    self.currentGoal = goal
                    return newGoal
        else:
            #Si ya hay un goal seleccionado: la vida ya esta comprobado si sigue estando en el anterior,
            #falta ver si el currentGoal es el jugador (si esta cerca del command center cambiamos goal)
            if self.currentGoal == self.GOAL_PLAYER:
                # Calcular distancia Manhattan al command center
                dist_player = abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.PLAYER_X]) + \
                abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.PLAYER_Y])

                dist_cc = abs(perception[AgentConsts.AGENT_X] - perception[AgentConsts.COMMAND_CENTER_X]) + \
                abs(perception[AgentConsts.AGENT_Y] - perception[AgentConsts.COMMAND_CENTER_Y])

                if dist_cc < dist_player:
                    self.currentGoal = self.GOAL_COMMAND_CENTER
                    return self.goals[self.GOAL_COMMAND_CENTER]
                return self.goals[self.currentGoal]
                #no se si deberia comprobar otra vez que el agente tenga la vida maxima en caso de que vaya a por el player (por cambiar el goal)

        self.currentGoal = -1

        return None
    
    def UpdateGoals(self,goal, goalId):
        self.goals[goalId] = goal
