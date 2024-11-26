# AI Research Hub

A comprehensive platform for AI researchers to search, analyze, and collaborate on research papers.

## Features

- 📚 Research Paper Search: Search and analyze papers from multiple sources (arXiv, Semantic Scholar)
- 📊 Project Management: Track and manage research projects
- 💾 Dataset Management: Organize and share research datasets
- 🔍 Advanced Analysis: Analyze papers using AI/ML techniques

## Tech Stack

- **Frontend**: React.js with Material-UI
- **Backend**: FastAPI (Python)
- **APIs**: arXiv, Semantic Scholar
- **Database**: PostgreSQL (planned)

## Getting Started

### Prerequisites

- [Anaconda](https://www.anaconda.com/download) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)
- Node.js 14+
- PostgreSQL (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/canncupiscent/AI-Research-Hub.git
   cd AI-Research-Hub
   ```

2. Set up the backend:
   ```bash
   # Create and activate Conda environment
   conda create --name ai_research_hub python=3.9
   conda activate ai_research_hub

   # Install dependencies
   cd src/backend
   pip install -r requirements.txt
   ```

3. Set up the frontend:
   ```bash
   cd src/frontend
   npm install
   ```

### Running the Application

1. Start the backend server:
   ```bash
   # Make sure you're in the conda environment
   conda activate ai_research_hub
   
   # From the backend directory
   cd src/backend
   uvicorn api.main:app --reload
   ```

2. Start the frontend development server:
   ```bash
   # From the frontend directory
   cd src/frontend
   npm start
   ```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Project Structure

```
AI-Research-Hub/
├── src/
│   ├── backend/
│   │   ├── api/              # FastAPI routes and endpoints
│   │   ├── models/           # Database models and configuration
│   │   ├── services/         # Business logic and external API integration
│   │   └── tests/           # Unit tests
│   └── frontend/
│       ├── public/          # Static assets
│       └── src/
│           ├── components/  # React components
│           └── config/      # Frontend configuration
└── docs/                   # Documentation
```

## Development

### Environment Management

```bash
# Create new environment
conda create --name ai_research_hub python=3.9

# Activate environment
conda activate ai_research_hub

# Deactivate environment
conda deactivate

# List all environments
conda env list
```

### Git Workflow

```bash
# Check status
git status

# Create new branch
git checkout -b feature/new-feature

# Add changes
git add .

# Commit changes
git commit -m "Description of changes"

# Push changes
git push origin feature/new-feature
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Repository

- GitHub: [canncupiscent/AI-Research-Hub](https://github.com/canncupiscent/AI-Research-Hub)
- Issues: [GitHub Issues](https://github.com/canncupiscent/AI-Research-Hub/issues)
- Pull Requests: [GitHub PRs](https://github.com/canncupiscent/AI-Research-Hub/pulls) 