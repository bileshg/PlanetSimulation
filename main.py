from enum import Enum

import pygame
import math

# Calculation related constants
AU = 149.6e9  # 1 AU (1 Astronomical Unit) = 149.6 million km = 149.6 billion m = 149.6e9 m
G = 6.67428e-11  # Gravitational constant

# UI related constants
WIDTH, HEIGHT = 400, 400
SCALE = 120 / AU  # 1AU = 200 pixels
TIME_STEP = 60 * 60 * 24  # 1 day


class Color(Enum):
    DEFAULT = (255, 255, 255)
    SPACE = (0, 0, 0)
    SUN = (255, 255, 0)
    MERCURY = (80, 78, 81)
    VENUS = (255, 192, 0)
    EARTH = (100, 149, 237)
    MARS = (188, 39, 50)


class CelestialObject:

    def __init__(self,
                 name,
                 radius,
                 color,
                 mass,
                 position=(0, 0),
                 velocity=(0, 0)):
        self.name = name
        self.radius = radius
        self.color = color
        self.mass = mass

        self.x, self.y = position
        self.x_vel, self.y_vel = velocity

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def set_velocity(self, x_vel, y_vel):
        self.x_vel = x_vel
        self.y_vel = y_vel

    def get_position(self):
        return self.x, self.y

    def calculate_distance_vectors(self, other_body):
        other_x, other_y = other_body.get_position()
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        return distance_x, distance_y

    def calculate_force_vectors(self, other_body):
        distance_x, distance_y = self.calculate_distance_vectors(other_body)
        distance = math.dist(self.get_position(), other_body.get_position())

        force = G * self.mass * other_body.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force

        return force_x, force_y

    def update_position(self, bodies):
        total_fx = total_fy = 0
        for body in bodies:
            if self == body:
                continue

            fx, fy = self.calculate_force_vectors(body)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * TIME_STEP
        self.y_vel += total_fy / self.mass * TIME_STEP

        self.x += self.x_vel * TIME_STEP
        self.y += self.y_vel * TIME_STEP

    def draw(self, window, font):
        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        pygame.draw.circle(window, self.color.value, (x, y), self.radius)
        body_name = font.render(self.name, True, Color.DEFAULT.value)
        window.blit(body_name, (x, y + self.radius))


class Planet(CelestialObject):

    def __init__(self,
                 name,
                 parent_star,
                 radius,
                 color,
                 mass,
                 position=(0, 0),
                 velocity=(0, 0)):
        super().__init__(name, radius, color, mass, position, velocity)

        self.orbit = []
        self.parent_star = parent_star
        self.distance_to_parent = math.dist(self.get_position(),
                                            parent_star.get_position())

    def draw(self, window, font):
        # Draw Orbit
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * SCALE + WIDTH / 2
                y = y * SCALE + HEIGHT / 2
                updated_points.append((x, y))
            pygame.draw.lines(window, self.color.value, False, updated_points,
                              1)

        x = self.x * SCALE + WIDTH / 2
        y = self.y * SCALE + HEIGHT / 2

        # Draw Planet
        pygame.draw.circle(window, self.color.value, (x, y), self.radius)

        # Display Name and Distance
        planet_name = font.render(self.name, True, Color.DEFAULT.value)
        distance_text = font.render(
            f"{round(self.distance_to_parent / 1000)} km", True,
            Color.DEFAULT.value)
        window.blit(planet_name, (x, y + self.radius))
        window.blit(distance_text, (x, y + self.radius + 10))

    def update_position(self, bodies):
        super().update_position(bodies)
        self.distance_to_parent = math.dist(self.get_position(),
                                            self.parent_star.get_position())
        self.orbit.append((self.x, self.y))

        tail_length = int(self.distance_to_parent * SCALE)

        if len(self.orbit) > tail_length:
            self.orbit = self.orbit[-tail_length:]


class SolarSystem:

    def __init__(self, name, star, planets):
        self.name = name
        self.star = star
        self.planets = planets

    def update_positions(self):
        self.star.update_position(self.planets)

        bodies = [self.star] + self.planets
        for planet in self.planets:
            planet.update_position(bodies)

    def draw(self, window, font):
        solar_system_name = font.render(self.name, True, Color.DEFAULT.value)
        window.blit(solar_system_name, (0, 0))

        self.star.draw(window, font)
        for planet in self.planets:
            planet.draw(window, font)


def create_solar_system():
    sun = CelestialObject("Sun", 16, Color.SUN, 1.98892 * 10**30)
    sun.set_position(0, 0)

    mercury = Planet("Mercury", sun, 4, Color.MERCURY, 3.30 * 10**23)
    mercury.set_position(0.387 * AU, 0)
    mercury.set_velocity(0, 47400)

    venus = Planet("Venus", sun, 5, Color.VENUS, 4.8685 * 10**24)
    venus.set_position(-0.723 * AU, 0)
    venus.set_velocity(0, -35020)

    earth = Planet("Earth", sun, 5, Color.EARTH, 5.9742 * 10**24)
    earth.set_position(1 * AU, 0)
    earth.set_velocity(0, 29783)

    mars = Planet("Mars", sun, 4, Color.MARS, 6.39 * 10**23)
    mars.set_position(-1.524 * AU, 0)
    mars.set_velocity(0, -24077)

    planets = [mercury, venus, earth, mars]

    return SolarSystem("The Solar System", sun, planets)


def run_simulation(window, clock, font):
    solar_system = create_solar_system()

    run = True
    while run:
        clock.tick(60)
        window.fill(Color.SPACE.value)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        solar_system.update_positions()
        solar_system.draw(window, font)

        pygame.display.update()

    pygame.quit()


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(pygame.font.get_fonts()[0], 10)
    pygame.display.set_caption("Planet Simulation")
    run_simulation(win, clock, font)


if __name__ == '__main__':
    main()
