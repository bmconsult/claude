//! Nexus HTTP Server for Model Inference
//!
//! A simple HTTP API for text generation:
//! - POST /generate - Generate text from a prompt
//! - GET /health - Health check
//! - GET /info - Model information
//!
//! Usage: cargo run --example serve --release -- [checkpoint_path] [port]
//!
//! Example requests:
//!   curl -X POST http://localhost:8080/generate \
//!     -H "Content-Type: application/json" \
//!     -d '{"prompt": "To be or not to be", "max_tokens": 50}'

use std::io::{BufRead, BufReader, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::Arc;
use std::time::Instant;
use nexus::{
    DifferentiableHybridNexusLM, HybridModelCheckpoint,
    SamplingConfig, Sampler,
};

// ============================================================================
// Configuration
// ============================================================================

#[derive(Clone)]
struct ServerConfig {
    port: u16,
    checkpoint_path: String,
    default_max_tokens: usize,
    default_temperature: f32,
}

impl Default for ServerConfig {
    fn default() -> Self {
        Self {
            port: 8080,
            checkpoint_path: "checkpoints/nexus_production/best.bin".to_string(),
            default_max_tokens: 100,
            default_temperature: 0.8,
        }
    }
}

// ============================================================================
// Request/Response Types (Simple JSON parsing)
// ============================================================================

struct GenerateRequest {
    prompt: String,
    max_tokens: Option<usize>,
    temperature: Option<f32>,
    top_k: Option<usize>,
    top_p: Option<f32>,
}

impl GenerateRequest {
    fn parse(body: &str) -> Option<Self> {
        // Simple JSON parsing without serde
        let prompt = extract_string_field(body, "prompt")?;
        let max_tokens = extract_number_field(body, "max_tokens").map(|n| n as usize);
        let temperature = extract_float_field(body, "temperature");
        let top_k = extract_number_field(body, "top_k").map(|n| n as usize);
        let top_p = extract_float_field(body, "top_p");

        Some(Self {
            prompt,
            max_tokens,
            temperature,
            top_k,
            top_p,
        })
    }
}

fn extract_string_field(json: &str, field: &str) -> Option<String> {
    let pattern = format!("\"{}\"", field);
    let start = json.find(&pattern)? + pattern.len();
    let rest = &json[start..];
    let colon = rest.find(':')?;
    let after_colon = rest[colon + 1..].trim();

    if after_colon.starts_with('"') {
        let start = 1;
        let end = after_colon[1..].find('"')? + 1;
        Some(after_colon[start..end].to_string())
    } else {
        None
    }
}

fn extract_number_field(json: &str, field: &str) -> Option<i64> {
    let pattern = format!("\"{}\"", field);
    let start = json.find(&pattern)? + pattern.len();
    let rest = &json[start..];
    let colon = rest.find(':')?;
    let after_colon = rest[colon + 1..].trim();

    let end = after_colon.find(|c: char| !c.is_numeric() && c != '-').unwrap_or(after_colon.len());
    after_colon[..end].parse().ok()
}

fn extract_float_field(json: &str, field: &str) -> Option<f32> {
    let pattern = format!("\"{}\"", field);
    let start = json.find(&pattern)? + pattern.len();
    let rest = &json[start..];
    let colon = rest.find(':')?;
    let after_colon = rest[colon + 1..].trim();

    let end = after_colon.find(|c: char| !c.is_numeric() && c != '.' && c != '-').unwrap_or(after_colon.len());
    after_colon[..end].parse().ok()
}

// ============================================================================
// Text Generation
// ============================================================================

fn generate_text(
    model: &DifferentiableHybridNexusLM,
    prompt: &str,
    max_tokens: usize,
    config: &SamplingConfig,
) -> (String, usize, f32) {
    let mut tokens: Vec<u32> = prompt.bytes().map(|b| b as u32).collect();
    let mut sampler = Sampler::new(config.clone());
    let start = Instant::now();
    let initial_len = tokens.len();

    for _ in 0..max_tokens {
        let logits = model.forward(&tokens);
        let logits_data = logits.data();
        let seq_len = tokens.len();

        let last_logits: Vec<f32> = (0..256)
            .map(|v| logits_data[[0, seq_len - 1, v]])
            .collect();

        let next_token = sampler.sample(&last_logits, &tokens);
        tokens.push(next_token);

        // Stop on newline or end
        if next_token == b'\n' as u32 || next_token == 0 {
            break;
        }
    }

    let elapsed = start.elapsed().as_secs_f32() * 1000.0;
    let generated_count = tokens.len() - initial_len;

    let text: String = tokens.iter()
        .filter_map(|&b| if b < 128 { Some(b as u8 as char) } else { None })
        .collect();

    (text, generated_count, elapsed)
}

// ============================================================================
// HTTP Handling
// ============================================================================

fn parse_request(stream: &mut TcpStream) -> Option<(String, String, String)> {
    let mut reader = BufReader::new(stream.try_clone().ok()?);
    let mut request_line = String::new();
    reader.read_line(&mut request_line).ok()?;

    let parts: Vec<&str> = request_line.trim().split_whitespace().collect();
    if parts.len() < 2 {
        return None;
    }

    let method = parts[0].to_string();
    let path = parts[1].to_string();

    // Read headers
    let mut content_length = 0usize;
    loop {
        let mut header = String::new();
        reader.read_line(&mut header).ok()?;
        let header = header.trim();
        if header.is_empty() {
            break;
        }
        if header.to_lowercase().starts_with("content-length:") {
            content_length = header.split(':').nth(1)?.trim().parse().ok()?;
        }
    }

    // Read body
    let mut body = vec![0u8; content_length];
    if content_length > 0 {
        std::io::Read::read_exact(&mut reader, &mut body).ok()?;
    }
    let body = String::from_utf8(body).ok()?;

    Some((method, path, body))
}

fn send_response(stream: &mut TcpStream, status: &str, content_type: &str, body: &str) {
    let response = format!(
        "HTTP/1.1 {}\r\nContent-Type: {}\r\nContent-Length: {}\r\nAccess-Control-Allow-Origin: *\r\n\r\n{}",
        status,
        content_type,
        body.len(),
        body
    );
    let _ = stream.write_all(response.as_bytes());
}

fn send_json(stream: &mut TcpStream, status: &str, json: &str) {
    send_response(stream, status, "application/json", json);
}

fn handle_generate(
    stream: &mut TcpStream,
    body: &str,
    model: &DifferentiableHybridNexusLM,
    config: &ServerConfig,
) {
    let request = match GenerateRequest::parse(body) {
        Some(r) => r,
        None => {
            send_json(stream, "400 Bad Request", r#"{"error": "Invalid JSON"}"#);
            return;
        }
    };

    let max_tokens = request.max_tokens.unwrap_or(config.default_max_tokens);
    let temperature = request.temperature.unwrap_or(config.default_temperature);

    let sampling_config = SamplingConfig {
        temperature,
        top_k: request.top_k.unwrap_or(40),
        top_p: request.top_p.unwrap_or(0.95),
        repetition_penalty: 1.1,
        greedy: false,
        seed: None,
    };

    let (text, tokens_generated, elapsed_ms) = generate_text(
        model,
        &request.prompt,
        max_tokens,
        &sampling_config,
    );

    let response = format!(
        r#"{{"text": "{}", "tokens_generated": {}, "elapsed_ms": {:.1}, "tokens_per_sec": {:.1}}}"#,
        text.replace('\\', "\\\\").replace('"', "\\\"").replace('\n', "\\n"),
        tokens_generated,
        elapsed_ms,
        tokens_generated as f32 / (elapsed_ms / 1000.0)
    );

    send_json(stream, "200 OK", &response);
}

fn handle_health(stream: &mut TcpStream) {
    send_json(stream, "200 OK", r#"{"status": "healthy"}"#);
}

fn handle_info(stream: &mut TcpStream, model: &DifferentiableHybridNexusLM) {
    let n_params = model.num_parameters();
    let n_layers = model.blocks.len();
    let n_attn = model.blocks.iter().filter(|b| b.attn.is_some()).count();
    let n_ssm = model.blocks.iter().filter(|b| b.ssm.is_some()).count();

    let response = format!(
        r#"{{"model": "nexus-hybrid", "parameters": {}, "layers": {}, "attention_layers": {}, "ssm_layers": {}}}"#,
        n_params, n_layers, n_attn, n_ssm
    );

    send_json(stream, "200 OK", &response);
}

fn handle_request(
    mut stream: TcpStream,
    model: &DifferentiableHybridNexusLM,
    config: &ServerConfig,
) {
    let (method, path, body) = match parse_request(&mut stream) {
        Some(r) => r,
        None => {
            send_json(&mut stream, "400 Bad Request", r#"{"error": "Invalid request"}"#);
            return;
        }
    };

    println!("  {} {}", method, path);

    match (method.as_str(), path.as_str()) {
        ("POST", "/generate") => handle_generate(&mut stream, &body, model, config),
        ("GET", "/health") => handle_health(&mut stream),
        ("GET", "/info") => handle_info(&mut stream, model),
        ("OPTIONS", _) => {
            // CORS preflight
            let response = "HTTP/1.1 200 OK\r\nAccess-Control-Allow-Origin: *\r\nAccess-Control-Allow-Methods: GET, POST, OPTIONS\r\nAccess-Control-Allow-Headers: Content-Type\r\nContent-Length: 0\r\n\r\n";
            let _ = stream.write_all(response.as_bytes());
        }
        _ => send_json(&mut stream, "404 Not Found", r#"{"error": "Not found"}"#),
    }
}

// ============================================================================
// Main
// ============================================================================

fn main() -> anyhow::Result<()> {
    println!("╔═══════════════════════════════════════════════════════════════════╗");
    println!("║                    NEXUS INFERENCE SERVER                         ║");
    println!("╚═══════════════════════════════════════════════════════════════════╝\n");

    // Parse args
    let args: Vec<String> = std::env::args().collect();
    let mut config = ServerConfig::default();

    if args.len() > 1 {
        config.checkpoint_path = args[1].clone();
    }
    if args.len() > 2 {
        config.port = args[2].parse().unwrap_or(8080);
    }

    // Load model
    println!("📂 Loading model from {}...", config.checkpoint_path);
    let checkpoint = HybridModelCheckpoint::load(&config.checkpoint_path)
        .map_err(|e| anyhow::anyhow!("Failed to load checkpoint: {}", e))?;

    let model = DifferentiableHybridNexusLM::new(checkpoint.config.clone());
    checkpoint.load_into(&model)
        .map_err(|e| anyhow::anyhow!("Failed to load weights: {}", e))?;

    println!("   ✓ Loaded {} parameters", model.num_parameters());
    println!("   ✓ Step {} | Loss {:.4}", checkpoint.step, checkpoint.loss);

    // Wrap model in Arc for thread safety (single-threaded for now)
    let model = Arc::new(model);
    let config = Arc::new(config);

    // Start server
    let addr = format!("0.0.0.0:{}", config.port);
    let listener = TcpListener::bind(&addr)?;
    println!("\n🚀 Server listening on http://{}", addr);
    println!("\n   Endpoints:");
    println!("   POST /generate - Generate text from prompt");
    println!("   GET  /health   - Health check");
    println!("   GET  /info     - Model information");
    println!("\n   Example:");
    println!("   curl -X POST http://localhost:{}/generate \\", config.port);
    println!("     -H \"Content-Type: application/json\" \\");
    println!("     -d '{{\"prompt\": \"To be\", \"max_tokens\": 50}}'\n");

    // Handle connections
    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                let model = Arc::clone(&model);
                let config = Arc::clone(&config);
                handle_request(stream, &model, &config);
            }
            Err(e) => {
                eprintln!("Connection error: {}", e);
            }
        }
    }

    Ok(())
}
