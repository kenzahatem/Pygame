# -*- coding: utf-8 -*-
"""
Created on Mon Mar  4 14:03:42 2024

@author: kenza_hatem
"""

import pygame
from math import cos, sin, pi, tan
from numpy import deg2rad
from random import randint

pygame.init()  # Initialise pygame

# Permet de gérer la vitesse du jeu
clock = pygame.time.Clock()
FPS = 60

# pygame.display Permet de nommer la fenetre, voir ses dimensions, parametres d'initialisation
pygame.display.set_caption("Drift")
HEIGHT = 920
WIDTH = 600
VELOCITY = 3
background_img = pygame.image.load("./fond.jpg")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

colors = [
    "#8FBCBB",
    "#88C0D0",
    "#81A1C1",
    "#5E81AC",
    "#BF616A",
    "#D08770",
    "#EBCB8B",
    "#A3BE8C",
    "#B48EAD",
]

taxi_img = pygame.image.load("./Taxi.png")
rock_img = pygame.image.load("./Rock_bery.png")


class Voiture(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__()
        self.image = taxi_img
        self.origin_image = self.image
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.angle = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def rotate(self, sens=1):
        self.angle = self.angle + 0.5 * sens
        self.image = pygame.transform.rotozoom(self.origin_image, self.angle, 1)
        self.rect = self.image.get_rect(center=self.rect.center)

    def move(self, direction):
        if direction == "right" and self.rect.x<300:
            self.rect.x += VELOCITY  # Bouge vers la droite

        elif direction == "left" and self.rect.x>-250:
            self.rect.x -= VELOCITY  # Bouge vers la gauche


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x=WIDTH // 3, y=0):
        super().__init__()
        self.x = x
        self.y = y

        self.image = rock_img
        self.origin_image = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.velocity = VELOCITY
        self.rect = self.image.get_rect(center=self.rect.center)

    def draw(self, angle):
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rect.x = self.rect.x + tan(deg2rad(angle)) * VELOCITY
        self.rect.y = self.rect.y + VELOCITY

        # permet de supprimer l'obstacle si l'on sort de l'écran
        if not screen.get_rect().contains(self.rect):
            self.remove()
            self.kill()
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    frame_count = 0
    running = True
    game_over = False  # Variable de statut de jeu
    score = 0  # Score initial
    taxi = Voiture(WIDTH // 2, HEIGHT // 2)
    Lobs = []


    obstacle_speed = 1  # Vitesse initiale des obstacles

    while running:
        frame_count += 1
        screen.blit(background_img, (0, 0))
        taxi.draw()

        if not game_over:  # Si le jeu n'est pas terminé
            # Création des obstacles
            if frame_count % 30 == 0:
                Lobs.append(Obstacle(x=randint(10, WIDTH - 10), y=0))
                score += 1

            # Gestion des événements clavier
            for event in pygame.event.get():
                # Gestion de la fermeture de la fenêtre
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    running = False
                elif event.type == pygame.KEYDOWN:
                    keypressed = event.key
                    if keypressed == pygame.K_SPACE:
                        print("space bar")
                        # proj = Projectile(player.x, player.y, player.angle)
                else:
                    keypressed = 0
            if keypressed == pygame.K_RIGHT:
                taxi.move("right")
            elif keypressed == pygame.K_LEFT:
                taxi.move("left")

            # Déplacement des obstacles
            for obs in Lobs:
                obs.draw(taxi.angle)
                obs.rect.y += obstacle_speed  # Déplacement vertical vers le bas

                # Vérification des collisions
                if obs.rect.collidepoint(taxi.rect.centerx, taxi.rect.centery):
                    game_over = True  # Le joueur a touché un obstacle, il perd
                    print("Game Over")

            # Augmentation de la vitesse après chaque 10 obstacles passés
            if score % 10 == 0 and score != 0:
                obstacle_speed += 0.05

        # Affichage du score en haut à droite de l'écran
        font_score = pygame.font.Font(None, 24)
        text_score = font_score.render("Score: " + str(score), True, (0, 0, 0))  # Couleur du texte : blanc
        text_score2 = text_score.get_rect(center=(WIDTH // 10, HEIGHT // 14))
        screen.blit(text_score, text_score2)

        # Affichage du message "Game Win" si le score dépasse 100
        if score >= 100:
            game_over = True  # Le joueur a atteint le score requis, il gagne
            print("Game Win")

        # Affichage du message "Game Over" si le jeu est terminé
        if game_over:
            # Affichage du message approprié sur l'écran
            font = pygame.font.Font(None, 36)
            if score >= 100:
                text = font.render("Game Win", True, (0, 255, 0))
            else:
                text = font.render("Game Over", True, (255, 0, 0))
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)

            # Quitter le jeu après quelques secondes
            running = False  # Arrêter le jeu

        pygame.display.flip()
        clock.tick(FPS)

    pygame.time.delay(2000)  # Attente de 2 secondes
    pygame.quit()