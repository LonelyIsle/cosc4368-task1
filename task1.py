from __future__ import annotations
import math
import random
from dataclasses import dataclass
from typing import Tuple, Dict, List
import argparse

Bounds = Tuple[float, float]
def f(x: float, y: float) -> float:
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2
@dataclass
class RHCRunResult:
    best_xy: Tuple[float, float]
    best_f: float
    solutions_generated: int  
    f_calls: int             

def clamp(v: float, lo: float, hi: float) -> float:
    return min(hi, max(lo, v))

def RHC(
    sp: Tuple[float, float],
    z: float,
    p: int,
    seed: int,
    bounds: Tuple[Bounds, Bounds] = ((-6.0, 6.0), (-6.0, 6.0)),
) -> RHCRunResult:
    rng = random.Random(seed)
    (xlo, xhi), (ylo, yhi) = bounds

    current = (float(sp[0]), float(sp[1]))
    best_val = f(*current)
    f_calls = 1
    solutions_generated = 0

    while True:
        improved = False
        best_neighbor_val = best_val
        best_neighbor_xy = current
        for _ in range(p):
            dx = rng.uniform(-z, z)
            dy = rng.uniform(-z, z)
            nx = clamp(current[0] + dx, xlo, xhi)
            ny = clamp(current[1] + dy, ylo, yhi)
            val = f(nx, ny)
            f_calls += 1
            solutions_generated += 1
            if val < best_neighbor_val:
                best_neighbor_val = val
                best_neighbor_xy = (nx, ny)
                improved = True
        if improved:
            current = best_neighbor_xy
            best_val = best_neighbor_val
        else:
            break
    return RHCRunResult(best_xy=current, best_f=best_val,
                        solutions_generated=solutions_generated,
                        f_calls=f_calls)

@dataclass
class RHCR2Result:
    sol1_xy: Tuple[float, float]
    sol2_xy: Tuple[float, float]
    sol3_xy: Tuple[float, float]
    f1: float
    f2: float
    f3: float
    n_solutions_1: int
    n_solutions_2: int
    n_solutions_3: int
    f_calls_1: int
    f_calls_2: int
    f_calls_3: int
    f_calls_total: int

def RHCR2(
    sp: Tuple[float, float],
    z: float,
    p: int,
    seed: int,
    bounds: Tuple[Bounds, Bounds] = ((-6.0, 6.0), (-6.0, 6.0)),
) -> RHCR2Result:
    run1 = RHC(sp, z, p, seed, bounds)
    run2 = RHC(run1.best_xy, z/20.0, p, seed, bounds)
    run3 = RHC(run2.best_xy, z/400.0, p, seed, bounds)

    return RHCR2Result(
        sol1_xy=run1.best_xy, sol2_xy=run2.best_xy, sol3_xy=run3.best_xy,
        f1=run1.best_f, f2=run2.best_f, f3=run3.best_f,
        n_solutions_1=run1.solutions_generated,
        n_solutions_2=run2.solutions_generated,
        n_solutions_3=run3.solutions_generated,
        f_calls_1=run1.f_calls,
        f_calls_2=run2.f_calls,
        f_calls_3=run3.f_calls,
        f_calls_total=run1.f_calls + run2.f_calls + run3.f_calls
    )

def run_bonus_33rd(
    sp=(0.0, 0.0), p=400, z=0.10, seed=9999
) -> RHCR2Result:
    return RHCR2(sp=sp, z=z, p=p, seed=seed)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run RHCR2 randomized hill climbing experiments.")
    parser.add_argument("--seed", type=int, help="Override base random seed (default 4368)")
    args = parser.parse_args()
    start_points = [(2.9, 3.2), (-2.5,+3.2), (4.2,-2), (-5,-5)]
    p_values = [30, 180]
    z_values = [0.05, 0.25]
    seed_base = args.seed if args.seed is not None else 4368

    def print_table_for(p, z, start_points, seed_base):
        title = f"Results for p={p}, z={z:.2f}"
        print("\n" + title)
        print("=" * len(title))
        header = (
            f"{'Start Point':>12} | {'Sol1':>20} | {'f(Sol1)':>10} | "
            f"{'Sol2':>20} | {'f(Sol2)':>10} | {'Sol3':>20} | {'f(Sol3)':>10} | "
            f"{'N1/N2/N3':>12} | {'Total f_calls':>14} | {'Seed':>6}"
        )
        print(header)
        print("-" * len(header))
        totals = []
        best_vals = []  
        for i, sp in enumerate(start_points):
            seed = seed_base + (p * 1000) + int(z * 1000) + i
            result = RHCR2(sp=sp, z=z, p=p, seed=seed)
            n_solutions_str = f"{result.n_solutions_1}/{result.n_solutions_2}/{result.n_solutions_3}"
            print(
                f"{str(sp):>12} | "
                f"{str(tuple(round(x, 4) for x in result.sol1_xy)):>20} | {result.f1:10.4f} | "
                f"{str(tuple(round(x, 4) for x in result.sol2_xy)):>20} | {result.f2:10.4f} | "
                f"{str(tuple(round(x, 4) for x in result.sol3_xy)):>20} | {result.f3:10.4f} | "
                f"{n_solutions_str:>12} | {result.f_calls_total:14} | {seed:>6}"
            )
            totals.append(result.f_calls_total)
            best_vals.append(result.f3)

        print("-" * len(header))
    for p in p_values:
        for z in z_values:
            print_table_for(p, z, start_points, seed_base)
    print("\n33rd Run (Bonus)")
    print("================")
    header = (
        f"{'Start Point':>12} | {'Sol1':>20} | {'f(Sol1)':>10} | "
        f"{'Sol2':>20} | {'f(Sol2)':>10} | {'Sol3':>20} | {'f(Sol3)':>10} | "
        f"{'N1/N2/N3':>12} | {'Total f_calls':>14} | {'Seed':>6}"
    )
    print(header)
    print("-" * len(header))
    bonus = run_bonus_33rd()
    n_solutions_str = f"{bonus.n_solutions_1}/{bonus.n_solutions_2}/{bonus.n_solutions_3}"
    sp_bonus = (1.6, -2.3)
    seed_bonus = 8188
    print(
        f"{str(sp_bonus):>12} | "
        f"{str(tuple(round(x, 4) for x in bonus.sol1_xy)):>20} | {bonus.f1:10.4f} | "
        f"{str(tuple(round(x, 4) for x in bonus.sol2_xy)):>20} | {bonus.f2:10.4f} | "
        f"{str(tuple(round(x, 4) for x in bonus.sol3_xy)):>20} | {bonus.f3:10.4f} | "
        f"{n_solutions_str:>12} | {bonus.f_calls_total:14} | {seed_bonus:>6}"
    )