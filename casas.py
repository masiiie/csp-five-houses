from csp import Constraint, CSP, backtracking_search
'''
Ejercicio 6.7 "Artificial Intelligence A Modern Approach"
Enfoque 1
Variables:
    Xi: caracteristica X de la i-esima casa
    X = { N:nacionalidad, C:color, M:mascota, B:bebida, D:dulce }
    i = {1..5}
Dominios:
    N = { englishman, spaniard, norwegian, ukrainian, japanese }
    M = { dog, fox, snail, horse, zebra }
    D = { Hershey bars, Kit Kats, Smarties, Snickers, Milky Ways}
    C = { red, green, ivory, yellow, blue }
    B = { milk, coffee, water, orange juice, tea }
'''

class Different_constraint(Constraint):
    def check(self,assigment:dict):
        if assigment == None: return False
        values = [assigment[varr] for varr in self.variables if varr in assigment]
        #print("values {0}".format(values))
        #print('assigment {0}'.format(assigment))
        return len(set(values)) == len(values)

class Constraint1(Constraint): 
    # El ingles vive en la casa roja
    def check(self, assigment:dict):
        for i in range(1,6):
            if assigment['N{0}'.format(i)] == 'englishman':
                return assigment['C{0}'.format(i)] == 'red'

class Constraint2(Constraint): 
    # El español tiene un perro
    def check(self, assigment:dict):
        for i in range(1,6):
            if assigment['N{0}'.format(i)] == 'spaniard':
                return assigment['M{0}'.format(i)] == 'dog'

class Constraint3(Constraint): 
    # El noruego vive en la primera casa
    def check(self, assigment:dict):
        return assigment['N1'] == 'norwegian'
class Constraint4(Constraint): 
    # La casa verde le sigue a la casa de color marfil
    def check(self, assigment:dict):
        for i in range(1,5):
            if assigment['C{0}'.format(i)] == 'ivory':
                return assigment['C{0}'.format(i+1)] == 'green'
            if assigment['C{0}'.format(i)] == 'green':
                return assigment['C{0}'.format(i+1)] == 'ivory'
class Constraint5(Constraint): 
    # La casa donde se consume Hershey bars es vecina de la casa donde hay un zorro  
    def check(self, assigment:dict):
        for i in range(1,5):
            if assigment['M{0}'.format(i)] == 'fox':
                return assigment['D{0}'.format(i+1)] == 'Hershey bars'
            if assigment['D{0}'.format(i)] == 'Hershey bars':
                return assigment['M{0}'.format(i+1)] == 'fox'
class Constraint6(Constraint): 
    # En la casa amarilla se consumen Kit Kats 
    def check(self, assigment:dict):
        for i in range(1,6):
            if assigment['D{0}'.format(i)] == 'Kit Kats':
                return assigment['C{0}'.format(i)] == 'yellow'
class Constraint7(Constraint): 
    # El noruego vive al lado de la casa azul 
    def check(self, assigment:dict):
        for i in range(1,5):
            if assigment['C{0}'.format(i)] == 'blue':
                return assigment['N{0}'.format(i+1)] == 'norwegian'
            if assigment['N{0}'.format(i)] == 'norwegian':
                return assigment['C{0}'.format(i+1)] == 'blue'
                
class Constraint8(Constraint): 
    # El dueño del caracol consume Smarties
    def check(self, assigment:dict):
        for i in range(1,6):
            if assigment['M{0}'.format(i)] == 'snail':
                return assigment['D{0}'.format(i)] == 'Smarties'

class Constraint9(Constraint): 
    # Quien consume Snickers bebe jugo de naranja
    def check(self, assigment:dict):
        for i in range(1,6):
            if assigment['D{0}'.format(i)] == 'Snickers':
                return assigment['B{0}'.format(i)] == 'orange juice'
class Constraint10(Constraint): 
    # El ucraniano bebe te
    def check(self, assigment:dict):
        for i in range(1,6):
            if assigment['N{0}'.format(i)] == 'ukrainian':
                return assigment['B{0}'.format(i)] == 'tea'
class Constraint11(Constraint): 
    # El japones consume Milky Ways
    def check(self, assigment:dict):
        for i in range(1,5):
            if assigment['N{0}'.format(i)] == 'japanese':
                return assigment['D{0}'.format(i)] == 'Milky Ways'
class Constraint12(Constraint): 
    # Al lado de la casa donde hay un caballo se consume Kit Kats
    def check(self, assigment:dict):
        for i in range(1,5):
            if assigment['M{0}'.format(i)] == 'horse':
                return assigment['D{0}'.format(i+1)] == 'Kit Kats'
            if assigment['D{0}'.format(i)] == 'Kit Kats':
                return assigment['M{0}'.format(i+1)] == 'horse'
class Constraint13(Constraint): 
    # En la casa verde se consume cafe
    def check(self, assigment:dict):
        for i in range(1,5):
            if assigment['C{0}'.format(i)] == 'green':
                return assigment['B{0}'.format(i)] == 'coffee'
class Constraint14(Constraint): 
    # En la casa del medio se consume leche
    def check(self, assigment:dict):
        return assigment['B3'] == 'milk'

vars_ = ['N','C','M','B','D']
nacionalidades = ['englishman', 'spaniard', 'norwegian', 'ukrainian', 'japanese']
mascotas = ['dog', 'fox', 'snail', 'horse', 'zebra']
dulces = ['Hershey bars', 'Kit Kats', 'Smarties', 'Snickers', 'Milky Ways']
colores = ['red', 'green', 'ivory', 'yellow', 'blue'] 
bebidas = ['milk', 'coffee', 'water', 'orange juice', 'tea']
domains_ = [nacionalidades,colores,mascotas,bebidas,dulces]
csp_variables = [['{0}{1}'.format(feature,index) for index in range(1,6)] for feature in vars_ ]
csp_domains = {}
for i,vari in enumerate(vars_):
    for index in range(1,6):
        csp_domains['{0}{1}'.format(vari,index)] = domains_[i]

csp_casas = CSP(['{0}{1}'.format(feature,index) for index in range(1,6) for feature in vars_ ],csp_domains)

init_constraint = []
init_constraint.append(csp_variables[0]+csp_variables[1])
init_constraint.append(csp_variables[0]+csp_variables[2])
init_constraint.append(['N1'])
init_constraint.append(csp_variables[1])
init_constraint.append(csp_variables[2]+csp_variables[4])
init_constraint.append(csp_variables[1]+csp_variables[4])
init_constraint.append(csp_variables[0]+csp_variables[1])
init_constraint.append(csp_variables[2]+csp_variables[4])
init_constraint.append(csp_variables[3]+csp_variables[4])
init_constraint.append(csp_variables[0]+csp_variables[3])
init_constraint.append(csp_variables[0]+csp_variables[4])
init_constraint.append(csp_variables[2]+csp_variables[4])
init_constraint.append(csp_variables[1]+csp_variables[3])
init_constraint.append(['B3'])

cons__ = [Constraint1,Constraint2,Constraint3,Constraint4,Constraint5,Constraint6,Constraint7,Constraint8,Constraint9,Constraint10,Constraint11,Constraint12,Constraint13,Constraint14]

for i in range(0,5):
    csp_casas.add_constraint(Different_constraint(csp_variables[i]))
for i in range(0,14):
    csp_casas.add_constraint(cons__[i](init_constraint[i]))

  
assigment = backtracking_search(csp_casas)
for key in assigment:
    print('{0} = {1}'.format(key,assigment[key]))