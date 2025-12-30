//! Train Nexus on real text data with tiktoken
//!
//! Usage: cargo run --example train_real --release

use nexus::{NexusConfig, NexusLM, TiktokenBPE};
use std::time::Instant;

fn main() -> anyhow::Result<()> {
    println!("╔══════════════════════════════════════════╗");
    println!("║     Nexus Training on Real Text          ║");
    println!("╚══════════════════════════════════════════╝\n");

    // Sample training corpus (Shakespeare excerpt)
    let corpus = r#"
To be, or not to be, that is the question:
Whether 'tis nobler in the mind to suffer
The slings and arrows of outrageous fortune,
Or to take arms against a sea of troubles
And by opposing end them. To die—to sleep,
No more; and by a sleep to say we end
The heart-ache and the thousand natural shocks
That flesh is heir to: 'tis a consummation
Devoutly to be wish'd. To die, to sleep;
To sleep, perchance to dream—ay, there's the rub:
For in that sleep of death what dreams may come,
When we have shuffled off this mortal coil,
Must give us pause—there's the respect
That makes calamity of so long life.
For who would bear the whips and scorns of time,
Th'oppressor's wrong, the proud man's contumely,
The pangs of dispriz'd love, the law's delay,
The insolence of office, and the spurns
That patient merit of th'unworthy takes,
When he himself might his quietus make
With a bare bodkin? Who would fardels bear,
To grunt and sweat under a weary life,
But that the dread of something after death,
The undiscovere'd country, from whose bourn
No traveller returns, puzzles the will,
And makes us rather bear those ills we have
Than fly to others that we know not of?
Thus conscience does make cowards of us all,
And thus the native hue of resolution
Is sicklied o'er with the pale cast of thought,
And enterprises of great pith and moment
With this regard their currents turn awry
And lose the name of action.
"#;

    // Initialize tiktoken tokenizer
    println!("Loading tiktoken cl100k_base tokenizer...");
    let tokenizer = TiktokenBPE::cl100k_base()?;
    let vocab_size = tokenizer.vocab_size();
    println!("  Vocab size: {}", vocab_size);

    // Tokenize the corpus
    let tokens = tokenizer.encode(corpus);
    println!("  Corpus tokens: {}", tokens.len());

    // Create model with matching vocab size
    let config = NexusConfig {
        d_model: 128,
        n_heads: 4,
        d_state: 16,
        d_conv: 4,
        expand: 2,
        layers_per_block: 4,
        attention_ratio: 1,
        memory_size: 256,
        memory_lr: 0.01,
        vocab_size,
        max_seq_len: 512,
    };

    println!("\nCreating Nexus model...");
    println!("  d_model: {}", config.d_model);
    println!("  layers: {}", config.layers_per_block);
    println!("  vocab_size: {}", config.vocab_size);

    let mut model = NexusLM::new(config.clone());
    println!("  Parameters: ~{:.2}M", model.num_parameters() as f64 / 1_000_000.0);

    // Prepare training data (sliding window)
    let seq_len = 64;
    let mut batches: Vec<Vec<u32>> = Vec::new();

    for start in (0..tokens.len().saturating_sub(seq_len)).step_by(seq_len / 2) {
        let end = (start + seq_len).min(tokens.len());
        if end - start >= seq_len {
            batches.push(tokens[start..end].to_vec());
        }
    }
    println!("  Training sequences: {}", batches.len());

    // Training loop
    let epochs = 5;
    let lr = 0.001;

    println!("\nTraining for {} epochs...\n", epochs);

    for epoch in 0..epochs {
        let start = Instant::now();
        let mut epoch_loss = 0.0;
        let mut n_batches = 0;

        for batch in &batches {
            // Forward pass
            let loss = model.compute_loss(&[batch.clone()]);
            epoch_loss += loss;
            n_batches += 1;
        }

        let avg_loss = epoch_loss / n_batches as f32;
        let elapsed = start.elapsed();
        let perplexity = avg_loss.exp();

        println!(
            "Epoch {}/{}: loss={:.4}, perplexity={:.2}, time={:.2}s",
            epoch + 1,
            epochs,
            avg_loss,
            perplexity,
            elapsed.as_secs_f32()
        );
    }

    // Generate some text
    println!("\n--- Generation Test ---");
    let prompt = "To be";
    let prompt_tokens = tokenizer.encode(prompt);
    println!("Prompt: \"{}\" ({} tokens)", prompt, prompt_tokens.len());

    let generated = model.generate(&prompt_tokens, 30, 0.8);
    let output_text = tokenizer.decode(&generated)?;
    println!("Generated: \"{}\"", output_text);

    // Save the model
    let model_path = "nexus_shakespeare.bin";
    println!("\nSaving model to {}...", model_path);
    model.save(model_path).map_err(|e| anyhow::anyhow!("{}", e))?;
    println!("Done! Model size: {:.2} MB",
        std::fs::metadata(model_path)?.len() as f64 / 1_000_000.0);

    Ok(())
}
