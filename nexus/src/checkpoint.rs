//! Model Checkpointing
//!
//! Save and load model weights for training resumption.

use ndarray::Array3;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::io::{BufReader, BufWriter};
use std::path::Path;

use crate::autograd::Variable;
use crate::differentiable::{
    DifferentiableAttention, DifferentiableBlock, DifferentiableMLP, DifferentiableNexusLM,
    DifferentiableRMSNorm, DifferentiableHybridBlock, DifferentiableHybridNexusLM,
};
use crate::differentiable_ssm::DifferentiableSSM;
use crate::differentiable_memory::DifferentiableMemory;
use crate::NexusConfig;

/// Serializable tensor data
#[derive(Clone, Serialize, Deserialize)]
pub struct TensorData {
    pub shape: Vec<usize>,
    pub data: Vec<f32>,
}

impl TensorData {
    pub fn from_array(arr: &Array3<f32>) -> Self {
        let shape = arr.shape().to_vec();
        let data = arr.iter().cloned().collect();
        Self { shape, data }
    }

    pub fn to_array(&self) -> Array3<f32> {
        Array3::from_shape_vec(
            (self.shape[0], self.shape[1], self.shape[2]),
            self.data.clone(),
        )
        .expect("Invalid tensor shape")
    }
}

/// Model checkpoint containing all weights
#[derive(Clone, Serialize, Deserialize)]
pub struct ModelCheckpoint {
    /// Model configuration
    pub config: NexusConfig,
    /// All model weights indexed by name
    pub weights: HashMap<String, TensorData>,
    /// Training step (for resumption)
    pub step: usize,
    /// Training loss at checkpoint
    pub loss: f32,
}

impl ModelCheckpoint {
    /// Create a checkpoint from a model
    pub fn from_model(model: &DifferentiableNexusLM, step: usize, loss: f32) -> Self {
        let mut weights = HashMap::new();

        // Save embedding
        weights.insert("embed".to_string(), TensorData::from_array(&model.embed.data()));

        // Save each block
        for (i, block) in model.blocks.iter().enumerate() {
            let prefix = format!("block.{}", i);
            Self::save_block_weights(&mut weights, &prefix, block);
        }

        // Save final norm
        weights.insert(
            "norm_f.weight".to_string(),
            TensorData::from_array(&model.norm_f.weight.data()),
        );

        // Save output projection
        weights.insert(
            "output.weight".to_string(),
            TensorData::from_array(&model.output.weight.data()),
        );
        if let Some(ref bias) = model.output.bias {
            weights.insert(
                "output.bias".to_string(),
                TensorData::from_array(&bias.data()),
            );
        }

        Self {
            config: model.config.clone(),
            weights,
            step,
            loss,
        }
    }

    fn save_block_weights(
        weights: &mut HashMap<String, TensorData>,
        prefix: &str,
        block: &DifferentiableBlock,
    ) {
        // Norm1
        weights.insert(
            format!("{}.norm1.weight", prefix),
            TensorData::from_array(&block.norm1.weight.data()),
        );

        // Attention
        weights.insert(
            format!("{}.attn.q_proj.weight", prefix),
            TensorData::from_array(&block.attn.q_proj.weight.data()),
        );
        weights.insert(
            format!("{}.attn.k_proj.weight", prefix),
            TensorData::from_array(&block.attn.k_proj.weight.data()),
        );
        weights.insert(
            format!("{}.attn.v_proj.weight", prefix),
            TensorData::from_array(&block.attn.v_proj.weight.data()),
        );
        weights.insert(
            format!("{}.attn.out_proj.weight", prefix),
            TensorData::from_array(&block.attn.out_proj.weight.data()),
        );

        // Norm2
        weights.insert(
            format!("{}.norm2.weight", prefix),
            TensorData::from_array(&block.norm2.weight.data()),
        );

        // MLP
        weights.insert(
            format!("{}.mlp.up_proj.weight", prefix),
            TensorData::from_array(&block.mlp.up_proj.weight.data()),
        );
        weights.insert(
            format!("{}.mlp.gate_proj.weight", prefix),
            TensorData::from_array(&block.mlp.gate_proj.weight.data()),
        );
        weights.insert(
            format!("{}.mlp.down_proj.weight", prefix),
            TensorData::from_array(&block.mlp.down_proj.weight.data()),
        );
    }

    /// Load weights into a model
    pub fn load_into(&self, model: &DifferentiableNexusLM) -> Result<(), String> {
        // Load embedding
        if let Some(data) = self.weights.get("embed") {
            let arr = data.to_array();
            model.embed.apply_update(&(&arr - &model.embed.data()));
        }

        // Load each block
        for (i, block) in model.blocks.iter().enumerate() {
            let prefix = format!("block.{}", i);
            Self::load_block_weights(&self.weights, &prefix, block)?;
        }

        // Load final norm
        if let Some(data) = self.weights.get("norm_f.weight") {
            let arr = data.to_array();
            model.norm_f.weight.apply_update(&(&arr - &model.norm_f.weight.data()));
        }

        // Load output projection
        if let Some(data) = self.weights.get("output.weight") {
            let arr = data.to_array();
            model.output.weight.apply_update(&(&arr - &model.output.weight.data()));
        }
        if let Some(ref bias) = model.output.bias {
            if let Some(data) = self.weights.get("output.bias") {
                let arr = data.to_array();
                bias.apply_update(&(&arr - &bias.data()));
            }
        }

        Ok(())
    }

    fn load_block_weights(
        weights: &HashMap<String, TensorData>,
        prefix: &str,
        block: &DifferentiableBlock,
    ) -> Result<(), String> {
        // Helper to load a weight
        let load = |name: &str, var: &Variable| {
            if let Some(data) = weights.get(name) {
                let arr = data.to_array();
                var.apply_update(&(&arr - &var.data()));
            }
        };

        // Norm1
        load(&format!("{}.norm1.weight", prefix), &block.norm1.weight);

        // Attention
        load(&format!("{}.attn.q_proj.weight", prefix), &block.attn.q_proj.weight);
        load(&format!("{}.attn.k_proj.weight", prefix), &block.attn.k_proj.weight);
        load(&format!("{}.attn.v_proj.weight", prefix), &block.attn.v_proj.weight);
        load(&format!("{}.attn.out_proj.weight", prefix), &block.attn.out_proj.weight);

        // Norm2
        load(&format!("{}.norm2.weight", prefix), &block.norm2.weight);

        // MLP
        load(&format!("{}.mlp.up_proj.weight", prefix), &block.mlp.up_proj.weight);
        load(&format!("{}.mlp.gate_proj.weight", prefix), &block.mlp.gate_proj.weight);
        load(&format!("{}.mlp.down_proj.weight", prefix), &block.mlp.down_proj.weight);

        Ok(())
    }

    /// Save checkpoint to file
    pub fn save<P: AsRef<Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        bincode::serialize_into(writer, self)?;
        Ok(())
    }

    /// Load checkpoint from file
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        let checkpoint = bincode::deserialize_from(reader)?;
        Ok(checkpoint)
    }

    /// Save as JSON (human-readable)
    pub fn save_json<P: AsRef<Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer_pretty(writer, self)?;
        Ok(())
    }

    /// Load from JSON
    pub fn load_json<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        let checkpoint = serde_json::from_reader(reader)?;
        Ok(checkpoint)
    }
}

/// Optimizer state for checkpointing
#[derive(Clone, Serialize, Deserialize)]
pub struct OptimizerCheckpoint {
    /// First moments (m) for AdamW
    pub m: HashMap<String, TensorData>,
    /// Second moments (v) for AdamW
    pub v: HashMap<String, TensorData>,
    /// Current step count
    pub step_count: usize,
}

impl OptimizerCheckpoint {
    /// Create from AdamW optimizer state
    pub fn from_adamw(
        m: &HashMap<usize, Array3<f32>>,
        v: &HashMap<usize, Array3<f32>>,
        step_count: usize,
        param_names: &HashMap<usize, String>,
    ) -> Self {
        let m_data: HashMap<String, TensorData> = m
            .iter()
            .filter_map(|(id, arr)| {
                param_names.get(id).map(|name| {
                    (name.clone(), TensorData::from_array(arr))
                })
            })
            .collect();

        let v_data: HashMap<String, TensorData> = v
            .iter()
            .filter_map(|(id, arr)| {
                param_names.get(id).map(|name| {
                    (name.clone(), TensorData::from_array(arr))
                })
            })
            .collect();

        Self {
            m: m_data,
            v: v_data,
            step_count,
        }
    }

    /// Save optimizer state
    pub fn save<P: AsRef<Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        bincode::serialize_into(writer, self)?;
        Ok(())
    }

    /// Load optimizer state
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        let checkpoint = bincode::deserialize_from(reader)?;
        Ok(checkpoint)
    }
}

/// Model checkpoint for hybrid architecture (Attention/SSM + Memory)
#[derive(Clone, Serialize, Deserialize)]
pub struct HybridModelCheckpoint {
    /// Model configuration
    pub config: NexusConfig,
    /// All model weights indexed by name
    pub weights: HashMap<String, TensorData>,
    /// Block types (true = attention, false = SSM)
    pub block_types: Vec<bool>,
    /// Training step (for resumption)
    pub step: usize,
    /// Training loss at checkpoint
    pub loss: f32,
}

impl HybridModelCheckpoint {
    /// Create a checkpoint from a hybrid model
    pub fn from_model(model: &DifferentiableHybridNexusLM, step: usize, loss: f32) -> Self {
        let mut weights = HashMap::new();

        // Save embedding
        weights.insert("embed".to_string(), TensorData::from_array(&model.embed.data()));

        // Save each hybrid block
        let mut block_types = Vec::new();
        for (i, block) in model.blocks.iter().enumerate() {
            let prefix = format!("block.{}", i);
            let use_attention = block.attn.is_some();
            block_types.push(use_attention);
            Self::save_hybrid_block_weights(&mut weights, &prefix, block);
        }

        // Save memory module
        Self::save_memory_weights(&mut weights, "memory", &model.memory);

        // Save final norm
        weights.insert(
            "norm_f.weight".to_string(),
            TensorData::from_array(&model.norm_f.weight.data()),
        );

        // Save output projection
        weights.insert(
            "output.weight".to_string(),
            TensorData::from_array(&model.output.weight.data()),
        );
        if let Some(ref bias) = model.output.bias {
            weights.insert(
                "output.bias".to_string(),
                TensorData::from_array(&bias.data()),
            );
        }

        Self {
            config: model.config.clone(),
            weights,
            block_types,
            step,
            loss,
        }
    }

    fn save_hybrid_block_weights(
        weights: &mut HashMap<String, TensorData>,
        prefix: &str,
        block: &DifferentiableHybridBlock,
    ) {
        // Norm1
        weights.insert(
            format!("{}.norm1.weight", prefix),
            TensorData::from_array(&block.norm1.weight.data()),
        );

        // Attention (if present)
        if let Some(ref attn) = block.attn {
            weights.insert(
                format!("{}.attn.q_proj.weight", prefix),
                TensorData::from_array(&attn.q_proj.weight.data()),
            );
            weights.insert(
                format!("{}.attn.k_proj.weight", prefix),
                TensorData::from_array(&attn.k_proj.weight.data()),
            );
            weights.insert(
                format!("{}.attn.v_proj.weight", prefix),
                TensorData::from_array(&attn.v_proj.weight.data()),
            );
            weights.insert(
                format!("{}.attn.out_proj.weight", prefix),
                TensorData::from_array(&attn.out_proj.weight.data()),
            );
        }

        // SSM (if present)
        if let Some(ref ssm) = block.ssm {
            Self::save_ssm_weights(weights, &format!("{}.ssm", prefix), ssm);
        }

        // Norm2
        weights.insert(
            format!("{}.norm2.weight", prefix),
            TensorData::from_array(&block.norm2.weight.data()),
        );

        // MLP
        weights.insert(
            format!("{}.mlp.up_proj.weight", prefix),
            TensorData::from_array(&block.mlp.up_proj.weight.data()),
        );
        weights.insert(
            format!("{}.mlp.gate_proj.weight", prefix),
            TensorData::from_array(&block.mlp.gate_proj.weight.data()),
        );
        weights.insert(
            format!("{}.mlp.down_proj.weight", prefix),
            TensorData::from_array(&block.mlp.down_proj.weight.data()),
        );
    }

    fn save_ssm_weights(
        weights: &mut HashMap<String, TensorData>,
        prefix: &str,
        ssm: &DifferentiableSSM,
    ) {
        // Input projection
        weights.insert(
            format!("{}.in_proj.weight", prefix),
            TensorData::from_array(&ssm.in_proj.weight.data()),
        );

        // Convolution
        weights.insert(
            format!("{}.conv.weight", prefix),
            TensorData::from_array(&ssm.conv.weight.data()),
        );
        weights.insert(
            format!("{}.conv.bias", prefix),
            TensorData::from_array(&ssm.conv.bias.data()),
        );

        // Output projection
        weights.insert(
            format!("{}.out_proj.weight", prefix),
            TensorData::from_array(&ssm.out_proj.weight.data()),
        );

        // A (log space) and D parameters
        weights.insert(
            format!("{}.a_log", prefix),
            TensorData::from_array(&ssm.a_log.data()),
        );
        weights.insert(
            format!("{}.d_param", prefix),
            TensorData::from_array(&ssm.d_param.data()),
        );

        // Selection projections
        weights.insert(
            format!("{}.x_proj.weight", prefix),
            TensorData::from_array(&ssm.x_proj.weight.data()),
        );
        weights.insert(
            format!("{}.dt_proj.weight", prefix),
            TensorData::from_array(&ssm.dt_proj.weight.data()),
        );
        if let Some(ref bias) = ssm.dt_proj.bias {
            weights.insert(
                format!("{}.dt_proj.bias", prefix),
                TensorData::from_array(&bias.data()),
            );
        }
    }

    fn save_memory_weights(
        weights: &mut HashMap<String, TensorData>,
        prefix: &str,
        memory: &DifferentiableMemory,
    ) {
        // Projections
        weights.insert(
            format!("{}.key_proj.weight", prefix),
            TensorData::from_array(&memory.key_proj.weight.data()),
        );
        weights.insert(
            format!("{}.value_proj.weight", prefix),
            TensorData::from_array(&memory.value_proj.weight.data()),
        );
        weights.insert(
            format!("{}.query_proj.weight", prefix),
            TensorData::from_array(&memory.query_proj.weight.data()),
        );
        weights.insert(
            format!("{}.out_proj.weight", prefix),
            TensorData::from_array(&memory.out_proj.weight.data()),
        );

        // Learned memory
        weights.insert(
            format!("{}.memory_keys", prefix),
            TensorData::from_array(&memory.memory_keys.data()),
        );
        weights.insert(
            format!("{}.memory_values", prefix),
            TensorData::from_array(&memory.memory_values.data()),
        );
    }

    /// Load weights into a hybrid model
    pub fn load_into(&self, model: &DifferentiableHybridNexusLM) -> Result<(), String> {
        // Load embedding
        if let Some(data) = self.weights.get("embed") {
            let arr = data.to_array();
            model.embed.apply_update(&(&arr - &model.embed.data()));
        }

        // Load each hybrid block
        for (i, block) in model.blocks.iter().enumerate() {
            let prefix = format!("block.{}", i);
            Self::load_hybrid_block_weights(&self.weights, &prefix, block)?;
        }

        // Load memory
        Self::load_memory_weights(&self.weights, "memory", &model.memory)?;

        // Load final norm
        if let Some(data) = self.weights.get("norm_f.weight") {
            let arr = data.to_array();
            model.norm_f.weight.apply_update(&(&arr - &model.norm_f.weight.data()));
        }

        // Load output projection
        if let Some(data) = self.weights.get("output.weight") {
            let arr = data.to_array();
            model.output.weight.apply_update(&(&arr - &model.output.weight.data()));
        }
        if let Some(ref bias) = model.output.bias {
            if let Some(data) = self.weights.get("output.bias") {
                let arr = data.to_array();
                bias.apply_update(&(&arr - &bias.data()));
            }
        }

        Ok(())
    }

    fn load_hybrid_block_weights(
        weights: &HashMap<String, TensorData>,
        prefix: &str,
        block: &DifferentiableHybridBlock,
    ) -> Result<(), String> {
        let load = |name: &str, var: &Variable| {
            if let Some(data) = weights.get(name) {
                let arr = data.to_array();
                var.apply_update(&(&arr - &var.data()));
            }
        };

        // Norm1
        load(&format!("{}.norm1.weight", prefix), &block.norm1.weight);

        // Attention (if present)
        if let Some(ref attn) = block.attn {
            load(&format!("{}.attn.q_proj.weight", prefix), &attn.q_proj.weight);
            load(&format!("{}.attn.k_proj.weight", prefix), &attn.k_proj.weight);
            load(&format!("{}.attn.v_proj.weight", prefix), &attn.v_proj.weight);
            load(&format!("{}.attn.out_proj.weight", prefix), &attn.out_proj.weight);
        }

        // SSM (if present)
        if let Some(ref ssm) = block.ssm {
            Self::load_ssm_weights(weights, &format!("{}.ssm", prefix), ssm)?;
        }

        // Norm2
        load(&format!("{}.norm2.weight", prefix), &block.norm2.weight);

        // MLP
        load(&format!("{}.mlp.up_proj.weight", prefix), &block.mlp.up_proj.weight);
        load(&format!("{}.mlp.gate_proj.weight", prefix), &block.mlp.gate_proj.weight);
        load(&format!("{}.mlp.down_proj.weight", prefix), &block.mlp.down_proj.weight);

        Ok(())
    }

    fn load_ssm_weights(
        weights: &HashMap<String, TensorData>,
        prefix: &str,
        ssm: &DifferentiableSSM,
    ) -> Result<(), String> {
        let load = |name: &str, var: &Variable| {
            if let Some(data) = weights.get(name) {
                let arr = data.to_array();
                var.apply_update(&(&arr - &var.data()));
            }
        };

        load(&format!("{}.in_proj.weight", prefix), &ssm.in_proj.weight);
        load(&format!("{}.conv.weight", prefix), &ssm.conv.weight);
        load(&format!("{}.conv.bias", prefix), &ssm.conv.bias);
        load(&format!("{}.out_proj.weight", prefix), &ssm.out_proj.weight);
        load(&format!("{}.a_log", prefix), &ssm.a_log);
        load(&format!("{}.d_param", prefix), &ssm.d_param);
        load(&format!("{}.x_proj.weight", prefix), &ssm.x_proj.weight);
        load(&format!("{}.dt_proj.weight", prefix), &ssm.dt_proj.weight);

        if let Some(ref bias) = ssm.dt_proj.bias {
            load(&format!("{}.dt_proj.bias", prefix), bias);
        }

        Ok(())
    }

    fn load_memory_weights(
        weights: &HashMap<String, TensorData>,
        prefix: &str,
        memory: &DifferentiableMemory,
    ) -> Result<(), String> {
        let load = |name: &str, var: &Variable| {
            if let Some(data) = weights.get(name) {
                let arr = data.to_array();
                var.apply_update(&(&arr - &var.data()));
            }
        };

        load(&format!("{}.key_proj.weight", prefix), &memory.key_proj.weight);
        load(&format!("{}.value_proj.weight", prefix), &memory.value_proj.weight);
        load(&format!("{}.query_proj.weight", prefix), &memory.query_proj.weight);
        load(&format!("{}.out_proj.weight", prefix), &memory.out_proj.weight);
        load(&format!("{}.memory_keys", prefix), &memory.memory_keys);
        load(&format!("{}.memory_values", prefix), &memory.memory_values);

        Ok(())
    }

    /// Save checkpoint to file
    pub fn save<P: AsRef<Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        bincode::serialize_into(writer, self)?;
        Ok(())
    }

    /// Load checkpoint from file
    pub fn load<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        let checkpoint = bincode::deserialize_from(reader)?;
        Ok(checkpoint)
    }

    /// Save as JSON (human-readable)
    pub fn save_json<P: AsRef<Path>>(&self, path: P) -> Result<(), Box<dyn std::error::Error>> {
        let file = File::create(path)?;
        let writer = BufWriter::new(file);
        serde_json::to_writer_pretty(writer, self)?;
        Ok(())
    }

    /// Load from JSON
    pub fn load_json<P: AsRef<Path>>(path: P) -> Result<Self, Box<dyn std::error::Error>> {
        let file = File::open(path)?;
        let reader = BufReader::new(file);
        let checkpoint = serde_json::from_reader(reader)?;
        Ok(checkpoint)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_tensor_data_roundtrip() {
        let arr = Array3::from_shape_fn((2, 3, 4), |(i, j, k)| {
            (i * 12 + j * 4 + k) as f32
        });
        let data = TensorData::from_array(&arr);
        let recovered = data.to_array();
        assert_eq!(arr, recovered);
    }

    #[test]
    fn test_checkpoint_save_load() {
        let config = NexusConfig {
            d_model: 32,
            n_heads: 2,
            layers_per_block: 1,
            vocab_size: 64,
            max_seq_len: 16,
            ..Default::default()
        };

        let model = DifferentiableNexusLM::new(config.clone());
        let checkpoint = ModelCheckpoint::from_model(&model, 100, 0.5);

        // Save and load
        let temp_path = "/tmp/nexus_test_checkpoint.bin";
        checkpoint.save(temp_path).unwrap();

        let loaded = ModelCheckpoint::load(temp_path).unwrap();
        assert_eq!(loaded.step, 100);
        assert_eq!(loaded.loss, 0.5);
        assert_eq!(loaded.config.d_model, 32);

        // Clean up
        std::fs::remove_file(temp_path).ok();
    }

    #[test]
    fn test_checkpoint_load_into_model() {
        let config = NexusConfig {
            d_model: 32,
            n_heads: 2,
            layers_per_block: 1,
            vocab_size: 64,
            max_seq_len: 16,
            ..Default::default()
        };

        // Create and save model
        let model1 = DifferentiableNexusLM::new(config.clone());
        let checkpoint = ModelCheckpoint::from_model(&model1, 50, 1.0);

        // Create new model and load weights
        let model2 = DifferentiableNexusLM::new(config);
        checkpoint.load_into(&model2).unwrap();

        // Verify weights match (using approximate equality for f32)
        let embed1 = model1.embed.data();
        let embed2 = model2.embed.data();

        let max_diff: f32 = embed1.iter()
            .zip(embed2.iter())
            .map(|(a, b)| (a - b).abs())
            .fold(0.0f32, f32::max);

        assert!(max_diff < 1e-6, "Embeddings differ by {}", max_diff);
    }

    #[test]
    fn test_hybrid_checkpoint_save_load() {
        let config = NexusConfig {
            d_model: 32,
            n_heads: 2,
            layers_per_block: 4,  // 4 layers: 1 attn, 3 ssm
            vocab_size: 64,
            max_seq_len: 16,
            memory_size: 8,
            d_state: 8,
            ..Default::default()
        };

        let model = DifferentiableHybridNexusLM::new(config.clone());
        let checkpoint = HybridModelCheckpoint::from_model(&model, 200, 0.75);

        // Save and load
        let temp_path = "/tmp/nexus_hybrid_checkpoint.bin";
        checkpoint.save(temp_path).unwrap();

        let loaded = HybridModelCheckpoint::load(temp_path).unwrap();
        assert_eq!(loaded.step, 200);
        assert_eq!(loaded.loss, 0.75);
        assert_eq!(loaded.config.d_model, 32);
        assert_eq!(loaded.block_types.len(), 4);

        // Verify block types were preserved
        assert_eq!(loaded.block_types, checkpoint.block_types);

        // Clean up
        std::fs::remove_file(temp_path).ok();
    }

    #[test]
    fn test_hybrid_checkpoint_load_into_model() {
        let config = NexusConfig {
            d_model: 32,
            n_heads: 2,
            layers_per_block: 4,
            vocab_size: 64,
            max_seq_len: 16,
            memory_size: 8,
            d_state: 8,
            ..Default::default()
        };

        // Create and checkpoint model
        let model1 = DifferentiableHybridNexusLM::new(config.clone());
        let checkpoint = HybridModelCheckpoint::from_model(&model1, 100, 0.5);

        // Create new model and load weights
        let model2 = DifferentiableHybridNexusLM::new(config);
        checkpoint.load_into(&model2).unwrap();

        // Verify embedding weights match
        let embed1 = model1.embed.data();
        let embed2 = model2.embed.data();

        let max_diff: f32 = embed1.iter()
            .zip(embed2.iter())
            .map(|(a, b)| (a - b).abs())
            .fold(0.0f32, f32::max);

        assert!(max_diff < 1e-6, "Embeddings differ by {}", max_diff);

        // Verify memory weights match
        let mem_keys1 = model1.memory.memory_keys.data();
        let mem_keys2 = model2.memory.memory_keys.data();

        let max_mem_diff: f32 = mem_keys1.iter()
            .zip(mem_keys2.iter())
            .map(|(a, b)| (a - b).abs())
            .fold(0.0f32, f32::max);

        assert!(max_mem_diff < 1e-6, "Memory keys differ by {}", max_mem_diff);

        // Verify SSM weights match (block 1 is SSM)
        let ssm1 = model1.blocks[1].ssm.as_ref().unwrap();
        let ssm2 = model2.blocks[1].ssm.as_ref().unwrap();

        let a_log1 = ssm1.a_log.data();
        let a_log2 = ssm2.a_log.data();

        let max_ssm_diff: f32 = a_log1.iter()
            .zip(a_log2.iter())
            .map(|(a, b)| (a - b).abs())
            .fold(0.0f32, f32::max);

        assert!(max_ssm_diff < 1e-6, "SSM A_log differ by {}", max_ssm_diff);
    }
}
