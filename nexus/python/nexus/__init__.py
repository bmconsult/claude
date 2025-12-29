"""
Nexus: Hybrid Intelligence Architecture

Combines the breakthroughs of 2024-2025:
- Hybrid Attention/SSM (Jamba-style 1:7 ratio)
- Test-time learning memory (Titans-style)
- Latent world model (JEPA-inspired)
- Neuro-symbolic reasoning pipeline

Example:
    >>> import nexus
    >>> config = nexus.NexusConfig(d_model=512, n_heads=8)
    >>> model = nexus.Nexus(config)
    >>> output = model.forward(input_tensor)
"""

__version__ = "0.1.0"

# Try to import native extension
try:
    from nexus._nexus import (
        NexusConfig,
        Nexus,
        TrainConfig,
        Trainer,
    )
except ImportError as e:
    import warnings
    warnings.warn(
        f"Native extension not available ({e}). "
        "Install with: pip install maturin && maturin develop"
    )

    # Provide pure-Python fallback stubs for development
    class NexusConfig:
        """Configuration for Nexus model."""

        def __init__(
            self,
            d_model: int = 512,
            n_heads: int = 8,
            d_state: int = 16,
            d_conv: int = 4,
            expand: int = 2,
            layers_per_block: int = 8,
            memory_size: int = 1024,
            vocab_size: int = 32000,
            max_seq_len: int = 8192,
        ):
            self.d_model = d_model
            self.n_heads = n_heads
            self.d_state = d_state
            self.d_conv = d_conv
            self.expand = expand
            self.layers_per_block = layers_per_block
            self.memory_size = memory_size
            self.vocab_size = vocab_size
            self.max_seq_len = max_seq_len

        def __repr__(self):
            return f"NexusConfig(d_model={self.d_model}, n_heads={self.n_heads}, layers={self.layers_per_block})"

    class Nexus:
        """Nexus model (stub - install native extension for full functionality)."""

        def __init__(self, config: NexusConfig):
            self.config = config
            raise NotImplementedError(
                "Native extension required. Install with: pip install maturin && maturin develop"
            )

    class TrainConfig:
        """Training configuration (stub)."""

        def __init__(self, **kwargs):
            raise NotImplementedError("Native extension required")

    class Trainer:
        """Trainer (stub)."""

        def __init__(self, **kwargs):
            raise NotImplementedError("Native extension required")


# Convenience functions
def create_model(
    d_model: int = 512,
    n_heads: int = 8,
    layers: int = 8,
    memory_size: int = 1024,
) -> "Nexus":
    """Create a Nexus model with common defaults.

    Args:
        d_model: Hidden dimension
        n_heads: Number of attention heads
        layers: Number of transformer layers
        memory_size: Size of test-time memory

    Returns:
        Configured Nexus model
    """
    config = NexusConfig(
        d_model=d_model,
        n_heads=n_heads,
        layers_per_block=layers,
        memory_size=memory_size,
    )
    return Nexus(config)


# Model size presets
PRESETS = {
    "tiny": {"d_model": 128, "n_heads": 4, "layers_per_block": 4},
    "small": {"d_model": 256, "n_heads": 8, "layers_per_block": 6},
    "base": {"d_model": 512, "n_heads": 8, "layers_per_block": 8},
    "large": {"d_model": 1024, "n_heads": 16, "layers_per_block": 12},
    "xl": {"d_model": 2048, "n_heads": 32, "layers_per_block": 24},
}


def from_preset(name: str, **overrides) -> "Nexus":
    """Create a Nexus model from a preset.

    Args:
        name: Preset name (tiny, small, base, large, xl)
        **overrides: Override any preset values

    Returns:
        Configured Nexus model
    """
    if name not in PRESETS:
        raise ValueError(f"Unknown preset: {name}. Available: {list(PRESETS.keys())}")

    params = {**PRESETS[name], **overrides}
    config = NexusConfig(**params)
    return Nexus(config)
