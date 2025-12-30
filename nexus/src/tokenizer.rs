//! Tokenizer module for text processing
//!
//! Wraps HuggingFace tokenizers for converting text to token IDs and back.

use anyhow::Result;
use tokenizers::Tokenizer as HFTokenizer;

/// Wrapper around HuggingFace tokenizers
pub struct Tokenizer {
    inner: HFTokenizer,
    vocab_size: usize,
}

impl Tokenizer {
    /// Load tokenizer from a local JSON file (standard HuggingFace format)
    ///
    /// To get a tokenizer file, download from HuggingFace:
    /// ```bash
    /// curl -L https://huggingface.co/gpt2/resolve/main/tokenizer.json -o tokenizer.json
    /// ```
    pub fn from_file(path: &str) -> Result<Self> {
        let inner = HFTokenizer::from_file(path)
            .map_err(|e| anyhow::anyhow!("Failed to load tokenizer from {}: {}", path, e))?;

        let vocab_size = inner.get_vocab_size(true);

        Ok(Self { inner, vocab_size })
    }

    /// Load tokenizer from bytes (for embedding in binary)
    pub fn from_bytes(bytes: &[u8]) -> Result<Self> {
        let inner = HFTokenizer::from_bytes(bytes)
            .map_err(|e| anyhow::anyhow!("Failed to load tokenizer from bytes: {}", e))?;

        let vocab_size = inner.get_vocab_size(true);

        Ok(Self { inner, vocab_size })
    }

    /// Encode text to token IDs
    pub fn encode(&self, text: &str) -> Result<Vec<u32>> {
        let encoding = self.inner.encode(text, false)
            .map_err(|e| anyhow::anyhow!("Encoding failed: {}", e))?;

        Ok(encoding.get_ids().to_vec())
    }

    /// Encode with special tokens (BOS, EOS, etc.)
    pub fn encode_with_special(&self, text: &str) -> Result<Vec<u32>> {
        let encoding = self.inner.encode(text, true)
            .map_err(|e| anyhow::anyhow!("Encoding failed: {}", e))?;

        Ok(encoding.get_ids().to_vec())
    }

    /// Decode token IDs back to text
    pub fn decode(&self, ids: &[u32]) -> Result<String> {
        self.inner.decode(ids, true)
            .map_err(|e| anyhow::anyhow!("Decoding failed: {}", e))
    }

    /// Get vocabulary size
    pub fn vocab_size(&self) -> usize {
        self.vocab_size
    }

    /// Encode a batch of texts
    pub fn encode_batch(&self, texts: &[&str]) -> Result<Vec<Vec<u32>>> {
        let encodings = self.inner.encode_batch(texts.to_vec(), false)
            .map_err(|e| anyhow::anyhow!("Batch encoding failed: {}", e))?;

        Ok(encodings.iter().map(|e| e.get_ids().to_vec()).collect())
    }

    /// Pad sequences to the same length
    pub fn pad_sequences(&self, sequences: Vec<Vec<u32>>, pad_id: u32) -> Vec<Vec<u32>> {
        let max_len = sequences.iter().map(|s| s.len()).max().unwrap_or(0);

        sequences.into_iter()
            .map(|mut seq| {
                seq.resize(max_len, pad_id);
                seq
            })
            .collect()
    }
}

/// Simple BPE tokenizer built from scratch (no pretrained required)
pub struct SimpleBPE {
    vocab: std::collections::HashMap<String, u32>,
    reverse_vocab: std::collections::HashMap<u32, String>,
    next_id: u32,
}

impl SimpleBPE {
    /// Create a new simple character-level tokenizer
    pub fn new() -> Self {
        let mut vocab = std::collections::HashMap::new();
        let mut reverse_vocab = std::collections::HashMap::new();

        // Initialize with ASCII printable characters + special tokens
        let mut next_id = 0u32;

        // Special tokens
        for special in ["<pad>", "<unk>", "<bos>", "<eos>"] {
            vocab.insert(special.to_string(), next_id);
            reverse_vocab.insert(next_id, special.to_string());
            next_id += 1;
        }

        // ASCII characters
        for c in 32u8..127 {
            let s = (c as char).to_string();
            vocab.insert(s.clone(), next_id);
            reverse_vocab.insert(next_id, s);
            next_id += 1;
        }

        Self { vocab, reverse_vocab, next_id }
    }

    /// Get token ID, using <unk> for unknown characters
    pub fn encode(&self, text: &str) -> Vec<u32> {
        text.chars()
            .map(|c| {
                *self.vocab.get(&c.to_string())
                    .unwrap_or(&1) // 1 = <unk>
            })
            .collect()
    }

    /// Decode token IDs to text
    pub fn decode(&self, ids: &[u32]) -> String {
        ids.iter()
            .filter_map(|id| self.reverse_vocab.get(id))
            .cloned()
            .collect()
    }

    /// Get vocabulary size
    pub fn vocab_size(&self) -> usize {
        self.vocab.len()
    }

    /// Get special token IDs
    pub fn pad_id(&self) -> u32 { 0 }
    pub fn unk_id(&self) -> u32 { 1 }
    pub fn bos_id(&self) -> u32 { 2 }
    pub fn eos_id(&self) -> u32 { 3 }
}

impl Default for SimpleBPE {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_simple_bpe() {
        let tokenizer = SimpleBPE::new();

        let text = "Hello, World!";
        let tokens = tokenizer.encode(text);
        let decoded = tokenizer.decode(&tokens);

        assert_eq!(text, decoded);
    }

    #[test]
    fn test_simple_bpe_special_tokens() {
        let tokenizer = SimpleBPE::new();

        assert_eq!(tokenizer.pad_id(), 0);
        assert_eq!(tokenizer.unk_id(), 1);
        assert_eq!(tokenizer.bos_id(), 2);
        assert_eq!(tokenizer.eos_id(), 3);
    }

    #[test]
    fn test_simple_bpe_vocab_size() {
        let tokenizer = SimpleBPE::new();
        // 4 special tokens + 95 printable ASCII chars
        assert_eq!(tokenizer.vocab_size(), 99);
    }
}
