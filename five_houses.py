from csp import Constraint, CSP, backtracking_search

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
all_ = ['{0}{1}'.format(feature,index) for index in range(1,6) for feature in vars_ ]
csp_casas = CSP(all_,csp_domains)


class Simple_constraint(Constraint):
    def __init__(self, feature, value):
        self.value = value
        Constraint.__init__(self, [feature])
    def check(self, assigment:dict):
        #print('Simple check: {0} = {1}'.format(self.variables[0],self.value))
        return not self.variables[0] in assigment or assigment[self.variables[0]] == self.value
    
class Five_houses_constraint(Constraint):
    '''
    features = lista de caracteristicas que el constraint relaciona
    '''
    def __init__(self, features, left, right):
        variables = ['{0}{1}'.format(feature,index) for feature in features for index in range(1,6)]
        Constraint.__init__(self, variables)
        self.v1 = left
        self.v2 = right
        self.features = features

class Neighbor_class_constraint(Five_houses_constraint):        
    def check(self, assigment:dict):
        #print('Check neighbor: {0} and {1} in {2}'.format(self.v1,self.v2,assigment))
        for i in range(1,5):
            f1 = '{0}{1}'.format(self.features[0],i)
            f2 = '{0}{1}'.format(self.features[1],i+1)
            f3 = '{0}{1}'.format(self.features[1],i)
            f4 = '{0}{1}'.format(self.features[0],i+1)
            if f1 in assigment and assigment[f1] == self.v1:
                return f2 in self.variables and (not f2 in assigment or assigment[f2] == self.v2)
            if f3 in assigment and assigment[f3] == self.v2:
                return f4 in self.variables and (not f4 in assigment or assigment[f4] == self.v1)
        return True

class Right_neighbor_class_constraint(Five_houses_constraint):        
    def check(self, assigment:dict):
        #print('Check right neighbor: {0} and {1} in {2}'.format(self.v1,self.v2,assigment))
        for i in range(1,5):
            f1 = '{0}{1}'.format(self.features[0],i)
            f2 = '{0}{1}'.format(self.features[1],i+1)

            if f1 in assigment and assigment[f1] == self.v1:
                return f2 in self.variables and (not f2 in assigment or assigment[f2] == self.v2)

            f1 = '{0}{1}'.format(self.features[1],i)
            f2 = '{0}{1}'.format(self.features[0],i-1)

            if f1 in assigment and assigment[f1] == self.v2:
                return f2 in self.variables and (not f2 in assigment or assigment[f2] == self.v1)

        return True
class Same_house_class_constraint(Five_houses_constraint):        
    def check(self, assigment:dict):
        #print('Check same house: {0} and {1} in {2}'.format(self.v1,self.v2,assigment))
        for i in range(1,5):
            f1 = '{0}{1}'.format(self.features[0],i)
            f2 = '{0}{1}'.format(self.features[1],i)

            if f1 in assigment and assigment[f1] == self.v1:
                return not f2 in assigment or assigment[f2] == self.v2
            elif f2 in assigment and assigment[f2] == self.v2:
                return not f1 in assigment or assigment[f1] == self.v1
                

        return True

class Different_constraint(Constraint):
    def check(self, assigment:dict):
        if assigment == None: return False
        values = [assigment[varr] for varr in self.variables if varr in assigment]
        #print('Check different: values = {0} variables = {1}'.format(values,self.variables))
        #print('assigment {0}'.format(assigment))
        return len(set(values)) == len(values)



c1 = Neighbor_class_constraint(['D','M'], dulces[0], mascotas[1])
c2 = Neighbor_class_constraint(['N','C'], nacionalidades[2], colores[4])
c3 = Neighbor_class_constraint(['D','M'], dulces[1], mascotas[3])
c4 = Right_neighbor_class_constraint(['C','C'],colores[2],colores[1])
c5 = Same_house_class_constraint(['N','C'], nacionalidades[0], colores[0])
c6 = Same_house_class_constraint(['N','M'], nacionalidades[1], mascotas[0])
c7 = Same_house_class_constraint(['D','C'], dulces[1], colores[3])
c8 = Same_house_class_constraint(['D','M'], dulces[2], mascotas[2])
c9 = Same_house_class_constraint(['D','B'], dulces[3], bebidas[3])
c10 = Same_house_class_constraint(['N','B'], nacionalidades[3], bebidas[4])
c11 = Same_house_class_constraint(['N','D'], nacionalidades[4], dulces[4])
c12 = Same_house_class_constraint(['C','B'], colores[1], bebidas[1])
c13 = Simple_constraint('N1',nacionalidades[2])
c14 = Simple_constraint('B3',bebidas[0])
d1 = Different_constraint(csp_variables[0])
d2 = Different_constraint(csp_variables[1])
d3 = Different_constraint(csp_variables[2])
d4 = Different_constraint(csp_variables[3])
d5 = Different_constraint(csp_variables[4])

constraints_ = [c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,d1,d2,d3,d4,d5]
for c_ in constraints_:
    csp_casas.add_constraint(c_)

assigment = backtracking_search(csp_casas)

for key in assigment:
    print('{0} = {1}'.format(key,assigment[key]))