//! # Nexus: Hybrid Intelligence Architecture
//!
//! Combines the breakthroughs of 2024-2025:
//! - Hybrid Attention/SSM (Jamba-style)
//! - Test-time learning memory (Titans-style)
//! - Latent world model (JEPA-inspired)
//! - Neuro-symbolic reasoning pipeline
//! - Automatic differentiation for training

pub mod tensor;
pub mod attention;
pub mod ssm;
pub mod memory;
pub mod block;
pub mod world_model;
pub mod symbolic;
pub mod autograd;
pub mod training;
pub mod tokenizer;
pub mod embedding;
pub mod differentiable;
pub mod differentiable_ssm;
pub mod differentiable_memory;
pub mod differentiable_world_model;
pub mod checkpoint;
pub mod gpu;

#[cfg(feature = "python")]
pub mod python;

// Re-exports
pub use tensor::Tensor;
pub use attention::MultiHeadAttention;
pub use ssm::SelectiveSSM;
pub use memory::TitansMemory;
pub use block::HybridBlock;
pub use symbolic::{Expr, ReasoningPipeline, ConstraintSolver};
pub use autograd::{Variable, Parameter, AdamW, SGD, Optimizer, DifferentiableLinear};
pub use training::{Trainer, TrainConfig, TrainState, DataLoader};
pub use tokenizer::{Tokenizer, SimpleBPE, TiktokenBPE};
pub use embedding::Embedding;
pub use differentiable::{
    DifferentiableNexusLM, DifferentiableBlock, DifferentiableMLP,
    DifferentiableHybridBlock, DifferentiableHybridNexusLM,
};
pub use differentiable_ssm::DifferentiableSSM;
pub use differentiable_memory::DifferentiableMemory;
pub use differentiable_world_model::{
    DifferentiableWorldModel, DifferentiableWorldModelEncoder, DifferentiableWorldModelPredictor,
    MaskStrategy,
};
pub use checkpoint::{ModelCheckpoint, OptimizerCheckpoint, TensorData};

// NexusLM is defined in this file, so just make it public (it already is)

use serde::{Deserialize, Serialize};

/// Configuration for Nexus model
#[derive(Debug, Clone, Serialize, Deserialize)]
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
#[derive(Clone, Serialize, Deserialize)]
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

    /// Get number of parameters (approximate)
    pub fn num_parameters(&self) -> usize {
        let d = self.config.d_model;
        let n_layers = self.config.layers_per_block;
        let d_ff = d * 4;

        // Per layer: attention/SSM + MLP
        let per_layer = d * d * 4 + d_ff * d * 3;

        n_layers * per_layer
    }
}

/// Nexus Language Model - wraps Nexus with embedding and output projection
#[derive(Clone, Serialize, Deserialize)]
pub struct NexusLM {
    pub config: NexusConfig,
    pub embedding: embedding::Embedding,
    pub core: Nexus,
}

impl NexusLM {
    /// Create a new language model
    pub fn new(config: NexusConfig) -> Self {
        let embedding = embedding::Embedding::new(
            config.vocab_size,
            config.d_model,
            config.max_seq_len,
        );
        let core = Nexus::new(config.clone());

        Self { config, embedding, core }
    }

    /// Forward pass from token IDs to logits
    ///
    /// # Arguments
    /// * `token_ids` - Token IDs, shape (batch_size, seq_len)
    /// * `update_memory` - Whether to update test-time memory
    ///
    /// # Returns
    /// Logits over vocabulary, shape (batch_size, seq_len, vocab_size)
    pub fn forward(&mut self, token_ids: &[Vec<u32>], update_memory: bool) -> ndarray::Array3<f32> {
        // Embed tokens
        let embedded = self.embedding.forward(token_ids);

        // Create tensor and run through core
        let input = Tensor { data: embedded };
        let output = self.core.forward(&input, update_memory);

        // Project to vocabulary logits (using tied weights)
        self.embedding.unembed(&output.data)
    }

    /// Generate text given a prompt
    ///
    /// # Arguments
    /// * `prompt_ids` - Token IDs for the prompt
    /// * `max_new_tokens` - Maximum tokens to generate
    /// * `temperature` - Sampling temperature (1.0 = normal, <1.0 = more focused, >1.0 = more random)
    pub fn generate(
        &mut self,
        prompt_ids: &[u32],
        max_new_tokens: usize,
        temperature: f32,
    ) -> Vec<u32> {
        use rand::Rng;

        let mut generated = prompt_ids.to_vec();
        let mut rng = rand::thread_rng();

        for _ in 0..max_new_tokens {
            // Get logits for current sequence
            let logits = self.forward(&[generated.clone()], true);

            // Get logits for last position
            let seq_len = generated.len();
            let vocab_size = self.config.vocab_size;

            // Extract last token's logits and apply temperature
            let last_logits: Vec<f32> = (0..vocab_size)
                .map(|v| logits[[0, seq_len - 1, v]] / temperature)
                .collect();

            // Softmax
            let max_logit = last_logits.iter().cloned().fold(f32::NEG_INFINITY, f32::max);
            let exp_sum: f32 = last_logits.iter().map(|x| (x - max_logit).exp()).sum();
            let probs: Vec<f32> = last_logits.iter().map(|x| (x - max_logit).exp() / exp_sum).collect();

            // Sample from distribution
            let mut cumsum = 0.0;
            let sample: f32 = rng.gen();
            let mut next_token = 0u32;
            for (i, &p) in probs.iter().enumerate() {
                cumsum += p;
                if sample <= cumsum {
                    next_token = i as u32;
                    break;
                }
            }

            generated.push(next_token);

            // Check for EOS (token 3 in SimpleBPE)
            if next_token == 3 {
                break;
            }
        }

        generated
    }

    /// Compute cross-entropy loss for language modeling
    pub fn compute_loss(&mut self, token_ids: &[Vec<u32>]) -> f32 {
        let logits = self.forward(token_ids, false);
        let (batch_size, seq_len, vocab_size) = logits.dim();

        let mut total_loss = 0.0;
        let mut count = 0;

        for b in 0..batch_size {
            for t in 0..(seq_len - 1) {
                // Target is next token
                let target = token_ids[b][t + 1] as usize;

                // Compute softmax and cross-entropy for this position
                let max_logit = (0..vocab_size)
                    .map(|v| logits[[b, t, v]])
                    .fold(f32::NEG_INFINITY, f32::max);

                let log_sum_exp: f32 = (0..vocab_size)
                    .map(|v| (logits[[b, t, v]] - max_logit).exp())
                    .sum::<f32>()
                    .ln();

                let log_prob = logits[[b, t, target]] - max_logit - log_sum_exp;
                total_loss -= log_prob;
                count += 1;
            }
        }

        if count > 0 { total_loss / count as f32 } else { 0.0 }
    }

    /// Total number of parameters
    pub fn num_parameters(&self) -> usize {
        self.embedding.num_parameters() + self.core.num_parameters()
    }

    /// Save model to a file (binary format)
    pub fn save<P: AsRef<std::path::Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let file = std::fs::File::create(path)?;
        let writer = std::io::BufWriter::new(file);
        bincode::serialize_into(writer, self)?;
        Ok(())
    }

    /// Load model from a file (binary format)
    pub fn load<P: AsRef<std::path::Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let file = std::fs::File::open(path)?;
        let reader = std::io::BufReader::new(file);
        let model = bincode::deserialize_from(reader)?;
        Ok(model)
    }

    /// Save model to JSON (human-readable, larger)
    pub fn save_json<P: AsRef<std::path::Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let file = std::fs::File::create(path)?;
        let writer = std::io::BufWriter::new(file);
        serde_json::to_writer_pretty(writer, self)?;
        Ok(())
    }

    /// Load model from JSON
    pub fn load_json<P: AsRef<std::path::Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let file = std::fs::File::open(path)?;
        let reader = std::io::BufReader::new(file);
        let model = serde_json::from_reader(reader)?;
        Ok(model)
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

    #[test]
    fn test_nexus_creation() {
        let config = NexusConfig {
            d_model: 64,
            n_heads: 4,
            layers_per_block: 4,
            ..Default::default()
        };

        let model = Nexus::new(config);
        assert_eq!(model.blocks.len(), 4);
    }

    #[test]
    fn test_nexus_forward() {
        let config = NexusConfig {
            d_model: 64,
            n_heads: 4,
            layers_per_block: 2,
            ..Default::default()
        };

        let mut model = Nexus::new(config);
        let input = Tensor::randn(1, 4, 64);
        let output = model.forward(&input, true);

        assert_eq!(output.shape(), (1, 4, 64));
    }

    #[test]
    fn test_config_serialization() {
        let config = NexusConfig::default();
        let json = serde_json::to_string(&config).unwrap();
        let loaded: NexusConfig = serde_json::from_str(&json).unwrap();
        assert_eq!(config.d_model, loaded.d_model);
    }

    #[test]
    fn test_model_save_load() {
        use tempfile::NamedTempFile;

        let config = NexusConfig {
            d_model: 32,
            n_heads: 2,
            layers_per_block: 1,
            vocab_size: 100,
            max_seq_len: 64,
            ..Default::default()
        };

        let model = NexusLM::new(config.clone());

        // Save to temp file
        let temp = NamedTempFile::new().unwrap();
        model.save(temp.path()).unwrap();

        // Load back
        let loaded = NexusLM::load(temp.path()).unwrap();

        // Verify config matches
        assert_eq!(loaded.config.d_model, config.d_model);
        assert_eq!(loaded.config.vocab_size, config.vocab_size);
        assert_eq!(loaded.num_parameters(), model.num_parameters());
    }
}
