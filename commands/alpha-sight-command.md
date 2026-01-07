# /alpha-sight-command

分析 arXiv 论文，提供深度分析和代码复现，生成结构化报告。

## Usage

/alpha-sight-command <arxiv-id-or-url> [--depth=shallow|medium|deep] [--language=english|chinese] 

## Parameters

- `<arxiv-id-or-url>`: 必需，arXiv 论文 ID 或完整 URL
  - 示例：2301.12345, https://arxiv.org/abs/2301.12345, arxiv:2301.12345
- `[--depth]`: 可选，分析深度（默认：medium）
  - `shallow`: 基础信息和摘要分析
  - `medium`: 包含项目契合度评估和技术细节
  - `deep`: 完整分析 + 代码复现
- `[--language]`: 可选，报告语言（默认：english）
  - `english`: 英文报告
  - `chinese`: 中文报告


## 输出目录结构

```
alpha-sight/
├── papers/           # PDF 文件存储
├── reports/          # 分析报告
├── sandbox/          # 代码复现工作区
└── index.json        # 论文索引
```

## Workflow

### Step 1: 参数解析与环境准备
**指令：** 解析用户输入的参数，提取 arXiv ID，创建必要的目录结构。

1. **提取 arXiv ID**：
   - 从 URL 中提取 ID（如果提供的是完整 URL）
   - 清理 `arxiv:` 前缀
   - 验证 ID 格式（YYMM.NNNNN 或 YYMM.NNNNNN）

2. **解析参数**：
   - `--depth=` (默认: medium)
   - `--language=` (默认: english)
   - `--cleanup=` (默认: on-success)

3. **创建目录结构**：
   ```bash
   mkdir -p alpha-sight/papers alpha-sight/reports alpha-sight/sandbox
   ```

### Step 2: 获取论文
**指令：** 使用 arxiv_fetcher.py 脚本下载论文 PDF 和元数据。

执行命令：
```bash
cd .claude/skills/alpha-sight/scripts && python arxiv_fetcher.py {arxiv_id}
```

该脚本将：
- 从 arXiv API 获取元数据
- 下载 PDF 到 `alpha-sight/papers/{arxiv_id}.pdf`
- 显示：标题、作者、摘要、分类

### Step 3: 论文阅读与分析
**指令：** 读取下载的 PDF，提取关键信息并进行初步分析。

读取文件：`alpha-sight/papers/{arxiv_id}.pdf`

提取并展示：
1. **标题** 和 **作者列表**
2. **发布日期** 和 **学科分类**
3. **摘要**（完整文本）
4. **核心贡献**（3-5 个要点）
5. **技术细节**（方法、算法、架构）

### Step 4: 项目契合度评估
**指令：** 仅在 `depth=medium` 或 `depth=deep` 时执行。扫描当前项目，评估论文与项目的相关性。

1. **扫描项目文件**：
   ```bash
   find . -name "package.json" -o -name "requirements.txt" -o -name "pyproject.toml" -o -name "*.py" -o -name "*.js" | head -20
   ```

2. **分析并提供**：
   - **相关性评分** (1-10)：论文与当前项目的相关程度
   - **技术重叠**：哪些技术/概念与项目重叠
   - **潜在应用**：论文如何改进当前项目
   - **实施建议**：具体可行的实施建议

3. **生成架构对比图**：
   - 使用 Mermaid 图表对比论文架构与项目架构

### Step 5: 代码复现
**指令：** 仅在 `depth=deep` 时执行。尝试复现论文中的代码实现。

#### 5.1 搜索官方代码库
- 检查论文中的代码链接
- 搜索 GitHub / Papers with Code

**如果找到官方仓库**：
```bash
cd alpha-sight/sandbox && mkdir -p {arxiv_id}_reproduction && cd {arxiv_id}_reproduction && git clone {repo_url} official_repo
```

**如果没有官方仓库**：

从零实现（最多 5 次迭代）：
1. 仔细阅读论文方法论部分
2. 识别所需库（PyTorch, TensorFlow 等）
3. 生成实现代码
4. 保存到 `alpha-sight/sandbox/{arxiv_id}_reproduction/custom_impl/`
5. 测试（超时 30 分钟）：
   ```bash
   cd alpha-sight/sandbox/{arxiv_id}_reproduction/custom_impl && timeout 1800 python main.py
   ```
6. 如果失败，分析错误并重试（最多 5 次）

#### 5.2 环境配置
使用 `uv` 管理 Python 依赖：
```bash
cd alpha-sight/sandbox/{arxiv_id}_reproduction && uv venv && source .venv/bin/activate
```

### Step 6: 生成分析报告
**指令：** 创建结构化的分析报告，根据 `--language` 参数选择语言。

报告路径：`alpha-sight/reports/{arxiv_id}_analysis.md`

#### 中文报告模板 (language=chinese)：
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

#### 英文报告模板 (language=english)：
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

### Step 7: 更新索引
**指令：** 将论文信息添加到 `alpha-sight/index.json` 索引文件。

执行命令：
```bash
cd .claude/skills/alpha-sight/scripts && python -c "from index_manager import IndexManager; m = IndexManager(); print('Index updated')"
```

索引条目包含：
- **基本信息**: arxiv_id, title, authors, dates, categories
- **分析信息**: depth, language, relevance_score, paths
- **复现信息**: status, method, iterations, notes
- **标签**: tags, project_impact

### Step 8: 清理临时文件
**指令：** 根据 `--cleanup` 参数清理临时文件。

清理条件：
- `cleanup=always`：总是清理
- `cleanup=on-success` 且复现成功：清理
- `cleanup=never`：不清理

清理命令：
```bash
rm -rf alpha-sight/sandbox/{arxiv_id}_reproduction/.venv alpha-sight/sandbox/{arxiv_id}_reproduction/temp
```

### Step 9: 输出总结
**指令：** 向用户展示分析完成的总结信息。

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

## 错误处理

- **论文未找到**: 验证 arXiv ID 是否正确
- **超时**: 在报告中标记为部分完成
- **API 错误**: 继续执行，跳过缺失数据
- **Git clone 错误**: 转向自实现
- **依赖安装失败**: 记录错误，继续其他步骤

## Constraints

1. 仅处理来自 arxiv.org 的论文
2. 在 sandbox 中使用 `uv` 管理 Python 依赖
3. 资源限制：4GB 内存，2GB 磁盘，根据深度设置超时
4. 分析后必须更新 index.json
5. 失败时保留 sandbox 以便调试
6. 自实现最多 5 次迭代
7. 报告必须使用指定语言
8. 所有路径使用相对路径（相对于项目根目录）
