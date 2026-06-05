import sys

def out(s):
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

def deduire(joueur):
    valeurs = [str(x) for x in range(1, k + 1)]
    couleurs = [chr(ord("A") + x) for x in range(k)]

    for p in range(k):
        if sait_valeur[joueur][p] == "?":
            possibles = [v for v in valeurs if v not in neg_valeurs[joueur][p]]
            if len(possibles) == 1:
                sait_valeur[joueur][p] = possibles[0]

        if sait_couleur[joueur][p] == "?":
            possibles = [c for c in couleurs if c not in neg_couleurs[joueur][p]]
            if len(possibles) == 1:
                sait_couleur[joueur][p] = possibles[0]

temps = 0
moi = n = k = mode = 0
mains = {}
sait_valeur = {}
sait_couleur = {}
neg_valeurs = {}
neg_couleurs = {}
special = {}
age = {}
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
        neg_valeurs = {j: [set() for _ in range(k)] for j in range(1, n + 1)}
        neg_couleurs = {j: [set() for _ in range(k)] for j in range(1, n + 1)}
        special = {j: [False] * k for j in range(1, n + 1)}
        age = {j: [0] * k for j in range(1, n + 1)}
        hauteurs = [0] * k

    elif cmd == "n":
        joueur = int(parties[1])
        pos = int(parties[2]) - 1
        v = parties[3]
        c = parties[4]

        mains[joueur][pos] = v + c
        sait_valeur[joueur][pos] = "?"
        sait_couleur[joueur][pos] = "?"
        neg_valeurs[joueur][pos] = set()
        neg_couleurs[joueur][pos] = set()
        special[joueur][pos] = False
        age[joueur][pos] = 0

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
            else:
                neg_valeurs[joueur][p].add(v)

        if bits.count("1") == 1:
            p_special = bits.index("1")
            special[joueur][p_special] = True

        deduire(joueur)

    elif cmd == "I":
        joueur = int(parties[1])
        c = parties[2]
        bits = parties[3:]

        for p in range(k):
            if bits[p] == "1":
                sait_couleur[joueur][p] = c
            else:
                neg_couleurs[joueur][p].add(c)

        if bits.count("1") == 1:
            p_special = bits.index("1")
            special[joueur][p_special] = True

        deduire(joueur)

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
            for p in range(k):
                age[moi][p] += 1

            action_faite = False

            # Règle 1 bis : jouer une carte avec indication specale
            if vies > 0:
                for p in range(k):
                    if special[moi][p]:
                        out(f"e {p + 1}")
                        action_faite = True
                        break

            # regke 1 : jouer une carte complete et empilable
            if not action_faite:
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

            # refle 2 bis : donner une indication speciale si possible
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
                        empilable = hauteurs[couleur_index] == valeur - 1
                        complete = sait_valeur[joueur][p] != "?" and sait_couleur[joueur][p] != "?"

                        if empilable and not complete and not special[joueur][p]:
                            nb_val = sum(1 for carte2 in mains[joueur] if carte2[0] == v)
                            nb_coul = sum(1 for carte2 in mains[joueur] if carte2[1] == c)

                            if nb_val == 1:
                                out(f"i {joueur} {v}")
                                action_faite = True
                                break
                            elif nb_coul == 1:
                                out(f"I {joueur} {c}")
                                action_faite = True
                                break

                    if action_faite:
                        break

            # regle 2 : indication normale
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

                        empilable = hauteurs[couleur_index] == valeur - 1
                        complete = sait_valeur[joueur][p] != "?" and sait_couleur[joueur][p] != "?"

                        if empilable and not complete:
                            if sait_valeur[joueur][p] == "?":
                                out(f"i {joueur} {v}")
                            else:
                                out(f"I {joueur} {c}")

                            action_faite = True
                            break

                    if action_faite:
                        break

            # regle 3 bis : defausser la carte la plus ancienne
            if not action_faite:
                meilleur = 0
                for p in range(1, k):
                    if age[moi][p] > age[moi][meilleur]:
                        meilleur = p

                out(f"d {meilleur + 1}")

    elif cmd == "f":
        if int(parties[1]) == 0:
            break