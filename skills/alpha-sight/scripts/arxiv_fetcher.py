#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
arXiv Paper Fetcher
Fetches paper metadata and PDFs from arXiv.org
"""

import sys
import io
import requests
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, Optional
import time

# Fix Windows console encoding issue
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


class ArxivFetcher:
    """Fetcher for arXiv papers"""

    BASE_API_URL = "http://export.arxiv.org/api/query"
    BASE_PDF_URL = "https://arxiv.org/pdf"

    def __init__(self, output_dir: str = None):
        if output_dir is None:
            # Get the project root (4 levels up from scripts directory)
            script_dir = Path(__file__).parent
            project_root = script_dir.parent.parent.parent.parent
            output_dir = project_root / "alpha-sight" / "papers"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def fetch_metadata(self, arxiv_id: str) -> Optional[Dict]:
        """
        Fetch paper metadata from arXiv API

        Args:
            arxiv_id: arXiv ID (e.g., "2401.12345")

        Returns:
            Dictionary with paper metadata or None if failed
        """
        # Clean arxiv_id
        arxiv_id = arxiv_id.replace("arxiv:", "").replace("arXiv:", "").strip()

        # Build API URL
        url = f"{self.BASE_API_URL}?id_list={arxiv_id}"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            # Parse XML
            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            entry = root.find('atom:entry', ns)
            if entry is None:
                print(f"No entry found for arXiv ID: {arxiv_id}")
                return None

            # Extract metadata
            metadata = {
                'arxiv_id': arxiv_id,
                'title': entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                'abstract': entry.find('atom:summary', ns).text.strip(),
                'published_date': entry.find('atom:published', ns).text.split('T')[0],
                'updated_date': entry.find('atom:updated', ns).text.split('T')[0],
                'authors': [
                    author.find('atom:name', ns).text
                    for author in entry.findall('atom:author', ns)
                ],
                'categories': [
                    cat.get('term')
                    for cat in entry.findall('atom:category', ns)
                ],
                'pdf_url': f"{self.BASE_PDF_URL}/{arxiv_id}.pdf"
            }

            return metadata

        except requests.RequestException as e:
            print(f"Error fetching metadata: {e}")
            return None
        except ET.ParseError as e:
            print(f"Error parsing XML: {e}")
            return None

    def download_pdf(self, arxiv_id: str, max_retries: int = 3) -> Optional[Path]:
        """
        Download paper PDF

        Args:
            arxiv_id: arXiv ID
            max_retries: Maximum number of retry attempts

        Returns:
            Path to downloaded PDF or None if failed
        """
        arxiv_id = arxiv_id.replace("arxiv:", "").replace("arXiv:", "").strip()
        pdf_url = f"{self.BASE_PDF_URL}/{arxiv_id}.pdf"
        pdf_path = self.output_dir / f"{arxiv_id}.pdf"

        # Check if already downloaded
        if pdf_path.exists():
            print(f"PDF already exists: {pdf_path}")
            return pdf_path

        # Download with retries
        for attempt in range(max_retries):
            try:
                print(f"Downloading PDF (attempt {attempt + 1}/{max_retries})...")
                response = requests.get(pdf_url, timeout=60, stream=True)
                response.raise_for_status()

                # Save PDF
                with open(pdf_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)

                print(f"PDF downloaded: {pdf_path}")
                return pdf_path

            except requests.RequestException as e:
                print(f"Download attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    print("Max retries reached. Download failed.")
                    return None

        return None

    def search_papers(self, query: str, max_results: int = 10) -> list:
        """
        Search arXiv papers by query

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of paper metadata dictionaries
        """
        url = f"{self.BASE_API_URL}?search_query=all:{query}&max_results={max_results}&sortBy=submittedDate&sortOrder=descending"

        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()

            root = ET.fromstring(response.content)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}

            papers = []
            for entry in root.findall('atom:entry', ns):
                # Extract arXiv ID from entry ID
                entry_id = entry.find('atom:id', ns).text
                arxiv_id = entry_id.split('/abs/')[-1]

                paper = {
                    'arxiv_id': arxiv_id,
                    'title': entry.find('atom:title', ns).text.strip().replace('\n', ' '),
                    'abstract': entry.find('atom:summary', ns).text.strip()[:200] + '...',
                    'published_date': entry.find('atom:published', ns).text.split('T')[0],
                    'authors': [
                        author.find('atom:name', ns).text
                        for author in entry.findall('atom:author', ns)
                    ][:3],  # First 3 authors
                    'categories': [
                        cat.get('term')
                        for cat in entry.findall('atom:category', ns)
                    ]
                }
                papers.append(paper)

            return papers

        except Exception as e:
            print(f"Error searching papers: {e}")
            return []


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python arxiv_fetcher.py <arxiv_id>")
        sys.exit(1)

    arxiv_id = sys.argv[1]
    fetcher = ArxivFetcher()

    # Fetch metadata
    metadata = fetcher.fetch_metadata(arxiv_id)
    if metadata:
        print("\n=== Paper Metadata ===")
        print(f"Title: {metadata['title']}")
        print(f"Authors: {', '.join(metadata['authors'])}")
        print(f"Published: {metadata['published_date']}")
        print(f"Categories: {', '.join(metadata['categories'])}")
        print(f"\nAbstract:\n{metadata['abstract']}")

        # Download PDF
        pdf_path = fetcher.download_pdf(arxiv_id)
        if pdf_path:
            print(f"\n[OK] Success! PDF saved to: {pdf_path}")
    else:
        print("Failed to fetch paper metadata")
        sys.exit(1)
