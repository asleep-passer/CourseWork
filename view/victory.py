import pygame
import random
import math

class VictoryEffect:
    """
    A particle effect system that displays colorful exploding particles
    to celebrate level victory or success events.
    """
    def __init__(self, screen, x, y):
        """
        Initialize the victory explosion effect with particles.

        Args:
            screen: The Pygame surface to draw particles on
            x: The X coordinate of the explosion center
            y: The Y coordinate of the explosion center
        """
        self.screen = screen
        self.particles = []
        self.timer = 0
        self.duration = 60
        self.finished = False

        colors = [
            (255, 215, 0), (255, 100, 100), (100, 255, 100),
            (100, 150, 255), (255, 200, 50), (255, 80, 200)
        ]

        for _ in range(120):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 8)
            life = random.randint(30, 60)
            color = random.choice(colors)
            self.particles.append({
                "x": x,
                "y": y,
                "vx": math.cos(angle) * speed,
                "vy": math.sin(angle) * speed,
                "life": life,
                "max_life": life,
                "color": color,
                "size": random.randint(3, 7)
            })

    def update(self):
        """
        Update particle positions, physics (gravity), lifetime, and effect timer.
        Marks the effect as finished when duration ends.
        """
        if self.finished:
            return
        self.timer += 1
        for p in self.particles:
            p["x"] += p["vx"]
            p["y"] += p["vy"]
            p["vy"] += 0.1
            p["life"] -= 1
        if self.timer >= self.duration:
            self.finished = True

    def draw(self):
        """
        Render all active particles with fade-out and shrink effects.
        Only draws particles that are still alive.
        """
        if self.finished:
            return
        for p in self.particles:
            if p["life"] > 0:
                alpha = int(255 * (p["life"] / p["max_life"]))
                size = max(1, int(p["size"] * (p["life"] / p["max_life"])))
                pg_color = (*p["color"], alpha)
                surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(surf, pg_color, (size, size), size)
                self.screen.blit(surf, (int(p["x"] - size), int(p["y"] - size)))