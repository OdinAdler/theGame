# Imports
import os
import pygame, random, time, sys
from pygame.locals import *

# Schachtel für alles mit Zeiten
class Zeiten:
    def __init__(self):
        self.night = 6
        self.fredbear = 0
        self.springbonnie = 0
        self.spieldauer = 300
        self.startzeit = None

    def zeit(self):
        if self.night == 1:
            self.fredbear = random.randint(100, 150)
            self.springbonnie = random.randint(100, 150)        
        if self.night == 2:
            self.fredbear = random.randint(80, 120)
            self.springbonnie = random.randint(80, 120)    
        if self.night == 3:
            self.fredbear = random.randint(50, 100)
            self.springbonnie = random.randint(50, 100)          
        if self.night == 4:
            self.fredbear = random.randint(40, 70)
            self.springbonnie = random.randint(40, 70)          
        if self.night == 5:
            self.fredbear = random.randint(20, 40)
            self.springbonnie = random.randint(20, 40)
        if self.night == 6:
            self.fredbear = random.randint(10, 20)
            self.springbonnie = random.randint(10, 20)

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
        self.shiftcomplete = pygame.image.load(os.path.join('assets','shift_complete.png'))

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
        self.zeige_endfenster = False
        self.zeige_fred = False
        self.zeige_spring = False
        self.linketuer = False
        self.rechtetuer = False

    def bei_event(self, event, zeiten):
        if event.type == pygame.QUIT:
            self.programmlaeuft = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                self.zeige_startfenster = False
                self.zeige_spielfenster = True
                self.zeige_fred = False
                self.zeige_spring = False
                zeiten.startzeit = time.time()
                self.spiellaeuft = True

            if event.key == pygame.K_q:
                self.linketuer = True     
                    
            if event.key == pygame.K_e:
                self.rechtetuer = True     

    def auswerten(self, spiel, zeiten):
        jetzt = time.time()
        if self.spiellaeuft == True:
            vergangezeit = jetzt - zeiten.startzeit
            if vergangezeit > zeiten.spieldauer:
                self.zeige_startfenster = False
                self.zeige_spielfenster = False
                self.zeige_endfenster = True
                self.zeige_fred = False
                self.zeige_spring = False

            if jetzt - zeiten.startzeit > zeiten.fredbear:
                self.zeige_startfenster = False
                self.zeige_spielfenster = True
                self.zeige_endfenster = False
                self.zeige_fred = True
                if self.linketuer == True:
                    self.zeige_fred = False

            if jetzt - zeiten.startzeit > zeiten.springbonnie:
                self.zeige_startfenster = False
                self.zeige_spielfenster = True
                self.zeige_endfenster = False
                self.zeige_spring = True
                if self.rechtetuer == True:
                    self.zeige_spring = False


    def zeichne_fenster(self, fenster):
        fenster.screen.fill((0,0,0))

        if self.zeige_startfenster == True:
            fenster.screen.blit(fenster.startbild, (0,0))

        if self.zeige_spielfenster == True:
            fenster.screen.blit(fenster.hintergrund, (0,0))

        if self.zeige_endfenster == True:
            fenster.screen.blit(fenster.shiftcomplete, (0,0))

        if self.zeige_fred == True:
            fenster.screen.blit(fenster.fred, (100,150))

        if self.zeige_spring == True:
            fenster.screen.blit(fenster.spring, (800, 150))

        pygame.display.flip
        pygame.display.update()

    def am_ende_aufraeumen(self):
        pygame.quit()


# Hauptprogramm
def main():
    pygame.init()

    # Alle Schachteln nehmen und befuellen
    zeiten = Zeiten()
    zeiten.zeit()
    
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