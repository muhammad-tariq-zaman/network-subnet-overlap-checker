"""Find overlapping subnets in a network inventory CSV.

Usage: python3 main.py networks.csv
CSV columns: network,name,cidr.
Each CIDR is parsed with the ipaddress module; invalid CIDRs are
reported as INVALID and skipped. Every pair of networks is checked
with overlaps(): two networks overlap when one contains the other
or they share addresses. Each overlapping pair is listed once.
IPv4 and IPv6 networks are never compared with each other.
"""
import argparse, csv, ipaddress, sys

def check(rows):
    networks = []
    invalid = []
    for row in rows:
        try:
            net = ipaddress.ip_network(row["cidr"].strip(), strict=False)
        except ValueError:
            invalid.append((row["network"].strip(), row["cidr"].strip()))
            continue
        networks.append((row["network"].strip(), row["name"].strip(), net))
    overlaps = []
    for i in range(len(networks)):
        for j in range(i + 1, len(networks)):
            a = networks[i]
            b = networks[j]
            if a[2].version != b[2].version:
                continue
            if a[2].overlaps(b[2]):
                pair = (a, b) if a[0] <= b[0] else (b, a)
                overlaps.append(pair)
    overlaps.sort(key=lambda p: (p[0][0], p[1][0]))
    return overlaps, invalid, len(networks)

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path")
    args = parser.parse_args(argv)
    with open(args.path, newline="", encoding="utf-8") as f:
        overlaps, invalid, total = check(list(csv.DictReader(f)))
    for (a_id, a_name, a_net), (b_id, b_name, b_net) in overlaps:
        print(f"{a_id} {a_name} ({a_net}) overlaps {b_id} {b_name} ({b_net})")
    for network_id, cidr in invalid:
        print(f"{network_id}: INVALID CIDR ({cidr})")
    print(f"{len(overlaps)} overlapping pair(s) across {total} network(s).")
    return 0

if __name__ == "__main__":
    sys.exit(main())
