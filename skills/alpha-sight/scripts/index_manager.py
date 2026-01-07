#!/usr/bin/env python3
"""
Index Manager for Alpha-Sight
Manages the index.json file for tracking analyzed papers
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class IndexManager:
    """Manager for alpha-sight index.json"""

    def __init__(self, index_path: str = None):
        if index_path is None:
            # Get the project root (4 levels up from scripts directory)
            script_dir = Path(__file__).parent
            project_root = script_dir.parent.parent.parent.parent
            index_path = project_root / "alpha-sight" / "index.json"
        self.index_path = Path(index_path)
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_index_exists()

    def _ensure_index_exists(self):
        """Create index.json if it doesn't exist"""
        if not self.index_path.exists():
            initial_data = {
                "version": "1.0",
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "papers": [],
                "statistics": {
                    "total_papers": 0,
                    "by_status": {
                        "analyzed_only": 0,
                        "reproduced": 0,
                        "failed": 0
                    },
                    "by_category": {}
                }
            }
            self._save_index(initial_data)

    def _load_index(self) -> Dict:
        """Load index.json"""
        with open(self.index_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_index(self, data: Dict):
        """Save index.json"""
        data["last_updated"] = datetime.utcnow().isoformat() + "Z"
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def paper_exists(self, arxiv_id: str) -> bool:
        """Check if paper already exists in index"""
        index = self._load_index()
        return any(p['arxiv_id'] == arxiv_id for p in index['papers'])

    def get_paper(self, arxiv_id: str) -> Optional[Dict]:
        """Get paper entry by arXiv ID"""
        index = self._load_index()
        for paper in index['papers']:
            if paper['arxiv_id'] == arxiv_id:
                return paper
        return None

    def add_paper(self, paper_data: Dict):
        """Add new paper to index"""
        index = self._load_index()

        # Check if already exists
        if self.paper_exists(paper_data['arxiv_id']):
            print(f"Paper {paper_data['arxiv_id']} already exists. Use update_paper() instead.")
            return

        # Add paper
        index['papers'].append(paper_data)

        # Update statistics
        self._update_statistics(index)

        # Save
        self._save_index(index)
        print(f"Added paper {paper_data['arxiv_id']} to index")

    def update_paper(self, arxiv_id: str, updates: Dict):
        """Update existing paper entry"""
        index = self._load_index()

        # Find and update paper
        for i, paper in enumerate(index['papers']):
            if paper['arxiv_id'] == arxiv_id:
                # Deep merge updates
                index['papers'][i] = self._deep_merge(paper, updates)
                break
        else:
            print(f"Paper {arxiv_id} not found in index")
            return

        # Update statistics
        self._update_statistics(index)

        # Save
        self._save_index(index)
        print(f"Updated paper {arxiv_id} in index")

    def _deep_merge(self, base: Dict, updates: Dict) -> Dict:
        """Deep merge two dictionaries"""
        result = base.copy()
        for key, value in updates.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def _update_statistics(self, index: Dict):
        """Update statistics in index"""
        papers = index['papers']

        # Total papers
        index['statistics']['total_papers'] = len(papers)

        # By status
        by_status = {
            "analyzed_only": 0,
            "reproduced": 0,
            "failed": 0
        }
        for paper in papers:
            status = paper.get('reproduction', {}).get('status', 'not_started')
            if status == 'completed':
                by_status['reproduced'] += 1
            elif status in ['failed', 'partial']:
                by_status['failed'] += 1
            else:
                by_status['analyzed_only'] += 1

        index['statistics']['by_status'] = by_status

        # By category
        by_category = {}
        for paper in papers:
            for cat in paper.get('categories', []):
                by_category[cat] = by_category.get(cat, 0) + 1

        index['statistics']['by_category'] = by_category

    def list_papers(self, sort_by: str = 'date', limit: Optional[int] = None) -> List[Dict]:
        """List all papers with optional sorting and limit"""
        index = self._load_index()
        papers = index['papers']

        # Sort
        if sort_by == 'date':
            papers = sorted(papers, key=lambda p: p.get('analyzed_date', ''), reverse=True)
        elif sort_by == 'relevance':
            papers = sorted(papers, key=lambda p: p.get('analysis', {}).get('relevance_score', 0), reverse=True)

        # Limit
        if limit:
            papers = papers[:limit]

        return papers

    def search_by_tag(self, tag: str) -> List[Dict]:
        """Search papers by tag"""
        index = self._load_index()
        return [p for p in index['papers'] if tag in p.get('tags', [])]

    def get_statistics(self) -> Dict:
        """Get index statistics"""
        index = self._load_index()
        return index['statistics']


if __name__ == "__main__":
    # Example usage
    manager = IndexManager()

    # Example paper data
    example_paper = {
        "arxiv_id": "2401.12345",
        "title": "Example Paper",
        "authors": ["Author A", "Author B"],
        "published_date": "2024-01-15",
        "analyzed_date": datetime.utcnow().isoformat() + "Z",
        "categories": ["cs.LG", "cs.AI"],
        "abstract": "This is an example abstract...",
        "analysis": {
            "depth": "medium",
            "language": "english",
            "relevance_score": 8.5,
            "report_path": "./reports/2401.12345_analysis.md",
            "pdf_path": "./papers/2401.12345.pdf"
        },
        "reproduction": {
            "status": "not_started",
            "method": "none",
            "repo_url": None,
            "sandbox_path": None,
            "iterations": 0,
            "success_rate": 0.0,
            "notes": ""
        },
        "citations": {
            "cited_by_count": 0,
            "references_count": 0,
            "related_papers": []
        },
        "tags": ["MoE", "Transformer"],
        "project_impact": {
            "applicable": True,
            "suggestions": []
        }
    }

    # Add paper
    if not manager.paper_exists("2401.12345"):
        manager.add_paper(example_paper)

    # Get statistics
    stats = manager.get_statistics()
    print("\n=== Statistics ===")
    print(json.dumps(stats, indent=2))
