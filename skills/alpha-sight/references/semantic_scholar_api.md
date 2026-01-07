# Semantic Scholar API Reference

## Overview
The Semantic Scholar Academic Graph API provides access to scholarly paper and author data, enabling retrieval of detailed information, citations, and references.

**Source**: Context7 - /websites/api_semanticscholar_api-docs

## Base URL
```
https://api.semanticscholar.org
```

## Authentication
Optional API key for higher rate limits:
```
x-api-key: YOUR_API_KEY
```

## Get Paper by External ID

### Endpoint
```
GET /graph/v1/paper/{paper_id}
```

### Paper ID Formats
- Semantic Scholar ID: `649def34f8be52c8b66281af98ae884c09aef38b`
- DOI: `DOI:10.18653/v1/N18-3011`
- arXiv: `arXiv:1705.10311` or `ARXIV:1705.10311`
- MAG: `MAG:112218234`
- ACL: `ACL:W12-3903`
- PubMed: `PMID:19872477`
- Corpus ID: `CorpusID:37220927`

### Query Parameters
- `fields`: Comma-separated list of fields to return

**Available Fields:**
- `paperId`, `corpusId`, `externalIds`
- `title`, `abstract`, `venue`, `year`
- `referenceCount`, `citationCount`, `influentialCitationCount`
- `isOpenAccess`, `openAccessPdf`
- `fieldsOfStudy`, `s2FieldsOfStudy`
- `publicationTypes`, `publicationDate`, `publicationVenue`
- `journal`, `authors`, `citations`, `references`
- `citationStyles` (includes BibTeX)

### Example Request
```bash
# Get paper by arXiv ID
curl "https://api.semanticscholar.org/graph/v1/paper/arXiv:2401.12345?fields=title,abstract,authors,citationCount,referenceCount,citations,references"
```

### Example Response
```json
{
  "paperId": "5c5751d45e298cea054f32b392c12c61027d2fe7",
  "corpusId": 215416146,
  "externalIds": {
    "ArXiv": "2401.12345",
    "DOI": "10.18653/V1/2020.ACL-MAIN.447",
    "CorpusId": 215416146
  },
  "url": "https://www.semanticscholar.org/paper/5c5751d45e298cea054f32b392c12c61027d2fe7",
  "title": "Paper Title",
  "abstract": "Paper abstract...",
  "venue": "Conference Name",
  "year": 2024,
  "referenceCount": 59,
  "citationCount": 453,
  "influentialCitationCount": 90,
  "isOpenAccess": true,
  "openAccessPdf": {
    "url": "https://example.com/paper.pdf",
    "status": "HYBRID"
  },
  "fieldsOfStudy": ["Computer Science"],
  "s2FieldsOfStudy": [
    {
      "category": "Computer Science",
      "source": "external"
    }
  ],
  "publicationTypes": ["JournalArticle"],
  "publicationDate": "2024-01-15",
  "journal": {
    "volume": "40",
    "pages": "116-135",
    "name": "Journal Name"
  },
  "citationStyles": {
    "bibtex": "@article{...}"
  },
  "authors": [
    {
      "authorId": "1741101",
      "name": "Author Name"
    }
  ]
}
```

## Get Paper Citations

### Endpoint
```
GET /graph/v1/paper/{paper_id}/citations
```

### Query Parameters
- `fields`: Fields to return for each citation
- `offset`: Pagination offset (default: 0)
- `limit`: Number of results (default: 100, max: 1000)

### Example
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/arXiv:2401.12345/citations?fields=title,year,authors&limit=10"
```

### Response
```json
{
  "offset": 0,
  "next": 10,
  "data": [
    {
      "citingPaper": {
        "paperId": "...",
        "title": "Citing Paper Title",
        "year": 2024,
        "authors": [...]
      }
    }
  ]
}
```

## Get Paper References

### Endpoint
```
GET /graph/v1/paper/{paper_id}/references
```

### Query Parameters
Same as citations endpoint

### Example
```bash
curl "https://api.semanticscholar.org/graph/v1/paper/arXiv:2401.12345/references?fields=title,year,authors&limit=10"
```

### Response
```json
{
  "offset": 0,
  "next": 10,
  "data": [
    {
      "citedPaper": {
        "paperId": "...",
        "title": "Referenced Paper Title",
        "year": 2023,
        "authors": [...]
      }
    }
  ]
}
```

## Get Recommended Papers

### Endpoint
```
GET /recommendations/v1/papers/forpaper/{paper_id}
```

### Query Parameters
- `fields`: Fields to return
- `limit`: Number of recommendations (default: 10, max: 500)

### Example
```bash
curl "https://api.semanticscholar.org/recommendations/v1/papers/forpaper/arXiv:2401.12345?fields=title,abstract,year,authors&limit=10"
```

### Response
```json
{
  "recommendedPapers": [
    {
      "paperId": "...",
      "title": "Recommended Paper Title",
      "abstract": "...",
      "year": 2024,
      "authors": [...]
    }
  ]
}
```

## Python Example

```python
import requests

def get_paper_by_arxiv(arxiv_id, api_key=None):
    """
    Fetch paper details from Semantic Scholar by arXiv ID

    Args:
        arxiv_id: arXiv ID (e.g., "2401.12345")
        api_key: Optional API key for higher rate limits

    Returns:
        Dictionary with paper details
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}"

    params = {
        'fields': 'title,abstract,authors,year,citationCount,referenceCount,externalIds,fieldsOfStudy'
    }

    headers = {}
    if api_key:
        headers['x-api-key'] = api_key

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()

def get_paper_citations(arxiv_id, limit=100, api_key=None):
    """
    Fetch citations for a paper

    Args:
        arxiv_id: arXiv ID
        limit: Number of citations to fetch
        api_key: Optional API key

    Returns:
        List of citing papers
    """
    url = f"https://api.semanticscholar.org/graph/v1/paper/arXiv:{arxiv_id}/citations"

    params = {
        'fields': 'title,year,authors',
        'limit': limit
    }

    headers = {}
    if api_key:
        headers['x-api-key'] = api_key

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()

    return response.json()['data']

# Example usage
if __name__ == "__main__":
    arxiv_id = "2401.12345"

    # Get paper details
    paper = get_paper_by_arxiv(arxiv_id)
    print(f"Title: {paper['title']}")
    print(f"Citations: {paper['citationCount']}")
    print(f"References: {paper['referenceCount']}")

    # Get citations
    citations = get_paper_citations(arxiv_id, limit=10)
    print(f"\nFirst 10 citing papers:")
    for item in citations:
        citing_paper = item['citingPaper']
        print(f"- {citing_paper['title']} ({citing_paper.get('year', 'N/A')})")
```

## Rate Limiting
- **Without API key**: 100 requests per 5 minutes
- **With API key**: 5,000 requests per 5 minutes

## Error Codes
- `400`: Bad Request (invalid parameters)
- `404`: Paper not found
- `429`: Rate limit exceeded
- `500`: Internal server error

## Best Practices
1. Use API key for production applications
2. Implement exponential backoff for retries
3. Cache results to minimize API calls
4. Request only needed fields to reduce response size
5. Handle 404 errors gracefully (paper may not be indexed)

## References
- Official API Documentation: https://api.semanticscholar.org/api-docs/
- Context7 Library: /websites/api_semanticscholar_api-docs
- Python Client: /danielnsilva/semanticscholar
