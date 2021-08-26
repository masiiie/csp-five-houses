from typing import Generic, TypeVar, Dict, List
from abc import ABC, abstractmethod
from copy import copy
  
V = TypeVar('V') # variable type
D = TypeVar('D') # domain type

class Constraint:
    def __init__(self, variables: list):
        self.variables = variables

    @abstractmethod
    def check(self, assignment: Dict[V, D]) -> bool:
        pass

class CSP(Generic[V, D]):
    def __init__(self, variables: List[V], domains: Dict[V, List[D]]):
        self.variables: List[V] = variables # variables to be constrained
        self.domains: Dict[V, List[D]] = domains # domain of each variable
        self.constraints_vars = {}
        self.constraints = []
        #print('variables {0}'.format(self.variables))
        for variable in self.variables:
            self.constraints_vars[variable] = []
            if variable not in self.domains:
                raise LookupError("Cada variable debe tener asignado un dominio.")
    
    def is_consistent(self, assigment: dict, variable):
        for cons_ in self.constraints_vars[variable]:
            if not cons_.check(assigment):
                return False
        return True

    def add_constraint(self, constraint: Constraint):
        #print("constraint_name: {0} variables: {1}".format(str(constraint),constraint.variables))
        self.constraints.append(constraint)
        for variable in constraint.variables:
            if variable not in self.variables:
                raise LookupError("La variable {0} de la restriccion no esta en el CSP.".format(variable))
            else:
                self.constraints_vars[variable].append(constraint)


def backtracking_search(csp):
    csp.nodos_visitados = 0
    s = recursive_backtracking({},csp,0)
    print('nodos visitados = {0}'.format(csp.nodos_visitados))
    return s
def recursive_backtracking(assigment:dict, csp:CSP, index:int):
    if len(assigment) == len(csp.variables):
        return assigment
    variable = csp.variables[index]
    for value in csp.domains[variable]:
        csp.nodos_visitados+=1
        assigment[variable] = value
        #print('-'*100,sep=' \n')
        #print('{1} = {2} assigment = {0}'.format(assigment,variable,value))
        #a = input('veamos si es consistente\n')
        if csp.is_consistent(assigment,variable):
            #print('is consistent','-'*10,sep='\n')
            result = recursive_backtracking(assigment,csp,index+1)
            if result != None:
                return result
        assigment.pop(variable)
    return None  

def comprobacion_hacia_adelante(csp:CSP, assigment:dict):
    copii = copy(csp)
    no_assigned = set(csp.variables) - set(assigment.keys())
    for variable in no_assigned:
        for value in csp.domains[variable]:
            assigment[variable] = value
            if not csp.is_consistent(assigment, variable):
                copii.domains[variable].remove(value)
        assigment.pop(variable)
    return copii