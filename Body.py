#CLASS FOR ALL CELESTIAL BODIES
import csv
import numpy as np

class Body(object):

    def __init__(self, name, mass, position, velocity, radius, colour):
        self.name = name                                # string representing name of celestial body
        self.mass = mass                                # float for the mass of celestial body
        self.position = position                        # numpy array representing position vector
        self.velocity = velocity                        # numpy array representing velocity vector
        self.radius = radius                            # integer for the radius of celestial body
        self.colour = colour                            # triple for colour of body
        self.acceleration = np.array([0.0, 0.0])        # initialising acceleration to zero vector
        self.prev_acceleration = np.array([0.0, 0.0])   # initialising previous acceleration to zero vector
        self.orbital_periods = []                       # store the orbital periods of the planet 
        self.prev_time = 0                              # used for keeping track when it last completed orbit


    # String representation of a body    
    def __str__(self):
        return f'name: {self.name}, \nmass: {self.mass}, \nposition: {self.position},\
            \nvelocity: {self.velocity}, \nradius: {self.radius}, \ncolour: {self.colour}\
            \nprev_acc: {self.prev_acceleration}'

    # Calculates the returns the next position of body using the Beeman Algorithm.
    def calc_position(self, timestep):
        next_position = self.position + (self.velocity*timestep) + ((1.0/6.0)*(4*self.acceleration - self.prev_acceleration)*(timestep**2))
        return next_position

    # Updates body position to given argument.
    def update_position(self, next_position):
        self.position = next_position

    # Calculates the returns the next velocity of argument body using the Beeman Algorithm.
    # Also requires an argument for the next_accelaration of argument body.
    def calc_velocity(self, timestep, next_acceleration):
        next_velocity = self.velocity + ((1.0/6.0)*((2.0*next_acceleration) + (5.0*self.acceleration) - self.prev_acceleration))*timestep
        return next_velocity

    # Updates body velocity to given argument.
    def update_velocity(self, next_velocity):
        self.velocity = next_velocity

    # Updates the current and previous accelaration given the next accelaration.
    def update_accelerations(self, next_acceleration):
        self.prev_acceleration = self.acceleration
        self.acceleration = next_acceleration

    # Calculates and returns the total kinetic energy of the body.
    def kinetic_energy(self):
        ke = (1/2)*self.mass*(np.linalg.norm(self.velocity))**2
        return ke

    # Checks if body has completed and orbit.
    # If so, it adds the orbital period to a list and writes the average of all stored orbital periods to a file.
    def check_orbit(self, time):
        if self.prev_acceleration[1] > 0 and self.acceleration[1] <= 0:
            # 31536000 is the number of seconds in an earth year, thus dividing by it gives us periods in earth years.
            # We obtain this by 60 seconds * 60 minutes * 24 hours * 356 days 
            orbital_period = (time - self.prev_time)/31536000
            self.prev_time = time
            self.orbital_periods.append(orbital_period)
            avg_orbital_period = sum(self.orbital_periods)/len(self.orbital_periods)
            # Writing to file
            with open(self.name+'OrbitalPeriod.csv', 'w') as file:
                writer = csv.writer(file)
                writer.writerow([avg_orbital_period])
                # Printing orbital period to console if orbit was completed.
                print(f'Orbital Period of {self.name}: {avg_orbital_period}')
                
