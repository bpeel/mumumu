#!/usr/bin/python3

import subprocess
import shutil
import cairo

BILDO_LARĜO = 1920
BILDO_ALTO = 1080
BILDFREKVENCO = 30
FINA_NOMBRO = 99

ciferoj = [ '', 'unu', 'du', 'tri', 'kvar', 'kvin', 'ses',
            'sep', 'ok', 'naŭ' ]
dekoj = [ '', 'dek', 'cent', 'mil' ]

def krei_skalskemon(surfaco, larĝo, alto):
    surfaclarĝo = surfaco.get_width()
    surfacalto = surfaco.get_height()
    skemo = cairo.SurfacePattern(surfaco)
    matrico = cairo.Matrix()
    matrico.scale(surfaclarĝo / larĝo, surfacalto / alto)
    skemo.set_matrix(matrico)
    return skemo

def krei_fonskemon():
    fono = cairo.ImageSurface.create_from_png("fono.png")
    return krei_skalskemon(fono, BILDO_LARĜO, BILDO_ALTO)

fonskemo = krei_fonskemon()

def krei_bovinsurfacon():
    el_surfaco = cairo.ImageSurface.create_from_png("bovino.png")
    alto = BILDO_ALTO // 8
    larĝo = (alto * el_surfaco.get_width() //
             el_surfaco.get_height())
    skemo = krei_skalskemon(el_surfaco, larĝo, alto)
    al_surfaco = cairo.ImageSurface(cairo.FORMAT_ARGB32, larĝo, alto)
    cr = cairo.Context(al_surfaco)
    cr.set_source(skemo)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

    return al_surfaco

bovinsurfaco = krei_bovinsurfacon()

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

def nombro_al_frazo(nombro):
    if nombro == 1:
        alia_parto = "bovino"
    else:
        alia_parto = "bovinoj"

    return nombro_al_teksto(nombro) + " " + alia_parto + " muĝas."

def rulu(*argoj):
    return subprocess.check_call(argoj)

def mezuri_daŭron(sondosiero):
    return float(subprocess.check_output(["soxi", "-D", "--", sondosiero]))

def sonnombro_al_dosiero(sonnombro):
    return "sono-{:04d}.wav".format(sonnombro)

def muo_al_dosiero(muo):
    return "muo{}.wav".format(muo)

def krei_bildon_por_nombro(nombro, muoj):
    surfaco = cairo.ImageSurface(cairo.FORMAT_ARGB32,
                                 BILDO_LARĜO,
                                 BILDO_ALTO)
    cr = cairo.Context(surfaco)
    cr.save()
    cr.set_source(fonskemo)
    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()
    cr.restore()

    frazo = nombro_al_frazo(nombro)

    cr.set_font_size(BILDO_ALTO / 10)

    dimensioj = cr.font_extents()
    alto_de_tiparo = dimensioj[2]

    cr.save()
    cr.move_to(BILDO_LARĜO / 100, alto_de_tiparo)
    cr.set_source_rgb(1.0, 1.0, 1.0)
    cr.set_line_width(8)
    cr.text_path(frazo)
    cr.stroke_preserve()
    pat = cairo.LinearGradient(0, 0, 0, alto_de_tiparo)
    pat.add_color_stop_rgb(0, 0, 198 / 255, 0)
    pat.add_color_stop_rgb(1, 0, 76 / 255, 0)
    cr.set_source(pat)
    cr.fill()
    cr.restore()

    bovino_larĝo = bovinsurfaco.get_width()
    bovino_alto = bovinsurfaco.get_height()

    x = 0
    y = alto_de_tiparo * 1.2
    for muo in range(muoj):
        cr.set_source_surface(bovinsurfaco, x, y)
        cr.paint()
        
        x += bovino_larĝo
        if x + bovino_larĝo > BILDO_LARĜO:
            x = 0
            y += bovino_alto

    surfaco.write_to_png("bildo.png")

class BildRipetilo:
    def __init__(self):
        self.sonhoro = 0
        self.bildhoro = 0

    def ripeti(self, alff, sontempo):
        bildoj = int(((self.sonhoro + sontempo) - self.bildhoro) *
                     BILDFREKVENCO)
        self.bildhoro += bildoj / BILDFREKVENCO
        self.sonhoro += sontempo

        buf = subprocess.check_output(["convert", "bildo.png", "rgb:-"])
        for i in range(bildoj):
            alff.stdin.write(buf)

muoj = [ "mu?", "mu!" ]

for muo in range(len(muoj)):
    rulu("espeak", "-veo", "-w" + muo_al_dosiero(muo), "--", muoj[muo])

daŭroj_de_muoj = list(map(lambda x: mezuri_daŭron(muo_al_dosiero(x)),
                          range(len(muoj))))
daŭroj_de_frazoj = []

sonnombro = 0

for nombro in range(1, FINA_NOMBRO + 1):
    sondosiero = sonnombro_al_dosiero(sonnombro)

    rulu("espeak",
         "-veo",
         "-w" + sondosiero,
         "--",
         nombro_al_frazo(nombro))
    
    daŭroj_de_frazoj.append(mezuri_daŭron(sondosiero))

    sonnombro += 1

    for muo in range(nombro):
        shutil.copyfile(muo_al_dosiero(muo % len(muoj)),
                        sonnombro_al_dosiero(sonnombro))
        sonnombro += 1

eligo = open("concat.txt", "w")
for nombro in range(sonnombro):
    eligo.write("file '" + sonnombro_al_dosiero(nombro) + "'\n")
eligo.close()

argoj = [ "ffmpeg",
          "-f", "rawvideo",
          "-pixel_format", "rgb24",
          "-video_size", "{}x{}".format(BILDO_LARĜO, BILDO_ALTO),
          "-framerate", str(BILDFREKVENCO),
          "-i", "-",
          "-f", "concat", "-i", "concat.txt",
          "-c:v", "libvpx",
          "-b:v", "3M",
          "-c:a", "libvorbis", "-aq", "4",
          "-y",
          "mumumu.webm" ]

alff = subprocess.Popen(argoj, stdin = subprocess.PIPE)

ripetilo = BildRipetilo()

for nombro in range(1, FINA_NOMBRO + 1):
    sondosiero = sonnombro_al_dosiero(sonnombro)

    krei_bildon_por_nombro(nombro, 0)

    ripetilo.ripeti(alff, daŭroj_de_frazoj[nombro - 1])
    
    for muo in range(nombro):
        krei_bildon_por_nombro(nombro, muo + 1)

        ripetilo.ripeti(alff, daŭroj_de_muoj[muo % len(muoj)])
        
alff.stdin.close()

if alff.wait() != 0:
    raise Exception("ffmpeg malsukcesis")
