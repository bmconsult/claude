//! Benchmarks for Nexus
//!
//! Run with: cargo bench

use criterion::{black_box, criterion_group, criterion_main, Criterion, BenchmarkId};
use nexus::{Nexus, NexusConfig, Tensor};

/// Benchmark forward pass with different sequence lengths
fn bench_forward_seq_len(c: &mut Criterion) {
    let config = NexusConfig {
        d_model: 256,
        n_heads: 8,
        layers_per_block: 4,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    let mut group = c.benchmark_group("forward_seq_len");
    for seq_len in [32, 64, 128, 256, 512].iter() {
        let input = Tensor::randn(1, *seq_len, 256);
        group.bench_with_input(
            BenchmarkId::from_parameter(seq_len),
            seq_len,
            |b, _| {
                b.iter(|| {
                    black_box(model.forward(&input, false))
                })
            },
        );
    }
    group.finish();
}

/// Benchmark forward pass with different batch sizes
fn bench_forward_batch_size(c: &mut Criterion) {
    let config = NexusConfig {
        d_model: 256,
        n_heads: 8,
        layers_per_block: 4,
        ..Default::default()
    };

    let mut model = Nexus::new(config);

    let mut group = c.benchmark_group("forward_batch_size");
    for batch_size in [1, 2, 4, 8].iter() {
        let input = Tensor::randn(*batch_size, 64, 256);
        group.bench_with_input(
            BenchmarkId::from_parameter(batch_size),
            batch_size,
            |b, _| {
                b.iter(|| {
                    black_box(model.forward(&input, false))
                })
            },
        );
    }
    group.finish();
}

/// Benchmark forward pass with vs without memory updates
fn bench_memory_update(c: &mut Criterion) {
    let config = NexusConfig {
        d_model: 256,
        n_heads: 8,
        layers_per_block: 4,
        memory_size: 256,
        ..Default::default()
    };

    let mut model = Nexus::new(config);
    let input = Tensor::randn(1, 64, 256);

    let mut group = c.benchmark_group("memory_update");

    group.bench_function("without_memory", |b| {
        b.iter(|| {
            black_box(model.forward(&input, false))
        })
    });

    group.bench_function("with_memory", |b| {
        b.iter(|| {
            black_box(model.forward(&input, true))
        })
    });

    group.finish();
}

/// Benchmark model initialization
fn bench_model_init(c: &mut Criterion) {
    let mut group = c.benchmark_group("model_init");

    // Small model
    group.bench_function("small", |b| {
        b.iter(|| {
            let config = NexusConfig {
                d_model: 128,
                n_heads: 4,
                layers_per_block: 2,
                ..Default::default()
            };
            black_box(Nexus::new(config))
        })
    });

    // Base model
    group.bench_function("base", |b| {
        b.iter(|| {
            let config = NexusConfig {
                d_model: 256,
                n_heads: 8,
                layers_per_block: 4,
                ..Default::default()
            };
            black_box(Nexus::new(config))
        })
    });

    group.finish();
}

/// Benchmark SSM vs Attention layer
fn bench_layer_comparison(c: &mut Criterion) {
    use nexus::attention::MultiHeadAttention;
    use nexus::ssm::SelectiveSSM;

    let d_model = 256;
    let n_heads = 8;
    let d_state = 16;
    let max_seq_len = 512;

    let attention = MultiHeadAttention::new(d_model, n_heads, max_seq_len);
    let ssm = SelectiveSSM::new(d_model, d_state, 4, 2);  // d_model, d_state, d_conv, expand

    let input = Tensor::randn(1, 64, d_model);

    let mut group = c.benchmark_group("layer_comparison");

    group.bench_function("attention", |b| {
        b.iter(|| {
            black_box(attention.forward(&input, true))
        })
    });

    group.bench_function("ssm", |b| {
        b.iter(|| {
            black_box(ssm.forward(&input))
        })
    });

    group.finish();
}

criterion_group!(
    benches,
    bench_forward_seq_len,
    bench_forward_batch_size,
    bench_memory_update,
    bench_model_init,
    bench_layer_comparison,
);

criterion_main!(benches);
