import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches

#===================================================
#Making classes for the interacting objects
#===================================================

class MassiveBody:

    def __init__(self, mass, radius, position):
        self.mass = mass
        self.radius = radius
        self.pos = position
    
   
    
class Particle(MassiveBody):

    def __init__(self, mass, radius, velocity, position):
        super().__init__(mass, radius, position)          #assigning tiny masses and radii to a photon to mimic massless tiny particle.
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

    def Direction(obj1, obj2):
        xrad = (obj1.pos)[0]-(obj2.pos)[0]
        yrad = (obj1.pos)[1]-(obj2.pos)[1]      #Returns normalized positional vectors
        radius = Distance(obj1,obj2)
        x_norm = ((xrad)/radius)
        y_norm = ((yrad)/radius)

        return np.array([x_norm, y_norm])
    
    
    def Force(obj1, obj2, g=g_const):
        rad = Distance(obj1, obj2)
        F_mag = ((g)*(obj1.mass)*(obj2.mass))/(rad)**2
        return (F_mag)
    

#=========================================
#Parameters for numerical path integration
#=========================================

n_iterations = 360
t_iter = 1

center = CentralMass(mass = 10e19, radius = 1000, position = (0,0))
photon = Particle(mass = 1, radius = 1, velocity = (0, 490), position = (12000,0))

#==========================================
#For loop/variables to ray trace
#==========================================

# F_init = Gravity.Force(photon, center)
# F_init_d = -(Gravity.Direction(photon, center))

pos_velo_list = np.empty((n_iterations, 4)) #2d array for position and velocity at each iteration, (4 columns = vx,vy,px,py).  

#===================================================
#initial position change, velocity change for plotting
#===================================================

pos_init_x = photon.pos[0]
pos_init_y = photon.pos[1]

v_init_x = photon.velocity[0]
v_init_y = photon.velocity[1]




pos_velo_list[(0),0:2] = [v_init_x, v_init_y]
pos_velo_list[(0), 2:] = [pos_init_x, pos_init_y]




#===================================================
#Looping over iterations and adding results into list of all positional changes for plotting later. 
#===================================================

#x-forces are being completely miscalculated. 

for i in (range(1,n_iterations)):
    v_0x = pos_velo_list[i-1, 0]
    v_0y = pos_velo_list[i-1, 1]

    p_0x = pos_velo_list[i-1, 2]
    p_0y = pos_velo_list[i-1, 3]


    photon.velocity = (v_0x, v_0y)
    photon.pos = (p_0x, p_0y)

    F_mag = Gravity.Force(photon, center)
    F_dir = -(Gravity.Direction(photon, center))

    agx = (F_mag*F_dir[0])/(photon.mass)          #Acceleration from Gravitational Force
    agy = (F_mag*F_dir[1])/(photon.mass)

    v_fx = v_0x + (agx*t_iter)
    v_fy = v_0y + (agy*t_iter)     


    pos_addx= v_fx*t_iter
    pos_addy = v_fy*t_iter
    pos_finx = p_0x + pos_addx
    pos_finy = p_0y + pos_addy


    pos_velo_list[(i), 0:2] = [v_fx, v_fy]
    pos_velo_list[(i), 2:] = [pos_finx, pos_finy]


# print(pos_velo_list[0:25])


print('==================')


# #===================================================
# #Plotting positions over time
# #===================================================




fig, ax = plt.subplots()

ax.plot(pos_velo_list[:,2],pos_velo_list[:,3] , c = 'blue')
ax.set_xlim(-19*center.radius,19*center.radius)
ax.set_ylim(-19*center.radius, 19*center.radius)
circ = matplotlib.patches.Circle((0,0), radius = center.radius)
ax.add_patch(circ)
plt.show()


   
    


