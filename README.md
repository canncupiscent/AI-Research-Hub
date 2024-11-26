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

- Python 3.9+
- Node.js 14+
- PostgreSQL (optional)

### Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd AI-Research-Hub
   ```

2. Set up the backend:
   ```bash
   cd src/backend
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
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
   cd src/backend
   uvicorn api.main:app --reload
   ```

2. Start the frontend development server:
   ```bash
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
│   │   ├── api/
│   │   ├── models/
│   │   ├── services/
│   │   └── tests/
│   └── frontend/
│       ├── public/
│       └── src/
│           ├── components/
│           └── config/
└── docs/
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 