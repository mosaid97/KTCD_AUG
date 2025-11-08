# Lab Generation System

This system generates personalized coding labs for every concept in the knowledge graph. It uses LLM (GPT-4) to create engaging, hands-on lab exercises tailored to student interests and hobbies.

## Overview

The lab generation system follows the same architectural pattern as `lab_tutor/knowledge_graph_builder` but focuses on creating practical coding labs instead of extracting concepts from documents.

### Key Features

- **Personalized Labs**: Generate labs customized to student interests (gaming, music, sports, etc.)
- **Concept-Based**: One lab per concept from the knowledge graph
- **Structured Output**: JSON format compatible with the existing system
- **Batch Processing**: Generate labs for all 272 concepts automatically
- **Multiple Difficulty Levels**: Easy, medium, and hard labs
- **Scaffolding Support**: Low, medium, and high guidance levels
- **Exercise Types**: Guided, challenge, and exploration exercises

## Directory Structure

```
Lab_generate/
├── models/
│   ├── __init__.py
│   └── lab_models.py          # Pydantic models for lab structure
├── services/
│   ├── __init__.py
│   └── lab_generation_service.py  # LLM-based lab generation
├── utils/
│   ├── __init__.py
│   └── file_utils.py          # File operations and utilities
├── batch_output/              # Generated labs (created on first run)
│   ├── NoSQL_Database/
│   │   ├── NoSQL_Database_lab.json
│   │   └── lab_content.json
│   └── ...
├── ingestion.py               # Main script for lab generation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## Installation

1. **Install dependencies**:
```bash
pip install -r requirements.txt
```

2. **Set up environment variables**:
Create a `.env` file in the `Lab_generate` directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

### Batch Mode (Generate All Labs)

Generate labs for all concepts in the knowledge graph:

```bash
python ingestion.py --mode batch
```

With personalization context:

```bash
python ingestion.py --mode batch --personalize "gaming"
```

Limit to first N concepts (for testing):

```bash
python ingestion.py --mode batch --limit 10
```

### Single Mode (Generate One Lab)

Generate a lab for a specific concept:

```bash
python ingestion.py --mode single --concept "NoSQL Database"
```

With personalization:

```bash
python ingestion.py --mode single --concept "CAP Theorem" --personalize "sports"
```

### Advanced Options

```bash
python ingestion.py \
  --mode batch \
  --export-path ../lab_tutor/knowledge_graph_builder/complete_neo4j_export_no_embeddings.json \
  --output-dir batch_output \
  --personalize "music" \
  --model gpt-4 \
  --temperature 0.7 \
  --limit 50
```

## Output Format

Each generated lab is saved in two formats:

### 1. Full Lab File (`{concept_name}_lab.json`)

Contains complete lab data with metadata:

```json
{
  "lab": {
    "title": "Personalized Lab: NoSQL Databases",
    "topic": "Introduction to NoSQL Databases",
    "difficulty": "medium",
    "estimated_time": 45,
    "sections": [
      {
        "concept": "NoSQL Database",
        "title": "Building a Game Leaderboard with NoSQL",
        "difficulty": "medium",
        "scaffolding_level": "high",
        "exercises": [
          {
            "type": "guided",
            "hints": 3,
            "description": "Implement a leaderboard using MongoDB",
            "starter_code": "# TODO: Connect to MongoDB\n",
            "solution": "# Complete solution here",
            "test_cases": [
              {"input": "...", "expected": "..."}
            ]
          }
        ],
        "learning_objectives": [
          "Understand NoSQL database structure",
          "Implement CRUD operations"
        ],
        "background": "NoSQL databases are..."
      }
    ],
    "prerequisites": ["Python basics", "Database concepts"],
    "technologies": ["Python", "MongoDB", "Jupyter"],
    "personalization_context": "gaming"
  },
  "metadata": {
    "concept_name": "NoSQL Database",
    "concept_definition": "non-relational databases based on...",
    "source_topic": "Introduction to NoSQL Databases",
    "model_used": "gpt-4",
    "personalization_applied": true
  },
  "success": true
}
```

### 2. Simplified Lab File (`lab_content.json`)

Contains only the lab content (for easier integration):

```json
{
  "title": "Personalized Lab: NoSQL Databases",
  "topic": "Introduction to NoSQL Databases",
  "difficulty": "medium",
  "estimated_time": 45,
  "sections": [...],
  "prerequisites": [...],
  "technologies": [...],
  "personalization_context": "gaming"
}
```

### 3. Summary Report (`generation_summary.json`)

Created after batch processing:

```json
{
  "total_labs": 272,
  "successful": 268,
  "failed": 4,
  "labs": [
    {
      "concept": "NoSQL Database",
      "topic": "Introduction to NoSQL Databases",
      "title": "Personalized Lab: NoSQL Databases",
      "difficulty": "medium",
      "estimated_time": 45,
      "num_sections": 2,
      "success": true
    }
  ]
}
```

## Lab Structure

Each lab follows this structure:

- **Title**: Engaging title for the lab
- **Topic**: The topic from the knowledge graph
- **Difficulty**: easy, medium, or hard
- **Estimated Time**: 15-180 minutes
- **Sections**: 1-3 sections, each covering an aspect of the concept
  - **Concept**: The concept being taught
  - **Title**: Section title
  - **Difficulty**: Section-specific difficulty
  - **Scaffolding Level**: low, medium, or high
  - **Exercises**: 1-3 exercises per section
    - **Type**: guided, challenge, or exploration
    - **Hints**: 0-5 hints available
    - **Description**: What to implement
    - **Starter Code**: Code template
    - **Solution**: Reference solution
    - **Test Cases**: Validation tests
  - **Learning Objectives**: What students will learn
  - **Background**: Context and explanation
- **Prerequisites**: Required knowledge
- **Technologies**: Tools and technologies used
- **Personalization Context**: How the lab was personalized

## Personalization

Labs can be personalized based on student interests:

- **Gaming**: Examples using game databases, leaderboards, player stats
- **Music**: Examples using music libraries, playlists, artist data
- **Sports**: Examples using team stats, player performance, match data
- **Art**: Examples using galleries, artwork metadata, artist portfolios
- **Custom**: Any other context you provide

## Integration with Existing System

The generated labs are designed to integrate seamlessly with the existing KTCD_Aug system:

1. **Same JSON Format**: Compatible with the knowledge graph structure
2. **Concept Mapping**: Each lab maps to a concept in Neo4j
3. **Topic Organization**: Labs are organized by topic
4. **Metadata Tracking**: Full metadata for provenance and debugging

## Development

### Adding New Features

1. **Modify Models**: Edit `models/lab_models.py` to add new fields
2. **Update Service**: Modify `services/lab_generation_service.py` for new generation logic
3. **Extend Utils**: Add new utilities to `utils/file_utils.py`

### Testing

Test with a small subset first:

```bash
python ingestion.py --mode batch --limit 5
```

### Debugging

Enable verbose output by checking the console logs. Each step prints status messages:
- 🔄 Processing
- ✅ Success
- ⚠️  Warning (fallback used)
- ❌ Error

## Performance

- **Single Lab**: ~10-30 seconds per concept
- **Batch Processing**: ~45-135 minutes for all 272 concepts
- **Cost**: ~$0.01-0.05 per lab (GPT-4 pricing)

## Troubleshooting

### Common Issues

1. **Missing API Key**:
   ```
   Error: OPENAI_API_KEY environment variable not set
   ```
   Solution: Create `.env` file with your OpenAI API key

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'langchain_openai'
   ```
   Solution: Run `pip install -r requirements.txt`

3. **File Not Found**:
   ```
   Error: complete_neo4j_export_no_embeddings.json not found
   ```
   Solution: Check the `--export-path` argument points to the correct file

## License

This project follows the same license as the parent KTCD_Aug project.

## Contact

For questions or issues, please refer to the main KTCD_Aug documentation.

