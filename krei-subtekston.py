#!/usr/bin/python3

import subprocess
from num2words import num2words
from nombroteksto import nombro_al_teksto

FINA_NOMBRO = 99

lingvoj = { 'en' : ('{} cow moos.', '{} cows moo.', 'Moo'),
            'eo' : ('{} bovino muĝas.', '{} bovinoj muĝas.', 'Mu',
                    nombro_al_teksto),
            'fr' : ('Une vache mugit.', '{} vaches mugissent.', 'Meuh') }

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

def krei_subtekston_por_lingvo(lingvo):
    eligo = open("mumumu-{}.srt".format(lingvo), "w")
    
    subtekstilo = Subtekstilo(eligo)

    argoj = lingvoj[lingvo]
    (frazo_1, frazo_n, musono) = argoj[0:3]

    if len(argoj) > 3:
        nombro_funkcio = argoj[3]
    else:
        nombro_funkcio = None

    for nombro in range(1, FINA_NOMBRO + 1):
        sondaŭro = mezuri_daŭron(sonnombro_al_dosiero(subtekstilo.sonnombro))

        if nombro == 1:
            formato = frazo_1
        else:
            formato = frazo_n

        if nombro_funkcio:
            nombro_ĉeno = nombro_funkcio(nombro)
        else:
            nombro_ĉeno = num2words(nombro, lang=lingvo)

        teksto = formato.format(nombro_ĉeno.capitalize())

        subtekstilo.aldoni_tekston(teksto, sondaŭro)

        for muo in range(nombro):
            dosiero = sonnombro_al_dosiero(subtekstilo.sonnombro)
            sondaŭro = mezuri_daŭron(dosiero)

            teksto = musono

            if muo & 1 == 0:
                teksto += "."
            else:
                teksto += "…"

            subtekstilo.aldoni_tekston(teksto, sondaŭro)

for lingvo in lingvoj.keys():
    krei_subtekston_por_lingvo(lingvo)
