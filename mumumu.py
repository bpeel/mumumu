#!/usr/bin/python3

import subprocess
import shutil

ciferoj = [ '', 'unu', 'du', 'tri', 'kvar', 'kvin', 'ses',
            'sep', 'ok', 'naŭ' ]
dekoj = [ '', 'dek', 'cent', 'mil' ]

def nombro_al_teksto(nombro):
    partoj = []

    if nombro >= 10 ** len(dekoj) or nombro < 0:
        return str(nombro)
    
    for loko in range(len(dekoj) - 1, -1, -1):
        dividanto = 10 ** loko
        cifero = (nombro // dividanto) % 10
        if cifero > 0:
            if cifero > 1 or loko == 0:
                partoj.append(ciferoj[cifero] + dekoj[loko])
            else:
                partoj.append(dekoj[loko])

    if len(partoj) == 0:
        return "nulo"

    return " ".join(partoj)

def rulu(*argoj):
    return subprocess.check_call(argoj)

def mezuri_daŭron(sondosiero):
    return float(subprocess.check_output(["soxi", "-D", "--", sondosiero]))

def sonnombro_al_dosiero(sonnombro):
    return "sono-{:04d}.wav".format(sonnombro)

def muo_al_dosiero(muo):
    return "muo{}.wav".format(muo)

muoj = [ "mu?", "mu!" ]

for muo in range(len(muoj)):
    rulu("espeak", "-veo", "-w" + muo_al_dosiero(muo), "--", muoj[muo])

daŭroj_de_muoj = list(map(lambda x: mezuri_daŭron(muo_al_dosiero(muo)),
                          range(len(muoj))))

sonnombro = 0

for nombro in range(1, 100):
    rulu("espeak",
         "-veo",
         "-w" + sonnombro_al_dosiero(sonnombro),
         "--",
         nombro_al_teksto(nombro) + "bovinoj muĝas.")
    sonnombro += 1

    for muo in range(nombro):
        shutil.copyfile(muo_al_dosiero(muo % len(muoj)),
                        sonnombro_al_dosiero(sonnombro))
        sonnombro += 1

eligo = open("concat.txt", "w")
for nombro in range(sonnombro):
    eligo.write("file '" + sonnombro_al_dosiero(nombro) + "'\n")
eligo.close()

rulu("ffmpeg", "-f", "concat", "-i", "concat.txt",
     "-c:a", "libvorbis", "-aq", "4", "-y", "sono.ogg")
