from itertools import permutations
import copy

def generatePerms(size_v,size_h):
    # create permutations of matrix contents
    perms = list(permutations(range(1,size_v*size_h+1)))

    # move data to a matrix structure
    matrices = []
    for perm in perms:
        matrix = []
        for i in range(size_v):
            row = []
            for j in range(size_h):
                row.append(perm[i*size_h + j])
            matrix.append(row)
        matrices.append(matrix)
        
    return matrices

def findUniqueSols(solutions):
    # make a local copy
    if len(solutions) <= 1:
        return solutions
    elif len(solutions) == 2:
        if areSame(solutions[0],solutions[1]):
            return [solutions[0]]
        else:
            return solutions
    else:
        left = findUniqueSols(solutions[len(solutions)//2:])
        right = findUniqueSols(solutions[:len(solutions)//2])
        for i in range(len(left)):
            for j in range(len(right)):
                if areSame(left[i],right[j]):
                    del right[j]
        return left + right
        
def areSame(a, b):
    if a == b.gettranspose():
        return False
    return True

def showSolutions(matrices, sum_number, hole_locations=[]):
    # create hole
    local = copy.deepcopy(matrices)
    #if hole_location[0] >= 0 and hole_location[1] >= 0:
    if len(hole_locations) != 0:
        for matrix in local:
            for hole_location in hole_locations:
                matrix[hole_location[0]][hole_location[1]] = 0
    
    # group solutions together
    solutions = []
    for matrix in local:
        s = Square(matrix)
        # check for solution
        if s.checkSums(sum_number):
            solutions.append(s)
            
    # show the solutions
    if len(solutions) > 1 :
        print("There are " + str(len(solutions)) + " solutions !")
        unique = findUniqueSols(solutions)
    
        if len(unique) != 1:
            print("There are " + str(len(unique)) + " unique solutions !")
        else:
            print("There is 1 unique solution !")

        for i in range(len(unique)):
            print(" ".join(("\nSolution",str(i+1),":\n")))
            unique[i].show()
    elif len(solutions) == 1 :
        print("There is 1 solution !")
        solutions[0].show()
    else:
        print("There are no solutions !")
    

class Square:
    
    def __init__(self, matrix):
        self.matrix = matrix;
        self.sums_v = [0] * len(self.matrix[0])
        self.sums_h = [0] * len(self.matrix)
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix)):
                self.sums_h[i] += matrix[i][j]
                self.sums_v[j] += matrix[i][j]
                
    def checkSums(self, number):
        for s in self.sums_v:
            if s != number:
                return False
        
        for s in self.sums_h:
            if s != number:
                return False
            
        # none not matching was found  
        
        return True
    
    def gettranspose(self):
        new = []
        for i in range(len(self.matrix)):
            row = []
            for j in range(len(self.matrix)):
                row.append(self.matrix[j][i])
                new.append(row)
            
        return new
        
    def show(self):
        print_string = "    "
        
        # vertical results
        for s in self.sums_v:
            print_string += str(s) + "   "

        # square
        row_num = 0
        for row in self.matrix:
            # horizontal result
            print_string += "\n"
            
            for i in range(3):
                print_string += " "
            
            print_string += "┼"
            for i in range(len(row)*4 - 1):
                if (i+1)%4 == 0:
                    print_string += "┼"
                else:
                    print_string += "─"
                    
            print_string += "┤"
                
            print_string += "\n"
            
            # print matrix contents
            print_string += str(self.sums_h[row_num]) + " │"
            for number in row:
                if number != 0:
                    num_str = str(number)
                else:
                    num_str = "◾"
                print_string += " " + num_str + " │"
            
            #increment counter for rows
            row_num += 1
        
        print_string += "\n   ┴"
        for i in range(len(self.matrix[1])*4 -1):
            if (i+1)%4 == 0:
                print_string += "┴"
            else:
                print_string += "─"
            
        print_string += "┘"
            
        print(print_string)