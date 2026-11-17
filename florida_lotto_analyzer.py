#!/usr/bin/env python3
"""
Florida Lotto Live Analysis & Ticket Generator
Uses official frequency data (Florida Lottery, current matrix era since Oct 1999).
Performs statistical calculations and generates tickets based on analysis.

IMPORTANT: All combinations have identical true probability.
This is for entertainment / statistical exploration only.
"""

import random
import math
from collections import Counter

# Official Florida Lotto frequencies (main game, since 10/24/99 matrix change)
# Source: Florida Lottery frequency chart (queried ~Nov 16, 2026)
# Total draws in this era: 2825
FREQ = {
    1: 334, 2: 304, 3: 303, 4: 338, 5: 333, 6: 346, 7: 319, 8: 315,
    9: 327, 10: 327, 11: 293, 12: 331, 13: 321, 14: 296, 15: 343, 16: 316,
    17: 288, 18: 313, 19: 317, 20: 321, 21: 303, 22: 315, 23: 298, 24: 296,
    25: 318, 26: 318, 27: 326, 28: 331, 29: 316, 30: 325, 31: 333, 32: 319,
    33: 305, 34: 305, 35: 292, 36: 337, 37: 318, 38: 343, 39: 311, 40: 319,
    41: 317, 42: 304, 43: 341, 44: 335, 45: 339, 46: 307, 47: 322, 48: 348,
    49: 321, 50: 304, 51: 344, 52: 346, 53: 309
}

TOTAL_DRAWS = 2825
NUMBERS_PER_DRAW = 6
POOL_SIZE = 53
JACKPOT_ODDS = math.comb(POOL_SIZE, NUMBERS_PER_DRAW)

# Expected frequency per number
EXPECTED = TOTAL_DRAWS * NUMBERS_PER_DRAW / POOL_SIZE  # ≈ 319.81


def analyze():
    """Perform statistical analysis on the frequency data."""
    print("=" * 60)
    print("FLORIDA LOTTO STATISTICAL ANALYSIS")
    print("=" * 60)
    print(f"Total draws analyzed: {TOTAL_DRAWS}")
    print(f"Expected appearances per number: {EXPECTED:.2f}")
    print(f"Jackpot odds (any specific ticket): 1 in {JACKPOT_ODDS:,}")
    print()

    deviations = []
    for num in range(1, 54):
        obs = FREQ[num]
        dev = obs - EXPECTED
        # Rough standardized residual (approx, ignoring dependence)
        std_dev = math.sqrt(EXPECTED * (1 - NUMBERS_PER_DRAW / POOL_SIZE))
        z = dev / std_dev if std_dev > 0 else 0
        deviations.append((num, obs, dev, z))

    # Sort by absolute z-score (most deviant)
    deviations.sort(key=lambda x: abs(x[3]), reverse=True)

    print("Most deviant numbers (by approximate z-score):")
    print(f"{'Num':>4} {'Obs':>6} {'Dev':>8} {'z':>7}")
    for num, obs, dev, z in deviations[:12]:
        sign = "+" if dev >= 0 else ""
        print(f"{num:4d} {obs:6d} {sign}{dev:7.1f} {z:7.2f}")

    print()
    hot = sorted(FREQ.items(), key=lambda x: x[1], reverse=True)[:8]
    cold = sorted(FREQ.items(), key=lambda x: x[1])[:8]
    print("Hottest (highest frequency):", [n for n, _ in hot])
    print("Coldest (lowest frequency):", [n for n, _ in cold])
    print()
    return deviations


def generate_weighted(n_tickets=5, strength=1.0, seed=None):
    """
    Generate tickets using frequency-weighted sampling.
    strength > 1 increases bias toward frequent numbers.
    """
    if seed is not None:
        random.seed(seed)

    numbers = list(FREQ.keys())
    weights = [FREQ[n] ** strength for n in numbers]

    tickets = []
    for _ in range(n_tickets):
        ticket = []
        avail = numbers[:]
        avail_w = weights[:]
        for _ in range(6):
            chosen = random.choices(avail, weights=avail_w, k=1)[0]
            ticket.append(chosen)
            idx = avail.index(chosen)
            avail.pop(idx)
            avail_w.pop(idx)
        tickets.append(sorted(ticket))
    return tickets


def generate_hot_cold_mix(n_tickets=5, hot_ratio=0.6):
    """Mix of hottest and coldest numbers."""
    hot = [n for n, _ in sorted(FREQ.items(), key=lambda x: x[1], reverse=True)[:15]]
    cold = [n for n, _ in sorted(FREQ.items(), key=lambda x: x[1])[:15]]
    tickets = []
    for _ in range(n_tickets):
        n_hot = random.randint(3, 4)
        n_cold = 6 - n_hot
        ticket = random.sample(hot, n_hot) + random.sample(cold, n_cold)
        # ensure unique
        ticket = list(dict.fromkeys(ticket))
        while len(ticket) < 6:
            extra = random.randint(1, 53)
            if extra not in ticket:
                ticket.append(extra)
        tickets.append(sorted(ticket[:6]))
    return tickets


def generate_random(n_tickets=5):
    """True uniform random (correct probability model)."""
    tickets = []
    for _ in range(n_tickets):
        ticket = sorted(random.sample(range(1, 54), 6))
        tickets.append(ticket)
    return tickets


def print_tickets(tickets, label=""):
    print(f"\n{label}")
    for i, t in enumerate(tickets, 1):
        print(f"  Ticket {i}: {t}")


def main():
    analyze()

    print("\n" + "=" * 60)
    print("GENERATED TICKETS (based on analysis)")
    print("=" * 60)

    print_tickets(generate_weighted(5, strength=1.3), "Frequency-weighted (strength 1.3):")
    print_tickets(generate_hot_cold_mix(5), "Hot + Cold mix:")
    print_tickets(generate_random(3), "Pure random (for comparison):")

    print("\n" + "-" * 60)
    print("Note: These calculations describe the past only.")
    print("They do not change the probability of any future draw.")
    print(f"True jackpot odds remain 1 in {JACKPOT_ODDS:,} for every ticket.")


if __name__ == "__main__":
    main()
