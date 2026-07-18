import numpy as np 
import matplotlib.pyplot as plt

#===================================================
#Making classes for the interacting objects
#===================================================

class MassiveBody:

    def __init__(self, mass, radius):
        self.shape = mass
        self.radius = radius
    
   
    
class Photon(MassiveBody):

    def __init__(self, mass, radius, velocity, direction):
        super().__init__(mass, radius)          #assigning tiny masses and radii to a photon to mimic massless tiny particle.
        self.velocity = velocity
        self.direction = direction

class CentralMass(MassiveBody):
    def __init__(self, mass, radius):
        super().__init__(mass,radius)
        self.position = np.array(0,0)


#====================================================
#Letting massive bodies interact
#====================================================

def Radius(obj1_pos, obj2_pos):
    xrad = obj1_pos[0]-obj2_pos[0]
    yrad = obj1_pos[1]-obj2_pos[1]
    dist_norm = np.sqrt((xrad**2) + (yrad**2))
    return dist_norm

class Gravity:

    g = (6.67*(10**(-11)))

    def direction(obj1_pos, obj2_pos):
        xrad = obj1_pos[0]-obj2_pos[0]
        yrad = obj1_pos[1]-obj2_pos[1]      #find positional vectors

        #normalize here

        return np.array(xrad, yrad)
    
    
    def force(obj1, obj2):
        rad = Radius(obj1.position(), obj2.position())
        F = (g*obj1.mass()*obj2.mass())/(rad)
        return F