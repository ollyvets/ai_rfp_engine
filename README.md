# AI RFP Insight Engine
An enterprise-grade, high-performance tool designed to automate the analysis of complex RFP (Request for Proposals) and tender documentation. This engine acts as an AI-powered CTO, transforming 50+ page PDFs into structured, actionable intelligence in seconds.

# 🚀 Key Architectural Advantages
This project demonstrates a Senior-level engineering approach to AI integration, prioritizing performance, cost-efficiency, and data integrity:

**Rust Performance Bridge (PyO3):** Unlike standard wrappers, this system features a custom-compiled Rust module (rust_core). It performs ultra-fast text normalization and pre-processing, handling heavy string manipulation tasks that would be bottlenecks in Python.

**Gemini 2.5 Flash Integration:** Leverages the massive 1M+ token context window to analyze entire documents natively. This removes the need for complex and often lossy RAG (Retrieval-Augmented Generation) pipelines for single-document analysis.

**Structured Output (Pydantic V2):** The AI is constrained by strict JSON Schemas. This ensures that the output is 100% valid, typed, and ready for immediate consumption by CRM or ERP systems.

**Asynchronous FastAPI:** Built for high concurrency, allowing the engine to handle multiple document uploads simultaneously without blocking.

# 💰 Business Value & ROI
Optimized for Scale and Cost-Efficiency:

**Token Economy:** The custom Rust module aggressively strips formatting noise and excessive whitespace. In benchmarks, this reduces the input size by ~3-5%, saving significant token costs at enterprise scale.

**Risk Mitigation:** The engine is programmed to be "ruthless." It identifies hidden "traps" in tender documents—such as unrealistic deadlines or predatory liability clauses—preventing costly business mistakes.

**Long-term Savings:** By offloading pre-processing to Rust and optimizing the prompt-to-token ratio, the system significantly lowers the Total Cost of Ownership (TCO) compared to naive LLM implementations.

# 📊 Performance Showcase
During testing with a 40+ page Energy Infrastructure RFP, the engine:

**Processed 87,000+ characters in ~30 seconds.**

Identified 3 Critical risks (including a suspiciously short submission window).

**Saved ~750 tokens through Rust-based text cleaning.**

Calculated a Go/No-Go score of 55/100, providing an immediate data-driven recommendation.

# 🛠️ Tech Stack
Backend: FastAPI (Python 3.10+)

Performance: Rust (via PyO3 & Maturin)

AI/LLM: Google Gemini 2.5 Flash

Validation: Pydantic V2

PDF Core: pypdf

# ⚙️ Installation & Setup
1. Clone & Environment

        git clone <https://github.com/ollyvets/ai_rfp_engine.git>

        cd ai_rfp_engine

        python -m venv .venv

        source .venv/bin/activate

        pip install -r requirements.txt

2. Build the Rust Core
        cd app/engine/rust_core

        maturin develop --release

        cd ../../..

3. Configuration
Set your Gemini API Key as an environment variable (standard security practice):

        export GEMINI_API_KEY="your_api_key_here"
4. Launch
        uvicorn app.main:app --reload

        Visit http://127.0.0.1:8000/docs to test the API via the interactive Swagger UI.

# Contacts 
 
 Upwork: https://www.upwork.com/freelancers/~010745b4d221a00300