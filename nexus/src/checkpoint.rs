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
    DifferentiableRMSNorm,
};
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
}
