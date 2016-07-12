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
