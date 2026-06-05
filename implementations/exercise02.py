import hashlib

txid = "49ff8cccf1ca12179e9ae7a4760f550b5a18401b27e1e057604e27c3e10c08fb"

with open("data/ex02_txid_list.txt", "r") as f:
    txids = [line.strip() for line in f if line.strip()]


def sha256(data):
    return hashlib.sha256(data).digest()


def merkle_parent(l, r):
    return sha256(l + r)


def build(txids, target):
    level = [bytes.fromhex(txid) for txid in txids]

    t_hash = bytes.fromhex(target)


    t_index = level.index(t_hash)

    proof = []

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])

        if t_index % 2 == 0:
            sib_index = t_index + 1
        else:
            sib_index = t_index - 1

        proof.append(level[sib_index].hex())

        nextl = []

        for i in range(0, len(level), 2):
            parent = merkle_parent(level[i], level[i + 1])
            nextl.append(parent)

        t_index = t_index // 2
        level = nextl

    merkle_root = level[0].hex()
    return merkle_root, proof



merkle_root, proof = build(txids, txid)

with open("solutions/exercise02.txt", "w") as f:
    f.write(merkle_root + "\n")

    for sibling in proof:
        f.write(sibling + "\n")
