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
  - `shallow`: Abstract and key information only
  - `medium`: Full analysis + project fit assessment
  - `deep`: Full analysis + code reproduction

- `--language=[english|chinese]` (default: `english`)
  - `english`: Report in English
  - `chinese`: Report in Chinese

- `--cleanup=[on-success|always|never]` (default: `on-success`)
  - `on-success`: Clean temp files after success
  - `always`: Always clean
  - `never`: Keep all files for debugging

## Output Directory Structure

```
alpha-sight/
├── papers/           # PDF file storage
├── reports/          # Analysis reports
├── sandbox/          # Code reproduction workspace
└── index.json        # Paper index
```

## Workflow

### Step 1: Parameter Parsing and Environment Setup
**Instruction:** Parse user input parameters, extract arXiv ID, create necessary directory structure.

1. **Extract arXiv ID**:
   - Extract ID from URL (if full URL provided)
   - Clean `arxiv:` prefix
   - Validate ID format (YYMM.NNNNN or YYMM.NNNNNN)

2. **Parse Parameters**:
   - `--depth=` (default: medium)
   - `--language=` (default: english)
   - `--cleanup=` (default: on-success)

3. **Create Directory Structure**:
   ```bash
   mkdir -p alpha-sight/papers alpha-sight/reports alpha-sight/sandbox
   ```

### Step 2: Fetch Paper
**Instruction:** Use arxiv_fetcher.py script to download paper PDF and metadata.

Execute command:
```bash
cd .claude/skills/alpha-sight/scripts && python arxiv_fetcher.py {arxiv_id}
```

The script will:
- Fetch metadata from arXiv API
- Download PDF to `alpha-sight/papers/{arxiv_id}.pdf`
- Display: title, authors, abstract, categories

### Step 3: Paper Reading and Analysis
**Instruction:** Read the downloaded PDF, extract key information and perform initial analysis.

Read file: `alpha-sight/papers/{arxiv_id}.pdf`

Extract and display:
1. **Title** and **Author List**
2. **Publication Date** and **Subject Categories**
3. **Abstract** (full text)
4. **Core Contributions** (3-5 bullet points)
5. **Technical Details** (methods, algorithms, architecture)

### Step 4: Project Fit Assessment
**Instruction:** Scan current project and evaluate paper's relevance to the project.

1. **Scan Project Files**:
   ```bash
   find . -name "package.json" -o -name "requirements.txt" -o -name "pyproject.toml" -o -name "*.py" -o -name "*.js" | head -20
   ```

2. **Analyze and Provide**:
   - **Relevance Score** (1-10): Paper's relevance to current project
   - **Technology Overlap**: Which technologies/concepts overlap with project
   - **Potential Applications**: How the paper can improve current project
   - **Implementation Suggestions**: Specific actionable implementation suggestions

3. **Generate Architecture Comparison**:
   - Use Mermaid diagram to compare paper architecture vs. project architecture

### Step 5: Code Reproduction
**Instruction:** Only execute when `depth=deep`. Attempt to reproduce code implementation from the paper.

#### 5.1 Search for Official Repository
- Check paper for code links
- Search GitHub / Papers with Code

**If official repository found**:
```bash
cd alpha-sight/sandbox && mkdir -p {arxiv_id}_reproduction && cd {arxiv_id}_reproduction && git clone {repo_url} official_repo
```

**If no official repository**:

Implement from scratch (maximum 5 iterations):
1. Carefully read paper methodology section
2. Identify required libraries (PyTorch, TensorFlow, etc.)
3. Generate implementation code
4. Save to `alpha-sight/sandbox/{arxiv_id}_reproduction/custom_impl/`
5. Test (30 minute timeout):
   ```bash
   cd alpha-sight/sandbox/{arxiv_id}_reproduction/custom_impl && timeout 1800 python main.py
   ```
6. If failed, analyze error and retry (maximum 5 times)

#### 5.2 Environment Configuration
Use `uv` to manage Python dependencies:
```bash
cd alpha-sight/sandbox/{arxiv_id}_reproduction && uv venv && source .venv/bin/activate
```

### Step 6: Generate Analysis Report
**Instruction:** Create structured analysis report, choose language based on `--language` parameter.

Report path: `alpha-sight/reports/{arxiv_id}_analysis.md`

#### Chinese Report Template (language=chinese):
```markdown
# 论文深度分析报告：{Title}

## 基本信息
- arXiv ID: {arxiv_id}
- 发布日期: {date}
- 作者: {authors}
- 分类: {categories}

## 摘要
{abstract in Chinese if needed}

## 核心贡献
1. ...
2. ...
3. ...

## 技术细节深度分析
{detailed analysis in Chinese}

## 项目契合度评估
### 相关性评分：X/10
{assessment in Chinese}

### 技术重叠
{technology overlap}

### 潜在应用
{potential applications}

## 实施建议
{suggestions in Chinese}

## 代码复现状态
- 状态: {成功/失败/部分成功}
- 方法: {官方仓库/自实现}
- 迭代次数: {iterations}
- 备注: {notes}

## 架构对比
{Mermaid diagram}
```

#### English Report Template (language=english):
```markdown
# Paper Analysis Report: {Title}

## Basic Information
- arXiv ID: {arxiv_id}
- Published: {date}
- Authors: {authors}
- Categories: {categories}

## Abstract
{original abstract}

## Core Contributions
1. ...
2. ...
3. ...

## Technical Details
{detailed analysis}

## Project Fit Assessment
### Relevance Score: X/10
{assessment}

### Technology Overlap
{technology overlap}

### Potential Applications
{potential applications}

## Implementation Suggestions
{suggestions}

## Reproduction Status
- Status: {success/failed/partial}
- Method: {official repo/custom implementation}
- Iterations: {iterations}
- Notes: {notes}

## Architecture Comparison
{Mermaid diagram}
```

### Step 7: Update Index
**Instruction:** Add paper information to `alpha-sight/index.json` index file.

Execute command:
```bash
cd .claude/skills/alpha-sight/scripts && python -c "from index_manager import IndexManager; m = IndexManager(); print('Index updated')"
```

Index entry contains:
- **Basic info**: arxiv_id, title, authors, dates, categories
- **Analysis info**: depth, language, relevance_score, paths
- **Reproduction info**: status, method, iterations, notes
- **Tags**: tags, project_impact

### Step 8: Clean Temporary Files
**Instruction:** Clean temporary files based on `--cleanup` parameter.

Cleanup conditions:
- `cleanup=always`: Always clean
- `cleanup=on-success` and reproduction succeeded: Clean
- `cleanup=never`: Don't clean

Cleanup command:
```bash
rm -rf alpha-sight/sandbox/{arxiv_id}_reproduction/.venv alpha-sight/sandbox/{arxiv_id}_reproduction/temp
```

### Step 9: Output Summary
**Instruction:** Display analysis completion summary to user.

```
✓ Analysis Complete!

Paper: {title}
arXiv ID: {arxiv_id}
Depth: {depth}
Language: {language}
Relevance Score: {score}/10

📄 Report: alpha-sight/reports/{arxiv_id}_analysis.md
📕 PDF: alpha-sight/papers/{arxiv_id}.pdf
🗂️ Index: alpha-sight/index.json

{If depth=deep:}
💻 Code: alpha-sight/sandbox/{arxiv_id}_reproduction/
```

## Error Handling

- **Paper not found**: Verify arXiv ID is correct
- **Timeout**: Mark as partial completion in report
- **API errors**: Continue execution, skip missing data
- **Git clone errors**: Switch to custom implementation
- **Dependency installation failed**: Log error, continue other steps

## Constraints

1. Only process papers from arxiv.org
2. Use `uv` to manage Python dependencies in sandbox
3. Resource limits: 4GB memory, 2GB disk, timeout based on depth
4. Must update index.json after analysis
5. Preserve sandbox on failure for debugging
6. Maximum 5 iterations for custom implementation
7. Report must use specified language
8. All paths use relative paths (relative to project root)

## Tools to Use

- **Bash**: Execute arxiv_fetcher.py, index_manager.py, git clone, sandbox commands
- **Read**: Read downloaded PDF, configuration files
- **Write**: Create reports, save code
- **Glob**: Find project files
- **Grep**: Search codebase patterns
- **mcp__context7__resolve-library-id**: Resolve library names (optional)
- **mcp__context7__query-docs**: Query library documentation (optional)
- **AskUserQuestion**: Confirm reproduction (when depth=medium)

## Important Notes

1. **Only process papers from arxiv.org** (English papers only)
2. **Always use `uv` for Python dependency management** in sandbox
3. **Never exceed resource limits** (4GB memory, 2GB disk, timeout per depth)
4. **Always update index.json** after each analysis using index_manager.py script
5. **Preserve sandbox on failure** for debugging
6. **Use Context7 only when available** - gracefully degrade if not
7. **Maximum 5 iterations** for self-implementation loop
8. **Always use arxiv_fetcher.py script** to fetch papers
9. **Always use index_manager.py script** to update index
10. **Project fit assessment is always performed** regardless of depth level

## Example Usage

```
User: "Analyze arXiv 2401.12345"
→ Triggers skill with default parameters (depth=medium, language=english)

User: "Find latest MoE papers and analyze with deep reproduction --language=chinese"
→ Searches arXiv for MoE papers, analyzes with depth=deep, outputs in Chinese

User: "Reproduce this paper 2312.xxxxx"
→ Triggers skill with depth=deep (implied by "reproduce")
```
