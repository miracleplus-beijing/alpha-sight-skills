# Alpha-Sight Skill

A powerful scientific research engineering assistant for Claude Code that fetches, analyzes arXiv papers, and transforms them into actionable project improvements or code implementations.

## Features

- 📄 **Paper Acquisition**: Fetch papers from arXiv by ID, keywords, or domain
- 🔍 **Deep Analysis**: Extract key contributions, methods, and technical details
- 📊 **Citation Analysis**: Track citations and references via Semantic Scholar
- 🎯 **Project Fit Assessment**: Evaluate relevance to your current codebase
- 🔧 **Code Reproduction**: Clone official repos or implement from scratch
- 📚 **Context7 Integration**: Query library documentation during reproduction
- 📝 **History Tracking**: Maintain index of all analyzed papers

## Installation

### Prerequisites

- Python 3.9+
- `uv` package manager
- `git`
- Optional: Docker (for stricter sandboxing)

### Setup

1. **Install the skill** (method depends on your Claude Code setup)

2. **Configure environment variables** (optional):

Create `./alpha-sight/.env` or `~/.config/alpha-sight/.env`:

```bash
SEMANTIC_SCHOLAR_API_KEY=your_key_here  # Optional, for higher rate limits
```

3. **Verify installation**:

The skill will automatically create the required directory structure on first use:

```
./alpha-sight/
├── .env
├── index.json
├── papers/
├── reports/
└── sandbox/
```

## Usage

### Basic Usage

The skill is automatically triggered when you mention arXiv papers or research keywords:

```
"Analyze arXiv 2401.12345"
```

### With Parameters

```
"Analyze arXiv 2401.12345 --depth=deep --language=chinese"
```

### Search and Analyze

```
"Find latest MoE papers and analyze their impact on my project"
```

### Code Reproduction

```
"Reproduce the code from paper 2312.xxxxx"
```

## Parameters

### --depth

Controls analysis depth and timeout:

- `shallow`: Abstract and key information only (5 min timeout)
- `medium`: Full analysis + project fit assessment (15 min timeout) **[default]**
- `deep`: Full analysis + code reproduction (30 min timeout)

### --language

Report language:

- `english`: Report in English **[default]**
- `chinese`: Report in Chinese with key translations

### --cleanup

Sandbox cleanup strategy:

- `on-success`: Clean temp files after success **[default]**
- `always`: Always clean temp files
- `never`: Keep all files for debugging

## Examples

### Example 1: Quick Analysis

```
User: "What's in arXiv 2401.12345?"

Alpha-Sight will:
1. Fetch paper metadata
2. Download PDF
3. Extract key information
4. Generate analysis report
```

### Example 2: Deep Analysis with Reproduction

```
User: "Analyze arXiv 2401.12345 --depth=deep"

Alpha-Sight will:
1. Fetch and analyze paper
2. Assess project fit
3. Search for official code repository
4. Clone and run (or implement from scratch)
5. Generate comprehensive report
```

### Example 3: Domain Search

```
User: "Find latest Mixture of Experts papers --depth=medium --language=chinese"

Alpha-Sight will:
1. Search arXiv for MoE papers
2. Present top results
3. Analyze selected paper(s)
4. Generate Chinese report
```

## Output

### Analysis Report

Generated at `./alpha-sight/reports/{arxiv_id}_analysis.md`:

```markdown
# Paper Analysis Report: {title}

## Basic Information
- arXiv ID: 2401.12345
- Published: 2024-01-15
- Authors: Author A, Author B
- Categories: cs.LG, cs.AI

## Core Contributions
- Contribution 1
- Contribution 2
- Contribution 3

## Technical Details
{methods, algorithms, architecture}

## Project Fit Assessment
### Relevance Score: 8/10
### Potential Applications
- Application 1
- Application 2

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
```

### Files Generated

- **PDF**: `./alpha-sight/papers/{arxiv_id}.pdf`
- **Report**: `./alpha-sight/reports/{arxiv_id}_analysis.md`
- **Code** (if reproduced): `./alpha-sight/sandbox/{arxiv_id}_reproduction/`
- **Index**: `./alpha-sight/index.json` (updated)

## History Management

View analyzed papers in `./alpha-sight/index.json`:

```json
{
  "version": "1.0",
  "papers": [
    {
      "arxiv_id": "2401.12345",
      "title": "Paper Title",
      "analyzed_date": "2026-01-07T10:30:00Z",
      "analysis": {
        "depth": "medium",
        "relevance_score": 8.5
      },
      "reproduction": {
        "status": "completed",
        "method": "official_repo"
      }
    }
  ]
}
```

## Code Reproduction Workflow

### Priority 1: Official Repository

Alpha-Sight searches for official code in this order:

1. arXiv page "Code" link
2. GitHub/GitLab URLs in PDF
3. Semantic Scholar linked repositories
4. Papers with Code database

If found, it will:
- Clone the repository
- Set up environment with `uv`
- Install dependencies
- Run tests/examples

### Priority 2: Self-Implementation

If no official code exists, Alpha-Sight will:

1. Read paper method sections
2. Identify required libraries
3. Query Context7 for documentation (if available)
4. Generate implementation code
5. Test in sandbox
6. Iterate up to 5 times if errors occur

## Resource Limits

- **Memory**: 4GB per sandbox
- **Disk**: 2GB per sandbox
- **Timeout**: Based on `--depth` parameter
- **Max Iterations**: 5 for self-implementation

## API Rate Limits

### arXiv API
- Recommended: 1 request per 3 seconds
- Automatic retry with exponential backoff

### Semantic Scholar API
- Without API key: 100 requests per 5 minutes
- With API key: 5,000 requests per 5 minutes

## Troubleshooting

### Paper Not Found
- Verify arXiv ID format (e.g., `2401.12345`)
- Check if paper exists on arxiv.org
- Only arxiv.org papers are supported

### Reproduction Failed
- Check `./alpha-sight/sandbox/{arxiv_id}_reproduction/` for logs
- Use `--cleanup=never` to preserve files for debugging
- Some papers may require manual intervention

### API Errors
- Semantic Scholar: Skill continues without citation data if API fails
- arXiv: Automatic retry up to 3 times

### Timeout
- Increase depth parameter if needed
- Complex reproductions may require manual implementation

## Advanced Usage

### Custom Scripts

Use the provided Python scripts directly:

```bash
# Fetch paper
python ./alpha-sight/skill/scripts/arxiv_fetcher.py 2401.12345

# Manage index
python ./alpha-sight/skill/scripts/index_manager.py
```

### Integration with Context7

Alpha-Sight automatically queries Context7 when:
- Specific libraries are detected (PyTorch, TensorFlow, JAX, etc.)
- Documentation is needed for implementation
- Context7 is available in your environment

## Contributing

Contributions are welcome! Please see the repository for guidelines.

## License

MIT License - see LICENSE file for details

## Support

- GitHub Issues: https://github.com/your-org/alpha-sight/issues
- Documentation: https://docs.alpha-sight.dev
- Email: support@alpha-sight.dev

## Acknowledgments

- arXiv for providing open access to scientific papers
- Semantic Scholar for citation data
- Context7 for library documentation
- Claude Code for the skill framework

---

**Version**: 1.0.0
**Last Updated**: 2026-01-07
