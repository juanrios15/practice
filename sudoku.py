from math import sqrt
class Sudoku(object):
    def __init__(self, data):
        self.data = data
        
    def is_valid(self):
        
        #Revisando que la caja tenga raiz cuadrada
        for x in self.data:
            if all(isinstance(item, bool) for item in x):
                return False
            
        raiz = int(sqrt(len(self.data)))
        if not sqrt(len(self.data)).is_integer():
            return False
        
        #Revisando que las filas son iguales de largas
        self.filas = [x for x in self.data]
        for x in self.filas:
            if len(x) != len(self.data):
                return False
        self.columnas = []
        self.cajas = []
        for y in range(len(self.data)):
            col = []      
            for x in self.data:
                col.append(x[y])
            self.columnas.append(col)

        conx = 0
        
        while conx < len(self.data):
            cony = 0
            while cony < len(self.data):
                caja = []
                for x in range(raiz):
                    #a = []
                    for y in range(raiz):
                        caja.append(self.data[x+conx][y+cony])
                    #caja.append(a)
                self.cajas.append(caja)   
                cony +=raiz    
            conx +=raiz    

        #for x in self.filas:
        for x in self.filas:
            d = list(range(1,len(self.data)+1))
            if list(d) != sorted(x):
                return False
        
        for x in self.columnas:
            d = set(x)
            if list(d) != sorted(x):
                return False
            
        for x in self.cajas:
            d = set(x)
            if list(d) != sorted(x):
                return False
        
        return True