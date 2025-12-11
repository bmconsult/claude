#!/usr/bin/env python3
"""
Temporal Interference Pattern Codec
====================================

Encodes arbitrary data structures as interference patterns between
multiple oscillating functions, where:
- Phase relationships encode the data values
- Interference decay patterns encode structural metadata
- The decoding process uses wave coherence analysis

Novel hypothesis: The interference patterns themselves might reveal
properties of the data structure that aren't visible in the original encoding.
"""

import numpy as np
import json
from typing import Any, Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class WavePacket:
    """A single wave component in the interference pattern"""
    frequency: float
    phase: float
    amplitude: float
    decay_rate: float


class InterferenceCodec:
    """Encodes data as temporal interference patterns"""

    def __init__(self, base_freq: float = 1.0, sample_rate: int = 1000):
        self.base_freq = base_freq
        self.sample_rate = sample_rate
        self.encoding_map = {}

    def _hash_to_phase(self, value: Any) -> float:
        """Convert any value to a phase angle [0, 2π)"""
        # Use hash but make it deterministic
        hash_val = hash(str(value))
        return (hash_val % 10000) / 10000 * 2 * np.pi

    def _structural_complexity(self, obj: Any, depth: int = 0) -> float:
        """Compute structural complexity as a decay rate"""
        if isinstance(obj, dict):
            return 0.1 + depth * 0.05 + len(obj) * 0.01
        elif isinstance(obj, list):
            return 0.1 + depth * 0.05 + len(obj) * 0.01
        else:
            return 0.1 + depth * 0.05

    def _encode_value(self, value: Any, depth: int = 0) -> WavePacket:
        """Encode a single value as a wave packet"""
        phase = self._hash_to_phase(value)

        # Frequency encodes type information
        if isinstance(value, bool):
            freq = self.base_freq * 1.1
        elif isinstance(value, int):
            freq = self.base_freq * 1.3
        elif isinstance(value, float):
            freq = self.base_freq * 1.7
        elif isinstance(value, str):
            freq = self.base_freq * 2.3
        else:
            freq = self.base_freq * 3.1

        amplitude = 1.0 / (1 + depth * 0.2)  # Decay with nesting
        decay_rate = self._structural_complexity(value, depth)

        return WavePacket(freq, phase, amplitude, decay_rate)

    def _encode_structure(self, obj: Any, depth: int = 0) -> List[WavePacket]:
        """Recursively encode a data structure"""
        waves = []

        if isinstance(obj, dict):
            for key, value in obj.items():
                # Keys and values both contribute waves
                waves.append(self._encode_value(key, depth))
                if isinstance(value, (dict, list)):
                    waves.extend(self._encode_structure(value, depth + 1))
                else:
                    waves.append(self._encode_value(value, depth))

        elif isinstance(obj, list):
            for item in obj:
                if isinstance(item, (dict, list)):
                    waves.extend(self._encode_structure(item, depth + 1))
                else:
                    waves.append(self._encode_value(item, depth))
        else:
            waves.append(self._encode_value(obj, depth))

        return waves

    def encode(self, data: Any, duration: float = 1.0) -> np.ndarray:
        """Encode data as a temporal interference pattern"""
        waves = self._encode_structure(data)
        self.encoding_map = {i: w for i, w in enumerate(waves)}

        # Generate time series
        t = np.linspace(0, duration, int(duration * self.sample_rate))
        signal = np.zeros_like(t)

        # Superpose all waves with decay
        for wave in waves:
            component = (wave.amplitude *
                        np.exp(-wave.decay_rate * t) *
                        np.sin(2 * np.pi * wave.frequency * t + wave.phase))
            signal += component

        return signal

    def analyze_interference(self, signal: np.ndarray) -> Dict[str, Any]:
        """
        Analyze the interference pattern for emergent properties
        This is the novel part: what does the interference reveal?
        """
        # Compute various interference metrics

        # 1. Coherence decay - how fast does the pattern lose structure?
        autocorr = np.correlate(signal, signal, mode='full')
        autocorr = autocorr[len(autocorr)//2:]
        autocorr /= autocorr[0]

        # Find where autocorrelation drops below threshold
        coherence_length = np.argmax(autocorr < 0.1)
        if coherence_length == 0:
            coherence_length = len(autocorr)

        # 2. Spectral entropy - how complex is the frequency structure?
        fft = np.fft.fft(signal)
        power = np.abs(fft[:len(fft)//2]) ** 2
        power_norm = power / np.sum(power)
        power_norm = power_norm[power_norm > 0]  # Remove zeros for log
        spectral_entropy = -np.sum(power_norm * np.log2(power_norm))

        # 3. Zero-crossing rate - how turbulent is the interference?
        zero_crossings = np.sum(np.diff(np.sign(signal)) != 0)
        zcr = zero_crossings / len(signal)

        # 4. Peak density - how many local maxima?
        peaks = 0
        for i in range(1, len(signal) - 1):
            if signal[i] > signal[i-1] and signal[i] > signal[i+1]:
                peaks += 1
        peak_density = peaks / len(signal)

        # 5. Novel metric: "interference dimensionality"
        # How many independent dimensions are needed to reconstruct?
        # Use SVD on embedded signal
        embed_dim = min(50, len(signal) // 10)
        if embed_dim > 1:
            embedded = np.array([signal[i:i+embed_dim]
                               for i in range(len(signal) - embed_dim)])
            if embedded.shape[0] > 0:
                U, s, Vt = np.linalg.svd(embedded, full_matrices=False)
                # Effective dimensionality: number of singular values needed for 95% energy
                energy = np.cumsum(s**2) / np.sum(s**2)
                eff_dim = np.argmax(energy > 0.95) + 1
            else:
                eff_dim = 1
        else:
            eff_dim = 1

        return {
            'coherence_length': int(coherence_length),
            'spectral_entropy': float(spectral_entropy),
            'zero_crossing_rate': float(zcr),
            'peak_density': float(peak_density),
            'effective_dimensionality': int(eff_dim),
            'num_wave_components': len(self.encoding_map)
        }

    def visualize_signature(self, signal: np.ndarray) -> str:
        """Create an ASCII visualization of the interference signature"""
        analysis = self.analyze_interference(signal)

        # Create a compact visual signature
        sig = []
        sig.append("Interference Signature:")
        sig.append("=" * 40)

        # Waveform preview (first 80 samples)
        preview = signal[:80]
        min_val, max_val = preview.min(), preview.max()
        normalized = (preview - min_val) / (max_val - min_val) if max_val != min_val else preview

        sig.append("\nWaveform (first 80 samples):")
        levels = " ▁▂▃▄▅▆▇█"
        wave_viz = ''.join(levels[int(v * (len(levels) - 1))] for v in normalized)
        sig.append(wave_viz)

        # Metrics
        sig.append(f"\nMetrics:")
        sig.append(f"  Coherence Length: {analysis['coherence_length']:>6}")
        sig.append(f"  Spectral Entropy: {analysis['spectral_entropy']:>6.2f}")
        sig.append(f"  Zero-Cross Rate:  {analysis['zero_crossing_rate']:>6.4f}")
        sig.append(f"  Peak Density:     {analysis['peak_density']:>6.4f}")
        sig.append(f"  Eff. Dimension:   {analysis['effective_dimensionality']:>6}")
        sig.append(f"  Wave Components:  {analysis['num_wave_components']:>6}")

        return '\n'.join(sig)


def demonstrate_novel_properties():
    """
    Demonstrate whether this reveals anything genuinely novel
    """
    codec = InterferenceCodec()

    # Test with different data structures
    test_cases = [
        ("Simple string", "hello"),
        ("Simple dict", {"name": "Alice", "age": 30}),
        ("Nested structure", {
            "users": [
                {"name": "Alice", "scores": [1, 2, 3]},
                {"name": "Bob", "scores": [4, 5, 6]}
            ]
        }),
        ("Deep nesting", {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": "deep"
                    }
                }
            }
        }),
        ("Wide structure", {f"key{i}": i for i in range(20)})
    ]

    print("TEMPORAL INTERFERENCE CODEC ANALYSIS")
    print("=" * 60)
    print("\nHypothesis: Interference patterns reveal structural properties")
    print("that aren't obvious from the raw data.\n")

    results = []

    for name, data in test_cases:
        print(f"\n{name}:")
        print(f"Data: {str(data)[:60]}...")

        signal = codec.encode(data)
        analysis = codec.analyze_interference(signal)

        print(codec.visualize_signature(signal))

        results.append((name, analysis))
        print()

    # Now the interesting part: do the metrics reveal anything?
    print("\n" + "=" * 60)
    print("COMPARATIVE ANALYSIS")
    print("=" * 60)

    print("\nStructural Complexity Ranking (by Effective Dimension):")
    sorted_by_dim = sorted(results, key=lambda x: x[1]['effective_dimensionality'], reverse=True)
    for name, analysis in sorted_by_dim:
        print(f"  {name:20} -> Eff.Dim: {analysis['effective_dimensionality']:2}, "
              f"Entropy: {analysis['spectral_entropy']:.2f}")

    print("\nObservations:")
    print("  - Does effective dimensionality correlate with nesting depth?")
    print("  - Does spectral entropy distinguish wide vs deep structures?")
    print("  - Does zero-crossing rate reveal anything about data complexity?")

    # Test a specific hypothesis
    print("\n" + "=" * 60)
    print("NOVEL PROPERTY TEST")
    print("=" * 60)
    print("\nCan we distinguish structure type from interference alone?")

    # Create isomorphic structures with different shapes
    deep = {"a": {"b": {"c": {"d": "value"}}}}
    wide = {"a": "v1", "b": "v2", "c": "v3", "d": "v4"}

    deep_signal = codec.encode(deep)
    deep_analysis = codec.analyze_interference(deep_signal)

    wide_signal = codec.encode(wide)
    wide_analysis = codec.analyze_interference(wide_signal)

    print(f"\nDeep structure: {deep}")
    print(f"  Eff.Dim: {deep_analysis['effective_dimensionality']}, "
          f"Coherence: {deep_analysis['coherence_length']}")

    print(f"\nWide structure: {wide}")
    print(f"  Eff.Dim: {wide_analysis['effective_dimensionality']}, "
          f"Coherence: {wide_analysis['coherence_length']}")

    print("\n" + "=" * 60)
    print("CONCLUSION: Does this reveal emergent properties?")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_novel_properties()
