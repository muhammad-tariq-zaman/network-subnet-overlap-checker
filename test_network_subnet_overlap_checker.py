import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import unittest
from main import check

def row(network, name, cidr):
    return {"network": network, "name": name, "cidr": cidr}

class TestSubnetOverlapChecker(unittest.TestCase):
    def test_overlap_detected(self):
        overlaps, _, _ = check([row("NET-1", "Office", "192.168.1.0/24"),
                                row("NET-2", "Lab", "192.168.1.128/25")])
        self.assertEqual(len(overlaps), 1)
        self.assertEqual(overlaps[0][0][0], "NET-1")

    def test_no_overlap(self):
        overlaps, _, _ = check([row("NET-1", "Office", "192.168.1.0/24"),
                                row("NET-2", "Branch", "192.168.2.0/24")])
        self.assertEqual(overlaps, [])

    def test_identical_cidrs_overlap(self):
        overlaps, _, _ = check([row("NET-1", "A", "10.0.0.0/24"),
                                row("NET-2", "B", "10.0.0.0/24")])
        self.assertEqual(len(overlaps), 1)

    def test_invalid_cidr_reported(self):
        _, invalid, total = check([row("NET-1", "A", "not-a-cidr"),
                                   row("NET-2", "B", "10.0.0.0/24")])
        self.assertEqual(invalid, [("NET-1", "not-a-cidr")])
        self.assertEqual(total, 1)

    def test_ipv4_and_ipv6_never_compared(self):
        overlaps, _, _ = check([row("NET-1", "A", "10.0.0.0/8"),
                                row("NET-2", "B", "2001:db8::/32")])
        self.assertEqual(overlaps, [])

    def test_host_bits_accepted(self):
        overlaps, _, total = check([row("NET-1", "A", "192.168.1.5/24"),
                                    row("NET-2", "B", "192.168.2.0/24")])
        self.assertEqual((overlaps, total), ([], 2))

    def test_pairs_sorted(self):
        overlaps, _, _ = check([row("NET-3", "C", "10.0.0.0/24"),
                                row("NET-1", "A", "10.0.0.0/24"),
                                row("NET-2", "B", "10.0.0.0/24")])
        self.assertEqual([(p[0][0], p[1][0]) for p in overlaps],
                         [("NET-1", "NET-2"), ("NET-1", "NET-3"), ("NET-2", "NET-3")])

    def test_empty_input(self):
        self.assertEqual(check([]), ([], [], 0))
