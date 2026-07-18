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

