#CLASS TO SIMULATE SYSTEM
import scipy.constants as constants
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import use
import math
import csv
use('TkAgg')
from Body import Body

class System(object):

    def __init__(self,  filename, timestep = 86400, nr_frames = -1):

        self.size_limit = 0                         # The total size of simulation, i.e. the extent till which to display.
        self.bodies = self.load_values(filename)    # A list of all Body objects in the simulation.
        self.timestep = timestep                    # The smallest time interval for the simulation.
        self.time = 0                               # The current time of the simulation, initialised to zero at the beggining.
        self.ax = None                              # Declared here and later defined as pyplot axes, otherwise leads to calling before declaration.
        self.nr_frames = nr_frames                  # The number of frames for which to run the simulation
        self.total_energy = None                    # The total energy of the system.
        self.has_satellite = False                  # A boolean to check if a satellite has been added to the system or not.

    # Method to return a list of body objects created using the values in a given csv file.
    def load_values(self,filename):
        bodies= []

        with open(filename, 'r') as file:
            reader = csv.reader(file)
            for body in reader:
                name = body[0]
                mass = float(body[1])
                position = np.array((float(body[2]), 0.0))
                # increases the size limit if the new body is further away than the previous ones.
                if (float(body[2])>self.size_limit):
                    self.size_limit = round(float(body[2]))
                # provides non-zero intial velocity to all bodies that are not the sun (sun will have x-coordinate as 0).
                if int(position[0])!=0:
                    velocity = np.array((0.0, math.sqrt(constants.gravitational_constant*1.9885E+30/position[0])))
                else:
                    velocity = np.array((0.0,0.0))
                radius = int(body[4])
                colour = (float(body[5]), float(body[6]), float(body[7]))
                # create and append new body to the list.
                new_body = Body(name, mass, position, velocity, radius, colour)
                bodies.append(new_body)
                
        return bodies
    # Creates and adds a body object representing a satellite to the simuation.
    # Requires a VSC file containing the values for the satellite. 
    def add_satellite(self, filename):
        with open(filename) as file:
            reader = csv.reader(file)
            for value in reader:
                name = value[0]
                mass = float(value[1])
                position = np.array((float(value[2]), 0.0))
                angle = math.radians(float(value[3]))
                velocity = np.array([eval(value[4])*math.cos(angle),eval(value[4])*math.sin(angle)])
                radius = int(value[5])
                colour = (float(value[6]), float(value[7]), float(value[8]))
                # Creating the body object representing the satellite.
                satellite = Body(name, mass, position, velocity ,radius, colour)
        self.bodies.append(satellite)
        # Setting boolean has_satellite to True as a satellite has been added.
        self.has_satellite = True
        # Clears any previous satellite data.
        with open('SatelliteExperimentData.csv', 'w') as file:
            file.truncate()

    # Writes the satellites distance to mars and distance to earth to a csv file along with the time in earth days.
    def write_satellite_dist(self, dist_to_mars, dist_to_earth):
        with open('SatelliteExperimentData.csv', 'a', newline = '') as file:
            writer = csv.writer(file)
            writer.writerow([self.time/86400, dist_to_mars, dist_to_earth])

    # Plots the percetage variation in energy using matplotlib and data from a given file.
    # The filename is the CSV file containing data for the total energy of system.  
    # The method also save the plot as a PNG file.
    def plot_energy_variation(self, filename):
        energy_time = []
        energy_data = []
        avg_energy = 0
        energy_difference = []
        with open(filename, 'r', newline='') as file:
            energy_reader = csv.reader(file)
            for i in energy_reader:
                # Division by 86400 to convert time from seconds to earth days.
                # 86400 is number of seconds in an Earth day (60 seconds * 60 minutes * 24 hours)
                energy_time.append(eval(i[0])/86400) 
                energy_data.append(eval(i[1]))

        # Gets the average energy from all the data
        avg_energy = sum(energy_data)/len(energy_data)

        # Calculating the percentage variation.
        for i in energy_data:
            energy_difference.append((i-avg_energy)*100/avg_energy)
        fig, ax = plt.subplots(1, figsize = (10,5))
        # Labelling the plot.
        ax.set_title('Percentage Variation of Total Energy of System about its mean', fontsize = 13)
        ax.set_xlabel('Time in Earth Days')
        ax.set_ylabel('Percentage of variation of Total Energy')
        # Plotting the data.
        ax.plot(energy_time,energy_difference, label = 'Calculated Total Energy')
        ax.legend()
        # Saving plot as PNG file.
        plt.savefig('TotalEnergyVariationGraph.png')
        plt.show()

    # Plots the total energy in the system using matplotlib and data from a given file.
    # The filename is the CSV file containing data for the total energy of system.
    # The method also saves the plot as a PNG file.
    def plot_energy(self, filename):
        energy_time = []
        energy_data = []
        with open(filename, 'r', newline='') as file:
            energy_reader = csv.reader(file)
            for i in energy_reader:
                # Division by 86400 to convert time from seconds to earth days.
                # 86400 is number of seconds in an Earth day (60 seconds * 60 minutes * 24 hours)
                energy_time.append(eval(i[0])/86400)
                energy_data.append(eval(i[1]))
        # Gets the average energy from all the data
        avg_energy = sum(energy_data)/len(energy_data)
        fig, ax = plt.subplots(1, figsize = (10,5))
        # Labelling the plot.
        ax.set_title('Total Energy of System over time', fontsize = 13)
        ax.set_xlabel('Time in Earth Days')
        ax.set_ylabel('Total Energy of System in Joules')
        ax.set_ylim(avg_energy*0.9999, avg_energy*1.0001)
        # Plotting the data.
        ax.plot(energy_time,energy_data, label = 'Calculated Total Energy')
        ax.legend()
        # Saving plot as PNG file.
        plt.savefig('TotalEnergyGraph.png')
        plt.show()

    # Calculates and returns the gravitational force on a given body due to all other bodies in the system.
    def g_force(self, body: Body):
      
        total_force = np.array([0.0, 0.0])
        for other_body in self.bodies:
            if other_body != body:
                relative_pos = other_body.position - body.position
                total_force += ( body.mass * other_body.mass * relative_pos)/(np.linalg.norm(relative_pos)**3)
        total_force *= constants.gravitational_constant
       
        return total_force
    
    # Initialises the accelaration for all bodies in the system by using formula Force = mass * accelaration.
    def initialise_acceleration(self):
        for body in self.bodies:
            body.prev_acceleration = self.g_force(body)/body.mass

    # Updates positions for all bodies in the system given a list of next positions for all bodies as argument.
    def update_positions(self, next_positions):
        for i in range(len(next_positions)):
            self.bodies[i].update_position(next_positions[i])

    # Calculates the total potential energy of the system.
    def total_potential_energy(self):
        # Variable for total potential energy.
        U = 0
        for body in self.bodies:
            for other_body in self.bodies:
                # To make sure we dont calulate the potential of a body in itself as will leade to divison by zero error.
                if body != other_body:
                    r = np.linalg.norm(other_body.position - body.position)
                    U -= (1/2)*(constants.gravitational_constant*body.mass*other_body.mass/abs(r))
        return U

    # Calculates and returns the total kinetic energy of all bodies in the system.
    def total_kinetic_energy(self):
        KE = 0
        for body in self.bodies:
            KE += body.kinetic_energy()
        return KE

    # Writes the total energy of the system along with time into a CSV file.
    def write_energy(self):
        with open('TotalEnergy.csv', 'a', newline = '') as file:
            energy_writer = csv.writer(file)
            energy_writer.writerow([self.time, self.total_energy])

    # Performs an iteration, i.e. increases time by the time-step and updates all bodies accordingly.
    def iterate(self):
        # Initialise accelaration for all bodies.
        if self.time == 0:
            self.initialise_acceleration()
        # Calulates and writes the satellites distance to mars and earth if a satellite has been added to the system.
        if self.has_satellite:
            dist_to_mars = np.linalg.norm(self.bodies[-1].position - self.bodies[4].position)
            dist_to_earth = np.linalg.norm(self.bodies[-1].position - self.bodies[3].position)
            self.write_satellite_dist(dist_to_mars, dist_to_earth)

        # we store next positions in alist as we need to update them in one go.
        # if we update as we go, then we could get incorrect values for force.                    
        next_positions = []

        for body in self.bodies:
            body.acceleration = self.g_force(body)/body.mass
            next_positions.append(body.calc_position(self.timestep))

        self.update_positions(next_positions)
        # Calculates next accelaration for a body and updates its velocity as well as accelarations.
        for body in self.bodies:
            next_acceleration = self.g_force(body)/body.mass
            body.update_velocity(body.calc_velocity(self.timestep, next_acceleration))
            body.update_accelerations(next_acceleration)
            # Checks if the body completed an orbit if it is not the sun.
            if body.name != 'Sun':
                body.check_orbit(self.time)
        # Updating the total energy of the system by addig the total kinetic and total potential energy.
        self.total_energy = self.total_kinetic_energy() + self.total_potential_energy()
        # Writing toal energy to file.
        self.write_energy()
        # Increasing time by the time-step
        self.time += self.timestep

    # Function to initialise animation by adding the background.
    def init_animate(self):
        plots = []
        im = plt.imread('Images\\stars.png')
        self.size_limit *= 1.25
        self.ax.set_xlim(-self.size_limit, self.size_limit)
        self.ax.set_ylim(-self.size_limit, self.size_limit)
        self.ax.set_aspect(1)
        plots.append(self.ax.imshow(im, extent = (-self.size_limit, self.size_limit, -self.size_limit, self.size_limit), zorder = -1))
        return plots

    # Function to return a list of artists to plot the various bodies and perform animation.
    def animate(self, i):
        while i<self.nr_frames or self.nr_frames == -1:    
            self.iterate()
            plots = []
            for body in self.bodies:
                # Reads image file of body.
                im = plt.imread('Images\\'+body.name.lower()+'.png')

                #FOR PATH LINE PLOTTING
                '''
                line = self.ax.add_patch(plt.Circle(body.position, 4e8,color = 'g', animated = False, zorder = 1 ))          
                line = self.ax.imshow(im, extent = (body.position[0]-4e9, body.position[0]+4e9, body.position[1]-4e9, body.position[1]+4e9), animated = False, zorder = 1 )
                plots.append(line)
                '''

                #SCALING RADIUS
                scaled_radius = 2*math.log(body.radius, 1.005)**4.4*(1/60000)

                #CIRCLE PLOTTING
                '''
                plot = plt.Circle(body.position, scaled_radius, color = body.colour, animated = True)
                plots.append(self.ax.add_patch(plot))
                '''
    
                #IMAGE PLOTTING
                plot = self.ax.imshow(im, extent = (body.position[0]-scaled_radius, body.position[0]+scaled_radius, body.position[1]-scaled_radius, body.position[1]+scaled_radius), animated = True, zorder = 2 )
                plots.append(plot)  

            # Prints total energy of system after every 100 frames.
            if i%100 == 0:
                print('Total Energy: '+str(self.total_energy))

            return plots

    def display(self):

        fig, self.ax = plt.subplots(1, figsize = (5,5))

        # SET BLACK BACKGROUND FOR CIRCLE PLOTTING
        '''
        self.ax.set_facecolor('k')
        self.ax.set_xlim(-3e+11, 3e+11)
        self.ax.set_ylim(-3e+11, 3e+11)
        self.ax.set_aspect(1)
        '''

        # Print string represntation of all bodies in simulation.
        for body in self.bodies:
            print(body)

        # Case for infinite frames
        if self.nr_frames == -1:
            anim = FuncAnimation(fig, self.animate, init_func= self.init_animate, repeat = False, interval = 20, blit = True)
        # Case for set number of frames.
        else:
            anim = FuncAnimation(fig, self.animate, init_func= self.init_animate, frames = self.nr_frames, repeat = False, interval = 20, blit = True)
        
        plt.show()
    