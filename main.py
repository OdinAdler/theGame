# Imports
import os
import pygame, random, time, sys
from pygame.locals import *

# Schachtel für alles mit Zeiten
class Zeiten:
    def __init__(self):
        self.night = 5
        self.fredbear = 0
        self.springbonnie = 0
        self.spieldauer = 20
        self.startzeit = None
        self.startfred = None
        self.endefred = None
        self.startspring = None
        self.endespring = None

    def fredzeit(self):
        self.fredbear = random.randint(3, 10)

    def springzeit(self):
        self.springbonnie = random.randint(3, 10)

    def zeitbistot(self):
        if self.night == 1:
            self.zeitbistot = 5    
        if self.night == 2:
            self.zeitbistot = 4
        if self.night == 3:
            self.zeitbistot = 3    
        if self.night == 4:
            self.zeitbistot = 2    
        if self.night == 5:
            self.zeitbistot = 1

# Schachtel für alles mit Musik
class Musik:

    def __init__(self):
        pass

    def ladeMusik(self):
        self.jumpscare = pygame.mixer.Sound(os.path.join('assets','jumpscare_sound-39630.mp3'))
        self.phone1 = pygame.mixer.Sound(os.path.join('assets','Phonecall.mp3'))
        self.phone2 = pygame.mixer.Sound(os.path.join('assets','Phonecall2.mp3'))
        self.phone3 = pygame.mixer.Sound(os.path.join('assets','Phonecall3.mp3'))
        self.phonedead = pygame.mixer.Sound(os.path.join('assets','Phonecall4.mp3'))
        self.end_sound = pygame.mixer.Sound(os.path.join('assets','shift_complete.mp3'))


# Schachtel für alles mit Fenster
class Fenster:

    def __init__(self):
        W1, H1 = 1031, 450
        self.screen = pygame.display.set_mode((W1, H1))
        pygame.display.set_caption("Five Nights at Fredbears")

    def ladeHintergrund(self):
        self.startbild = pygame.image.load(os.path.join('assets','startbild.png')).convert()
        self.hintergrund = pygame.image.load(os.path.join('assets','Background.png')).convert()
        self.easteregg = pygame.image.load(os.path.join('assets','easteregg.png')).convert()
        self.gewonnen = pygame.image.load(os.path.join('assets','shift_complete.png')).convert()
        self.verloren = pygame.image.load(os.path.join('assets','Springbonnie Jumpscare.png')).convert()

    def ladeBilder(self):
        self.spring = pygame.image.load(os.path.join('assets','neu.png')).convert()
        self.fred = pygame.image.load(os.path.join('assets','Fredbear neu.png')).convert()


# Schachtel für alles mit Spiel
class Spiel:

    def __init__(self):
        self.programmlaeuft = True
        self.zeige_startfenster = True
        self.spiellaeuft = False
        self.zeige_spielfenster = False
        self.zeige_endgewonnen = False
        self.zeige_endverloren = False
        self.zeige_fred = False
        self.zeige_spring = False
        self.verloren = False

    def bei_event(self, event, zeiten):
        if event.type == pygame.QUIT:
            self.programmlaeuft = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                jetzt = time.time()
                self.zeige_startfenster = False
                self.zeige_spielfenster = True
                self.zeige_fred = False
                self.zeige_spring = False
                self.zeige_endgewonnen = False
                self.zeige_endverloren = False
                zeiten.startzeit = jetzt
                zeiten.endefred = jetzt
                zeiten.endespring = jetzt
                self.spiellaeuft = True

            if event.key == pygame.K_q:
                zeiten.endefred = time.time()
                zeiten.fredzeit()
                self.zeige_fred = False
                    
            if event.key == pygame.K_e:
                zeiten.endespring = time.time()
                zeiten.springzeit()
                self.zeige_spring = False

    def auswerten(self, spiel, zeiten):
        jetzt = time.time()
        if self.spiellaeuft == True:
            # spieldauer checken
            vergangezeit = jetzt - zeiten.startzeit
            if vergangezeit > zeiten.spieldauer:
                self.zeige_startfenster = False
                self.zeige_spielfenster = False
                self.zeige_fred = False
                self.zeige_spring = False

                if self.verloren == True:
                    self.zeige_endverloren = True
                    self.zeige_endgewonnen = False
                else:
                    if zeiten.night > 5:
                        zeiten.night = zeiten.night + 1
                    else:
                        self.spiellaeuft = False
                        self.zeige_endverloren = False
                        self.zeige_endgewonnen = True


            # checken ob fred erscheint
            if jetzt - zeiten.endefred > zeiten.fredbear:
                self.zeige_startfenster = False
                self.zeige_spielfenster = True
                self.zeige_endgewonnen = False
                self.zeige_endverloren = False
                if self.zeige_fred == False:
                    self.zeige_fred = True
                    zeiten.startfred = time.time()

            #checken ob verloren
            if self.zeige_fred:
                if jetzt - zeiten.startfred > zeiten.zeitbistot:
                    self.spiellaeuft = False
                    self.verloren = True
                    self.zeige_endgewonnen = False
                    self.zeige_endverloren = True
                    self.zeige_startfenster = False
                    self.zeige_spielfenster = False
                    self.zeige_fred = False
                    self.zeige_spring = False

            # checken ob spring erscheint
            if jetzt - zeiten.endespring >=  + zeiten.springbonnie:
                self.zeige_startfenster = False
                self.zeige_spielfenster = True
                self.zeige_endgewonnen = False
                self.zeige_endverloren = False
                if self.zeige_spring == False:
                    self.zeige_spring = True
                    zeiten.startspring = time.time()

            #checken ob verloren
            if self.zeige_spring:
                if jetzt - zeiten.startspring > zeiten.zeitbistot:
                    self.spiellaeuft = False
                    self.verloren = True
                    self.zeige_endgewonnen = False
                    self.zeige_endverloren = True
                    self.zeige_startfenster = False
                    self.zeige_spielfenster = False
                    self.zeige_fred = False
                    self.zeige_spring = False

    def zeichne_fenster(self, fenster):
        fenster.screen.fill((0,0,0))

        if self.zeige_startfenster == True:
            fenster.screen.blit(fenster.startbild, (0,0))

        if self.zeige_spielfenster == True:
            fenster.screen.blit(fenster.hintergrund, (0,0))

        if self.zeige_endgewonnen == True:
            fenster.screen.blit(fenster.gewonnen, (0,0))

        if self.zeige_fred == True:
            fenster.screen.blit(fenster.fred, (100,150))

        if self.zeige_spring == True:
            fenster.screen.blit(fenster.spring, (800, 150))

        if self.zeige_endverloren == True:
            fenster.screen.blit(fenster.verloren, (0,0))

        pygame.display.flip
        pygame.display.update()

    def am_ende_aufraeumen(self):
        pygame.quit()


# Hauptprogramm
def main():
    pygame.init()

    # Alle Schachteln nehmen und befuellen
    zeiten = Zeiten()
    zeiten.zeitbistot()
    zeiten.fredzeit()
    zeiten.springzeit()
    
    musik = Musik()
    musik.ladeMusik()

    fenster = Fenster()
    fenster.ladeHintergrund()
    fenster.ladeBilder()

    spiel = Spiel()

    # Mainloop des Spiels
    while spiel.programmlaeuft == True:
        for event in pygame.event.get():
            spiel.bei_event(event, zeiten)

        spiel.auswerten(spiel, zeiten)

        spiel.zeichne_fenster(fenster)

    # Aufraeumen nach Ende vom Mainloop
    spiel.am_ende_aufraeumen()  


# Ruft das Hauptprogramm auf
if __name__ == "__main__" :
    main()