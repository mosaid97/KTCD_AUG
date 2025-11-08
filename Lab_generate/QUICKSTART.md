# Quick Start Guide

Get started with the Lab Generation System in 5 minutes!

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Access to the KTCD_Aug knowledge graph export file

## Step 1: Installation

```bash
# Navigate to the Lab_generate directory
cd Lab_generate

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Configuration

Create a `.env` file with your OpenAI API key:

```bash
# Copy the template
cp .env.template .env

# Edit .env and add your API key
# OPENAI_API_KEY=sk-your-actual-key-here
```

## Step 3: Test the System

Run the test script to verify everything works:

```bash
python test_generation.py
```

This will:
- Generate a sample lab for "NoSQL Database"
- Save it to `test_output/`
- Display the lab structure

Expected output:
```
✅ Lab generated successfully!
Title: Personalized Lab: Building a Game Leaderboard with NoSQL
Difficulty: medium
Estimated Time: 60 minutes
Number of Sections: 2
```

## Step 4: Generate Labs

### Option A: Generate a Single Lab

```bash
python ingestion.py --mode single --concept "CAP Theorem" --personalize "gaming"
```

### Option B: Generate All Labs (Batch Mode)

```bash
# Start with a small batch for testing
python ingestion.py --mode batch --limit 5

# Generate all 272 labs (takes ~2 hours)
python ingestion.py --mode batch --personalize "sports"
```

## Step 5: View Results

Generated labs are saved in `batch_output/`:

```
batch_output/
├── NoSQL_Database/
│   ├── NoSQL_Database_lab.json      # Full lab with metadata
│   └── lab_content.json             # Simplified lab content
├── CAP_Theorem/
│   ├── CAP_Theorem_lab.json
│   └── lab_content.json
└── generation_summary.json          # Overall summary
```

## Example: View a Generated Lab

```bash
# Pretty-print a lab
python -m json.tool batch_output/NoSQL_Database/lab_content.json
```

Or use Python:

```python
import json

with open('batch_output/NoSQL_Database/lab_content.json') as f:
    lab = json.load(f)

print(f"Title: {lab['title']}")
print(f"Difficulty: {lab['difficulty']}")
print(f"Time: {lab['estimated_time']} minutes")
print(f"Sections: {len(lab['sections'])}")
```

## Personalization Options

Customize labs based on student interests:

```bash
# Gaming context
python ingestion.py --mode batch --personalize "gaming"

# Music context
python ingestion.py --mode batch --personalize "music"

# Sports context
python ingestion.py --mode batch --personalize "sports"

# Custom context
python ingestion.py --mode batch --personalize "cooking and recipes"
```

## Common Commands

```bash
# Generate first 10 labs for testing
python ingestion.py --mode batch --limit 10

# Generate with specific model
python ingestion.py --mode batch --model gpt-4-turbo --temperature 0.8

# Generate for specific concept
python ingestion.py --mode single --concept "MapReduce"

# View help
python ingestion.py --help
```

## Troubleshooting

### Issue: "OPENAI_API_KEY not set"

**Solution**: Create `.env` file with your API key:
```bash
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Issue: "Module not found"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Export file not found"

**Solution**: Check the path to the Neo4j export:
```bash
python ingestion.py --export-path ../lab_tutor/knowledge_graph_builder/complete_neo4j_export_no_embeddings.json
```

## Next Steps

1. **Review Sample Labs**: Check `sample_output/` for examples
2. **Customize Generation**: Modify `services/lab_generation_service.py`
3. **Integrate with System**: Use generated labs in your application
4. **Generate All Labs**: Run full batch processing

## Sample Output Structure

Each lab includes:

- **Title**: Engaging, personalized title
- **Sections**: 1-3 sections per lab
- **Exercises**: Guided, challenge, or exploration types
- **Code**: Starter code, solutions, and test cases
- **Metadata**: Concept, topic, difficulty, time estimate

Example:
```json
{
  "title": "Building a Game Leaderboard with NoSQL",
  "difficulty": "medium",
  "estimated_time": 60,
  "sections": [
    {
      "concept": "NoSQL Database",
      "exercises": [
        {
          "type": "guided",
          "hints": 3,
          "starter_code": "# TODO: Your code here",
          "solution": "# Complete solution"
        }
      ]
    }
  ]
}
```

## Performance Tips

- **Start Small**: Use `--limit 10` for testing
- **Batch Processing**: Generate all labs overnight
- **Cost**: ~$0.02-0.05 per lab with GPT-4
- **Time**: ~15-30 seconds per lab

## Support

For issues or questions:
1. Check the main [README.md](README.md)
2. Review sample outputs in `sample_output/`
3. Run test script: `python test_generation.py`

---

**Ready to generate labs?** Start with:
```bash
python ingestion.py --mode batch --limit 5 --personalize "gaming"
```

This will generate 5 sample labs in ~2 minutes! 🚀

