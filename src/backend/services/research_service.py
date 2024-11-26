"""Research service for paper search and analysis."""
import aiohttp
import asyncio
import logging
import xml.etree.ElementTree as ET
from typing import List, Optional, Dict
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ResearchService:
    def __init__(self):
        """Initialize the research service."""
        self.semantic_scholar_url = "https://api.semanticscholar.org/graph/v1"  # Updated to v1 graph API
        self.arxiv_url = "http://export.arxiv.org/api/query"
        self.session = None
        logger.info("ResearchService initialized")

    async def initialize(self):
        """Initialize HTTP session."""
        if not self.session:
            self.session = aiohttp.ClientSession(
                headers={
                    "User-Agent": "AI Research Hub/1.0",
                }
            )
            logger.info("HTTP session initialized")

    async def close(self):
        """Close HTTP session."""
        if self.session:
            await self.session.close()
            self.session = None
            logger.info("HTTP session closed")

    async def search_papers(
        self,
        query: str,
        page: int = 1,
        limit: int = 20,
        sources: List[str] = None
    ) -> Dict:
        """Search for papers using multiple sources."""
        start_time = datetime.now()
        logger.info(f"Starting paper search for query: {query}, page: {page}, limit: {limit}, sources: {sources}")

        if not self.session:
            logger.info("Initializing HTTP session")
            await self.initialize()

        try:
            # Calculate offset based on page number
            offset = (page - 1) * limit
            # Request more results per source to ensure we have enough after deduplication
            per_source_limit = limit * 2

            # Default to all sources if none specified
            sources = sources or ["semantic_scholar", "arxiv"]
            tasks = []

            # Create tasks based on selected sources
            if "semantic_scholar" in sources:
                tasks.append(self._search_semantic_scholar(query, per_source_limit, offset))
            else:
                tasks.append(asyncio.sleep(0))  # Dummy task if source not selected

            if "arxiv" in sources:
                tasks.append(self._search_arxiv(query, per_source_limit, offset))
            else:
                tasks.append(asyncio.sleep(0))  # Dummy task if source not selected

            # Search selected sources concurrently
            logger.info(f"Starting concurrent search of selected sources: {sources}")
            results = await asyncio.gather(*tasks)
            
            # Filter out empty results from dummy tasks
            semantic_results = results[0] if "semantic_scholar" in sources else []
            arxiv_results = results[1] if "arxiv" in sources else []
            
            logger.info(f"Found {len(semantic_results)} results from Semantic Scholar")
            logger.info(f"Found {len(arxiv_results)} results from arXiv")

            # Merge and deduplicate results
            combined_results = self._merge_results(semantic_results, arxiv_results)
            
            # Calculate total results (estimate)
            total_results = len(combined_results) * (page + 1)  # Estimate total based on current page
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            logger.info(f"Search completed in {duration} seconds with {len(combined_results)} total results")

            return {
                "results": combined_results[:limit],  # Return only requested number of results
                "total": total_results,
                "duration": duration,
                "page": page,
                "limit": limit,
                "query": query,
                "sources": sources
            }

        except Exception as e:
            logger.error(f"Error in search_papers: {str(e)}")
            logger.exception("Full traceback:")
            raise

    async def _search_semantic_scholar(self, query: str, limit: int, offset: int = 0) -> List[Dict]:
        """Search papers using Semantic Scholar API."""
        try:
            start_time = datetime.now()
            logger.info(f"Searching Semantic Scholar for: {query}")
            
            params = {
                "query": query,
                "limit": limit,
                "offset": offset,
                "fields": "title,abstract,authors,year,venue,url,citationCount"
            }
            
            async with self.session.get(
                f"{self.semantic_scholar_url}/paper/search",
                params=params
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    papers = data.get("data", [])
                    
                    # Transform to common format
                    transformed_papers = [{
                        "title": paper.get("title", ""),
                        "abstract": paper.get("abstract", ""),
                        "authors": [author.get("name", "") for author in paper.get("authors", [])],
                        "year": paper.get("year"),
                        "venue": paper.get("venue", ""),
                        "url": paper.get("url", ""),
                        "citations": paper.get("citationCount", 0),
                        "source": "Semantic Scholar"
                    } for paper in papers]
                    
                    logger.info(f"Found {len(transformed_papers)} papers from Semantic Scholar")
                    return transformed_papers
                else:
                    logger.error(f"Semantic Scholar API error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error in Semantic Scholar search: {str(e)}")
            return []

    async def _search_arxiv(self, query: str, limit: int, offset: int = 0) -> List[Dict]:
        """Search papers using arXiv API."""
        try:
            start_time = datetime.now()
            logger.info(f"Searching arXiv for: {query}")
            
            # Format query according to arXiv API standards
            formatted_query = query.replace(' ', '+AND+')
            
            params = {
                'search_query': f'all:{formatted_query}',
                'start': str(offset),
                'max_results': str(limit),
                'sortBy': 'relevance',
                'sortOrder': 'descending'
            }
            
            async with self.session.get(
                self.arxiv_url,
                params=params
            ) as response:
                if response.status == 200:
                    results = self._parse_arxiv_response(await response.text())
                    duration = (datetime.now() - start_time).total_seconds()
                    logger.info(f"arXiv search completed in {duration} seconds")
                    logger.info(f"Found {len(results)} papers from arXiv")
                    return results
                else:
                    logger.error(f"arXiv API error: {response.status}")
                    return []
        except Exception as e:
            logger.error(f"Error in arXiv search: {str(e)}")
            return []

    def _parse_arxiv_response(self, xml_text: str) -> List[Dict]:
        """Parse arXiv XML response into common format."""
        try:
            root = ET.fromstring(xml_text)
            papers = []
            
            # Define XML namespaces
            ns = {
                'atom': 'http://www.w3.org/2005/Atom',
                'arxiv': 'http://arxiv.org/schemas/atom'
            }
            
            # Parse each entry
            for entry in root.findall('atom:entry', ns):
                try:
                    # Get basic metadata
                    title = entry.find('atom:title', ns).text.strip().replace('\n', ' ')
                    abstract = entry.find('atom:summary', ns).text.strip().replace('\n', ' ')
                    authors = [author.find('atom:name', ns).text.strip() for author in entry.findall('atom:author', ns)]
                    published = entry.find('atom:published', ns).text[:4]  # Get year
                    
                    # Get arXiv specific data
                    arxiv_id = entry.find('atom:id', ns).text.split('/')[-1]
                    primary_category = entry.find('arxiv:primary_category', ns).get('term', '')
                    
                    # Construct URLs
                    abstract_url = f"https://arxiv.org/abs/{arxiv_id}"
                    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
                    
                    paper = {
                        "title": title,
                        "abstract": abstract,
                        "authors": authors,
                        "year": published,
                        "venue": f"arXiv - {primary_category}",
                        "url": abstract_url,
                        "pdf_url": pdf_url,
                        "citations": 0,  # arXiv doesn't provide citation count
                        "source": "arXiv",
                        "arxiv_id": arxiv_id
                    }
                    papers.append(paper)
                except Exception as e:
                    logger.error(f"Error parsing arXiv entry: {str(e)}")
                    continue
            
            return papers
        except Exception as e:
            logger.error(f"Error parsing arXiv response: {str(e)}")
            return []

    def _merge_results(self, semantic_results: List[Dict], arxiv_results: List[Dict]) -> List[Dict]:
        """Merge and deduplicate results from multiple sources."""
        try:
            merged = []
            seen_titles = set()

            # Interleave results from both sources
            max_len = max(len(semantic_results), len(arxiv_results))
            for i in range(max_len):
                # Add Semantic Scholar result
                if i < len(semantic_results):
                    paper = semantic_results[i]
                    title = paper.get("title", "").lower()
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        merged.append(paper)
                
                # Add arXiv result
                if i < len(arxiv_results):
                    paper = arxiv_results[i]
                    title = paper.get("title", "").lower()
                    if title and title not in seen_titles:
                        seen_titles.add(title)
                        merged.append(paper)

            logger.info(f"Merged results: {len(merged)} unique papers")
            return merged
        except Exception as e:
            logger.error(f"Error merging results: {str(e)}")
            return []

    async def get_paper_details(self, paper_id: str) -> Optional[Dict]:
        """Get detailed information about a specific paper."""
        if not self.session:
            await self.initialize()

        try:
            logger.info(f"Fetching details for paper: {paper_id}")
            async with self.session.get(
                f"{self.semantic_scholar_url}/paper/{paper_id}"
            ) as response:
                response_text = await response.text()
                logger.info(f"Paper details response status: {response.status}")
                logger.info(f"Paper details response: {response_text[:200]}...")
                
                if response.status == 200:
                    data = await response.json()
                    logger.info("Successfully retrieved paper details")
                    return data
                else:
                    logger.error(f"Error getting paper details: {response.status}")
                    return None
        except Exception as e:
            logger.error(f"Error in get_paper_details: {str(e)}")
            return None

    async def analyze_paper(self, paper_id: str) -> Dict:
        """Analyze a paper using LLM."""
        logger.info(f"Analyzing paper: {paper_id}")
        # This is a placeholder for LLM integration
        return {
            "summary": "Paper analysis not implemented yet",
            "key_findings": [],
            "methodology": "",
            "future_work": []
        }