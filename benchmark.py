import pygame
from screen import Screen

class Benchmark:
    SMALL_FONT = None
    FRAME_START = 0
    FRAME_TIME_MS = 0
    FPS = 0
    CLOCK = None
    SHOW_STATS = False
    SCREEN_NAME = ""

    @staticmethod
    def init():
        # Initialize the font for displaying FPS
        Benchmark.SMALL_FONT = pygame.font.SysFont("Arial", 20)

    @staticmethod
    def frameStart():
        Benchmark.FRAME_START = pygame.time.get_ticks()

    @staticmethod
    def update():
        # Calculate FPS and frame time
        Benchmark.FRAME_TIME_MS = pygame.time.get_ticks() - Benchmark.FRAME_START
        Benchmark.FPS = Benchmark.CLOCK.get_fps()
        Benchmark.SCREEN_NAME = Screen.currentScreen.name if Screen.currentScreen else "Unknown"

    @staticmethod
    def draw(screen):
        if not Benchmark.SHOW_STATS:
            return
        # Render performance info
        info_text = f"FPS: {Benchmark.FPS:.1f}  Frame: {Benchmark.FRAME_TIME_MS} ms  Screen: {Benchmark.SCREEN_NAME}"
        info_surface = Benchmark.SMALL_FONT.render(info_text, True, (200, 200, 200))
        screen.blit(info_surface, (5, 5))

    @staticmethod
    def handleTabPress():
        # Toggle the visibility of performance stats
        Benchmark.SHOW_STATS = not Benchmark.SHOW_STATS