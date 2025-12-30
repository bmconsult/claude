//! KV-Cache for Efficient Autoregressive Inference
//!
//! Stores past key/value states to avoid recomputation during generation.
//! Supports:
//! - Dynamic sequence growth
//! - Multi-layer caching
//! - Memory-efficient sliding window (optional)
//! - Batch inference with different sequence lengths

use ndarray::{Array3, Array4, Axis, s};

/// KV-Cache for a single attention layer
#[derive(Clone)]
pub struct LayerKVCache {
    /// Cached keys: [batch, n_heads, cached_len, head_dim]
    keys: Option<Array4<f32>>,
    /// Cached values: [batch, n_heads, cached_len, head_dim]
    values: Option<Array4<f32>>,
    /// Current cached length
    cached_len: usize,
    /// Maximum cache size (for sliding window)
    max_cache_size: Option<usize>,
    /// Number of heads
    n_heads: usize,
    /// Head dimension
    head_dim: usize,
}

impl LayerKVCache {
    /// Create empty cache
    pub fn new(n_heads: usize, head_dim: usize, max_cache_size: Option<usize>) -> Self {
        Self {
            keys: None,
            values: None,
            cached_len: 0,
            max_cache_size,
            n_heads,
            head_dim,
        }
    }

    /// Update cache with new keys and values
    ///
    /// # Arguments
    /// * `new_k` - New keys [batch, n_heads, new_seq_len, head_dim]
    /// * `new_v` - New values [batch, n_heads, new_seq_len, head_dim]
    ///
    /// # Returns
    /// (full_k, full_v) - Concatenated with cache
    pub fn update(
        &mut self,
        new_k: &Array4<f32>,
        new_v: &Array4<f32>,
    ) -> (Array4<f32>, Array4<f32>) {
        let (batch, n_heads, new_len, head_dim) = new_k.dim();

        match (&self.keys, &self.values) {
            (Some(cached_k), Some(cached_v)) => {
                // Concatenate with existing cache
                let mut full_k = Array4::zeros((batch, n_heads, self.cached_len + new_len, head_dim));
                let mut full_v = Array4::zeros((batch, n_heads, self.cached_len + new_len, head_dim));

                // Copy cached values
                for b in 0..batch {
                    for h in 0..n_heads {
                        for s in 0..self.cached_len {
                            for d in 0..head_dim {
                                full_k[[b, h, s, d]] = cached_k[[b, h, s, d]];
                                full_v[[b, h, s, d]] = cached_v[[b, h, s, d]];
                            }
                        }
                        // Add new values
                        for s in 0..new_len {
                            for d in 0..head_dim {
                                full_k[[b, h, self.cached_len + s, d]] = new_k[[b, h, s, d]];
                                full_v[[b, h, self.cached_len + s, d]] = new_v[[b, h, s, d]];
                            }
                        }
                    }
                }

                // Apply sliding window if needed
                let (final_k, final_v, new_cached_len) = if let Some(max_size) = self.max_cache_size {
                    let total_len = self.cached_len + new_len;
                    if total_len > max_size {
                        let start = total_len - max_size;
                        let k_sliced = full_k.slice(s![.., .., start.., ..]).to_owned();
                        let v_sliced = full_v.slice(s![.., .., start.., ..]).to_owned();
                        (k_sliced, v_sliced, max_size)
                    } else {
                        (full_k, full_v, total_len)
                    }
                } else {
                    (full_k, full_v, self.cached_len + new_len)
                };

                self.keys = Some(final_k.clone());
                self.values = Some(final_v.clone());
                self.cached_len = new_cached_len;

                (final_k, final_v)
            }
            _ => {
                // First update - just store the new values
                self.keys = Some(new_k.clone());
                self.values = Some(new_v.clone());
                self.cached_len = new_len;
                (new_k.clone(), new_v.clone())
            }
        }
    }

    /// Get current cache length
    pub fn len(&self) -> usize {
        self.cached_len
    }

    /// Check if cache is empty
    pub fn is_empty(&self) -> bool {
        self.cached_len == 0
    }

    /// Clear the cache
    pub fn clear(&mut self) {
        self.keys = None;
        self.values = None;
        self.cached_len = 0;
    }

    /// Get cached keys (if any)
    pub fn keys(&self) -> Option<&Array4<f32>> {
        self.keys.as_ref()
    }

    /// Get cached values (if any)
    pub fn values(&self) -> Option<&Array4<f32>> {
        self.values.as_ref()
    }
}

/// Full KV-Cache for all layers
#[derive(Clone)]
pub struct KVCache {
    /// Per-layer caches
    layers: Vec<LayerKVCache>,
    /// Number of layers
    n_layers: usize,
}

impl KVCache {
    /// Create empty cache for all layers
    pub fn new(
        n_layers: usize,
        n_heads: usize,
        head_dim: usize,
        max_cache_size: Option<usize>,
    ) -> Self {
        let layers = (0..n_layers)
            .map(|_| LayerKVCache::new(n_heads, head_dim, max_cache_size))
            .collect();

        Self { layers, n_layers }
    }

    /// Get mutable reference to layer cache
    pub fn layer_mut(&mut self, layer_idx: usize) -> &mut LayerKVCache {
        &mut self.layers[layer_idx]
    }

    /// Get reference to layer cache
    pub fn layer(&self, layer_idx: usize) -> &LayerKVCache {
        &self.layers[layer_idx]
    }

    /// Get current sequence length (from first layer)
    pub fn seq_len(&self) -> usize {
        self.layers.first().map(|l| l.len()).unwrap_or(0)
    }

    /// Clear all layer caches
    pub fn clear(&mut self) {
        for layer in &mut self.layers {
            layer.clear();
        }
    }

    /// Number of layers
    pub fn n_layers(&self) -> usize {
        self.n_layers
    }
}

/// Paged KV-Cache for memory-efficient long sequences
/// Uses block-based allocation similar to vLLM
#[derive(Clone)]
pub struct PagedKVCache {
    /// Block size (number of tokens per block)
    block_size: usize,
    /// Allocated blocks per layer: Vec<(key_block, value_block)>
    blocks: Vec<Vec<(Array4<f32>, Array4<f32>)>>,
    /// Number of tokens currently cached per layer
    cached_lens: Vec<usize>,
    /// Configuration
    n_layers: usize,
    n_heads: usize,
    head_dim: usize,
}

impl PagedKVCache {
    /// Create paged cache
    pub fn new(
        n_layers: usize,
        n_heads: usize,
        head_dim: usize,
        block_size: usize,
    ) -> Self {
        Self {
            block_size,
            blocks: vec![Vec::new(); n_layers],
            cached_lens: vec![0; n_layers],
            n_layers,
            n_heads,
            head_dim,
        }
    }

    /// Allocate a new block for a layer
    fn allocate_block(&self, batch_size: usize) -> (Array4<f32>, Array4<f32>) {
        let k_block = Array4::zeros((batch_size, self.n_heads, self.block_size, self.head_dim));
        let v_block = Array4::zeros((batch_size, self.n_heads, self.block_size, self.head_dim));
        (k_block, v_block)
    }

    /// Update cache for a layer
    pub fn update_layer(
        &mut self,
        layer_idx: usize,
        new_k: &Array4<f32>,
        new_v: &Array4<f32>,
    ) -> (Array4<f32>, Array4<f32>) {
        let (batch, _, new_len, _) = new_k.dim();
        let current_len = self.cached_lens[layer_idx];

        // Determine how many blocks we need
        let total_len = current_len + new_len;
        let blocks_needed = (total_len + self.block_size - 1) / self.block_size;

        // Allocate new blocks if needed
        let block_size = self.block_size;
        let n_heads = self.n_heads;
        let head_dim = self.head_dim;
        while self.blocks[layer_idx].len() < blocks_needed {
            // Inline block allocation to avoid borrowing issues
            let k_block = Array4::zeros((batch, n_heads, block_size, head_dim));
            let v_block = Array4::zeros((batch, n_heads, block_size, head_dim));
            self.blocks[layer_idx].push((k_block, v_block));
        }

        // Write new tokens into blocks
        for i in 0..new_len {
            let global_pos = current_len + i;
            let block_idx = global_pos / self.block_size;
            let pos_in_block = global_pos % self.block_size;

            let (ref mut k_block, ref mut v_block) = self.blocks[layer_idx][block_idx];

            for b in 0..batch {
                for h in 0..self.n_heads {
                    for d in 0..self.head_dim {
                        k_block[[b, h, pos_in_block, d]] = new_k[[b, h, i, d]];
                        v_block[[b, h, pos_in_block, d]] = new_v[[b, h, i, d]];
                    }
                }
            }
        }

        self.cached_lens[layer_idx] = total_len;

        // Reconstruct full K, V from blocks
        let mut full_k = Array4::zeros((batch, self.n_heads, total_len, self.head_dim));
        let mut full_v = Array4::zeros((batch, self.n_heads, total_len, self.head_dim));

        for (block_idx, (k_block, v_block)) in self.blocks[layer_idx].iter().enumerate() {
            let start = block_idx * self.block_size;
            let end = (start + self.block_size).min(total_len);

            for pos in start..end {
                let pos_in_block = pos - start;
                for b in 0..batch {
                    for h in 0..self.n_heads {
                        for d in 0..self.head_dim {
                            full_k[[b, h, pos, d]] = k_block[[b, h, pos_in_block, d]];
                            full_v[[b, h, pos, d]] = v_block[[b, h, pos_in_block, d]];
                        }
                    }
                }
            }
        }

        (full_k, full_v)
    }

    /// Get current sequence length for a layer
    pub fn seq_len(&self, layer_idx: usize) -> usize {
        self.cached_lens[layer_idx]
    }

    /// Clear all caches
    pub fn clear(&mut self) {
        for blocks in &mut self.blocks {
            blocks.clear();
        }
        for len in &mut self.cached_lens {
            *len = 0;
        }
    }

    /// Get memory usage in bytes (approximate)
    pub fn memory_usage(&self) -> usize {
        let bytes_per_element = 4; // f32
        let elements_per_block = self.n_heads * self.block_size * self.head_dim;
        let total_blocks: usize = self.blocks.iter().map(|v| v.len()).sum();
        total_blocks * elements_per_block * bytes_per_element * 2 // *2 for K and V
    }
}

/// Streaming cache that supports continuous batching
#[derive(Clone)]
pub struct StreamingKVCache {
    /// Per-sequence caches (sequence_id -> cache)
    sequence_caches: std::collections::HashMap<u64, KVCache>,
    /// Configuration
    n_layers: usize,
    n_heads: usize,
    head_dim: usize,
    max_cache_size: Option<usize>,
}

impl StreamingKVCache {
    pub fn new(
        n_layers: usize,
        n_heads: usize,
        head_dim: usize,
        max_cache_size: Option<usize>,
    ) -> Self {
        Self {
            sequence_caches: std::collections::HashMap::new(),
            n_layers,
            n_heads,
            head_dim,
            max_cache_size,
        }
    }

    /// Get or create cache for a sequence
    pub fn get_or_create(&mut self, sequence_id: u64) -> &mut KVCache {
        self.sequence_caches.entry(sequence_id).or_insert_with(|| {
            KVCache::new(
                self.n_layers,
                self.n_heads,
                self.head_dim,
                self.max_cache_size,
            )
        })
    }

    /// Remove a sequence's cache (when generation is complete)
    pub fn remove(&mut self, sequence_id: u64) {
        self.sequence_caches.remove(&sequence_id);
    }

    /// Clear all sequence caches
    pub fn clear(&mut self) {
        self.sequence_caches.clear();
    }

    /// Number of active sequences
    pub fn num_sequences(&self) -> usize {
        self.sequence_caches.len()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_layer_cache_basic() {
        let mut cache = LayerKVCache::new(4, 32, None);
        assert!(cache.is_empty());

        let k = Array4::ones((2, 4, 10, 32));
        let v = Array4::ones((2, 4, 10, 32));

        let (full_k, full_v) = cache.update(&k, &v);
        assert_eq!(full_k.dim(), (2, 4, 10, 32));
        assert_eq!(cache.len(), 10);
    }

    #[test]
    fn test_layer_cache_accumulation() {
        let mut cache = LayerKVCache::new(4, 32, None);

        // First update
        let k1 = Array4::from_elem((1, 4, 5, 32), 1.0);
        let v1 = Array4::from_elem((1, 4, 5, 32), 1.0);
        cache.update(&k1, &v1);
        assert_eq!(cache.len(), 5);

        // Second update
        let k2 = Array4::from_elem((1, 4, 3, 32), 2.0);
        let v2 = Array4::from_elem((1, 4, 3, 32), 2.0);
        let (full_k, _) = cache.update(&k2, &v2);

        assert_eq!(cache.len(), 8);
        assert_eq!(full_k.dim(), (1, 4, 8, 32));

        // Check values are correctly concatenated
        assert!((full_k[[0, 0, 0, 0]] - 1.0).abs() < 1e-6);
        assert!((full_k[[0, 0, 6, 0]] - 2.0).abs() < 1e-6);
    }

    #[test]
    fn test_layer_cache_sliding_window() {
        let mut cache = LayerKVCache::new(4, 32, Some(10)); // max 10 tokens

        // Add 8 tokens
        let k1 = Array4::from_elem((1, 4, 8, 32), 1.0);
        let v1 = Array4::from_elem((1, 4, 8, 32), 1.0);
        cache.update(&k1, &v1);
        assert_eq!(cache.len(), 8);

        // Add 5 more (should trigger sliding window)
        let k2 = Array4::from_elem((1, 4, 5, 32), 2.0);
        let v2 = Array4::from_elem((1, 4, 5, 32), 2.0);
        let (full_k, _) = cache.update(&k2, &v2);

        assert_eq!(cache.len(), 10); // Capped at max
        assert_eq!(full_k.dim(), (1, 4, 10, 32));
    }

    #[test]
    fn test_kv_cache_multilayer() {
        let mut cache = KVCache::new(6, 8, 64, None);
        assert_eq!(cache.n_layers(), 6);
        assert_eq!(cache.seq_len(), 0);

        // Update each layer
        for layer_idx in 0..6 {
            let k = Array4::ones((1, 8, 5, 64));
            let v = Array4::ones((1, 8, 5, 64));
            cache.layer_mut(layer_idx).update(&k, &v);
        }

        assert_eq!(cache.seq_len(), 5);

        cache.clear();
        assert_eq!(cache.seq_len(), 0);
    }

    #[test]
    fn test_paged_cache() {
        let mut cache = PagedKVCache::new(2, 4, 32, 16); // block_size = 16

        let k = Array4::ones((1, 4, 10, 32));
        let v = Array4::ones((1, 4, 10, 32));

        let (full_k, full_v) = cache.update_layer(0, &k, &v);
        assert_eq!(full_k.dim(), (1, 4, 10, 32));
        assert_eq!(cache.seq_len(0), 10);

        // Add more to exceed block size
        let k2 = Array4::ones((1, 4, 10, 32));
        let v2 = Array4::ones((1, 4, 10, 32));
        let (full_k2, _) = cache.update_layer(0, &k2, &v2);

        assert_eq!(full_k2.dim(), (1, 4, 20, 32));
        assert_eq!(cache.seq_len(0), 20);
    }

    #[test]
    fn test_streaming_cache() {
        let mut cache = StreamingKVCache::new(4, 8, 64, None);

        // Create caches for two sequences
        let cache1 = cache.get_or_create(100);
        let k = Array4::ones((1, 8, 5, 64));
        let v = Array4::ones((1, 8, 5, 64));
        cache1.layer_mut(0).update(&k, &v);

        let cache2 = cache.get_or_create(200);
        cache2.layer_mut(0).update(&k, &v);

        assert_eq!(cache.num_sequences(), 2);

        cache.remove(100);
        assert_eq!(cache.num_sequences(), 1);
    }
}
