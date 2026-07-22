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
        F_mag = (g*obj1.mass*obj2.mass)/(rad)
        return (F_mag)
    

#=========================================
#Parameters for numerical path integration
#=========================================

n_iterations = 2000
t_iter = .1

center = CentralMass(mass = 10e31, radius = 14852, position = (0,0))
photon = Particle(mass = 1, radius = 1, velocity = (0, 3*(10**8)), position = ((center.radius+ 7411.1111),0))

#==========================================
#For loop/variables to ray trace
#==========================================

F_init = Gravity.Force(photon, center)
F_init_d = Gravity.Direction(photon, center)

velocity_list = np.empty(((n_iterations+1), 2))  #two dimensional array for 2d vector sums, not plotting with a for loop. 
pos_list = np.empty(((n_iterations+1),2))       #same for positions, both with one extra slot for initial part. 
forces = np.empty(((n_iterations+1),1))
#===================================================
#initial position change, velocity change for plotting
#===================================================

F_mag = F_init
F_dir = F_init_d

pos_init_x = photon.pos[0]
pos_init_y = photon.pos[1]

v_init_x = photon.velocity[0]
v_init_y = photon.velocity[1]



velocity_list[(0),:] = [v_init_x, v_init_y]
pos_list[(0), :] = [pos_init_x, pos_init_y]



v_iter_x = -(F_mag*F_dir[0]*t_iter)/(photon.mass)          #Velocity (vector) gained from Gravitational Force
v_iter_y = -(F_mag*F_dir[1]*t_iter)/(photon.mass)



v_fx = v_init_x + v_iter_x 
v_fy = v_init_y + v_iter_y

pos_iter_x = v_fx*t_iter
pos_iter_y = v_fy*t_iter

pos_init_dispx = pos_iter_x+pos_init_x
pos_init_dispy = pos_iter_y+pos_init_y

velocity_list[(1),:] = [v_fx, v_fy]
pos_list[(1), :] = [pos_init_dispx, pos_init_dispy]


#===================================================
#Looping over iterations and adding results into list of all positional changes for plotting later. 
#===================================================

print("Beginning For Loop")


for i in range((n_iterations-1)):
    
    if Distance(photon,center) >= center.radius:
        v_0x = velocity_list[(i+1),0]
        v_0y = velocity_list[(i+1),1]

        x_0 = pos_list[(i+1),0]
        y_0 = pos_list[(i+1),1]

        setattr(photon,'velocity',(v_0x,v_0y))
        setattr(photon,'position',(x_0,y_0))



        F_mag = Gravity.Force(photon, center)
        F_dir = Gravity.Direction(photon, center)



        v_iter_x = -(F_mag*F_dir[0]*t_iter)/(photon.mass)          
        v_iter_y = -(F_mag*F_dir[1]*t_iter)/(photon.mass)


        v_fx = v_0x + v_iter_x
        v_fy = v_0y + v_iter_y

        pos_iter_x = v_fx*t_iter
        pos_iter_y = v_fy*t_iter

        pos_fx = pos_iter_x + x_0
        pos_fy = pos_iter_y + y_0


        velocity_list[(i+2), :] = [v_fx, v_fy]
        pos_list[(i+2), :] = [pos_fx, pos_fy]
    else:
        pos_list[(i+2),:] = np.nan
        velocity_list[(i+2), :] = np.nan

print(velocity_list)
print(pos_list)


print('==================')


# #===================================================
# #Plotting positions over time
# #===================================================

xpos = pos_list[:,0]
ypos = pos_list[:,1]



fig, ax = plt.subplots()

ax.plot(xpos, ypos, c = 'blue')
ax.set_xlim(0,2.9*center.radius)
ax.set_ylim(-.85*center.radius, 1.6*center.radius)
circ = matplotlib.patches.Circle((0,0), radius = center.radius)
ax.add_patch(circ)
plt.show()


#git test
   
    


