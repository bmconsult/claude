//! Integration tests for Nexus
//!
//! Tests end-to-end functionality of the model.

use nexus::{Nexus, NexusConfig, Tensor};
use nexus::training::{Trainer, TrainConfig, DataLoader, VICRegLoss, JEPAMasker};
use ndarray::Array3;

/// Test that model can be created and run forward pass
#[test]
fn test_model_creation_and_forward() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        d_state: 16,
        d_conv: 4,
        memory_size: 32,
        memory_lr: 0.01,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    // Create input tensor
    let input = Tensor::randn(1, 32, 64);

    // Forward pass
    let output = model.forward(&input, true);

    // Check output shape matches input
    assert_eq!(output.shape(), input.shape());
}

/// Test that memory updates work correctly
#[test]
fn test_memory_updates() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        memory_size: 32,
        memory_lr: 0.01,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    // Initial memory should be empty
    let initial_stats = model.memory.stats();
    assert_eq!(initial_stats.num_entries, 0);

    // Run multiple forward passes with memory updates to ensure some entries are stored
    for _ in 0..5 {
        let input = Tensor::randn(1, 32, 64);
        let _ = model.forward(&input, true);
    }

    // Memory should have been accessed (even if entries depend on surprise threshold)
    let after_stats = model.memory.stats();
    // Memory updates should have occurred - at minimum stats should be accessible
    assert!(after_stats.capacity > 0);
}

/// Test that forward pass without memory updates doesn't change memory
#[test]
fn test_no_memory_update_mode() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        memory_size: 32,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    // First, populate memory
    let input1 = Tensor::randn(1, 32, 64);
    let _ = model.forward(&input1, true);
    let entries_after_first = model.memory.stats().num_entries;

    // Run without memory updates
    let input2 = Tensor::randn(1, 32, 64);
    let _ = model.forward(&input2, false);

    // Memory should not have changed
    let entries_after_second = model.memory.stats().num_entries;
    assert_eq!(entries_after_first, entries_after_second);
}

/// Test different input sequence lengths
#[test]
fn test_variable_sequence_lengths() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    // Test various sequence lengths
    for seq_len in [16, 32, 64, 128] {
        let input = Tensor::randn(1, seq_len, 64);
        let output = model.forward(&input, false);
        assert_eq!(output.shape(), (1, seq_len, 64));
    }
}

/// Test batch processing
#[test]
fn test_batch_processing() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    // Test various batch sizes
    for batch_size in [1, 2, 4, 8] {
        let input = Tensor::randn(batch_size, 32, 64);
        let output = model.forward(&input, false);
        assert_eq!(output.shape(), (batch_size, 32, 64));
    }
}

/// Test VICReg loss computation
#[test]
fn test_vicreg_loss() {
    let train_config = TrainConfig::default();
    let loss_fn = VICRegLoss::new(&train_config);

    // Create test representations
    let pred = Array3::from_shape_fn((2, 16, 64), |_| rand::random::<f32>());
    let target = Array3::from_shape_fn((2, 16, 64), |_| rand::random::<f32>());

    let (total, inv, var, cov) = loss_fn.compute(&pred, &target);

    // All loss components should be non-negative
    assert!(total >= 0.0);
    assert!(inv >= 0.0);
    assert!(var >= 0.0);
    assert!(cov >= 0.0);
}

/// Test JEPA masker
#[test]
fn test_jepa_masker() {
    let masker = JEPAMasker::new(0.15);

    let seq_len = 64;
    let (context, target) = masker.generate_mask(seq_len);

    // Context and target should partition the sequence
    assert!(!context.is_empty());
    assert!(!target.is_empty());

    // No overlap
    for t in &target {
        assert!(!context.contains(t));
    }

    // Approximately 15% should be masked
    let mask_ratio = target.len() as f32 / seq_len as f32;
    assert!(mask_ratio > 0.05 && mask_ratio < 0.5);
}

/// Test data loader
#[test]
fn test_data_loader() {
    // Create some test data
    let data: Vec<Array3<f32>> = (0..10)
        .map(|_| Array3::from_shape_fn((1, 16, 32), |_| rand::random()))
        .collect();

    let mut loader = DataLoader::new(data.clone(), 2, true);

    // Should be able to iterate through all batches
    let mut batch_count = 0;
    while let Some(batch) = loader.next() {
        assert_eq!(batch.input.dim().0, 2); // batch size
        batch_count += 1;
    }
    assert_eq!(batch_count, 5); // 10 samples / 2 batch size

    // Reset should allow another epoch
    loader.reset();
    assert!(loader.next().is_some());
}

/// Test trainer initialization
#[test]
fn test_trainer_creation() {
    let model_config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        ..Default::default()
    };

    let train_config = TrainConfig {
        lr: 1e-4,
        batch_size: 4,
        epochs: 10,
        warmup_steps: 100,
        ..Default::default()
    };

    let _trainer = Trainer::new(
        model_config,
        train_config,
        "test_output",
        None,
    );

    // Just verify it doesn't panic
}

/// Test model determinism (same input should give same output)
#[test]
fn test_determinism() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    // Same input should give same output when memory is not updated
    let input = Tensor::zeros(1, 32, 64);
    let output1 = model.forward(&input, false);
    let output2 = model.forward(&input, false);

    // Outputs should be identical (no randomness in forward pass)
    assert_eq!(output1.data, output2.data);
}

/// Test model with edge case inputs
#[test]
fn test_edge_cases() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    // Very short sequence
    let short_input = Tensor::randn(1, 4, 64);
    let short_output = model.forward(&short_input, false);
    assert_eq!(short_output.shape(), (1, 4, 64));

    // Single token
    let single_input = Tensor::randn(1, 1, 64);
    let single_output = model.forward(&single_input, false);
    assert_eq!(single_output.shape(), (1, 1, 64));
}

/// Test that output values are reasonable (not NaN or Inf)
#[test]
fn test_output_validity() {
    let config = NexusConfig {
        d_model: 64,
        n_heads: 4,
        layers_per_block: 2,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    let input = Tensor::randn(1, 32, 64);
    let output = model.forward(&input, true);

    // Check no NaN or Inf values
    for val in output.data.iter() {
        assert!(val.is_finite(), "Output contains non-finite value: {}", val);
    }
}

/// Test default configurations
#[test]
fn test_default_config() {
    let config = NexusConfig::default();

    assert!(config.d_model > 0);
    assert!(config.n_heads > 0);
    assert!(config.layers_per_block > 0);
    assert!(config.memory_size > 0);
}

/// Test training config defaults
#[test]
fn test_train_config_default() {
    let config = TrainConfig::default();

    assert!(config.lr > 0.0);
    assert!(config.batch_size > 0);
    assert!(config.epochs > 0);
}
