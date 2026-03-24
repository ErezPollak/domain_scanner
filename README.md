# DomainScanner – AI-Powered Web Analysis Tool

**DomainScanner** is an advanced multi-agent system built with [CrewAI](https://www.crewai.com) designed to perform **comprehensive analysis of web services**.  
It leverages AI agents, and specialized tools to evaluate **security, technology, performance, UX/UI, and metadata**.

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

## Key Features

1. **AI-Powered UX/UI Agent**  
   - Evaluates usability, navigation clarity, and user convenience.  
   - Provides actionable feedback on site design and accessibility.

2. **Advanced Security Toolset**  
   - Improved detection of missing or misconfigured HTTP headers.  
   - Enhanced SSL/TLS certificate inspection for real-world security auditing.

3. **Full Domain Crawl with Parallel Fetching**  
   - Fetches multiple pages concurrently to map internal links efficiently.  
   - Limits requests to avoid overload while providing comprehensive coverage.

4. **Tech Stack Analysis Enhancements**  
   - Integrates Wappalyzer for detailed detection of frameworks, CMS, and server technologies.  
   - Provides insights into software versions, enabling better risk assessment.

5. **Metadata & SEO Improvements**  
   - Extracts structured headings, meta tags, sitemap.xml, and robots.txt rules.  
   - Highlights SEO issues or accessibility concerns.

6. **Automated, Domain-Named Reporting**  
   - Each scan generates a Markdown report named after the target domain.  
   - Structured with clear sections: Infrastructure, Security, Tech Stack, UX/UI, Performance, and SEO.

7. **Extensible Agent & Tool Framework**  
   - Agents can be easily customized or extended.  
   - Tools are modular, allowing future integration of new analysis capabilities.

---

## Benefits

- **Automated Efficiency** – Reduces manual effort and human error in domain audits.  
- **Comprehensive Coverage** – Combines security, UX/UI, performance, and SEO in one scan.  
- **Professional Reporting** – Outputs structured, actionable reports suitable for internal review or client presentation.  
- **Modular & Extensible** – New tools and agents can be added as requirements evolve.  
- **AI-Powered Insights** – Uses specialized agents to provide intelligent evaluations beyond simple checks.

---

## Version Highlights

- **v2.0** introduces the **UX/UI analysis agent** and **enhanced report generation**.  
- **Improved concurrency** for website crawling, reducing scan times without sacrificing thoroughness.  
- **Better error handling** in tools, ensuring robustness against unreachable pages or malformed responses.  
- **Expanded toolset** including `robots.txt` and `sitemap.xml` analysis.  
- Fully aligned **agent specialization**: each agent now has a clear role, goal, and backstory for higher quality outputs.

---

DomainScanner represents a **professional-grade, AI-driven approach to web service analysis**, combining the efficiency of automation with the insight of human-like evaluation.
