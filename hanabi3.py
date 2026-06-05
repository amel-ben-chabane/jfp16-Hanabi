import sys

def out(s):
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

temps = 0
moi = n = k = 0
mains = {}
sait_valeur = {}
sait_couleur = {}

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

    elif cmd == "n":
        j = int(parties[1])
        p = int(parties[2])
        v = parties[3]
        c = parties[4]

        mains[j][p - 1] = v + c

        # une nouvelle carte remplace l'ancienne : elle ne sait plus rien
        sait_valeur[j][p - 1] = "?"
        sait_couleur[j][p - 1] = "?"

    elif cmd == "i":
        j = int(parties[1])
        v = parties[2]
        bits = parties[3:]

        for p in range(k):
            if bits[p] == "1":
                sait_valeur[j][p] = v

    elif cmd == "I":
        j = int(parties[1])
        c = parties[2]
        bits = parties[3:]

        for p in range(k):
            if bits[p] == "1":
                sait_couleur[j][p] = c

    elif cmd == "m":
        for j in range(1, n + 1):
            if j != moi:
                out(str(j) + " m " + " ".join(mains[j]))

    elif cmd == "r":
        for j in range(1, n + 1):
            cartes = []
            for p in range(k):
                cartes.append(sait_valeur[j][p] + sait_couleur[j][p])
            out(str(j) + " r " + " ".join(cartes))

    elif cmd == "t":
        joueur = int(parties[1])

        if joueur == moi:
            temps += 1

            if temps % 3 == 0:
                out("e 1")
            elif temps % 3 == 1:
                prochain = 1 + (moi % n)
                out(f"I {prochain} A")
            else:
                out("d 1")

    elif cmd == "f":
        if int(parties[1]) == 0:
            break