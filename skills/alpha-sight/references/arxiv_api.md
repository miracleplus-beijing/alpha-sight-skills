# arXiv API Reference

## Overview
Official documentation for the arXiv API, providing programmatic access to arXiv's e-print repository.

**Source**: Context7 - /websites/info_arxiv-help-api

## Base URL
```
http://export.arxiv.org/api/query
```

## Query Parameters

### search_query (string)
Specifies search terms and fields. Supports logical operators (AND, OR, NOT).

**Search Fields:**
- `all:` - All fields
- `ti:` - Title
- `au:` - Author
- `abs:` - Abstract
- `cat:` - Category

**Example:**
```
search_query=all:electron+AND+ti:positron
search_query=au:"Einstein"+AND+ti:"Relativity"
```

### id_list (comma-delimited string)
A comma-separated list of arXiv document IDs to retrieve.

**Example:**
```
id_list=2401.12345,2401.12346
```

### start (int)
The index of the first result to return (0-based). Default: 0

### max_results (int)
The maximum number of results to return. Default: 10

### sortBy (string)
Field to sort results by:
- `relevance`
- `lastUpdatedDate`
- `submittedDate`

### sortOrder (string)
Order of sorting:
- `ascending`
- `descending`

## Example Queries

### Fetch by ID
```bash
GET http://export.arxiv.org/api/query?id_list=2401.12345
```

### Search by keyword
```bash
GET http://export.arxiv.org/api/query?search_query=all:electron&start=0&max_results=5
```

### Search with sorting
```bash
GET http://export.arxiv.org/api/query?search_query=all:mixture+of+experts&sortBy=submittedDate&sortOrder=descending&max_results=10
```

## Response Format (Atom XML)

### Feed Metadata
- `<title>`: Title of the feed
- `<id>`: Unique identifier for the feed
- `<link>`: Links related to the feed (self, next)
- `<updated>`: Timestamp of the last update
- `<opensearch:totalResults>`: Total number of results
- `<opensearch:startIndex>`: Starting index of current result set
- `<opensearch:itemsPerPage>`: Number of items returned

### Entry Metadata (Individual Papers)
- `<id>`: arXiv identifier (e.g., http://arxiv.org/abs/2401.12345v1)
- `<published>`: Publication date
- `<updated>`: Last update date
- `<title>`: Title of the article
- `<summary>`: Abstract of the article
- `<author>`: Author information
  - `<name>`: Author's name
  - `<arxiv:affiliation>`: Author's affiliation (optional)
- `<link>`: Links to the article
  - `rel='alternate'`: Link to abstract page
  - `type='application/pdf'`: Link to PDF version
- `<category>`: Subject classifications
- `<arxiv:primary_category>`: Primary subject category
- `<arxiv:comment>`: Comments section
- `<arxiv:journal_ref>`: Journal reference

## PDF Download
```
GET https://arxiv.org/pdf/{arxiv_id}.pdf
```

**Example:**
```bash
curl -O "https://arxiv.org/pdf/2401.12345.pdf"
```

## Python Example (using feedparser)

```python
import urllib
import feedparser

# Base API query URL
base_url = 'http://export.arxiv.org/api/query?'

# Search parameters
search_query = 'all:electron'
start = 0
max_results = 5

query = 'search_query=%s&start=%i&max_results=%i' % (search_query, start, max_results)

# Expose namespaces in feedparser
feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'

# Perform GET request
response = urllib.urlopen(base_url + query).read()

# Parse response
feed = feedparser.parse(response)

# Print feed information
print('Feed title: %s' % feed.feed.title)
print('totalResults: %s' % feed.feed.opensearch_totalresults)

# Process entries
for entry in feed.entries:
    arxiv_id = entry.id.split('/abs/')[-1]
    print('arXiv ID: %s' % arxiv_id)
    print('Title: %s' % entry.title)
    print('Published: %s' % entry.published)
    print('Authors: %s' % ', '.join(author.name for author in entry.authors))

    # Get PDF link
    for link in entry.links:
        if link.title == 'pdf':
            print('PDF: %s' % link.href)

    print('Abstract: %s' % entry.summary)
```

## Common Subject Categories
- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning
- `cs.CL` - Computation and Language
- `cs.CV` - Computer Vision
- `cs.NE` - Neural and Evolutionary Computing
- `cs.CR` - Cryptography and Security
- `cs.DC` - Distributed, Parallel, and Cluster Computing

## Best Practices
1. Respect rate limits (avoid excessive requests)
2. Use exponential backoff for retries
3. Handle 503 errors (server busy) gracefully
4. Cache results when possible
5. Use specific search queries to reduce result sets

## References
- Official API Manual: http://export.arxiv.org/api_help/docs/user-manual.html
- Contact: arxiv-api@googlegroups.com
- Context7 Library: /websites/info_arxiv-help-api
