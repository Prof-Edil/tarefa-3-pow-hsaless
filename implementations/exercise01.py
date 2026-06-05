max_weight = 4_000_000
tx = "4c50e3dad7f98bceb6441f96b23748dea84fbdb7cedd603441e6ea4a574d04a6"

txs = {}

with open("data/mempool.csv") as f:
    for line in f:
        line = line.strip()

        if not line:
            continue

        parts = line.split(",")

        txid = parts[0]

        fee = int(parts[1])
        weight = int(parts[2])

        parents = []
        if len(parts) > 3 and parts[3]:
            parents = parts[3].split(";")

        txs[txid] = {"fee": fee,"weight": weight, "parents": parents}




def get_ancestors(txid, visited=None):
    if visited is None:
        visited = set()

    if txid in visited:
        return []

    visited.add(txid)

    result = []

    for parent in txs[txid]["parents"]:
        if parent in txs:
            result.extend(get_ancestors(parent, visited))
            result.append(parent)

    return result


selected = []
selected_set = set()
total_fee = 0
total_weight = 0

def add_package(package):
    global total_fee, total_weight

    for txid in package:
        if txid not in selected_set:
            selected.append(txid)
            selected_set.add(txid)
            total_fee += txs[txid]["fee"]
            total_weight += txs[txid]["weight"]


package = get_ancestors(tx)
package.append(tx)


add_package(package)

while True:
    best_package = None
    best_ratio = -1

    for txid in txs:
        if txid in selected_set:
            continue

        package = get_ancestors(txid)
        package.append(txid)

        seen = set()
        package = [x for x in package if not (x in seen or seen.add(x))]

        package_weight = 0

        for t in package:
            if t not in selected_set:
                package_weight += txs[t]["weight"]
        package_fee = 0

        for t in package:
            if t not in selected_set:
                package_fee += txs[t]["fee"]

        if package_weight == 0:
            continue

        if total_weight + package_weight > max_weight:
            continue

        ratio = package_fee / package_weight

        if ratio > best_ratio:
            best_ratio = ratio
            best_package = package

    if best_package is None:
        break

    add_package(best_package)
with open("solutions/exercise01.txt", "w") as f:
    for txid in selected:
        f.write(txid + "\n")
