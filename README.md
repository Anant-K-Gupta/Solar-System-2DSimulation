# 2D Solar System Simulation

This Python program simulates the motion of planets and satellites in a 2D solar system using the 3-step Beeman integration scheme to calculate the positions and velocities of celestial bodies based on gravitational forces.

## Simulation Details

The initial simulation focuses on the Sun and the inner planets: Venus, Mercury, Earth, and Mars. Experiments were conducted to test the accuracy and realism of the simulation.

## Files

- `SatelliteValues.csv`: Contains data for satellites (name, mass, position, angle, velocity, radius, color).
- `InnerPlanets.csv`: Contains data for planets (name, mass, position, velocity, radius, color).

## Accuracy and Realism

The simulation results match real-world data, with orbital periods closely aligning with actual figures. The total energy of the system remains conserved, showing small fluctuations around a mean.

The object-oriented design allows for easy extension, such as adding asteroid belts and more planets. A file (`InnerPlanets.csv`) is included for simulating all eight planets.

## Satellite Launch

A satellite launch feature towards Mars is included, with the satellite reaching approximately 170,000 kilometers from Mars' center. Fine-tuning launch velocities and angles, along with mid-flight corrections, can further improve the distance.

## Integration Scheme

The 3-step Beeman integration scheme, a predictor-corrector method, is used for accurate and efficient calculation of celestial body movements.

## Rendering

By default, celestial objects are rendered using images. Uncomment lines labeled `'CIRCLE PLOTTING'` in the `animation` method to use circles instead.

## Conclusion

This 2D Solar System Simulation provides a realistic representation of celestial body motion, conserving energy and incorporating gravitational forces. Its extensible design allows for further customization and additions.
