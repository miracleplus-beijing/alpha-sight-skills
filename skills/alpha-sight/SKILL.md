# Alpha-Sight: Scientific Research Engineering Assistant

A powerful skill for fetching, analyzing arXiv papers, and transforming them into actionable project improvements or code implementations.

## When to Use This Skill

This skill should be automatically triggered when the user:
- Provides an arXiv ID (e.g., `2401.12345`, `arxiv:2401.12345`)
- Mentions keywords: `arxiv`, `paper`, `论文`, `latest research`, `frontiers`, `前沿`
- References technical domains: `MoE`, `Transformer`, `Diffusion`, `RL`, `LLM`, etc.
- Requests: `reproduce`, `复现`, `implement`, `analyze paper`, `分析论文`

## Parameters

Parse the following optional parameters from user input:

- `--depth=[shallow|medium|deep]` (default: `medium`)
  - `shallow`: Abstract and key information only (5 min timeout)
  - `medium`: Full analysis + project fit assessment (15 min timeout)
  - `deep`: Full analysis + code reproduction (30 min timeout)

- `--language=[english|chinese]` (default: `english`)
  - `english`: Report in English
  - `chinese`: Report in Chinese with key translations

- `--cleanup=[on-success|always|never]` (default: `on-success`)
  - `on-success`: Clean temp files after success
  - `always`: Always clean
  - `never`: Keep all files for debugging

## Environment Setup

### Required Environment Variables

Check for these environment variables in order of priority:
1. `./alpha-sight/.env` (project-level)
2. `~/.config/alpha-sight/.env` (global-level)
3. System environment variables

```bash
SEMANTIC_SCHOLAR_API_KEY=xxx  # Optional, for citation analysis
```

### Directory Structure

Ensure the following structure exists (create if missing):

```
./alpha-sight/
├── .env                    # Environment configuration
├── index.json              # Historical records index
├── papers/                 # PDF storage
│   └── {arxiv_id}.pdf
├── reports/                # Analysis reports
│   └── {arxiv_id}_analysis.md
└── sandbox/                # Sandbox for reproduction
    └── {arxiv_id}_reproduction/
        ├── official_repo/  # Official repository (if available)
        ├── custom_impl/    # Custom implementation
        └── .venv/          # Virtual environment
```

## Workflow

### Phase 1: Paper Acquisition (Automatic)

1. **Parse User Input**
   - Extract arXiv ID, keywords, or domain
   - Parse optional parameters

2. **Fetch Paper Metadata**
   - Call arXiv API: `http://export.arxiv.org/api/query?id_list={arxiv_id}`
   - Extract: title, authors, abstract, published_date, categories

3. **Download PDF**
   - Download from: `https://arxiv.org/pdf/{arxiv_id}.pdf`
   - Save to: `./alpha-sight/papers/{arxiv_id}.pdf`

4. **Check History**
   - Read `./alpha-sight/index.json`
   - If paper already analyzed, ask user: "This paper was analyzed on {date}. Re-analyze?"

### Phase 2: Initial Analysis (Automatic)

1. **Extract Key Information**
   - Title, authors, abstract
   - Published date, categories
   - Key contributions (3-5 bullet points)

2. **Fetch Citation Data** (if SEMANTIC_SCHOLAR_API_KEY available)
   - Call Semantic Scholar API: `https://api.semanticscholar.org/v1/paper/arXiv:{arxiv_id}`
   - Extract: citation count, references, related papers

3. **Generate Initial Report**
   - Create Markdown report with basic information
   - Save to: `./alpha-sight/reports/{arxiv_id}_analysis.md`

### Phase 3: Deep Analysis (User Confirmation Required)

**Skip if `depth=shallow`**

1. **Read Paper Content**
   - Use Read tool to extract text from PDF
   - Focus on: Method, Algorithm, Implementation sections

2. **Analyze Current Project**
   - Use Glob to identify tech stack (package.json, requirements.txt, etc.)
   - Use Grep to search for relevant patterns
   - Read key configuration files

3. **Generate Project Fit Assessment**
   - Relevance score (1-10)
   - Potential application scenarios
   - Specific improvement suggestions

4. **Create Architecture Comparison**
   - Generate Mermaid diagram comparing paper method vs. current project

5. **Ask User for Reproduction**
   - If `depth=shallow`: Skip reproduction
   - If `depth=medium`: Ask "Would you like to reproduce the code?"
   - If `depth=deep`: Automatically proceed to reproduction

### Phase 4: Code Reproduction (Conditional)

**Only execute if:**
- User confirmed reproduction, OR
- `depth=deep` parameter set

#### Step 1: Find Official Repository

Search for official code in this order:

1. Check arXiv page for "Code" link
2. Parse PDF for GitHub/GitLab URLs
3. Query Semantic Scholar API for linked repositories
4. Search Papers with Code database

#### Step 2a: If Official Repository Found

```bash
cd ./alpha-sight/sandbox/{arxiv_id}_reproduction/
git clone {repo_url} official_repo
cd official_repo

# Check for dependency files
# - requirements.txt
# - environment.yml
# - pyproject.toml
# - setup.py

# Create virtual environment with uv
uv venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows

# Install dependencies
uv pip install -r requirements.txt

# Try to run (with timeout)
# Record results
```

#### Step 2b: If No Official Repository - Self-Implementation Loop

**Maximum 5 iterations:**

```python
for iteration in range(1, 6):
    # 1. Read paper method section
    method_content = read_paper_section(["Method", "Algorithm", "Implementation"])

    # 2. Identify required libraries
    required_libs = extract_dependencies(method_content)

    # 3. Query Context7 (if available and needed)
    if context7_available and needs_documentation(required_libs):
        docs = query_context7(required_libs)
    else:
        docs = None

    # 4. Generate implementation code
    code = generate_implementation(
        paper_content=method_content,
        documentation=docs,
        previous_errors=errors_from_last_iteration
    )

    # 5. Save code to sandbox
    save_code(f"./alpha-sight/sandbox/{arxiv_id}_reproduction/custom_impl/")

    # 6. Run in sandbox with timeout
    result = run_with_timeout(
        code=code,
        timeout=TIMEOUT_LIMITS[depth],
        memory_limit="4GB"
    )

    # 7. Check result
    if result.success:
        log_success(iteration)
        break
    else:
        log_error(iteration, result.error)
        if iteration == 5:
            mark_as_partial_completion()
```

**Context7 Query Strategy:**
- Only query when specific libraries detected (PyTorch, TensorFlow, JAX, etc.)
- Query for: API usage, best practices, common errors
- If Context7 unavailable, skip and use built-in knowledge

**Resource Limits:**
- Memory: 4GB
- Disk: 2GB per sandbox
- Timeout: Based on `depth` parameter

### Phase 5: Report Generation & Archiving

1. **Generate Final Report**

```markdown
# Paper Analysis Report: {title}

## Basic Information
- arXiv ID: {arxiv_id}
- Published: {date}
- Authors: {authors}
- Categories: {categories}

## Core Contributions
{3-5 bullet points}

## Technical Details
{key methods, algorithms, architecture}

## Project Fit Assessment
### Relevance Score: {score}/10
### Potential Applications
- {application 1}
- {application 2}

### Architecture Comparison
```mermaid
{comparison diagram}
```

## Implementation Suggestions
{specific recommendations}

## Reproduction Status
- [x] Environment setup
- [x] Core code implementation
- [x] Experimental validation

### Reproduction Method: {official_repo | self_implemented}
### Iterations: {count}
### Success Rate: {rate}
### Notes: {details}
```

2. **Update index.json**

Add or update entry:

```json
{
  "arxiv_id": "{arxiv_id}",
  "title": "{title}",
  "authors": ["{author1}", "{author2}"],
  "published_date": "{date}",
  "analyzed_date": "{timestamp}",
  "categories": ["{cat1}", "{cat2}"],
  "abstract": "{abstract}",

  "analysis": {
    "depth": "{depth}",
    "language": "{language}",
    "relevance_score": {score},
    "report_path": "./reports/{arxiv_id}_analysis.md",
    "pdf_path": "./papers/{arxiv_id}.pdf"
  },

  "reproduction": {
    "status": "{not_started|in_progress|completed|failed|partial}",
    "method": "{official_repo|self_implemented|none}",
    "repo_url": "{url}",
    "sandbox_path": "./sandbox/{arxiv_id}_reproduction/",
    "iterations": {count},
    "success_rate": {rate},
    "notes": "{details}"
  },

  "citations": {
    "cited_by_count": {count},
    "references_count": {count},
    "related_papers": ["{id1}", "{id2}"]
  },

  "tags": ["{tag1}", "{tag2}"],
  "project_impact": {
    "applicable": true,
    "suggestions": ["{suggestion1}", "{suggestion2}"]
  }
}
```

3. **Cleanup (Based on --cleanup parameter)**
   - `on-success`: Remove temp files if successful
   - `always`: Always remove temp files
   - `never`: Keep all files

## Error Handling

### Timeout Errors
- Log to report: "Reproduction timed out after {duration}"
- Mark status as "partial"
- Preserve all files for debugging

### Memory Errors
- Suggest lighter implementation
- Reduce batch size or model size
- Mark status as "failed"

### API Errors
- arXiv API: Retry up to 3 times with exponential backoff
- Semantic Scholar: Continue without citation data if fails
- Context7: Continue without documentation if unavailable

### Git Clone Errors
- If official repo inaccessible, proceed to self-implementation
- Log error details in report

## Output Format

### Success Message
```
✓ Paper Analysis Complete

Paper: {title}
arXiv ID: {arxiv_id}
Relevance Score: {score}/10

Report: ./alpha-sight/reports/{arxiv_id}_analysis.md
PDF: ./alpha-sight/papers/{arxiv_id}.pdf

{If reproduced:}
Reproduction: {status}
Method: {official_repo | self_implemented}
Code: ./alpha-sight/sandbox/{arxiv_id}_reproduction/
```

### Language-Specific Output
- If `--language=chinese`, translate all output messages to Chinese
- Keep technical terms in English with Chinese annotations

## Tools to Use

- **WebFetch**: Fetch arXiv API and Semantic Scholar API
- **Bash**: Download PDFs, git clone, run sandbox commands
- **Read**: Read PDF content, configuration files
- **Write**: Create reports, save code
- **Glob**: Find project files
- **Grep**: Search codebase patterns
- **mcp__context7__resolve-library-id**: Resolve library names
- **mcp__context7__query-docs**: Query library documentation
- **AskUserQuestion**: Confirm reproduction (when depth=medium)

## Important Notes

1. **Only process papers from arxiv.org** (English papers only)
2. **Always use `uv` for Python dependency management** in sandbox
3. **Never exceed resource limits** (4GB memory, 2GB disk, timeout per depth)
4. **Always update index.json** after each analysis
5. **Preserve sandbox on failure** for debugging
6. **Use Context7 only when available** - gracefully degrade if not
7. **Maximum 5 iterations** for self-implementation loop
8. **No user confirmation during iterations** - run automatically

## Example Usage

```
User: "Analyze arXiv 2401.12345"
→ Triggers skill with default parameters (depth=medium, language=english)

User: "Find latest MoE papers and analyze with deep reproduction --language=chinese"
→ Searches arXiv for MoE papers, analyzes with depth=deep, outputs in Chinese

User: "Reproduce this paper 2312.xxxxx"
→ Triggers skill with depth=deep (implied by "reproduce")
```
