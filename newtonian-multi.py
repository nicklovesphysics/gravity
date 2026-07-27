import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches
from tqdm import tqdm
import math

#===================================================
#Making classes for the interacting objects
#===================================================
c = 299792458       #m/s

class MassiveBody:

    def __init__(self, mass, radius, position):
        self.mass = mass
        self.radius = radius                    #initializing general attributes for interacting bodies in the simulation. 
        self.pos = position
    
   
    
class Particle(MassiveBody):

    def __init__(self, mass, radius, velocity, position):
        super().__init__(mass, radius, position)          #assigning tiny masses and radii to a photon can mimic a real one: massless, radius-less particle.
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
    dist_norm = np.sqrt((xrad**2) + (yrad**2))    #Distance between centers of mass

    valid = dist_norm > (obj1.radius + obj2.radius)

    if valid == True:
        return dist_norm        #Masking out positions of collision between planets. 
                                
    else: 
        return np.nan

class Gravity:                          #General gravity operations and related information

    g_const = (6.67*(10**(-11)))

    def Direction(obj1, obj2):                  #direction of gravitation force
        xrad = (obj1.pos)[0]-(obj2.pos)[0]
        yrad = (obj1.pos)[1]-(obj2.pos)[1]      #Returns normalized positional vectors
        radius = Distance(obj1,obj2)
        x_norm = ((xrad)/radius)
        y_norm = ((yrad)/radius)

        return np.array([x_norm, y_norm])
    
    
    def Force(obj1, obj2, g=g_const):           #magnitude of gravitation force
        rad = Distance(obj1, obj2)
        F_mag = ((g)*(obj1.mass)*(obj2.mass))/(rad)**2
        return (F_mag)

    def Photon_Sphere(obj, g=g_const):      #radius of photon sphere
        radius = (3*g*obj.mass)/c**2
        return radius
    

#=========================================
#Parameters for numerical path integration
#=========================================

#**EVERY TIME UNIT IS IN seconds!** 

n_iterations = 2000       #number of iterations of for loop.
t_iter = .000001                  #time used for linear approximations of each iteration. Comparable to resolution. 

#for a smooth simulation, t_iter*n_iterations should be comparable to orbital period.
#a good rule of thumb is: if t_iter goes down an order of magnitude, n_iteratoins must go up by one.
#Increase n_iterations after this if you do not see a complete trajectory.

center = CentralMass(mass = 10e31, radius = 14852.32, position = (0,0))

#==========================================
#For loop/variables to ray trace
#==========================================

pos_velo_list = np.empty((n_iterations, 4)) #2d array for position and velocity at each iteration, (4 columns = vx,vy,px,py).  


#==================================================================================================
#Looping over increments of 5 degrees in velocities from a point-like source 
#==================================================================================================

fig, ax = plt.subplots()
fig.set_facecolor('white')
ax.set_facecolor('black')
circ = matplotlib.patches.Circle((0,0), radius = center.radius, color = 'yellow')         #circle to show central body "surface". 
ax.add_patch(circ)
ax.set_aspect('equal')

for i in tqdm(range(0,36)):         #looping through different radial initial velocities (360 degrees).
    photon = Particle(mass = 1, radius = 1, velocity = (c*(np.cos(math.radians(10*i))), (c*(np.sin(math.radians(10*i))))), position = (120000,0))      #name is photon, but orbital object could be anything. 
    #===================================================
    #initial position change, velocity change for plotting
    #===================================================

    pos_init_x = photon.pos[0]
    pos_init_y = photon.pos[1]      #initial position of the orbiting object for  loop array initialization

    v_init_x = photon.velocity[0]
    v_init_y = photon.velocity[1]       #initial velocity of the 




    pos_velo_list[(0),0:2] = [v_init_x, v_init_y]
    pos_velo_list[(0), 2:] = [pos_init_x, pos_init_y]       #adding initial position and velocity into a list for easy looping and plotting 


    #ALL VALUES FOR POSITION, ACCELERATION, VELOCITY ARE VECTOR AND CAN BE GENERALIZED INTO N DIMENSIONS.

    for i in (range(1,n_iterations)):
        v_0x = pos_velo_list[i-1, 0]        #initial velocity from list, uses last iteration's final velocity.
        v_0y = pos_velo_list[i-1, 1]

        p_0x = pos_velo_list[i-1, 2]        #initial velocity from list, uses last iteration's final velocity.
        p_0y = pos_velo_list[i-1, 3]


        photon.velocity = (v_0x, v_0y)      #rewriting the attributes of the orbiting element to the new initial values
        photon.pos = (p_0x, p_0y)

        F_mag = Gravity.Force(photon, center)              #calculating magnitude and direction of gravitational force from new rewritten attributes
        F_dir = -(Gravity.Direction(photon, center))

        agx = (F_mag*F_dir[0])/(photon.mass)          #Acceleration from Gravitational Force = F_g/m_orbit
        agy = (F_mag*F_dir[1])/(photon.mass)

        v_fx = v_0x + (agx*t_iter)          #approximating a small dv = a*t (linear), adding to initial velocity for a final velocity 
        v_fy = v_0y + (agy*t_iter)             #to be used in position calculation as a linear approximation


        pos_addx= v_fx*t_iter               #previously mentioned linear approximation x = v*t for position vector to be added to initial position vector
        pos_addy = v_fy*t_iter              
        pos_finx = p_0x + pos_addx          #adding linear dx to initial position for a final position
        pos_finy = p_0y + pos_addy


        pos_velo_list[(i), 0:2] = [v_fx, v_fy]          #adding final x,v to the list to be used in next run of loop
        pos_velo_list[(i), 2:] = [pos_finx, pos_finy]

    #plotting each time


    ax.plot(pos_velo_list[:,2],pos_velo_list[:,3] , c = 'white')
    ax.set_xlim(-150000,200000)
    ax.set_ylim(-150000,200000)


plt.tight_layout()
plt.show()
plt.close()


print('==================')

print(f'pay special attention to the radius of the photon sphere: ', Gravity.Photon_Sphere(center))


print('==================')







   
    


