import numpy as np 
import matplotlib.pyplot as plt

#===================================================
#Making classes for the interacting objects
#===================================================

class MassiveBody:

    def __init__(self, mass, radius, position):
        self.mass = mass
        self.radius = radius
        self.pos = position
    
   
    
class Particle(MassiveBody):

    def __init__(self, mass, radius, direction, velocity, position):
        super().__init__(mass, radius, position)          #assigning tiny masses and radii to a photon to mimic massless tiny particle.
        self.direction = direction
        self.velocity = velocity
        


class CentralMass(MassiveBody):
    def __init__(self, mass, radius, position):
        super().__init__(mass,radius, position)
        self.position = np.array([0,0])
        self.velocity = 0


#====================================================
#Letting massive bodies interact ---   COMPONENT-WISE COMPUTATION FOR A VECTOR OUTPUT
#====================================================

def Distance(obj1, obj2):       #Returns magnitude of distance from one object to another in Cartesian Coordinates
    xrad = (obj1.pos[0])-(obj2.pos[0])
    yrad = (obj1.pos[1])-(obj2.pos[1])     
    dist_norm = np.sqrt((xrad**2) + (yrad**2))
    return dist_norm

class Gravity:                          #General gravity operations and related information

    g_const = (6.67*(10**(-11)))

    def Direction(obj1, obj2):
        xrad = (obj1.pos)[0]-(obj2.pos)[0]
        yrad = (obj1.pos)[1]-(obj2.pos)[1]      #Returns normalized positional vectors
        radius = Distance(obj1,obj2)
        x_norm = ((xrad)/radius)
        y_norm = ((yrad)/radius)

        return np.array([x_norm, y_norm])
    
    
    def Force(obj1, obj2, g=g_const):
        rad = Distance(obj1, obj2)
        F_mag = (g*obj1.mass*obj2.mass)/(rad)
        return (F_mag)
    

#=========================================
#Parameters for numerical path integration
#=========================================

n_iterations = 20
t_iter = 1/n_iterations


photon = Particle(mass = 1e-50, radius = 1e-50, direction = (1,2), velocity = (1,2), position = (3,0))
center = CentralMass(mass = 10e10, radius = 10e4, position = (0,0))




#==========================================
#For loop/variables to ray trace
#==========================================

v_init_x = photon.velocity[0]
v_init_y = photon.velocity[1]

F_init = Gravity.Force(photon, center)
F_init_d = Gravity.Direction(photon, center)

vector_list = np.empty((n_iterations, 2))  #two dimensional array for 2d vector sums, not plotting with a for loop. 

print("Beginning For Loop")

for i in range(n_iterations):
 

    if i == 0:

        F_mag = F_init
        F_dir = F_init_d

        v_0x = v_init_x
        v_0y = v_init_y 

        v_iter_x = (F_mag*F_dir[0]*t_iter)/(photon.mass)          #Velocity (vector) gained from Gravitational Force
        v_iter_y = (F_mag*F_dir[1]*t_iter)/(photon.mass)
        
        v_fx = v_0x + v_iter_x                  #to annotate
        v_fy = v_0y + v_iter_y

        pos_iter_x = v_iter_x*t_iter
        pos_iter_y = v_iter_y*t_iter


    photon.velocity == [v_fx, v_fy]
    photon.pos == [pos_iter_x, pos_iter_y]

    F_mag = Gravity.Force(photon, center)
    F_dir = Gravity.Direction(photon, center)


    v_iter_x = (F_mag*F_dir[0]*t_iter)/(photon.mass)          
    v_iter_y = (F_mag*F_dir[1]*t_iter)/(photon.mass)

    pos_iter_x = v_iter_x*t_iter
    pos_iter_y = v_iter_y*t_iter

    v_fx = v_0x + v_iter_x
    v_fy = v_0y + v_iter_y

    vector_list[(i-1), :] = [v_fx, v_fy]
    print(f"Array row {i} calculated")

print(vector_list[2:5, :])

   
    


