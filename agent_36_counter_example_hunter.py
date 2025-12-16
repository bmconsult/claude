#!/usr/bin/env python3
"""
Agent 36: Counter-Example Hunter
Mission: Find counter-examples to Collatz claims about hitting time and descent
"""

import sys
from collections import defaultdict
from typing import List, Tuple, Optional

class CounterExampleHunter:
    def __init__(self):
        self.counter_examples = []
        self.late_hitters = []
        self.increasing_sequences = []
        self.worst_cases = []

    def collatz_step(self, n: int) -> int:
        """Single Collatz step"""
        if n % 2 == 0:
            return n // 2
        else:
            return 3 * n + 1

    def full_trajectory(self, n: int, max_steps: int = 100000) -> Optional[List[int]]:
        """
        Compute full trajectory to 1.
        Returns None if doesn't reach 1 within max_steps (MAJOR COUNTER-EXAMPLE!)
        """
        trajectory = [n]
        current = n
        steps = 0

        while current != 1 and steps < max_steps:
            current = self.collatz_step(current)
            trajectory.append(current)
            steps += 1

        if current != 1:
            return None  # COUNTER-EXAMPLE: Doesn't reach 1!

        return trajectory

    def extract_mod4_equals_1(self, trajectory: List[int]) -> List[int]:
        """Extract subsequence where n ≡ 1 (mod 4)"""
        return [x for x in trajectory if x % 4 == 1]

    def time_to_hit_mod4_equals_1(self, n: int, max_steps: int = 100000) -> Optional[int]:
        """
        Count steps until first hitting n ≡ 1 (mod 4).
        Returns None if doesn't hit within max_steps (COUNTER-EXAMPLE!)
        """
        if n % 4 == 1:
            return 0

        current = n
        steps = 0

        while steps < max_steps:
            current = self.collatz_step(current)
            steps += 1

            if current % 4 == 1:
                return steps

        return None  # COUNTER-EXAMPLE: Never hits!

    def analyze_number(self, n: int) -> dict:
        """Complete analysis of a single number"""
        result = {
            'n': n,
            'trajectory': None,
            'reaches_1': False,
            'hitting_time': None,
            'hits_mod4_1': False,
            'mod4_sequence': [],
            'max_in_mod4': None,
            'max_overall': None,
            'increases_after_hitting': [],
            'worst_increase_ratio': 0.0,
            'total_steps': 0,
            'is_counter_example': False,
            'counter_example_type': []
        }

        # Full trajectory
        trajectory = self.full_trajectory(n, max_steps=100000)

        if trajectory is None:
            result['is_counter_example'] = True
            result['counter_example_type'].append('DOES_NOT_REACH_1')
            return result

        result['trajectory'] = trajectory
        result['reaches_1'] = True
        result['total_steps'] = len(trajectory) - 1
        result['max_overall'] = max(trajectory)

        # Hitting time
        hitting_time = self.time_to_hit_mod4_equals_1(n, max_steps=100000)

        if hitting_time is None:
            result['is_counter_example'] = True
            result['counter_example_type'].append('NEVER_HITS_MOD4_1')
            return result

        result['hitting_time'] = hitting_time
        result['hits_mod4_1'] = True

        # Mod 4 ≡ 1 subsequence
        mod4_seq = self.extract_mod4_equals_1(trajectory)
        result['mod4_sequence'] = mod4_seq

        if len(mod4_seq) > 0:
            result['max_in_mod4'] = max(mod4_seq)

            # Check for increases in mod4 sequence
            increases = []
            for i in range(len(mod4_seq) - 1):
                if mod4_seq[i+1] > mod4_seq[i]:
                    ratio = mod4_seq[i+1] / mod4_seq[i]
                    increases.append({
                        'from': mod4_seq[i],
                        'to': mod4_seq[i+1],
                        'ratio': ratio,
                        'difference': mod4_seq[i+1] - mod4_seq[i]
                    })

            result['increases_after_hitting'] = increases

            if increases:
                result['worst_increase_ratio'] = max(inc['ratio'] for inc in increases)
                result['is_counter_example'] = True
                result['counter_example_type'].append('INCREASES_IN_MOD4_SEQUENCE')

            # Check if max in mod4 sequence exceeds starting n
            if result['max_in_mod4'] > n:
                result['is_counter_example'] = True
                result['counter_example_type'].append('MOD4_MAX_EXCEEDS_N')

        return result

    def hunt_range(self, start: int, end: int, verbose: bool = True):
        """Hunt for counter-examples in a range"""
        print(f"\n{'='*80}")
        print(f"HUNTING RANGE: {start} to {end}")
        print(f"{'='*80}\n")

        counter_examples = []
        late_hitters = []  # hitting_time > 1000
        mod4_exceeders = []  # max in mod4 seq > n
        increasers = []  # any increase in mod4 seq

        for n in range(start, end + 1):
            if n % 2 == 0:  # Skip even numbers
                continue

            if verbose and n % 1000 == 1:
                print(f"Progress: {n}/{end} ({100*n/end:.1f}%)")

            result = self.analyze_number(n)

            if result['is_counter_example']:
                counter_examples.append(result)

            if result['hitting_time'] and result['hitting_time'] > 1000:
                late_hitters.append(result)

            if result['max_in_mod4'] and result['max_in_mod4'] > n:
                mod4_exceeders.append(result)

            if result['increases_after_hitting']:
                increasers.append(result)

        return {
            'counter_examples': counter_examples,
            'late_hitters': late_hitters,
            'mod4_exceeders': mod4_exceeders,
            'increasers': increasers
        }

    def report_findings(self, findings: dict):
        """Generate detailed report"""
        print(f"\n{'='*80}")
        print("COUNTER-EXAMPLE HUNTER REPORT")
        print(f"{'='*80}\n")

        ce = findings['counter_examples']
        lh = findings['late_hitters']
        me = findings['mod4_exceeders']
        inc = findings['increasers']

        print(f"Total Counter-Examples Found: {len(ce)}")
        print(f"  - Never reaches 1: {sum(1 for x in ce if 'DOES_NOT_REACH_1' in x['counter_example_type'])}")
        print(f"  - Never hits mod4≡1: {sum(1 for x in ce if 'NEVER_HITS_MOD4_1' in x['counter_example_type'])}")
        print(f"  - Increases in mod4 seq: {len(inc)}")
        print(f"  - Mod4 max exceeds n: {len(me)}")
        print(f"\nLate Hitters (>1000 steps): {len(lh)}")

        # Report increases
        if inc:
            print(f"\n{'='*80}")
            print("INCREASES IN MOD4≡1 SEQUENCE (VIOLATIONS OF DESCENT)")
            print(f"{'='*80}\n")

            # Sort by worst increase ratio
            inc_sorted = sorted(inc, key=lambda x: x['worst_increase_ratio'], reverse=True)

            print(f"Found {len(inc)} numbers with increases in mod4≡1 sequence\n")

            for i, result in enumerate(inc_sorted[:20], 1):  # Top 20
                print(f"{i}. n = {result['n']}")
                print(f"   Worst increase ratio: {result['worst_increase_ratio']:.4f}")
                print(f"   Number of increases: {len(result['increases_after_hitting'])}")
                print(f"   Mod4 sequence length: {len(result['mod4_sequence'])}")
                print(f"   Increases:")
                for inc_detail in result['increases_after_hitting'][:5]:  # First 5 increases
                    print(f"     {inc_detail['from']} → {inc_detail['to']} "
                          f"(ratio: {inc_detail['ratio']:.4f}, diff: +{inc_detail['difference']})")
                if len(result['increases_after_hitting']) > 5:
                    print(f"     ... and {len(result['increases_after_hitting']) - 5} more")
                print()

        # Report mod4 exceeders
        if me:
            print(f"\n{'='*80}")
            print("NUMBERS WHERE MAX(MOD4 SEQUENCE) > n")
            print(f"{'='*80}\n")

            me_sorted = sorted(me, key=lambda x: x['max_in_mod4'] / x['n'], reverse=True)

            print(f"Found {len(me)} such numbers\n")

            for i, result in enumerate(me_sorted[:20], 1):
                ratio = result['max_in_mod4'] / result['n']
                print(f"{i}. n = {result['n']}, max(mod4) = {result['max_in_mod4']}, ratio = {ratio:.4f}")

        # Report late hitters
        if lh:
            print(f"\n{'='*80}")
            print("LATE HITTERS (>1000 STEPS TO HIT MOD4≡1)")
            print(f"{'='*80}\n")

            lh_sorted = sorted(lh, key=lambda x: x['hitting_time'], reverse=True)

            print(f"Found {len(lh)} late hitters\n")

            for i, result in enumerate(lh_sorted[:10], 1):
                print(f"{i}. n = {result['n']}, hitting_time = {result['hitting_time']} steps")

        # Overall worst case
        if inc:
            worst = max(inc, key=lambda x: x['worst_increase_ratio'])
            print(f"\n{'='*80}")
            print("WORST CASE FOUND")
            print(f"{'='*80}\n")
            print(f"n = {worst['n']}")
            print(f"Worst increase ratio: {worst['worst_increase_ratio']:.6f}")
            print(f"Total increases: {len(worst['increases_after_hitting'])}")
            print(f"\nFull mod4≡1 sequence:")
            print(worst['mod4_sequence'][:50])  # First 50 terms
            if len(worst['mod4_sequence']) > 50:
                print(f"... and {len(worst['mod4_sequence']) - 50} more terms")
            print(f"\nAll increases:")
            for inc_detail in worst['increases_after_hitting']:
                print(f"  {inc_detail['from']} → {inc_detail['to']} "
                      f"(×{inc_detail['ratio']:.4f}, +{inc_detail['difference']})")

    def construct_theoretical_bad_case(self):
        """
        Try to construct a number whose mod4≡1 sequence grows.

        Strategy: Work backwards from a target that would increase.
        If we have n ≡ 1 (mod 4), the next value in trajectory is:
        - If n ≡ 1 (mod 4): next is (3n+1)/2 (after odd→even→odd compression)
        - For next to also be ≡ 1 (mod 4): need (3n+1)/2 ≡ 1 (mod 4)
        """
        print(f"\n{'='*80}")
        print("THEORETICAL CONSTRUCTION ATTEMPT")
        print(f"{'='*80}\n")

        print("Analyzing the structure of increases...\n")

        print("For n ≡ 1 (mod 4):")
        print("  - Apply 3n+1: get 3n+1 ≡ 0 (mod 4), so even")
        print("  - Divide by 2: get (3n+1)/2")
        print("  - For this to be ≡ 1 (mod 4): need (3n+1)/2 ≡ 1 (mod 4)")
        print("  - This means 3n+1 ≡ 2 (mod 8)")
        print("  - So 3n ≡ 1 (mod 8)")
        print("  - Since n ≡ 1 (mod 4), we have n ≡ 1 or 5 (mod 8)")
        print("  - Testing: 3×1 = 3 ≡ 3 (mod 8) ✗")
        print("  - Testing: 3×5 = 15 ≡ 7 (mod 8) ✗")
        print("  - So (3n+1)/2 is NEVER ≡ 1 (mod 4) when n ≡ 1 (mod 4)\n")

        print("For n ≡ 1 (mod 4), after 3n+1 and dividing by 2^k, we get (3n+1)/2^k")
        print("For this to be odd and ≡ 1 (mod 4):")
        print("  - Must have maximal power of 2 dividing 3n+1")
        print("  - Then (3n+1)/2^k ≡ 1 (mod 4)")
        print()

        # Check specific patterns
        print("Checking n = 4k+1 pattern:")
        for k in range(10):
            n = 4*k + 1
            m = 3*n + 1
            power_of_2 = 0
            while m % 2 == 0:
                m //= 2
                power_of_2 += 1
            print(f"  n={n}: 3n+1={3*n+1}=2^{power_of_2}×{m}, m≡{m%4} (mod 4), increase={m>n}")

        print("\nConclusion: Finding patterns where mod4≡1 sequence increases...")

        # Analyze known bad cases
        print("\nAnalyzing known case n=9:")
        result = self.analyze_number(9)
        print(f"  Mod4≡1 sequence: {result['mod4_sequence']}")
        print(f"  Increases: {result['increases_after_hitting']}")


def main():
    hunter = CounterExampleHunter()

    # Test on known cases first
    print("Testing known cases:")
    print("\n1. Testing n=9 (known to have 9→17 increase):")
    result_9 = hunter.analyze_number(9)
    print(f"   Mod4≡1 sequence: {result_9['mod4_sequence']}")
    print(f"   Increases: {result_9['increases_after_hitting']}")

    print("\n2. Testing n=1:")
    result_1 = hunter.analyze_number(1)
    print(f"   Mod4≡1 sequence: {result_1['mod4_sequence']}")

    # Hunt in range 1-100000 (odd numbers only)
    print("\n\nStarting main hunt...")
    findings = hunter.hunt_range(1, 100000, verbose=True)

    # Report
    hunter.report_findings(findings)

    # Theoretical construction
    hunter.construct_theoretical_bad_case()

    # Save worst cases to file
    if findings['increasers']:
        print(f"\n{'='*80}")
        print("SAVING DETAILED RESULTS")
        print(f"{'='*80}\n")

        import json

        # Prepare data for JSON (convert to serializable format)
        export_data = {
            'summary': {
                'total_counter_examples': len(findings['counter_examples']),
                'total_increasers': len(findings['increasers']),
                'total_mod4_exceeders': len(findings['mod4_exceeders']),
                'total_late_hitters': len(findings['late_hitters'])
            },
            'top_increasers': []
        }

        inc_sorted = sorted(findings['increasers'],
                           key=lambda x: x['worst_increase_ratio'],
                           reverse=True)

        for result in inc_sorted[:100]:  # Top 100
            export_data['top_increasers'].append({
                'n': result['n'],
                'worst_ratio': result['worst_increase_ratio'],
                'num_increases': len(result['increases_after_hitting']),
                'mod4_sequence': result['mod4_sequence'],
                'increases': result['increases_after_hitting']
            })

        with open('/home/user/claude/agent_36_counter_examples.json', 'w') as f:
            json.dump(export_data, f, indent=2)

        print("Saved to agent_36_counter_examples.json")


if __name__ == '__main__':
    main()
