import pygame
import threading
from pathlib import Path

pygame.mixer.init()

sound = pygame.mixer.Sound(str(Path.cwd()) + r"\assets\sounds\beep.mp3")

# Fonction pour jouer le son dans un thread séparé
def beep():
    threading.Thread(target=sound.play, daemon=True).start()

