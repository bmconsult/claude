//! Train the JEPA-style World Model
//!
//! Demonstrates self-supervised learning by predicting in latent space:
//! - Encode current state to latent representation
//! - Predict next latent from current latent + context
//! - Compare prediction to actual next latent (with stop-gradient)
//!
//! Usage: cargo run --example train_world_model --release

use std::time::Instant;
use ndarray::Array3;
use nexus::{
    DifferentiableWorldModel, MaskStrategy,
    AdamW, Optimizer,
    autograd::Variable,
};

fn main() {
    println!("═══════════════════════════════════════════════════════════════");
    println!("       JEPA-style World Model Training");
    println!("═══════════════════════════════════════════════════════════════");

    // Configuration
    let d_input = 64;      // Input dimension
    let d_model = 128;     // Latent dimension
    let d_hidden = 256;    // Predictor hidden dimension
    let n_encoder_layers = 3;

    // Create world model
    let world_model = DifferentiableWorldModel::new(d_input, d_model, d_hidden, n_encoder_layers);
    let n_params = world_model.num_parameters();

    println!("\nModel Configuration:");
    println!("  d_input: {}", d_input);
    println!("  d_model (latent): {}", d_model);
    println!("  d_hidden: {}", d_hidden);
    println!("  encoder_layers: {}", n_encoder_layers);
    println!("  parameters: {}", n_params);

    // Create optimizer
    let lr = 1e-3;
    let mut optimizer = AdamW::new(lr, 0.01);

    // Training parameters
    let n_epochs = 100;
    let batch_size = 4;
    let seq_len = 16;

    // Masking strategy for JEPA training
    let mask_strategy = MaskStrategy::Causal;

    println!("\nTraining Configuration:");
    println!("  epochs: {}", n_epochs);
    println!("  batch_size: {}", batch_size);
    println!("  seq_len: {}", seq_len);
    println!("  mask: {:?}", mask_strategy);

    println!("\nStarting training...\n");

    let start_time = Instant::now();
    let mut total_samples = 0;

    for epoch in 0..n_epochs {
        let mut epoch_loss = 0.0f32;
        let mut n_batches = 0;

        // Simulate batches of sequential data
        for _ in 0..8 {
            // Generate synthetic sequential data
            // In practice, this would be real embeddings from text/images
            let data = generate_sequential_data(batch_size, seq_len + 1, d_input);

            // Split into current and next timesteps (both same length)
            let x_t = data.slice(ndarray::s![.., ..seq_len, ..]).to_owned();
            let x_next = data.slice(ndarray::s![.., 1..seq_len+1, ..]).to_owned();

            // Convert to Variables
            let x_t_var = Variable::parameter(x_t.clone());
            let x_next_var = Variable::parameter(x_next);

            // Create context by encoding a shifted version
            // (in practice, context could be anything - position, global features, etc.)
            let context_input = compute_context(&x_t);
            let context_var = Variable::parameter(context_input);
            // Encode context to latent space (same dimension as z)
            let context_encoded = world_model.encode(&context_var);

            // Zero gradients
            world_model.zero_grad();

            // Forward pass: encode x_t, predict next latent using encoded context
            let z_t = world_model.encode(&x_t_var);
            let z_pred = world_model.predict(&z_t, &context_encoded);

            // Encode target (with stop gradient)
            let z_target = world_model.encode(&x_next_var).detach();

            // L2 loss in latent space
            let diff = z_pred.sub(&z_target);
            let sq = diff.mul(&diff);
            let loss_var = sq.mean();

            let data = sq.data();
            let loss: f32 = data.iter().sum::<f32>() / data.len() as f32;

            // Backward pass
            loss_var.backward();

            // Update weights
            let params = world_model.parameters();
            for param in &params {
                if let Some(grad) = param.get_grad() {
                    let param_data = param.data();

                    // Gradient clipping
                    let grad_norm: f32 = grad.iter().map(|x| x * x).sum::<f32>().sqrt();
                    let max_norm = 1.0;
                    let clipped_grad = if grad_norm > max_norm {
                        grad.mapv(|x| x * max_norm / grad_norm)
                    } else {
                        grad
                    };

                    // Get update and apply
                    let update = optimizer.get_update(param.id, &clipped_grad, &param_data);
                    param.apply_update(&(-&update));
                }
            }

            epoch_loss += loss;
            n_batches += 1;
            total_samples += batch_size;
        }

        epoch_loss /= n_batches as f32;

        if (epoch + 1) % 10 == 0 || epoch == 0 {
            let elapsed = start_time.elapsed().as_secs_f32();
            let samples_per_sec = total_samples as f32 / elapsed;
            println!(
                "Epoch {:3}/{} | Loss: {:.6} | {:.0} samples/s",
                epoch + 1, n_epochs, epoch_loss, samples_per_sec
            );
        }
    }

    let elapsed = start_time.elapsed().as_secs_f32();

    println!("\n═══════════════════════════════════════════════════════════════");
    println!("   Training complete!");
    println!("   Total time: {:.1}s", elapsed);
    println!("   Total samples: {}", total_samples);
    println!("   Throughput: {:.0} samples/s", total_samples as f32 / elapsed);
    println!("═══════════════════════════════════════════════════════════════");

    // Demonstrate prediction
    println!("\nDemonstrating latent prediction:\n");

    let test_data = generate_sequential_data(1, 8, d_input);
    let x_test = Variable::parameter(test_data.clone());
    let context_input = Variable::parameter(compute_context(&test_data));
    let context_encoded = world_model.encode(&context_input);

    let (z_current, z_predicted) = world_model.forward(&x_test, &context_encoded);

    println!("Input shape: {:?}", x_test.shape());
    println!("Current latent shape: {:?}", z_current.shape());
    println!("Predicted next latent shape: {:?}", z_predicted.shape());

    // Show some latent values
    let z_data = z_current.data();
    let zp_data = z_predicted.data();
    println!("\nCurrent latent (first 4 dims): [{:.3}, {:.3}, {:.3}, {:.3}]",
             z_data[[0, 0, 0]], z_data[[0, 0, 1]], z_data[[0, 0, 2]], z_data[[0, 0, 3]]);
    println!("Predicted latent (first 4 dims): [{:.3}, {:.3}, {:.3}, {:.3}]",
             zp_data[[0, 0, 0]], zp_data[[0, 0, 1]], zp_data[[0, 0, 2]], zp_data[[0, 0, 3]]);

    println!("\nJEPA-style world model training complete!");
}

/// Generate synthetic sequential data with temporal correlation
fn generate_sequential_data(batch: usize, seq_len: usize, d_model: usize) -> Array3<f32> {
    use rand::Rng;
    let mut rng = rand::thread_rng();

    // Start with random initial state
    let mut data = Array3::zeros((batch, seq_len, d_model));

    for b in 0..batch {
        // Initialize first position
        for d in 0..d_model {
            data[[b, 0, d]] = rng.gen::<f32>() * 2.0 - 1.0;
        }

        // Generate sequential data with temporal correlation
        for t in 1..seq_len {
            for d in 0..d_model {
                // 80% previous + 20% new random
                let prev = data[[b, t - 1, d]];
                let noise = rng.gen::<f32>() * 0.5 - 0.25;
                data[[b, t, d]] = 0.8 * prev + 0.2 * (prev + noise);
            }
        }
    }

    data
}

/// Compute context from input (simple sliding average)
fn compute_context(x: &Array3<f32>) -> Array3<f32> {
    let (batch, seq_len, d_model) = x.dim();
    let mut context = Array3::zeros((batch, seq_len, d_model));

    for b in 0..batch {
        for t in 0..seq_len {
            // Use average of past positions as context
            let window_start = t.saturating_sub(3);
            let window_len = (t - window_start + 1) as f32;

            for d in 0..d_model {
                let mut sum = 0.0f32;
                for w in window_start..=t {
                    sum += x[[b, w, d]];
                }
                context[[b, t, d]] = sum / window_len;
            }
        }
    }

    context
}
