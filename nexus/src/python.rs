//! Python bindings for Nexus via PyO3
//!
//! Provides a Pythonic interface to the Nexus model.

#[cfg(feature = "python")]
use pyo3::prelude::*;
#[cfg(feature = "python")]
use pyo3::exceptions::PyValueError;
#[cfg(feature = "python")]
use ndarray::Array3;

#[cfg(feature = "python")]
use crate::{Nexus, NexusConfig, Tensor};
#[cfg(feature = "python")]
use crate::training::{Trainer, TrainConfig};

/// Python wrapper for NexusConfig
#[cfg(feature = "python")]
#[pyclass(name = "NexusConfig")]
#[derive(Clone)]
pub struct PyNexusConfig {
    inner: NexusConfig,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyNexusConfig {
    #[new]
    #[pyo3(signature = (
        d_model = 512,
        n_heads = 8,
        d_state = 16,
        d_conv = 4,
        expand = 2,
        layers_per_block = 8,
        memory_size = 1024,
        vocab_size = 32000,
        max_seq_len = 8192
    ))]
    fn new(
        d_model: usize,
        n_heads: usize,
        d_state: usize,
        d_conv: usize,
        expand: usize,
        layers_per_block: usize,
        memory_size: usize,
        vocab_size: usize,
        max_seq_len: usize,
    ) -> Self {
        Self {
            inner: NexusConfig {
                d_model,
                n_heads,
                d_state,
                d_conv,
                expand,
                layers_per_block,
                attention_ratio: 1,
                memory_size,
                memory_lr: 0.01,
                vocab_size,
                max_seq_len,
            },
        }
    }

    #[getter]
    fn d_model(&self) -> usize {
        self.inner.d_model
    }

    #[getter]
    fn n_heads(&self) -> usize {
        self.inner.n_heads
    }

    #[getter]
    fn layers(&self) -> usize {
        self.inner.layers_per_block
    }

    fn __repr__(&self) -> String {
        format!(
            "NexusConfig(d_model={}, n_heads={}, layers={})",
            self.inner.d_model,
            self.inner.n_heads,
            self.inner.layers_per_block
        )
    }
}

/// Python wrapper for Nexus model
#[cfg(feature = "python")]
#[pyclass(name = "Nexus")]
pub struct PyNexus {
    inner: Nexus,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyNexus {
    #[new]
    fn new(config: &PyNexusConfig) -> Self {
        Self {
            inner: Nexus::new(config.inner.clone()),
        }
    }

    /// Forward pass
    /// Args:
    ///     x: Input tensor as numpy array [batch, seq_len, d_model]
    ///     update_memory: Whether to update test-time memory
    /// Returns:
    ///     Output tensor as numpy array
    #[pyo3(signature = (x, update_memory = true))]
    fn forward(&mut self, x: Vec<Vec<Vec<f32>>>, update_memory: bool) -> PyResult<Vec<Vec<Vec<f32>>>> {
        let batch = x.len();
        if batch == 0 {
            return Err(PyValueError::new_err("Empty input"));
        }
        let seq_len = x[0].len();
        if seq_len == 0 {
            return Err(PyValueError::new_err("Empty sequence"));
        }
        let d_model = x[0][0].len();

        // Convert to ndarray
        let mut data = Array3::zeros((batch, seq_len, d_model));
        for (b, seq) in x.iter().enumerate() {
            for (s, vec) in seq.iter().enumerate() {
                for (d, &val) in vec.iter().enumerate() {
                    data[[b, s, d]] = val;
                }
            }
        }

        let input = Tensor { data };
        let output = self.inner.forward(&input, update_memory);

        // Convert back to Vec
        let (ob, os, od) = output.shape();
        let mut result = vec![vec![vec![0.0f32; od]; os]; ob];
        for b in 0..ob {
            for s in 0..os {
                for d in 0..od {
                    result[b][s][d] = output.data[[b, s, d]];
                }
            }
        }

        Ok(result)
    }

    /// Get memory statistics
    fn memory_stats(&self) -> PyResult<(usize, usize, f32, f32)> {
        let stats = self.inner.memory.stats();
        Ok((
            stats.num_entries,
            stats.capacity,
            stats.avg_surprise,
            stats.avg_age,
        ))
    }

    /// Clear test-time memory
    fn clear_memory(&mut self) {
        self.inner.memory = crate::TitansMemory::new(
            self.inner.config.d_model,
            self.inner.config.memory_size,
            self.inner.config.memory_lr,
        );
    }

    fn __repr__(&self) -> String {
        format!(
            "Nexus(d_model={}, layers={}, memory_entries={})",
            self.inner.config.d_model,
            self.inner.config.layers_per_block,
            self.inner.memory.stats().num_entries
        )
    }
}

/// Python wrapper for TrainConfig
#[cfg(feature = "python")]
#[pyclass(name = "TrainConfig")]
#[derive(Clone)]
pub struct PyTrainConfig {
    inner: TrainConfig,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyTrainConfig {
    #[new]
    #[pyo3(signature = (
        lr = 3e-4,
        weight_decay = 0.01,
        batch_size = 32,
        epochs = 10,
        warmup_steps = 1000,
        mask_ratio = 0.3
    ))]
    fn new(
        lr: f32,
        weight_decay: f32,
        batch_size: usize,
        epochs: usize,
        warmup_steps: usize,
        mask_ratio: f32,
    ) -> Self {
        Self {
            inner: TrainConfig {
                lr,
                weight_decay,
                batch_size,
                epochs,
                warmup_steps,
                mask_ratio,
                ..Default::default()
            },
        }
    }

    #[getter]
    fn lr(&self) -> f32 {
        self.inner.lr
    }

    #[getter]
    fn batch_size(&self) -> usize {
        self.inner.batch_size
    }

    #[getter]
    fn epochs(&self) -> usize {
        self.inner.epochs
    }
}

/// Python wrapper for Trainer
#[cfg(feature = "python")]
#[pyclass(name = "Trainer")]
pub struct PyTrainer {
    inner: Trainer,
}

#[cfg(feature = "python")]
#[pymethods]
impl PyTrainer {
    #[new]
    #[pyo3(signature = (model_config, train_config, checkpoint_dir = "checkpoints"))]
    fn new(
        model_config: &PyNexusConfig,
        train_config: &PyTrainConfig,
        checkpoint_dir: &str,
    ) -> Self {
        Self {
            inner: Trainer::new(
                model_config.inner.clone(),
                train_config.inner.clone(),
                checkpoint_dir,
                None,
            ),
        }
    }

    /// Train for one step
    fn train_step(&mut self, model: &mut PyNexus, x: Vec<Vec<Vec<f32>>>) -> PyResult<(f32, f32, f32, f32)> {
        let batch = x.len();
        if batch == 0 {
            return Err(PyValueError::new_err("Empty input"));
        }
        let seq_len = x[0].len();
        let d_model = x[0][0].len();

        // Convert to ndarray
        let mut data = Array3::zeros((batch, seq_len, d_model));
        for (b, seq) in x.iter().enumerate() {
            for (s, vec) in seq.iter().enumerate() {
                for (d, &val) in vec.iter().enumerate() {
                    data[[b, s, d]] = val;
                }
            }
        }

        let batch_data = crate::training::Batch {
            input: data,
            target: None,
        };

        let (total, inv, var, cov) = self.inner.train_step(&mut model.inner, &batch_data);
        Ok((total, inv, var, cov))
    }

    /// Get current step
    #[getter]
    fn step(&self) -> usize {
        self.inner.state.step
    }

    /// Get best loss so far
    #[getter]
    fn best_loss(&self) -> f32 {
        self.inner.state.best_loss
    }
}

/// Module initialization for Python
#[cfg(feature = "python")]
#[pymodule]
fn nexus(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyNexusConfig>()?;
    m.add_class::<PyNexus>()?;
    m.add_class::<PyTrainConfig>()?;
    m.add_class::<PyTrainer>()?;

    // Add version info
    m.add("__version__", "0.1.0")?;
    m.add("__doc__", "Nexus: Hybrid Intelligence Architecture")?;

    Ok(())
}
