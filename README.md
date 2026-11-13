# network-subnet-overlap-checker

Find overlapping subnets in a network inventory CSV: each CIDR is parsed with the ipaddress module (invalid CIDRs are reported INVALID and skipped), every pair is checked with overlaps(), and each overlapping pair is listed once — IPv4 and IPv6 are never compared with each other.

Sample input is included (sample.csv with four networks).

## How to run

```sh
python3 main.py sample.csv
```

## Example output

```
NET-1 Office LAN (192.168.1.0/24) overlaps NET-2 Lab LAN (192.168.1.128/25)
1 overlapping pair(s) across 4 network(s).
```

Standard library only. Run the tests with `python3 -m unittest discover`.
