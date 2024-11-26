"""Ollama service for paper analysis."""
import logging
from typing import Dict, Optional
import ollama
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self):
        """Initialize the Ollama service."""
        self.model = "llama3.2"  # Using llama3.2 for better performance
        self._executor = ThreadPoolExecutor(max_workers=2)  # Limit concurrent Ollama calls
        logger.info(f"OllamaService initialized with model: {self.model}")

    async def analyze_paper(self, paper_data: Dict) -> Dict:
        """Analyze a paper using Ollama."""
        try:
            # Extract relevant information
            title = paper_data.get("title", "")
            abstract = paper_data.get("abstract", "")
            authors = paper_data.get("authors", [])
            
            # Create analysis prompt
            prompt = self._create_analysis_prompt(title, abstract, authors)
            
            # Run analysis in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self._executor,
                self._run_ollama_analysis,
                prompt
            )
            
            # Parse and structure the response
            analysis = self._parse_analysis_response(response)
            
            logger.info(f"Successfully analyzed paper: {title}")
            return analysis
            
        except Exception as e:
            logger.error(f"Error in paper analysis: {str(e)}")
            return {
                "error": "Failed to analyze paper",
                "details": str(e)
            }

    def _create_analysis_prompt(self, title: str, abstract: str, authors: list) -> str:
        """Create a prompt for paper analysis."""
        return f"""Analyze the following research paper:

Title: {title}
Authors: {', '.join(authors)}
Abstract: {abstract}

Please provide a structured analysis with the following sections:
1. Summary (2-3 sentences)
2. Key Findings (bullet points)
3. Methodology Overview
4. Potential Applications
5. Future Research Directions

Format the response in a clear, structured way."""

    def _run_ollama_analysis(self, prompt: str) -> str:
        """Run the actual Ollama analysis."""
        try:
            # Generate response from Ollama
            response = ollama.generate(
                model=self.model,
                prompt=prompt,
                options={
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            )
            return response['response']
        except Exception as e:
            logger.error(f"Ollama generation error: {str(e)}")
            raise

    def _parse_analysis_response(self, response: str) -> Dict:
        """Parse and structure the Ollama response."""
        try:
            # Basic structure for the analysis
            analysis = {
                "summary": "",
                "key_findings": [],
                "methodology": "",
                "applications": [],
                "future_work": []
            }
            
            # Simple parsing based on section headers
            current_section = None
            current_text = []
            
            for line in response.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # Check for section headers
                lower_line = line.lower()
                if 'summary' in lower_line and ':' in line:
                    current_section = 'summary'
                    current_text = []
                elif 'key findings' in lower_line and ':' in line:
                    current_section = 'key_findings'
                    current_text = []
                elif 'methodology' in lower_line and ':' in line:
                    current_section = 'methodology'
                    current_text = []
                elif 'applications' in lower_line and ':' in line:
                    current_section = 'applications'
                    current_text = []
                elif 'future' in lower_line and 'research' in lower_line and ':' in line:
                    current_section = 'future_work'
                    current_text = []
                else:
                    # Add content to current section
                    if current_section:
                        if line.startswith('- '):
                            line = line[2:]  # Remove bullet point
                        current_text.append(line)
                        
                        # Update the analysis dict
                        if current_section == 'summary':
                            analysis['summary'] = ' '.join(current_text)
                        elif current_section in ['key_findings', 'applications', 'future_work']:
                            analysis[current_section] = current_text
                        else:
                            analysis[current_section] = ' '.join(current_text)
            
            return analysis
            
        except Exception as e:
            logger.error(f"Error parsing analysis response: {str(e)}")
            return {
                "error": "Failed to parse analysis",
                "raw_response": response
            }

    async def check_health(self) -> Dict:
        """Check if Ollama is available and responding."""
        try:
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                self._executor,
                lambda: ollama.generate(
                    model=self.model,
                    prompt="Hi",
                    options={"temperature": 0.7}
                )
            )
            return {
                "status": "healthy", 
                "model": self.model,
                "model_version": "3.2"  # Added model version info
            }
        except Exception as e:
            logger.error(f"Ollama health check failed: {str(e)}")
            return {
                "status": "unhealthy", 
                "model": self.model,
                "error": str(e)
            } 