from __future__ import annotations

import pygame
from sim.physics import RocketSimulation


class RocketRenderer:
    def __init__(self, width: int = 1280, height: int = 720):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Educational Rocket Flight Visualization")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 22)

    def draw(self, sim: RocketSimulation) -> None:
        self.screen.fill((10, 10, 25))
        ground_y = self.height - 80

        pygame.draw.line(self.screen, (100, 100, 100), (0, ground_y), (self.width, ground_y), 3)

        rocket_x = self.width // 2
        altitude_px = min(int(sim.altitude_m * 2.0), ground_y - 120)
        rocket_y = ground_y - altitude_px

        # Body
        pygame.draw.rect(self.screen, (220, 220, 240), (rocket_x - 10, rocket_y - 60, 20, 60))
        # Nose cone
        pygame.draw.polygon(
            self.screen,
            (240, 80, 80),
            [(rocket_x - 10, rocket_y - 60), (rocket_x + 10, rocket_y - 60), (rocket_x, rocket_y - 90)],
        )
        # Fins
        pygame.draw.polygon(
            self.screen,
            (80, 140, 255),
            [(rocket_x - 10, rocket_y - 5), (rocket_x - 35, rocket_y + 15), (rocket_x - 10, rocket_y + 15)],
        )
        pygame.draw.polygon(
            self.screen,
            (80, 140, 255),
            [(rocket_x + 10, rocket_y - 5), (rocket_x + 35, rocket_y + 15), (rocket_x + 10, rocket_y + 15)],
        )

        # Flame if thrusting
        if sim.thrust_at_time(sim.t) > 0:
            pygame.draw.polygon(
                self.screen,
                (255, 165, 0),
                [(rocket_x - 8, rocket_y + 5), (rocket_x + 8, rocket_y + 5), (rocket_x, rocket_y + 35)],
            )

        text = self.font.render(
            f"t={sim.t:.1f}s  alt={sim.altitude_m:.1f}m  vel={sim.velocity_mps:.1f}m/s",
            True,
            (240, 240, 240),
        )
        self.screen.blit(text, (30, 20))
        pygame.display.flip()
        self.clock.tick(60)

    def close(self) -> None:
        pygame.quit()
