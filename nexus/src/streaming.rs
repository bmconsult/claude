//! Streaming Token Generation
//!
//! Provides token-by-token generation with callbacks for real-time interfaces.
//! Supports:
//! - Streaming callbacks
//! - Various sampling strategies (greedy, top-k, top-p, temperature)
//! - Stop conditions
//! - Speculative decoding

use std::collections::HashSet;

/// Sampling configuration for generation
#[derive(Clone, Debug)]
pub struct SamplingConfig {
    /// Temperature for softmax (1.0 = normal, <1 = sharper, >1 = flatter)
    pub temperature: f32,
    /// Top-k sampling (0 = disabled)
    pub top_k: usize,
    /// Top-p (nucleus) sampling (1.0 = disabled)
    pub top_p: f32,
    /// Repetition penalty (1.0 = disabled)
    pub repetition_penalty: f32,
    /// Whether to use greedy decoding (ignores temperature/top_k/top_p)
    pub greedy: bool,
    /// Random seed (None = use system entropy)
    pub seed: Option<u64>,
}

impl Default for SamplingConfig {
    fn default() -> Self {
        Self {
            temperature: 1.0,
            top_k: 0,
            top_p: 1.0,
            repetition_penalty: 1.0,
            greedy: false,
            seed: None,
        }
    }
}

impl SamplingConfig {
    /// Greedy decoding
    pub fn greedy() -> Self {
        Self { greedy: true, ..Default::default() }
    }

    /// Temperature sampling
    pub fn with_temperature(temperature: f32) -> Self {
        Self { temperature, ..Default::default() }
    }

    /// Top-k sampling
    pub fn with_top_k(k: usize) -> Self {
        Self { top_k: k, ..Default::default() }
    }

    /// Top-p (nucleus) sampling
    pub fn with_top_p(p: f32) -> Self {
        Self { top_p: p, ..Default::default() }
    }

    /// Combined top-k and top-p
    pub fn with_top_k_p(k: usize, p: f32) -> Self {
        Self { top_k: k, top_p: p, ..Default::default() }
    }
}

/// Stop condition for generation
#[derive(Clone, Debug)]
pub enum StopCondition {
    /// Stop at specific token IDs
    TokenIds(HashSet<u32>),
    /// Stop at maximum length
    MaxLength(usize),
    /// Stop at specific text sequences
    Sequences(Vec<String>),
    /// Custom predicate
    Custom(fn(&[u32], &str) -> bool),
}

impl StopCondition {
    pub fn eos(eos_token_id: u32) -> Self {
        let mut set = HashSet::new();
        set.insert(eos_token_id);
        Self::TokenIds(set)
    }

    pub fn max_tokens(n: usize) -> Self {
        Self::MaxLength(n)
    }
}

/// Token callback type for streaming
pub type TokenCallback = Box<dyn FnMut(u32, &str) -> bool>;

/// Sampler for token selection
pub struct Sampler {
    config: SamplingConfig,
    rng: Option<rand::rngs::StdRng>,
}

impl Sampler {
    pub fn new(config: SamplingConfig) -> Self {
        use rand::SeedableRng;

        let rng = config.seed.map(|s| rand::rngs::StdRng::seed_from_u64(s));

        Self { config, rng }
    }

    /// Sample a token from logits
    pub fn sample(&mut self, logits: &[f32], generated_tokens: &[u32]) -> u32 {
        use rand::Rng;

        let vocab_size = logits.len();

        // Apply repetition penalty
        let mut adjusted_logits = logits.to_vec();
        if self.config.repetition_penalty != 1.0 {
            for &token in generated_tokens {
                let idx = token as usize;
                if idx < vocab_size {
                    if adjusted_logits[idx] > 0.0 {
                        adjusted_logits[idx] /= self.config.repetition_penalty;
                    } else {
                        adjusted_logits[idx] *= self.config.repetition_penalty;
                    }
                }
            }
        }

        // Greedy decoding
        if self.config.greedy {
            return adjusted_logits
                .iter()
                .enumerate()
                .max_by(|(_, a), (_, b)| a.partial_cmp(b).unwrap())
                .map(|(i, _)| i as u32)
                .unwrap_or(0);
        }

        // Apply temperature
        if self.config.temperature != 1.0 && self.config.temperature > 0.0 {
            for logit in &mut adjusted_logits {
                *logit /= self.config.temperature;
            }
        }

        // Get sorted indices by logit value (descending)
        let mut indices: Vec<usize> = (0..vocab_size).collect();
        indices.sort_by(|&a, &b| adjusted_logits[b].partial_cmp(&adjusted_logits[a]).unwrap());

        // Apply top-k
        let top_k = if self.config.top_k > 0 && self.config.top_k < vocab_size {
            self.config.top_k
        } else {
            vocab_size
        };

        // Compute softmax over top-k
        let max_logit = adjusted_logits[indices[0]];
        let mut probs: Vec<(usize, f32)> = indices[..top_k]
            .iter()
            .map(|&i| (i, (adjusted_logits[i] - max_logit).exp()))
            .collect();

        let sum: f32 = probs.iter().map(|(_, p)| p).sum();
        for (_, p) in &mut probs {
            *p /= sum;
        }

        // Apply top-p (nucleus sampling)
        if self.config.top_p < 1.0 {
            let mut cumsum = 0.0;
            let mut cutoff_idx = probs.len();
            for (i, (_, p)) in probs.iter().enumerate() {
                cumsum += p;
                if cumsum >= self.config.top_p {
                    cutoff_idx = i + 1;
                    break;
                }
            }
            probs.truncate(cutoff_idx);

            // Renormalize
            let sum: f32 = probs.iter().map(|(_, p)| p).sum();
            for (_, p) in &mut probs {
                *p /= sum;
            }
        }

        // Sample from distribution
        let sample: f32 = match &mut self.rng {
            Some(rng) => rng.gen(),
            None => rand::thread_rng().gen(),
        };

        // Save the last element before consuming
        let last_idx = probs.last().map(|(idx, _)| *idx as u32).unwrap_or(0);

        let mut cumsum = 0.0;
        for (idx, prob) in probs {
            cumsum += prob;
            if sample <= cumsum {
                return idx as u32;
            }
        }

        last_idx
    }
}

/// Streaming generator state
pub struct StreamingGenerator<M, T>
where
    M: StreamingModel,
    T: Tokenizer,
{
    model: M,
    tokenizer: T,
    sampling_config: SamplingConfig,
    stop_conditions: Vec<StopCondition>,
}

/// Trait for models that support streaming generation
pub trait StreamingModel {
    /// Forward pass returning logits for last token
    /// Should use internal KV cache
    fn forward_one(&mut self, token_id: u32, position: usize) -> Vec<f32>;

    /// Reset/clear the KV cache
    fn reset_cache(&mut self);

    /// Prefill with a sequence of tokens
    fn prefill(&mut self, token_ids: &[u32]) -> Vec<f32>;
}

/// Trait for tokenizers
pub trait Tokenizer {
    fn encode(&self, text: &str) -> Vec<u32>;
    fn decode(&self, tokens: &[u32]) -> String;
    fn decode_single(&self, token: u32) -> String;
}

impl<M, T> StreamingGenerator<M, T>
where
    M: StreamingModel,
    T: Tokenizer,
{
    pub fn new(model: M, tokenizer: T, sampling_config: SamplingConfig) -> Self {
        Self {
            model,
            tokenizer,
            sampling_config,
            stop_conditions: Vec::new(),
        }
    }

    pub fn add_stop_condition(&mut self, condition: StopCondition) {
        self.stop_conditions.push(condition);
    }

    pub fn clear_stop_conditions(&mut self) {
        self.stop_conditions.clear();
    }

    /// Generate tokens with a streaming callback
    ///
    /// The callback receives each token and its text representation.
    /// Return `false` from the callback to stop generation.
    pub fn generate_streaming<F>(
        &mut self,
        prompt: &str,
        max_new_tokens: usize,
        mut callback: F,
    ) -> Vec<u32>
    where
        F: FnMut(u32, &str) -> bool,
    {
        let prompt_tokens = self.tokenizer.encode(prompt);
        self.model.reset_cache();

        // Prefill with prompt
        let mut logits = self.model.prefill(&prompt_tokens);

        let mut generated = prompt_tokens.clone();
        let mut sampler = Sampler::new(self.sampling_config.clone());
        let mut generated_text = String::new();

        for i in 0..max_new_tokens {
            // Sample next token
            let next_token = sampler.sample(&logits, &generated);

            // Decode token
            let token_text = self.tokenizer.decode_single(next_token);
            generated_text.push_str(&token_text);

            // Check stop conditions
            let should_stop = self.check_stop_conditions(&generated, &generated_text, next_token);

            // Callback (before adding to generated so user can see EOS)
            if !callback(next_token, &token_text) {
                break;
            }

            generated.push(next_token);

            if should_stop {
                break;
            }

            // Forward for next token
            let position = prompt_tokens.len() + i;
            logits = self.model.forward_one(next_token, position);
        }

        generated
    }

    /// Generate without streaming (returns all at once)
    pub fn generate(&mut self, prompt: &str, max_new_tokens: usize) -> String {
        let mut output = String::new();

        self.generate_streaming(prompt, max_new_tokens, |_, text| {
            output.push_str(text);
            true
        });

        output
    }

    fn check_stop_conditions(&self, tokens: &[u32], text: &str, last_token: u32) -> bool {
        for condition in &self.stop_conditions {
            match condition {
                StopCondition::TokenIds(ids) => {
                    if ids.contains(&last_token) {
                        return true;
                    }
                }
                StopCondition::MaxLength(max_len) => {
                    if tokens.len() >= *max_len {
                        return true;
                    }
                }
                StopCondition::Sequences(seqs) => {
                    for seq in seqs {
                        if text.ends_with(seq) {
                            return true;
                        }
                    }
                }
                StopCondition::Custom(f) => {
                    if f(tokens, text) {
                        return true;
                    }
                }
            }
        }
        false
    }
}

/// Speculative decoding for faster generation
/// Uses a small draft model to propose tokens, verified by main model
pub struct SpeculativeDecoder<M, D, T>
where
    M: StreamingModel,
    D: StreamingModel,
    T: Tokenizer,
{
    main_model: M,
    draft_model: D,
    tokenizer: T,
    /// Number of tokens to speculate
    speculation_length: usize,
    sampling_config: SamplingConfig,
}

impl<M, D, T> SpeculativeDecoder<M, D, T>
where
    M: StreamingModel,
    D: StreamingModel,
    T: Tokenizer,
{
    pub fn new(
        main_model: M,
        draft_model: D,
        tokenizer: T,
        speculation_length: usize,
        sampling_config: SamplingConfig,
    ) -> Self {
        Self {
            main_model,
            draft_model,
            tokenizer,
            speculation_length,
            sampling_config,
        }
    }

    /// Generate with speculative decoding
    pub fn generate(&mut self, prompt: &str, max_new_tokens: usize) -> Vec<u32> {
        let prompt_tokens = self.tokenizer.encode(prompt);

        self.main_model.reset_cache();
        self.draft_model.reset_cache();

        // Prefill both models
        self.main_model.prefill(&prompt_tokens);
        self.draft_model.prefill(&prompt_tokens);

        let mut generated = prompt_tokens.clone();
        let mut sampler = Sampler::new(self.sampling_config.clone());
        let mut tokens_generated = 0;

        while tokens_generated < max_new_tokens {
            // Draft model proposes tokens
            let mut draft_tokens = Vec::new();
            let mut position = generated.len() - 1;

            for _ in 0..self.speculation_length {
                position += 1;
                let draft_logits = if draft_tokens.is_empty() {
                    self.draft_model.forward_one(*generated.last().unwrap(), position)
                } else {
                    self.draft_model.forward_one(*draft_tokens.last().unwrap(), position)
                };

                let draft_token = sampler.sample(&draft_logits, &generated);
                draft_tokens.push(draft_token);
            }

            // Main model verifies (in parallel if possible)
            // For simplicity, we verify sequentially here
            let mut accepted = 0;
            let base_position = generated.len();

            for (i, &draft_token) in draft_tokens.iter().enumerate() {
                let token_to_forward = if i == 0 {
                    *generated.last().unwrap()
                } else {
                    draft_tokens[i - 1]
                };

                let main_logits = self.main_model.forward_one(token_to_forward, base_position + i);
                let main_token = sampler.sample(&main_logits, &generated);

                if main_token == draft_token {
                    generated.push(draft_token);
                    accepted += 1;
                    tokens_generated += 1;

                    if tokens_generated >= max_new_tokens {
                        break;
                    }
                } else {
                    // Rejection - use main model's token instead
                    generated.push(main_token);
                    tokens_generated += 1;
                    break;
                }
            }

            // If all draft tokens were rejected, just continue with main model's token
            if accepted == 0 && draft_tokens.is_empty() {
                break;
            }
        }

        generated
    }

    /// Get acceptance rate statistics
    pub fn acceptance_rate(&self) -> f32 {
        // Would need to track stats during generation
        // Placeholder
        0.0
    }
}

/// Batch generation for throughput
pub struct BatchGenerator<M, T>
where
    M: StreamingModel,
    T: Tokenizer,
{
    _model: M,
    tokenizer: T,
    sampling_config: SamplingConfig,
}

impl<M, T> BatchGenerator<M, T>
where
    M: StreamingModel,
    T: Tokenizer + Clone,
{
    pub fn new(model: M, tokenizer: T, sampling_config: SamplingConfig) -> Self {
        Self { _model: model, tokenizer, sampling_config }
    }

    /// Generate for multiple prompts
    /// Note: This is a simplified implementation; true batched generation
    /// would require batched forward passes
    pub fn generate_batch(&mut self, prompts: &[&str], max_new_tokens: usize) -> Vec<String> {
        prompts
            .iter()
            .map(|prompt| {
                let mut generator = StreamingGenerator::new(
                    DummyModel,
                    self.tokenizer.clone(),
                    self.sampling_config.clone(),
                );
                generator.generate(prompt, max_new_tokens)
            })
            .collect()
    }
}

// Dummy model for batch generator (real implementation would share the model)
struct DummyModel;
impl StreamingModel for DummyModel {
    fn forward_one(&mut self, _: u32, _: usize) -> Vec<f32> { vec![0.0; 100] }
    fn reset_cache(&mut self) {}
    fn prefill(&mut self, _: &[u32]) -> Vec<f32> { vec![0.0; 100] }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_sampling_config() {
        let greedy = SamplingConfig::greedy();
        assert!(greedy.greedy);

        let temp = SamplingConfig::with_temperature(0.7);
        assert_eq!(temp.temperature, 0.7);

        let top_k = SamplingConfig::with_top_k(50);
        assert_eq!(top_k.top_k, 50);

        let top_p = SamplingConfig::with_top_p(0.9);
        assert_eq!(top_p.top_p, 0.9);
    }

    #[test]
    fn test_sampler_greedy() {
        let config = SamplingConfig::greedy();
        let mut sampler = Sampler::new(config);

        let logits = vec![1.0, 5.0, 2.0, 3.0]; // Max at index 1
        let token = sampler.sample(&logits, &[]);
        assert_eq!(token, 1);
    }

    #[test]
    fn test_sampler_with_temperature() {
        let config = SamplingConfig {
            temperature: 0.1, // Very low temperature -> almost greedy
            seed: Some(42),
            ..Default::default()
        };
        let mut sampler = Sampler::new(config);

        let logits = vec![1.0, 10.0, 2.0, 3.0]; // Strong peak at index 1
        let token = sampler.sample(&logits, &[]);
        assert_eq!(token, 1); // Should almost always pick the max
    }

    #[test]
    fn test_sampler_top_k() {
        let config = SamplingConfig {
            top_k: 2,
            seed: Some(42),
            ..Default::default()
        };
        let mut sampler = Sampler::new(config);

        let logits = vec![1.0, 10.0, 9.0, 0.5]; // Top 2 are indices 1 and 2

        // Sample multiple times - should only see 1 or 2
        for _ in 0..10 {
            let token = sampler.sample(&logits, &[]);
            assert!(token == 1 || token == 2, "Got token {}", token);
        }
    }

    #[test]
    fn test_sampler_top_p() {
        let config = SamplingConfig {
            top_p: 0.5,
            seed: Some(42),
            ..Default::default()
        };
        let mut sampler = Sampler::new(config);

        // Create logits where first token has >50% probability after softmax
        let logits = vec![10.0, 1.0, 1.0, 1.0];

        // With top_p=0.5, should mostly pick token 0
        let mut count_0 = 0;
        for _ in 0..20 {
            if sampler.sample(&logits, &[]) == 0 {
                count_0 += 1;
            }
        }
        assert!(count_0 > 15, "Expected mostly token 0, got {} out of 20", count_0);
    }

    #[test]
    fn test_sampler_repetition_penalty() {
        let config = SamplingConfig {
            repetition_penalty: 2.0, // Strong penalty
            greedy: true,
            ..Default::default()
        };
        let mut sampler = Sampler::new(config);

        let logits = vec![5.0, 4.9, 4.8, 4.7]; // Close values

        // Without history, should pick 0
        assert_eq!(sampler.sample(&logits, &[]), 0);

        // With 0 in history, should pick something else
        let token = sampler.sample(&logits, &[0]);
        assert_ne!(token, 0, "Repetition penalty should prevent picking token 0");
    }

    #[test]
    fn test_stop_conditions() {
        let eos_condition = StopCondition::eos(2);
        let max_len_condition = StopCondition::max_tokens(100);

        match eos_condition {
            StopCondition::TokenIds(ids) => assert!(ids.contains(&2)),
            _ => panic!("Wrong type"),
        }

        match max_len_condition {
            StopCondition::MaxLength(n) => assert_eq!(n, 100),
            _ => panic!("Wrong type"),
        }
    }

    // Test with mock model and tokenizer
    struct MockModel {
        vocab_size: usize,
        call_count: usize,
    }

    impl StreamingModel for MockModel {
        fn forward_one(&mut self, _: u32, _: usize) -> Vec<f32> {
            self.call_count += 1;
            // Return logits that favor token 1
            let mut logits = vec![0.0; self.vocab_size];
            logits[1] = 10.0;
            logits
        }

        fn reset_cache(&mut self) {
            self.call_count = 0;
        }

        fn prefill(&mut self, tokens: &[u32]) -> Vec<f32> {
            self.call_count += tokens.len();
            let mut logits = vec![0.0; self.vocab_size];
            logits[1] = 10.0;
            logits
        }
    }

    #[derive(Clone)]
    struct MockTokenizer;

    impl Tokenizer for MockTokenizer {
        fn encode(&self, text: &str) -> Vec<u32> {
            text.chars().map(|c| c as u32 % 100).collect()
        }

        fn decode(&self, tokens: &[u32]) -> String {
            tokens.iter().map(|&t| (t as u8 as char)).collect()
        }

        fn decode_single(&self, token: u32) -> String {
            String::from(token as u8 as char)
        }
    }

    #[test]
    fn test_streaming_generator() {
        let model = MockModel { vocab_size: 100, call_count: 0 };
        let tokenizer = MockTokenizer;
        let config = SamplingConfig::greedy();

        let mut generator = StreamingGenerator::new(model, tokenizer, config);
        generator.add_stop_condition(StopCondition::max_tokens(5));

        let mut tokens_received = Vec::new();
        generator.generate_streaming("hi", 3, |token, _| {
            tokens_received.push(token);
            true
        });

        assert_eq!(tokens_received.len(), 3);
        assert!(tokens_received.iter().all(|&t| t == 1)); // Mock always returns token 1
    }
}
