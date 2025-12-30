//! Tokenizer module for text processing
//!
//! Supports multiple tokenizer backends:
//! - HuggingFace tokenizers (from JSON files)
//! - Tiktoken (GPT-4/cl100k_base compatible)
//! - SimpleBPE (character-level, no pretrained required)

use anyhow::Result;
use tokenizers::Tokenizer as HFTokenizer;
use tiktoken_rs::CoreBPE;

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

/// Tiktoken-based BPE tokenizer (GPT-4 compatible)
///
/// Uses the cl100k_base encoding by default, which is used by GPT-4, GPT-3.5-turbo,
/// and text-embedding-ada-002.
pub struct TiktokenBPE {
    encoder: CoreBPE,
    name: String,
}

impl TiktokenBPE {
    /// Create a new tiktoken tokenizer with cl100k_base encoding (GPT-4)
    pub fn cl100k_base() -> Result<Self> {
        let encoder = tiktoken_rs::cl100k_base()
            .map_err(|e| anyhow::anyhow!("Failed to load cl100k_base: {}", e))?;
        Ok(Self {
            encoder,
            name: "cl100k_base".to_string(),
        })
    }

    /// Create a new tiktoken tokenizer with p50k_base encoding (GPT-3/Codex)
    pub fn p50k_base() -> Result<Self> {
        let encoder = tiktoken_rs::p50k_base()
            .map_err(|e| anyhow::anyhow!("Failed to load p50k_base: {}", e))?;
        Ok(Self {
            encoder,
            name: "p50k_base".to_string(),
        })
    }

    /// Create a new tiktoken tokenizer with r50k_base encoding (GPT-2)
    pub fn r50k_base() -> Result<Self> {
        let encoder = tiktoken_rs::r50k_base()
            .map_err(|e| anyhow::anyhow!("Failed to load r50k_base: {}", e))?;
        Ok(Self {
            encoder,
            name: "r50k_base".to_string(),
        })
    }

    /// Create a new tiktoken tokenizer with o200k_base encoding (GPT-4o)
    pub fn o200k_base() -> Result<Self> {
        let encoder = tiktoken_rs::o200k_base()
            .map_err(|e| anyhow::anyhow!("Failed to load o200k_base: {}", e))?;
        Ok(Self {
            encoder,
            name: "o200k_base".to_string(),
        })
    }

    /// Get the encoding name
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Encode text to token IDs
    pub fn encode(&self, text: &str) -> Vec<u32> {
        self.encoder.encode_ordinary(text)
            .into_iter()
            .map(|id| id as u32)
            .collect()
    }

    /// Encode with special tokens allowed
    pub fn encode_with_special(&self, text: &str, allowed_special: &[&str]) -> Vec<u32> {
        let special_set: std::collections::HashSet<&str> = allowed_special.iter().copied().collect();
        let (tokens, _byte_count) = self.encoder.encode(text, &special_set);
        tokens
    }

    /// Decode token IDs back to text
    pub fn decode(&self, ids: &[u32]) -> Result<String> {
        self.encoder.decode(ids.to_vec())
            .map_err(|e| anyhow::anyhow!("Decoding failed: {}", e))
    }

    /// Get vocabulary size
    pub fn vocab_size(&self) -> usize {
        match self.name.as_str() {
            "cl100k_base" => 100277,
            "p50k_base" => 50281,
            "r50k_base" => 50257,
            "o200k_base" => 200019,
            _ => 100000, // fallback
        }
    }

    /// Encode a batch of texts
    pub fn encode_batch(&self, texts: &[&str]) -> Vec<Vec<u32>> {
        texts.iter()
            .map(|text| self.encode(text))
            .collect()
    }

    /// Count tokens in text (useful for context length checks)
    pub fn count_tokens(&self, text: &str) -> usize {
        self.encoder.encode_ordinary(text).len()
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

    #[test]
    fn test_tiktoken_cl100k() {
        let tokenizer = TiktokenBPE::cl100k_base().unwrap();

        let text = "Hello, world!";
        let tokens = tokenizer.encode(text);
        let decoded = tokenizer.decode(&tokens).unwrap();

        assert_eq!(text, decoded);
        assert_eq!(tokenizer.name(), "cl100k_base");
    }

    #[test]
    fn test_tiktoken_count_tokens() {
        let tokenizer = TiktokenBPE::cl100k_base().unwrap();

        // "Hello" is typically 1 token, ", world!" is a few more
        let count = tokenizer.count_tokens("Hello, world!");
        assert!(count > 0 && count < 10);
    }

    #[test]
    fn test_tiktoken_batch_encode() {
        let tokenizer = TiktokenBPE::cl100k_base().unwrap();

        let texts = vec!["Hello", "World", "Test"];
        let batch = tokenizer.encode_batch(&texts);

        assert_eq!(batch.len(), 3);
        for tokens in batch {
            assert!(!tokens.is_empty());
        }
    }

    #[test]
    fn test_tiktoken_vocab_sizes() {
        assert_eq!(TiktokenBPE::cl100k_base().unwrap().vocab_size(), 100277);
        assert_eq!(TiktokenBPE::p50k_base().unwrap().vocab_size(), 50281);
        assert_eq!(TiktokenBPE::r50k_base().unwrap().vocab_size(), 50257);
    }
}
