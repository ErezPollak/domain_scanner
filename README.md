# DomainScanner – AI-Powered Web Analysis Tool

**DomainScanner** is an advanced multi-agent system built with [CrewAI](https://www.crewai.com) designed to perform **comprehensive analysis of web services**.  
It leverages AI agents and specialized tools to evaluate **security, technology, performance, UX/UI, and metadata**.

---

## Overview

DomainScanner is designed to replace manual auditing with an **automated, intelligent workflow**. Each component of the system is focused on a specific domain of web analysis:

- **Infrastructure & DNS** – Maps domain IPs, discovers subdomains, and detects potential entry points.
- **Security Analysis** – Evaluates HTTP security headers, SSL/TLS certificates, and web server configurations.
- **Tech Stack Detection** – Automatically identifies frameworks, CMS platforms, libraries, and hosting technologies using Wappalyzer.
- **UX/UI Evaluation** – Provides AI-driven usability assessments, highlighting areas where navigation or design can be improved.
- **Performance & Reliability** – Measures latency, response times, and content delivery efficiency.
- **SEO & Metadata Inspection** – Extracts titles, meta descriptions, headings, sitemap, and robots.txt rules.
- **Automated Reporting** – Consolidates all findings into a clear, structured Markdown report for easy review.

---

## Agents, Tasks, and Tools

The system orchestrates specialized AI agents that execute specific assigned tasks using a suite of custom Python tools:

1. **Reconnaissance Agent** (`recon_agent`)
   - **Task**: `reconnaissance_task` (Identify DNS records, IPs, subdomains, and exposed ports)
   - **Tools Used**: `DNS Lookup`, `Subdomain Discovery`, `Port Scanner`, `Robots.txt Analyzer`

2. **Technology Intelligence Analyst** (`tech_stack_agent`)
   - **Task**: `tech_stack_analysis_task` (Identify frontend/backend frameworks, web servers, and CDNs)
   - **Tools Used**: `Detect Tech Stack`

3. **Cloud Infrastructure Analyst** (`infrastructure_agent`)
   - **Task**: `infrastructure_analysis_task` (Determine hosting environments, CDN usage, and TLS config)
   - **Tools Used**: `DNS Lookup`, `SSL Certificate Analysis`

4. **Web Security Analyst** (`security_agent`)
   - **Task**: `security_analysis_task` (Evaluate vulnerabilities, missing security headers, and risks)
   - **Tools Used**: `Security Headers Scan`, `SSL Certificate Analysis`

5. **Performance Engineer** (`performance_agent`)
   - **Task**: `performance_analysis_task` (Analyze response latency, content size, and performance behavior)
   - **Tools Used**: `Performance Measurement`

6. **Web Content Analyst** (`website_content_agent`)
   - **Task**: `website_content_analysis_task` (Retrieve HTML, extract main metadata and content)
   - **Tools Used**: `Fetch Website HTML`, `Extract Metadata`, `Parallel Website Crawler`, `Sitemap Analyzer`, `Robots.txt Analyzer`

7. **UX/UI Evaluation Specialist** (`ux_ui_agent`)
   - **Task**: `ux_ui_analysis_task` (Assess navigation clarity, accessibility, and overall user experience)
   - **Tools Used**: `Fetch Website HTML`, `Extract Metadata`, `Parallel Website Crawler`, `Sitemap Analyzer`

8. **Technical Report Architect** (`report_agent`)
   - **Task**: `report_generation_task` (Synthesize all previous agent findings into a final consolidated Markdown report)
   - **Tools Used**: None (Consumes context from previous tasks)

---

## Key Features

1. **AI-Powered UX/UI Agent**  
   - Evaluates usability, navigation clarity, and user convenience.  

2. **Advanced Security Toolset**  
   - Improved detection of missing or misconfigured HTTP headers and SSL inspection.  

3. **Full Domain Crawl with Parallel Fetching**  
   - Fetches multiple pages concurrently to map internal links efficiently.  

4. **Tech Stack Analysis Enhancements**  
   - Integrates Wappalyzer for detailed footprint scanning.  

5. **Metadata & SEO Improvements**  
   - Extracts structured headings, meta tags, sitemap.xml, and robots.txt rules.  

6. **Automated, Domain-Named Reporting**  
   - Each scan generates a Markdown report formatted for professional review.  

7. **Extensible Agent & Tool Framework**  
   - Modular workflow for simple integrations of future toolkits.  

---

## Running Locally

To run the DomainScanner crew locally, you need to execute the main script that kicks off the CrewAI execution flow.

### Step-by-Step Execution

1. **Install Dependencies:**
   Ensure all dependencies are synced perfectly:
   ```bash
   uv sync
   ```

2. **Configure Environment (`.env`):**
   Create a `.env` file in the root directory to supply your API keys and the required LLM configuration. For LiteLLM supported models, you need to provide the specific provider's API key and define the model string. For example:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   OPENAI_MODEL_NAME=openai/gpt-4o
   ```
   Or if using Anthropic:
   ```env
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   OPENAI_MODEL_NAME=anthropic/claude-3-5-sonnet-20240620
   ```
   *(Note: CrewAI utilizes `OPENAI_MODEL_NAME` natively as its default routing variable, even when using other provider strings through LiteLLM).*

> [!IMPORTANT]
> Do **NOT** use basic or strictly conversational models for this project. DomainScanner heavily relies on functional execution, meaning you must provide **Tool-Oriented Models** (also known as Function-Calling models).
>
> **Examples of strongly recommended tool-oriented models:**
> - `openai/gpt-4o` or `openai/gpt-4-turbo` 
> - `anthropic/claude-3-5-sonnet-20240620`
> - `google/gemini-1.5-pro`
>
> Specifying models that lack robust tool execution capabilities (like `gpt-3.5-turbo` or small local models like `llama3` without proper routing) will result in unpredictable behavior or immediate agent failure!

3. **Set the Target Domain (`main.py`):**
   Before running the crew, you must edit the input parameters directly inside `src/domain_scanner/main.py`. Locate the `run()` function (and optionally the other functions like `test()` and `train()`) and change the target domain string:
   ```python
   def run():
       inputs = {
           'domain': 'your-target-domain.com'
       }
       # ...
   ```

4. **Run the Crew:**
   Run the scanner by using the provided `uv` script alias:
   ```bash
   uv run run_crew
   ```
   Or manually specifying the script:
   ```bash
   uv run domain_scanner
   ```

---

## Testing

A comprehensive unit test suite ensures all the custom tools function reliably without triggering actual live network calls to arbitrary target domains. This means your testing workflows are completely deterministic, fast, and fail-proof against rate-limiting or network downtime!

### Running the Test Suite

1. **Dependencies:** Make sure your `dev` dependencies are synced with `uv`:
   ```bash
   uv sync
   ```

2. **Execute pytest:** From the root folder, run `pytest` either globally if your virtual environment is active, or safely through `uv`:
   ```bash
   uv run pytest tests/ -v
   ```
   Or inside the activated environment:
   ```bash
   pytest .
   ```

**What the tests cover:**
- **`tests/test_domain_tools.py`**: Exhaustive function validation for all domain tools. Uses `pytest-mock` to seamlessly mock heavy elements such as `requests`, `socket`, `ssl`, and ThreadPools!
- **`tests/test_crew.py`**: Ensures `DomainScanner` instantiation operates flawlessly by testing the integrity between the `crew.py` classes and their YAML configs.

---

DomainScanner represents a **professional-grade, AI-driven approach to web service analysis**, combining the efficiency of automation with the insight of human-like evaluation.
