import pygame
from sys import exit
from os import chdir, path

# Only do this if running as main process
if __name__ == "__main__":
    from screen import Screen
    from button import Button, IconButton
    from benchmark import Benchmark
    from user import User
    from mainUI import MainUI
    from facerecognitionScreen import Facerecognition

    # Change the working directory to the script's directory
    chdir(path.dirname(path.abspath(__file__)))

    #### Initialize Pygame and Benchmark
    pygame.init()
    Benchmark.init()

    class pygameScreen:
        screen = pygame.display.set_mode((800, 480))

    pygame.display.set_caption("FaceIgnition")
    appIcon = pygame.image.load('res/applogo.png')
    pygame.display.set_icon(appIcon)
    clock = pygame.time.Clock()
    Benchmark.CLOCK = clock

    User.loadUsers()
    MainUI.initUI()

    while True:
        Benchmark.frameStart()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                Facerecognition.stopThreads()
                User.saveUsers()  # Save users before quitting
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION:
                Button.onMouseMotion(event)
                IconButton.onMouseMotion(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    Benchmark.handleTabPress()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    Button.onMouseButtonDown(event)
                    IconButton.onMouseButtonDown(event)

        #### Updates
        Screen.updateCurrentScreen()

        #### Draw everything
        pygameScreen.screen.fill((40, 40, 40))
        Screen.drawCurrentScreen(pygameScreen.screen)

        #### Benchmark
        Benchmark.update()
        Benchmark.draw(pygameScreen.screen)

        #### Flip and tick
        pygame.display.flip()
        clock.tick(60)