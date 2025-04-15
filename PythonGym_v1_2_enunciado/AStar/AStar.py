from typing import List, Optional
from .Problem import Problem
from .Node import Node  # Asegúrate de que esta importación sea correcta

class AStar:
    def __init__(self, problem: Problem):
        self.open: List[Node] = []          # Lista de nodos abiertos (type hint)
        self.processed: set[Node] = set()   # Conjunto de nodos procesados
        self.problem: Problem = problem     # Tipo Problem

    def GetPlan(self):
    #TODO implementar A*
        self.open = []
        self.processed = set()
        self.open.append(self.problem.Initial())
        
        while self.open:
            # Selecciona el nodo con menor costo F
            current = min(self.open, key=lambda node: node.F())
            self.open.remove(current)
            
            # Verifica si es la meta (sin paréntesis)
            if current == self.problem.goal:
                return self.ReconstructPath(current)
            
            self.processed.add(current)
            successors = self.problem.GetSucessors(current)
            
            for successor in successors:
                if successor in self.processed:
                    continue
                
                new_g = current.G() + self.problem.GetGCost(successor)
                existing = next((n for n in self.open if n == successor), None)
                
                if not existing:
                    self._ConfigureNode(successor, current, new_g)
                    self.open.append(successor)
                elif new_g < existing.G():
                    self._ConfigureNode(existing, current, new_g)
        
        return []  # No hay ruta
       
    def _ConfigureNode(self, node: Node, parent: Node, newG: float) -> None:
        node.SetParent(parent)
        node.SetG(newG)
        node.SetH(self.problem.Heuristic(node))  # Heurística calculada

    def GetSucesorInOpen(self, sucesor: Node) -> Optional[Node]:
        for node in self.open:
            if node == sucesor:
                return node
        return None

    def ReconstructPath(self, goal):
        #TOdo
        path = []
        current = goal
        while current is not None:
            path.append(current)
            current = current.GetParent()
        return path[::-1]
