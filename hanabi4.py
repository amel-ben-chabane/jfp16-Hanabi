import sys

def out(s):
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

temps = 0
moi = n = k = mode = 0
mains = {}
sait_valeur = {}
sait_couleur = {}
vies = 3
jetons = 8
hauteurs = []

for ligne in sys.stdin:
    ligne = ligne.strip()
    if not ligne:
        continue

    parties = ligne.split()
    cmd = parties[0]

    if cmd == "p":
        k = int(parties[1])
        n = int(parties[2])
        moi = int(parties[3])
        mode = int(parties[4])
        temps = 0

        mains = {j: ["??"] * k for j in range(1, n + 1)}
        sait_valeur = {j: ["?"] * k for j in range(1, n + 1)}
        sait_couleur = {j: ["?"] * k for j in range(1, n + 1)}
        hauteurs = [0] * k

    elif cmd == "n":
        joueur = int(parties[1])
        pos = int(parties[2]) - 1
        v = parties[3]
        c = parties[4]

        mains[joueur][pos] = v + c
        sait_valeur[joueur][pos] = "?"
        sait_couleur[joueur][pos] = "?"

    elif cmd == "j":
        vies = int(parties[1])
        jetons = int(parties[2])
        hauteurs = list(map(int, parties[3:]))

    elif cmd == "i":
        joueur = int(parties[1])
        v = parties[2]
        bits = parties[3:]
        for p in range(k):
            if bits[p] == "1":
                sait_valeur[joueur][p] = v

    elif cmd == "I":
        joueur = int(parties[1])
        c = parties[2]
        bits = parties[3:]
        for p in range(k):
            if bits[p] == "1":
                sait_couleur[joueur][p] = c

    elif cmd == "m":
        for joueur in range(1, n + 1):
            if joueur != moi:
                out(str(joueur) + " m " + " ".join(mains[joueur]))

    elif cmd == "r":
        for joueur in range(1, n + 1):
            cartes = []
            for p in range(k):
                cartes.append(sait_valeur[joueur][p] + sait_couleur[joueur][p])
            out(str(joueur) + " r " + " ".join(cartes))

    elif cmd == "t":
        joueur_tour = int(parties[1])

        if joueur_tour == moi:
            # MODE 4

            action_faite = False

            # regle 1 : si moi j'ai une carte complete et empilable, je la joue
            for p in range(k):
                v = sait_valeur[moi][p]
                c = sait_couleur[moi][p]

                if v != "?" and c != "?":
                    valeur = int(v)
                    couleur_index = ord(c) - ord("A")

                    if hauteurs[couleur_index] == valeur - 1:
                        out(f"e {p + 1}")
                        action_faite = True
                        break

            # regle 2 : donner une info a un autre joueur sur une carte empilable
            if not action_faite and jetons > 0:
                for joueur in range(1, n + 1):
                    if joueur == moi:
                        continue

                    for p in range(k):
                        carte = mains[joueur][p]
                        v = carte[0]
                        c = carte[1]

                        valeur = int(v)
                        couleur_index = ord(c) - ord("A")

                        empilable = (hauteurs[couleur_index] == valeur - 1)
                        complete = (sait_valeur[joueur][p] != "?" and sait_couleur[joueur][p] != "?")

                        if empilable and not complete:
                            if sait_valeur[joueur][p] == "?":
                                out(f"i {joueur} {v}")
                            else:
                                out(f"I {joueur} {c}")

                            action_faite = True
                            break

                    if action_faite:
                        break

            # regel 3 : sinon defausse position 1
            if not action_faite:
                out("d 1")

    elif cmd == "f":
        if int(parties[1]) == 0:
            break