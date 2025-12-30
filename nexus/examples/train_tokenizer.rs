//! BPE Tokenizer Training
//!
//! Trains a Byte Pair Encoding tokenizer on a text corpus.
//! BPE provides better compression than byte-level tokenization,
//! leading to faster training and better generalization.
//!
//! Usage: cargo run --example train_tokenizer --release -- [corpus_path] [vocab_size] [output_path]

use std::collections::HashMap;
use std::fs;
use std::io::{BufRead, BufReader, Write};

// ============================================================================
// BPE Tokenizer
// ============================================================================

/// A trained BPE tokenizer
pub struct BPETokenizer {
    /// Maps token strings to IDs
    vocab: HashMap<String, u32>,
    /// Maps IDs back to token strings
    id_to_token: Vec<String>,
    /// Merge rules in order of application
    merges: Vec<(String, String)>,
}

impl BPETokenizer {
    /// Train a BPE tokenizer on the given text
    pub fn train(text: &str, vocab_size: usize, verbose: bool) -> Self {
        // Start with byte-level vocabulary (256 base tokens)
        let mut vocab: HashMap<String, u32> = HashMap::new();
        let mut id_to_token: Vec<String> = Vec::new();

        // Initialize with single bytes
        for i in 0..256u32 {
            let token = format!("{}", i as u8 as char);
            vocab.insert(token.clone(), i);
            id_to_token.push(token);
        }

        // Tokenize text into bytes
        let mut words: Vec<Vec<String>> = text
            .lines()
            .map(|line| {
                let mut word_tokens = Vec::new();
                for c in line.chars() {
                    if (c as u32) < 256 {
                        word_tokens.push(format!("{}", c));
                    }
                }
                word_tokens
            })
            .filter(|w| !w.is_empty())
            .collect();

        let mut merges: Vec<(String, String)> = Vec::new();
        let target_vocab_size = vocab_size.min(50000); // Cap for safety

        if verbose {
            println!("Starting BPE training...");
            println!("  Initial vocab size: {}", vocab.len());
            println!("  Target vocab size:  {}", target_vocab_size);
            println!("  Corpus lines:       {}", words.len());
        }

        // Iteratively merge most common pairs
        while vocab.len() < target_vocab_size {
            // Count all adjacent pairs
            let mut pair_counts: HashMap<(String, String), usize> = HashMap::new();

            for word in &words {
                for i in 0..word.len().saturating_sub(1) {
                    let pair = (word[i].clone(), word[i + 1].clone());
                    *pair_counts.entry(pair).or_insert(0) += 1;
                }
            }

            if pair_counts.is_empty() {
                break;
            }

            // Find most common pair
            let best_pair = pair_counts
                .iter()
                .max_by_key(|(_, count)| *count)
                .map(|(pair, _)| pair.clone());

            let (first, second) = match best_pair {
                Some(p) => p,
                None => break,
            };

            // Create merged token
            let merged = format!("{}{}", first, second);
            let new_id = vocab.len() as u32;
            vocab.insert(merged.clone(), new_id);
            id_to_token.push(merged.clone());
            merges.push((first.clone(), second.clone()));

            // Apply merge to all words
            for word in &mut words {
                let mut i = 0;
                while i < word.len().saturating_sub(1) {
                    if word[i] == first && word[i + 1] == second {
                        word[i] = merged.clone();
                        word.remove(i + 1);
                    } else {
                        i += 1;
                    }
                }
            }

            if verbose && (vocab.len() % 100 == 0 || vocab.len() == target_vocab_size) {
                println!("  Vocab size: {} | Last merge: {} + {} -> {}",
                         vocab.len(), first, second, merged);
            }
        }

        if verbose {
            println!("Training complete!");
            println!("  Final vocab size: {}", vocab.len());
            println!("  Merge rules:      {}", merges.len());
        }

        Self {
            vocab,
            id_to_token,
            merges,
        }
    }

    /// Encode text to token IDs
    pub fn encode(&self, text: &str) -> Vec<u32> {
        // Start with byte-level tokens
        let mut tokens: Vec<String> = text
            .chars()
            .filter(|c| (*c as u32) < 256)
            .map(|c| format!("{}", c))
            .collect();

        // Apply merges in order
        for (first, second) in &self.merges {
            let merged = format!("{}{}", first, second);
            let mut i = 0;
            while i < tokens.len().saturating_sub(1) {
                if &tokens[i] == first && &tokens[i + 1] == second {
                    tokens[i] = merged.clone();
                    tokens.remove(i + 1);
                } else {
                    i += 1;
                }
            }
        }

        // Convert to IDs
        tokens
            .iter()
            .filter_map(|t| self.vocab.get(t).copied())
            .collect()
    }

    /// Decode token IDs to text
    pub fn decode(&self, ids: &[u32]) -> String {
        ids.iter()
            .filter_map(|&id| self.id_to_token.get(id as usize))
            .cloned()
            .collect()
    }

    /// Get vocabulary size
    pub fn vocab_size(&self) -> usize {
        self.vocab.len()
    }

    /// Save tokenizer to file
    pub fn save(&self, path: &str) -> std::io::Result<()> {
        let mut file = fs::File::create(path)?;

        // Write vocab size
        writeln!(file, "{}", self.vocab.len())?;

        // Write each token (escaped)
        for token in &self.id_to_token {
            let escaped = token
                .replace('\\', "\\\\")
                .replace('\n', "\\n")
                .replace('\r', "\\r")
                .replace('\t', "\\t");
            writeln!(file, "{}", escaped)?;
        }

        // Write number of merges
        writeln!(file, "{}", self.merges.len())?;

        // Write merges
        for (first, second) in &self.merges {
            let first_escaped = first
                .replace('\\', "\\\\")
                .replace('\n', "\\n")
                .replace(' ', "\\s");
            let second_escaped = second
                .replace('\\', "\\\\")
                .replace('\n', "\\n")
                .replace(' ', "\\s");
            writeln!(file, "{} {}", first_escaped, second_escaped)?;
        }

        Ok(())
    }

    /// Load tokenizer from file
    pub fn load(path: &str) -> std::io::Result<Self> {
        let file = fs::File::open(path)?;
        let reader = BufReader::new(file);
        let mut lines = reader.lines();

        // Read vocab size
        let vocab_size: usize = lines
            .next()
            .ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData, "Empty file"))??
            .parse()
            .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

        // Read tokens
        let mut vocab = HashMap::new();
        let mut id_to_token = Vec::new();

        for i in 0..vocab_size {
            let line = lines
                .next()
                .ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData, "Unexpected EOF"))??;
            let token = line
                .replace("\\n", "\n")
                .replace("\\r", "\r")
                .replace("\\t", "\t")
                .replace("\\\\", "\\");
            vocab.insert(token.clone(), i as u32);
            id_to_token.push(token);
        }

        // Read number of merges
        let num_merges: usize = lines
            .next()
            .ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData, "Missing merge count"))??
            .parse()
            .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

        // Read merges
        let mut merges = Vec::new();
        for _ in 0..num_merges {
            let line = lines
                .next()
                .ok_or_else(|| std::io::Error::new(std::io::ErrorKind::InvalidData, "Missing merge"))??;
            let parts: Vec<&str> = line.split(' ').collect();
            if parts.len() >= 2 {
                let first = parts[0]
                    .replace("\\s", " ")
                    .replace("\\n", "\n")
                    .replace("\\\\", "\\");
                let second = parts[1]
                    .replace("\\s", " ")
                    .replace("\\n", "\n")
                    .replace("\\\\", "\\");
                merges.push((first, second));
            }
        }

        Ok(Self {
            vocab,
            id_to_token,
            merges,
        })
    }
}

// ============================================================================
// Statistics
// ============================================================================

fn compute_compression_ratio(tokenizer: &BPETokenizer, text: &str) -> f32 {
    let original_bytes = text.len();
    let token_count = tokenizer.encode(text).len();
    original_bytes as f32 / token_count as f32
}

// ============================================================================
// Main
// ============================================================================

fn main() -> anyhow::Result<()> {
    println!("╔═══════════════════════════════════════════════════════════════════╗");
    println!("║                   BPE TOKENIZER TRAINING                          ║");
    println!("╚═══════════════════════════════════════════════════════════════════╝\n");

    // Parse args
    let args: Vec<String> = std::env::args().collect();

    let corpus_path = args.get(1)
        .map(|s| s.as_str())
        .unwrap_or("data/shakespeare.txt");
    let vocab_size: usize = args.get(2)
        .and_then(|s| s.parse().ok())
        .unwrap_or(1000);
    let output_path = args.get(3)
        .map(|s| s.as_str())
        .unwrap_or("data/tokenizer.bpe");

    // Load corpus
    println!("📂 Loading corpus from {}...", corpus_path);
    let text = fs::read_to_string(corpus_path)?;
    println!("   {} characters loaded\n", text.len());

    // Train tokenizer
    println!("🔧 Training BPE tokenizer with vocab size {}...\n", vocab_size);
    let tokenizer = BPETokenizer::train(&text, vocab_size, true);

    // Compute statistics
    println!("\n📊 Tokenizer Statistics:");
    println!("   Vocabulary size:    {}", tokenizer.vocab_size());
    println!("   Merge rules:        {}", tokenizer.merges.len());

    let compression = compute_compression_ratio(&tokenizer, &text);
    println!("   Compression ratio:  {:.2}x", compression);
    println!("   Bytes per token:    {:.2}", compression);

    // Test encoding/decoding
    let test_text = "To be, or not to be, that is the question.";
    let encoded = tokenizer.encode(test_text);
    let decoded = tokenizer.decode(&encoded);

    println!("\n📝 Test encoding:");
    println!("   Original:  \"{}\"", test_text);
    println!("   Tokens:    {} (was {} bytes)", encoded.len(), test_text.len());
    println!("   Decoded:   \"{}\"", decoded);
    println!("   Match:     {}", if test_text == decoded { "✓" } else { "✗" });

    // Save tokenizer
    println!("\n💾 Saving tokenizer to {}...", output_path);
    tokenizer.save(output_path)?;
    println!("   ✓ Saved successfully!");

    // Test loading
    println!("\n🔄 Testing load...");
    let loaded = BPETokenizer::load(output_path)?;
    let loaded_encoded = loaded.encode(test_text);
    let loaded_decoded = loaded.decode(&loaded_encoded);
    println!("   Loaded vocab size: {}", loaded.vocab_size());
    println!("   Encode/decode:     {}", if loaded_decoded == test_text { "✓" } else { "✗" });

    println!("\n✅ Tokenizer training complete!");
    println!("\n   To use in training:");
    println!("   1. Load with BPETokenizer::load(\"{}\")", output_path);
    println!("   2. Use tokenizer.encode(text) for tokenization");
    println!("   3. Set vocab_size={} in training config", tokenizer.vocab_size());

    Ok(())
}
