#!/usr/bin/python3

import subprocess
from num2words import num2words

FINA_NOMBRO = 99

def sonnombro_al_dosiero(sonnombro):
    return "sono-{:04d}.wav".format(sonnombro)

def mezuri_daŭron(sondosiero):
    return float(subprocess.check_output(["soxi", "-D", "--", sondosiero]))

class Subtekstilo:
    def __init__(self, eligo):
        self.eligo = eligo
        self.sonnombro = 0
        self.nun = 0

    @staticmethod
    def formatigi_tempon(tempo):
        return "{:02d}:{:02d}:{:02d},{:03d}".format(
            int(tempo / 3600),
            int(tempo / 60) % 60,
            int(tempo) % 60,
            int(tempo * 1000) % 1000)

    def aldoni_tekston(self, teksto, daŭro):
        fino = self.nun + daŭro
        
        self.eligo.write("{}\n"
                         "{} --> {}\n"
                         "{}\n"
                         "\n".format(self.sonnombro + 1,
                                     Subtekstilo.formatigi_tempon(self.nun),
                                     Subtekstilo.formatigi_tempon(fino),
                                     teksto))

        self.sonnombro += 1
        self.nun += daŭro

nun = 0

eligo = open("mumumu-en.srt", "w")
subtekstilo = Subtekstilo(eligo)

for nombro in range(1, FINA_NOMBRO + 1):
    sondaŭro = mezuri_daŭron(sonnombro_al_dosiero(subtekstilo.sonnombro))

    if nombro == 1:
        teksto = "One cow moos."
    else:
        teksto = "{} cows moo.".format(num2words(nombro).capitalize())

    subtekstilo.aldoni_tekston(teksto, sondaŭro)
    
    for muo in range(nombro):
        sondaŭro = mezuri_daŭron(sonnombro_al_dosiero(subtekstilo.sonnombro))

        if muo & 1 == 0:
            teksto = "Moo."
        else:
            teksto = "Moo…"

        subtekstilo.aldoni_tekston(teksto, sondaŭro)
