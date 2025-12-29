//! # Nexus: Hybrid Intelligence Architecture
//!
//! Combines the breakthroughs of 2024-2025:
//! - Hybrid Attention/SSM (Jamba-style)
//! - Test-time learning memory (Titans-style)
//! - Latent world model (JEPA-inspired)
//! - Neuro-symbolic reasoning pipeline

pub mod tensor;
pub mod attention;
pub mod ssm;
pub mod memory;
pub mod block;
pub mod world_model;
pub mod symbolic;

// Re-exports
pub use tensor::Tensor;
pub use attention::MultiHeadAttention;
pub use ssm::SelectiveSSM;
pub use memory::TitansMemory;
pub use block::HybridBlock;
pub use symbolic::{Expr, ReasoningPipeline, ConstraintSolver};

/// Configuration for Nexus model
#[derive(Debug, Clone)]
pub struct NexusConfig {
    /// Hidden dimension
    pub d_model: usize,
    /// Number of attention heads
    pub n_heads: usize,
    /// SSM state dimension
    pub d_state: usize,
    /// SSM convolution width
    pub d_conv: usize,
    /// Expansion factor for SSM
    pub expand: usize,
    /// Number of layers per block
    pub layers_per_block: usize,
    /// Ratio of attention to SSM layers (e.g., 1 means 1:7)
    pub attention_ratio: usize,
    /// Memory size for Titans-style memory
    pub memory_size: usize,
    /// Learning rate for test-time memory updates
    pub memory_lr: f32,
    /// Vocabulary size (for embeddings)
    pub vocab_size: usize,
    /// Maximum sequence length
    pub max_seq_len: usize,
}

impl Default for NexusConfig {
    fn default() -> Self {
        Self {
            d_model: 512,
            n_heads: 8,
            d_state: 16,
            d_conv: 4,
            expand: 2,
            layers_per_block: 8,
            attention_ratio: 1, // 1:7 ratio
            memory_size: 1024,
            memory_lr: 0.01,
            vocab_size: 32000,
            max_seq_len: 8192,
        }
    }
}

/// The main Nexus model
pub struct Nexus {
    pub config: NexusConfig,
    pub blocks: Vec<HybridBlock>,
    pub memory: TitansMemory,
}

impl Nexus {
    pub fn new(config: NexusConfig) -> Self {
        let mut blocks = Vec::new();

        // Create hybrid blocks with 1:7 attention:SSM ratio
        for i in 0..config.layers_per_block {
            let use_attention = i % (config.attention_ratio + 7) < config.attention_ratio;
            blocks.push(HybridBlock::new(&config, use_attention));
        }

        let memory = TitansMemory::new(config.d_model, config.memory_size, config.memory_lr);

        Self { config, blocks, memory }
    }

    /// Forward pass with test-time memory updates
    pub fn forward(&mut self, x: &Tensor, update_memory: bool) -> Tensor {
        let mut hidden = x.clone();

        for block in &self.blocks {
            hidden = block.forward(&hidden);
        }

        // Query and update memory (Titans-style)
        if update_memory {
            let surprise = self.memory.compute_surprise(&hidden);
            self.memory.update(&hidden, surprise);
        }

        let memory_context = self.memory.read(&hidden);

        // Combine hidden state with memory
        hidden.add(&memory_context)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_config_default() {
        let config = NexusConfig::default();
        assert_eq!(config.d_model, 512);
        assert_eq!(config.attention_ratio, 1);
    }
}
