# 🌍 Planet Simulation

This Python project uses the pygame library to create a simple, yet visually interesting, simulation of a solar system, including the Sun and the four innermost planets: Mercury, Venus, Earth, and Mars.

## Requirements

The application requires `pygame`. Install it via pip:

```bash
pip install pygame
```

## Usage

Run the `main.py` script:

```bash
python main.py
```

## Overview

The application consists of three classes: `CelestialObject`, `Planet`, and `SolarSystem`. 

- `CelestialObject` is the base class representing any celestial object (like the Sun or planets) in the solar system, with properties such as name, radius, color, mass, position, and velocity.
- `Planet` is a subclass of `CelestialObject`, representing a planet orbiting around a parent star. It has additional properties, including the distance to the parent star and the path of its orbit.
- `SolarSystem` is a class that encapsulates a whole solar system, including a central star and multiple planets.

The simulation involves calculating gravitational forces and updating positions of celestial objects, and drawing orbits for planets.
