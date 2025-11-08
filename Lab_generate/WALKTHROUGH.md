# Complete System Walkthrough

This document walks you through the entire lab generation system, explaining how each component works and how they fit together.

## System Overview

The lab generation system transforms concepts from your knowledge graph into personalized, hands-on coding labs. Think of it as an automated lab instructor that creates custom exercises for each concept.

```
Knowledge Graph Concepts → Lab Generation System → Personalized Labs
```

## Component Walkthrough

### 1. Data Models (`models/lab_models.py`)

**What it does**: Defines the structure of a lab using Pydantic models.

**Key Models**:

```python
# A single exercise
class LabExercise(BaseModel):
    type: 'guided' | 'challenge' | 'exploration'
    hints: int (0-5)
    description: str
    starter_code: str
    solution: str
    test_cases: List[dict]

# A section covering one concept
class LabSection(BaseModel):
    concept: str
    title: str
    difficulty: 'easy' | 'medium' | 'hard'
    scaffolding_level: 'low' | 'medium' | 'high'
    exercises: List[LabExercise]
    learning_objectives: List[str]
    background: str

# Complete lab
class PersonalizedLab(BaseModel):
    title: str
    topic: str
    difficulty: str
    estimated_time: int
    sections: List[LabSection]
    prerequisites: List[str]
    technologies: List[str]
    personalization_context: str
```

**Why Pydantic?**
- Automatic validation
- Type safety
- Easy JSON serialization
- Clear error messages

### 2. Lab Generation Service (`services/lab_generation_service.py`)

**What it does**: Uses GPT-4 to generate personalized labs.

**How it works**:

```python
class LabGenerationService:
    def __init__(self, model_name="gpt-4"):
        # Initialize OpenAI LLM
        self.llm = ChatOpenAI(model=model_name)
        
    def generate_lab(self, concept_name, concept_definition, 
                    topic, personalization_context=None):
        # 1. Create prompt
        prompt = self._create_lab_prompt(...)
        
        # 2. Call LLM
        response = self.llm.invoke(prompt)
        
        # 3. Parse JSON response
        lab_data = self.parser.parse(response.content)
        
        # 4. Validate with Pydantic
        lab = PersonalizedLab(**lab_data)
        
        # 5. Return result
        return CompleteLabResult(lab=lab, metadata=...)
```

**Prompt Engineering**:

The prompt includes:
- Concept name and definition
- Topic context
- Personalization context (e.g., "gaming")
- Detailed instructions for lab structure
- JSON schema specification
- Examples of good exercises

**Example Prompt**:
```
You are an expert educator creating hands-on coding labs.

Concept: NoSQL Database
Definition: non-relational databases based on distributed file systems
Topic: Introduction to NoSQL Databases
Personalization: gaming

Create a lab that uses gaming examples (leaderboards, player data, etc.)
Include 2-3 sections with guided and challenge exercises.
Return JSON matching this structure: {...}
```

### 3. File Utilities (`utils/file_utils.py`)

**What it does**: Handles file operations and data loading.

**Key Functions**:

```python
# Load concepts from Neo4j export
def load_concepts_from_export(export_path):
    # Parse JSON file
    # Extract all concepts with their topics
    # Return list of concept dictionaries

# Create organized output
def organize_lab_output(lab_result, output_dir, concept_name):
    # Create concept-specific directory
    # Save full lab JSON
    # Save simplified JSON
    # Return file paths

# Generate summary report
def create_summary_report(results, output_dir):
    # Count successful/failed
    # List all labs
    # Save summary JSON
```

### 4. Ingestion Script (`ingestion.py`)

**What it does**: Main entry point for lab generation.

**Architecture**:

```python
class LabIngestionService:
    def __init__(self):
        self.lab_generator = LabGenerationService()
    
    def generate_single_lab(self, concept_name, ...):
        # Generate one lab
        # Save output
        # Return result
    
    def generate_batch_labs(self, export_path, ...):
        # Load all concepts
        # Generate lab for each
        # Create summary
        # Return batch results

def main():
    # Parse command-line arguments
    # Initialize service
    # Run single or batch mode
```

**Command-Line Interface**:

```bash
# Single mode
python ingestion.py --mode single --concept "NoSQL Database"

# Batch mode
python ingestion.py --mode batch --limit 10

# With personalization
python ingestion.py --mode batch --personalize "gaming"
```

## Data Flow Example

Let's trace how a lab is generated for "NoSQL Database":

### Step 1: Load Concept Data

```python
# From complete_neo4j_export_no_embeddings.json
concept = {
    'name': 'NoSQL Database',
    'definition': 'non-relational databases based on distributed file systems',
    'topic': 'Introduction to NoSQL Databases'
}
```

### Step 2: Create Prompt

```python
prompt = f"""
Create a lab for:
Concept: {concept['name']}
Definition: {concept['definition']}
Topic: {concept['topic']}
Personalization: gaming

Include:
- 2 sections
- Guided and challenge exercises
- Gaming examples (leaderboards, player data)
- Starter code and solutions
"""
```

### Step 3: LLM Generation

```python
# GPT-4 generates:
{
  "title": "Building a Game Leaderboard with NoSQL",
  "sections": [
    {
      "concept": "NoSQL Database",
      "title": "Setting Up Your First NoSQL Database",
      "exercises": [
        {
          "type": "guided",
          "description": "Create MongoDB database for players",
          "starter_code": "# TODO: Connect to MongoDB",
          "solution": "client = MongoClient(...)"
        }
      ]
    }
  ]
}
```

### Step 4: Validation

```python
# Pydantic validates the structure
lab = PersonalizedLab(**lab_data)
# Raises error if invalid
```

### Step 5: Save Output

```python
# Create directory
batch_output/NoSQL_Database/

# Save files
NoSQL_Database_lab.json      # Full lab with metadata
lab_content.json             # Simplified content
```

## Personalization System

### How Personalization Works

**Input**: `personalization_context = "gaming"`

**Prompt Modification**:
```python
if personalization_context:
    prompt += f"""
    Personalization Context: {personalization_context}
    
    Use {personalization_context}-related examples:
    - For "gaming": leaderboards, player stats, game databases
    - For "music": playlists, artist data, streaming services
    - For "sports": team stats, player performance, match data
    """
```

**LLM Adaptation**:
- Changes variable names (e.g., `player_score` instead of `user_score`)
- Uses domain-specific scenarios
- Creates relevant examples
- Maintains technical accuracy

**Example Transformations**:

| Concept | Generic | Gaming | Music | Sports |
|---------|---------|--------|-------|--------|
| NoSQL DB | User database | Player leaderboard | Music library | Team statistics |
| CAP Theorem | Distributed system | Multiplayer sync | Playlist sync | Live scores |
| MapReduce | Data processing | Player stats | Song analytics | Performance data |

## Output Format Details

### Full Lab File

```json
{
  "lab": {
    "title": "Building a Game Leaderboard with NoSQL",
    "topic": "Introduction to NoSQL Databases",
    "difficulty": "medium",
    "estimated_time": 60,
    "sections": [
      {
        "concept": "NoSQL Database",
        "title": "Setting Up Your First NoSQL Database",
        "difficulty": "easy",
        "scaffolding_level": "high",
        "exercises": [
          {
            "type": "guided",
            "hints": 3,
            "description": "Create a MongoDB database for game players",
            "starter_code": "# TODO: Connect to MongoDB\nclient = None",
            "solution": "client = MongoClient('mongodb://localhost:27017/')",
            "test_cases": [
              {"input": "client.list_database_names()", "expected": "['gaming_db']"}
            ]
          }
        ],
        "learning_objectives": [
          "Understand NoSQL database structure",
          "Learn MongoDB connection"
        ],
        "background": "NoSQL databases store data in flexible documents..."
      }
    ],
    "prerequisites": ["Python basics", "Database concepts"],
    "technologies": ["Python", "MongoDB", "Jupyter"],
    "personalization_context": "gaming"
  },
  "metadata": {
    "concept_name": "NoSQL Database",
    "concept_definition": "non-relational databases...",
    "source_topic": "Introduction to NoSQL Databases",
    "model_used": "gpt-4",
    "personalization_applied": true
  },
  "success": true,
  "error": null
}
```

### Simplified Lab File

```json
{
  "title": "Building a Game Leaderboard with NoSQL",
  "topic": "Introduction to NoSQL Databases",
  "difficulty": "medium",
  "estimated_time": 60,
  "sections": [...],
  "prerequisites": [...],
  "technologies": [...],
  "personalization_context": "gaming"
}
```

## Error Handling

### Three-Level Fallback

1. **Success**: LLM generates valid lab
2. **Fallback**: Template-based basic lab
3. **Error**: Detailed error in result

### Example Error Flow

```python
try:
    # Try LLM generation
    response = self.llm.invoke(prompt)
    lab = PersonalizedLab(**response)
    return CompleteLabResult(lab=lab, success=True)
    
except Exception as e:
    # Use fallback template
    fallback_lab = self._create_fallback_lab(concept_name, topic)
    return CompleteLabResult(
        lab=fallback_lab,
        success=False,
        error=str(e)
    )
```

## Testing the System

### Test Script (`test_generation.py`)

```python
# Test 1: Single concept
result = test_single_concept()
# Generates lab for "NoSQL Database"

# Test 2: Batch concepts
results = test_batch_concepts()
# Generates labs for first 3 concepts

# Test 3: Save output
saved_files = test_save_output()
# Saves to test_output/

# Test 4: Load and display
lab_data = test_load_and_display()
# Loads and prints lab structure
```

### Running Tests

```bash
python test_generation.py
```

**Expected Output**:
```
✅ Lab generated successfully!
Title: Building a Game Leaderboard with NoSQL
Difficulty: medium
Estimated Time: 60 minutes
Number of Sections: 2
```

## Integration with KTCD_Aug

### Loading Labs

```python
import json
from pathlib import Path

# Load all labs
labs = {}
for lab_dir in Path('batch_output').iterdir():
    if lab_dir.is_dir():
        lab_file = lab_dir / 'lab_content.json'
        if lab_file.exists():
            with open(lab_file) as f:
                labs[lab_dir.name] = json.load(f)

# Access specific lab
nosql_lab = labs['NoSQL_Database']
print(nosql_lab['title'])
```

### Matching to Concepts

```python
# In your KTCD_Aug system
def get_lab_for_concept(concept_name):
    # Sanitize concept name
    sanitized = concept_name.replace(' ', '_')
    
    # Load lab
    lab_path = f'batch_output/{sanitized}/lab_content.json'
    with open(lab_path) as f:
        return json.load(f)

# Usage
lab = get_lab_for_concept('NoSQL Database')
```

## Performance and Cost

### Single Lab
- **Time**: 15-30 seconds
- **API Calls**: 1 per lab
- **Cost**: ~$0.02-0.05 (GPT-4)

### Batch Processing (272 concepts)
- **Time**: ~2 hours
- **API Calls**: 272
- **Cost**: ~$5-15 total

### Optimization Tips
- Use `--limit` for testing
- Run overnight for full batch
- Consider GPT-3.5-turbo for lower cost
- Cache results for reuse

## Troubleshooting

### Common Issues

**Issue**: "OPENAI_API_KEY not set"
```bash
# Solution
echo "OPENAI_API_KEY=sk-your-key" > .env
```

**Issue**: "Module not found"
```bash
# Solution
pip install -r requirements.txt
```

**Issue**: "Export file not found"
```bash
# Solution
python ingestion.py --export-path /correct/path/to/export.json
```

## Summary

The lab generation system:

1. **Loads** concepts from knowledge graph
2. **Generates** personalized labs with GPT-4
3. **Validates** structure with Pydantic
4. **Saves** in organized JSON format
5. **Reports** success/failure statistics

**Result**: 272 high-quality, personalized coding labs ready for your students!

---

**Next**: Read [QUICKSTART.md](QUICKSTART.md) to start generating labs!

