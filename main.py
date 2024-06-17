from System import System
import tkinter
from tkinter import messagebox
from tkinter import simpledialog
import csv

with open('TotalEnergy.csv', 'w') as file:
    file.truncate()
simulation = System('InnerPlanets.csv', 100000, 730)

root = tkinter.Tk()
root.withdraw()
messagebox.showinfo("Welcome", "Hi! This is Anant's Solar System Simulation. \nPress ok to continue.")
planets_wanted = messagebox.askquestion("Planets", "Would you like to simulate only the inner planets?\n(Simulating all planets leads to very small graphics)")
if planets_wanted=='yes':
    simulation = System('InnerPlanets.csv', 100000)
else:
    simulation = System('AllPlanets.csv', 100000)
sat_wanted = messagebox.askquestion("Satellite", "Would you like to add a satellite to the simulation?")
if sat_wanted=='yes':
    sat_file = open('SatelliteValues.csv', 'w', newline='')
    speed = simpledialog.askstring('Speed', 'At what speed do you want to launch (in m/s)?\n(suggested range 25000-45000)')
    angle = simpledialog.askstring('Angle', 'At what angle do you want to launch (in degrees)?\n(suggested range 30-60)')
    writer = csv.writer(sat_file)
    writer.writerow(['Satellite', 1000, 1.501E+11, angle, speed, 5000, 0.0, 0.6, 0.6])
    sat_file.close()
    simulation.add_satellite('SatelliteValues.csv')


simulation.display()

graphs_wanted = messagebox.askquestion("Graphs", "Would you like to see some energy graphs for the simulation?")
if graphs_wanted=='yes':
    simulation.plot_energy_variation('TotalEnergy.csv')
    simulation.plot_energy('TotalEnergy.csv')

messagebox.showinfo("Bye", "That's all folks!")
