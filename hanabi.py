import sys

temps = 0
moi = 0
n = 0

for ligne in sys.stdin:
    ligne = ligne.strip()

    if not ligne:
        continue

    parties = ligne.split()
    cmd = parties[0]

    # debutt de partie
    if cmd == "p":
        k = int(parties[1])
        n = int(parties[2])
        moi = int(parties[3])
        mode = int(parties[4])
        temps = 0

    # touur dun joueur
    elif cmd == "t":
        joueur = int(parties[1])

        if joueur == moi:
            temps += 1

            if temps % 3 == 0:
                print("e 1")
            elif temps % 3 == 1:
                prochain = 1 + (moi % n)
                print(f"I {prochain} A")
            else:
                print("d 1")

            sys.stdout.flush()

    # fin de partie
    elif cmd == "f":
        code = int(parties[1])

        if code == 0:
            break