import sys

def out(s):
    sys.stdout.write(s + "\n")
    sys.stdout.flush()

temps = 0
moi = 0
n = 0
k = 0
mains = {}

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

        mains = {}
        for j in range(1, n + 1):
            mains[j] = ["??"] * k

    elif cmd == "n":
        j = int(parties[1])
        p = int(parties[2])
        v = parties[3]
        c = parties[4]

        mains[j][p - 1] = v + c

    elif cmd == "m":
        for j in range(1, n + 1):
            if j != moi:
                out(str(j) + " m " + " ".join(mains[j]))

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
        code = int(parties[1])
        if code == 0:
            break