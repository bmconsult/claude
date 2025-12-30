//! Nexus HTTP Inference Server
//!
//! Usage: nexus-serve [--port 8080]
//!
//! Endpoints:
//!   POST /generate - Generate text from prompt
//!   GET /health - Health check
//!   GET /stats - Memory and model statistics

use anyhow::Result;
use nexus::{NexusConfig, NexusLM, SimpleBPE};
use std::io::{Read, Write};
use std::net::{TcpListener, TcpStream};
use std::sync::{Arc, Mutex};

struct Server {
    model: Arc<Mutex<NexusLM>>,
    tokenizer: SimpleBPE,
}

impl Server {
    fn new(config: NexusConfig) -> Self {
        let model = Arc::new(Mutex::new(NexusLM::new(config)));
        let tokenizer = SimpleBPE::new();
        Self { model, tokenizer }
    }

    fn handle_request(&self, mut stream: TcpStream) -> Result<()> {
        let mut buffer = [0u8; 4096];
        let n = stream.read(&mut buffer)?;
        let request = String::from_utf8_lossy(&buffer[..n]);

        // Parse request line
        let first_line = request.lines().next().unwrap_or("");
        let parts: Vec<&str> = first_line.split_whitespace().collect();

        if parts.len() < 2 {
            return self.send_error(&mut stream, 400, "Bad Request");
        }

        let method = parts[0];
        let path = parts[1];

        match (method, path) {
            ("GET", "/health") => self.handle_health(&mut stream),
            ("GET", "/stats") => self.handle_stats(&mut stream),
            ("POST", "/generate") => self.handle_generate(&mut stream, &request),
            _ => self.send_error(&mut stream, 404, "Not Found"),
        }
    }

    fn handle_health(&self, stream: &mut TcpStream) -> Result<()> {
        let response = r#"{"status":"ok","version":"0.1.0"}"#;
        self.send_json(stream, 200, response)
    }

    fn handle_stats(&self, stream: &mut TcpStream) -> Result<()> {
        let model = self.model.lock().unwrap();
        let mem_stats = model.core.memory.stats();

        let response = format!(
            r#"{{"parameters":{},"vocab_size":{},"memory":{{"entries":{},"capacity":{},"avg_surprise":{:.4}}}}}"#,
            model.num_parameters(),
            model.config.vocab_size,
            mem_stats.num_entries,
            mem_stats.capacity,
            mem_stats.avg_surprise
        );

        self.send_json(stream, 200, &response)
    }

    fn handle_generate(&self, stream: &mut TcpStream, request: &str) -> Result<()> {
        // Parse JSON body (simple parsing)
        let body_start = request.find("\r\n\r\n").map(|i| i + 4).unwrap_or(0);
        let body = &request[body_start..];

        // Extract prompt from JSON {"prompt": "...", "max_tokens": N, "temperature": T}
        let prompt = extract_json_string(body, "prompt").unwrap_or_default();
        let max_tokens = extract_json_number(body, "max_tokens").unwrap_or(50) as usize;
        let temperature = extract_json_float(body, "temperature").unwrap_or(0.8);

        if prompt.is_empty() {
            return self.send_error(stream, 400, "Missing prompt");
        }

        // Tokenize
        let prompt_tokens = self.tokenizer.encode(&prompt);

        // Generate
        let mut model = self.model.lock().unwrap();
        let generated = model.generate(&prompt_tokens, max_tokens, temperature);
        drop(model);

        // Decode
        let output = self.tokenizer.decode(&generated);

        let response = format!(
            r#"{{"prompt":"{}","output":"{}","tokens":{}}}"#,
            escape_json(&prompt),
            escape_json(&output),
            generated.len()
        );

        self.send_json(stream, 200, &response)
    }

    fn send_json(&self, stream: &mut TcpStream, status: u16, body: &str) -> Result<()> {
        let status_text = match status {
            200 => "OK",
            400 => "Bad Request",
            404 => "Not Found",
            500 => "Internal Server Error",
            _ => "Unknown",
        };

        let response = format!(
            "HTTP/1.1 {} {}\r\n\
             Content-Type: application/json\r\n\
             Content-Length: {}\r\n\
             Access-Control-Allow-Origin: *\r\n\
             \r\n\
             {}",
            status, status_text, body.len(), body
        );

        stream.write_all(response.as_bytes())?;
        Ok(())
    }

    fn send_error(&self, stream: &mut TcpStream, status: u16, message: &str) -> Result<()> {
        let body = format!(r#"{{"error":"{}"}}"#, message);
        self.send_json(stream, status, &body)
    }
}

fn extract_json_string(json: &str, key: &str) -> Option<String> {
    let pattern = format!("\"{}\"", key);
    let start = json.find(&pattern)?;
    let after_key = &json[start + pattern.len()..];

    // Find the colon and opening quote
    let colon_pos = after_key.find(':')?;
    let after_colon = &after_key[colon_pos + 1..].trim_start();
    if !after_colon.starts_with('"') {
        return None;
    }

    let after_quote = &after_colon[1..];
    let end_quote = after_quote.find('"')?;

    Some(after_quote[..end_quote].to_string())
}

fn extract_json_number(json: &str, key: &str) -> Option<i64> {
    let pattern = format!("\"{}\"", key);
    let start = json.find(&pattern)?;
    let after_key = &json[start + pattern.len()..];

    let colon_pos = after_key.find(':')?;
    let after_colon = after_key[colon_pos + 1..].trim_start();

    // Parse number
    let end = after_colon.find(|c: char| !c.is_ascii_digit() && c != '-').unwrap_or(after_colon.len());
    after_colon[..end].parse().ok()
}

fn extract_json_float(json: &str, key: &str) -> Option<f32> {
    let pattern = format!("\"{}\"", key);
    let start = json.find(&pattern)?;
    let after_key = &json[start + pattern.len()..];

    let colon_pos = after_key.find(':')?;
    let after_colon = after_key[colon_pos + 1..].trim_start();

    // Parse float
    let end = after_colon.find(|c: char| !c.is_ascii_digit() && c != '.' && c != '-').unwrap_or(after_colon.len());
    after_colon[..end].parse().ok()
}

fn escape_json(s: &str) -> String {
    s.replace('\\', "\\\\")
     .replace('"', "\\\"")
     .replace('\n', "\\n")
     .replace('\r', "\\r")
     .replace('\t', "\\t")
}

fn main() -> Result<()> {
    println!("╔══════════════════════════════════════════╗");
    println!("║        NEXUS Inference Server v0.1       ║");
    println!("╚══════════════════════════════════════════╝");
    println!();

    // Parse arguments
    let args: Vec<String> = std::env::args().collect();

    let port: u16 = args.iter()
        .position(|x| x == "--port")
        .map(|i| args[i + 1].parse().unwrap_or(8080))
        .unwrap_or(8080);

    // Create tokenizer for config
    let tokenizer = SimpleBPE::new();

    // Configure model
    let config = NexusConfig {
        d_model: 128,
        n_heads: 4,
        d_state: 16,
        d_conv: 4,
        expand: 2,
        layers_per_block: 4,
        attention_ratio: 1,
        memory_size: 64,
        memory_lr: 0.01,
        vocab_size: tokenizer.vocab_size(),
        max_seq_len: 512,
    };

    println!("Loading model...");
    let server = Server::new(config);
    println!("  Model loaded!");
    println!();

    // Start server
    let addr = format!("0.0.0.0:{}", port);
    let listener = TcpListener::bind(&addr)?;
    println!("Server listening on http://{}", addr);
    println!();
    println!("Endpoints:");
    println!("  GET  /health   - Health check");
    println!("  GET  /stats    - Model statistics");
    println!("  POST /generate - Generate text");
    println!();
    println!("Example:");
    println!(r#"  curl -X POST http://localhost:{}/generate -d '{{"prompt":"Hello","max_tokens":20}}'"#, port);
    println!();

    for stream in listener.incoming() {
        match stream {
            Ok(stream) => {
                if let Err(e) = server.handle_request(stream) {
                    eprintln!("Error handling request: {}", e);
                }
            }
            Err(e) => {
                eprintln!("Connection error: {}", e);
            }
        }
    }

    Ok(())
}
