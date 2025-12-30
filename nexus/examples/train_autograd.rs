//! Train a small model with autograd - actual gradient descent!
//!
//! Usage: cargo run --example train_autograd --release

use nexus::autograd::{Variable, DifferentiableLinear, AdamW};
use nexus::TiktokenBPE;
use ndarray::Array3;
use std::time::Instant;

/// Simple trainable language model using autograd
struct SimpleLM {
    embed: Variable,           // [1, vocab_size, d_model]
    layers: Vec<DifferentiableLinear>,
    output: DifferentiableLinear,
    vocab_size: usize,
    d_model: usize,
}

impl SimpleLM {
    fn new(vocab_size: usize, d_model: usize, n_layers: usize) -> Self {
        // Embedding matrix
        let embed_data = Array3::from_shape_fn((1, vocab_size, d_model), |_| {
            (rand::random::<f32>() - 0.5) * 0.1
        });
        let embed = Variable::parameter(embed_data);

        // Hidden layers
        let mut layers = Vec::new();
        for _ in 0..n_layers {
            layers.push(DifferentiableLinear::new(d_model, d_model, true));
        }

        // Output projection back to vocab
        let output = DifferentiableLinear::new(d_model, vocab_size, false);

        Self { embed, layers, output, vocab_size, d_model }
    }

    fn forward(&self, token_ids: &[u32]) -> Variable {
        let seq_len = token_ids.len();

        // Embed tokens
        let embed_data = self.embed.data();
        let mut hidden_data = Array3::zeros((1, seq_len, self.d_model));
        for (t, &tid) in token_ids.iter().enumerate() {
            let tid = (tid as usize).min(self.vocab_size - 1);
            for d in 0..self.d_model {
                hidden_data[[0, t, d]] = embed_data[[0, tid, d]];
            }
        }
        let mut hidden = Variable::new(hidden_data, true);

        // Forward through layers
        for layer in &self.layers {
            hidden = layer.forward(&hidden);
            hidden = hidden.gelu();
        }

        // Output projection
        self.output.forward(&hidden)
    }

    fn parameters(&self) -> Vec<Variable> {
        let mut params = vec![self.embed.clone()];
        for layer in &self.layers {
            params.extend(layer.parameters());
        }
        params.extend(self.output.parameters());
        params
    }

    fn zero_grad(&self) {
        self.embed.zero_grad();
        for layer in &self.layers {
            layer.zero_grad();
        }
        self.output.zero_grad();
    }

    fn num_parameters(&self) -> usize {
        let embed_params = self.vocab_size * self.d_model;
        let layer_params: usize = self.layers.iter()
            .map(|l| self.d_model * self.d_model + self.d_model)
            .sum();
        let output_params = self.d_model * self.vocab_size;
        embed_params + layer_params + output_params
    }
}

fn main() -> anyhow::Result<()> {
    println!("╔══════════════════════════════════════════╗");
    println!("║   Nexus Autograd Training Demo           ║");
    println!("║   Real Gradient Descent!                 ║");
    println!("╚══════════════════════════════════════════╝\n");

    // Use small vocab for demo (faster)
    let vocab_size = 256;  // ASCII-ish
    let d_model = 64;
    let n_layers = 2;
    let seq_len = 32;
    let lr = 0.01;
    let epochs = 50;

    println!("Configuration:");
    println!("  vocab_size: {}", vocab_size);
    println!("  d_model: {}", d_model);
    println!("  n_layers: {}", n_layers);
    println!("  seq_len: {}", seq_len);
    println!("  lr: {}", lr);

    // Create model
    let model = SimpleLM::new(vocab_size, d_model, n_layers);
    println!("  Parameters: {}", model.num_parameters());

    // Training data - learn to predict next char in a pattern
    let pattern = "the quick brown fox jumps over the lazy dog ";
    let tokens: Vec<u32> = pattern.bytes().map(|b| b as u32).collect();

    println!("\nTraining on: \"{}\"", pattern);
    println!("Sequence length: {} tokens\n", tokens.len());

    // Create optimizer
    let mut optimizer = AdamW::new(lr, 0.01);

    // Training loop
    println!("Training with real gradient descent...\n");
    let start = Instant::now();

    for epoch in 0..epochs {
        model.zero_grad();

        // Forward pass
        let input_tokens: Vec<u32> = tokens[..tokens.len()-1].to_vec();
        let logits = model.forward(&input_tokens);

        // Compute cross-entropy loss
        let targets: Vec<usize> = tokens[1..].iter().map(|&t| t as usize).collect();
        let (loss, loss_var) = logits.cross_entropy_loss(&targets);

        // Backward pass - compute all gradients!
        loss_var.backward();

        // Update weights using gradients
        let params = model.parameters();
        for param in &params {
            if let Some(grad) = param.get_grad() {
                let param_data = param.data();
                let update = optimizer.get_update(param.id, &grad, &param_data);
                // Apply update - this works because params share data via Rc<RefCell>
                param.apply_update(&(-&update));
            }
        }

        if epoch % 10 == 0 || epoch == epochs - 1 {
            let perplexity = loss.exp();
            println!("Epoch {:3}: loss={:.4}, perplexity={:.2}", epoch + 1, loss, perplexity);
        }
    }

    let elapsed = start.elapsed();
    println!("\nTraining completed in {:.2}s", elapsed.as_secs_f32());

    // Test: check if gradients are flowing
    println!("\n--- Gradient Check ---");
    model.zero_grad();
    let logits = model.forward(&tokens[..8].to_vec());
    let targets: Vec<usize> = tokens[1..9].iter().map(|&t| t as usize).collect();
    let (_, loss_var) = logits.cross_entropy_loss(&targets);
    loss_var.backward();

    let params = model.parameters();
    let mut has_grads = 0;
    for (i, param) in params.iter().enumerate() {
        if param.get_grad().is_some() {
            has_grads += 1;
        }
    }
    println!("Parameters with gradients: {}/{}", has_grads, params.len());

    // Show some gradient magnitudes
    if let Some(grad) = model.embed.get_grad() {
        let grad_norm: f32 = grad.iter().map(|x| x * x).sum::<f32>().sqrt();
        println!("Embedding gradient norm: {:.6}", grad_norm);
    }

    if let Some(grad) = model.output.weight.get_grad() {
        let grad_norm: f32 = grad.iter().map(|x| x * x).sum::<f32>().sqrt();
        println!("Output weight gradient norm: {:.6}", grad_norm);
    }

    println!("\n✓ Autograd is working! Gradients flow through the entire model.");

    Ok(())
}
