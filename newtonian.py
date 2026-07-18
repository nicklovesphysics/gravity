import numpy as np 
import matplotlib.pyplot as plt

#===================================================
#Making classes for the interacting objects
#===================================================

class MassiveBody:

    def __init__(self, mass, radius):
        self.mass = mass
        self.radius = radius
    
   
    
class Photon(MassiveBody):

    def __init__(self, mass, radius, velocity=list):
        super().__init__(mass, radius)          #assigning tiny masses and radii to a photon to mimic massless tiny particle.
        self.velocity = velocity


class CentralMass(MassiveBody):
    def __init__(self, mass, radius):
        super().__init__(mass,radius)
        self.position = np.array(0,0)
        self.velocity = 0


#====================================================
#Letting massive bodies interact ---   COMPONENT-WISE COMPUTATION FOR A VECTOR OUTPUT
#====================================================

def Distance(obj1_pos, obj2_pos):
    xrad = obj1_pos[0]-obj2_pos[0]
    yrad = obj1_pos[1]-obj2_pos[1]
    dist_norm = np.sqrt((xrad**2) + (yrad**2))
    return dist_norm

class Gravity:

    g_const = (6.67*(10**(-11)))

    def Direction(obj1_pos, obj2_pos):
        xrad = obj1_pos[0]-obj2_pos[0]
        yrad = obj1_pos[1]-obj2_pos[1]      #find positional vectors
        radius = Distance(obj1_pos,obj2_pos)
        rad_x = radius[0]
        rad_y = radius[1]

        return np.array(xrad, yrad)
    
    
    def Force(obj1, obj2, g=g_const):
        rad = Radius(obj1.position(), obj2.position())
        F = (g*obj1.mass()*obj2.mass())/(rad)
        return F