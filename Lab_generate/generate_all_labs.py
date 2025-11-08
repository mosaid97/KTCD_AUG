"""
Generate labs for ALL concepts in the knowledge graph.

This script generates personalized coding labs for all 272 concepts
from the knowledge graph export file.
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Any
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models.lab_models import (
    PersonalizedLab,
    LabSection,
    LabExercise,
    LabGenerationMetadata,
    CompleteLabResult
)
from utils.file_utils import (
    load_concepts_from_export,
    organize_lab_output,
    create_summary_report,
    sanitize_filename
)


class TemplateLabGenerator:
    """
    Template-based lab generator that doesn't require LLM API.
    Creates structured labs based on concept information.
    """
    
    def __init__(self):
        self.difficulty_map = {
            'database': 'medium',
            'algorithm': 'hard',
            'system': 'hard',
            'data': 'easy',
            'processing': 'medium',
            'analysis': 'medium',
            'storage': 'easy',
            'framework': 'medium',
            'model': 'hard',
            'technique': 'medium'
        }
    
    def _determine_difficulty(self, concept_name: str, definition: str) -> str:
        """Determine difficulty based on concept characteristics."""
        concept_lower = concept_name.lower()
        definition_lower = definition.lower()
        
        # Check for keywords
        for keyword, difficulty in self.difficulty_map.items():
            if keyword in concept_lower or keyword in definition_lower:
                return difficulty
        
        # Default based on definition length
        if len(definition) > 200:
            return 'hard'
        elif len(definition) > 100:
            return 'medium'
        else:
            return 'easy'
    
    def _estimate_time(self, difficulty: str, num_sections: int) -> int:
        """Estimate lab completion time."""
        base_time = {
            'easy': 30,
            'medium': 45,
            'hard': 60
        }
        return base_time.get(difficulty, 45) + (num_sections - 1) * 15
    
    def _create_exercises(self, concept_name: str, difficulty: str, 
                         personalization_context: str = None) -> List[LabExercise]:
        """Create exercises for a concept."""
        exercises = []
        
        # Guided exercise
        exercises.append(LabExercise(
            type='guided',
            hints=3 if difficulty == 'easy' else 2,
            description=f"Implement a basic example demonstrating {concept_name}",
            starter_code=f"# TODO: Implement {concept_name}\n# Your code here\n",
            solution=f"# Solution for {concept_name}\n# Implementation details\n",
            test_cases=[
                {"input": "test_input", "expected": "expected_output"}
            ]
        ))
        
        # Challenge exercise for medium/hard
        if difficulty in ['medium', 'hard']:
            exercises.append(LabExercise(
                type='challenge',
                hints=1,
                description=f"Apply {concept_name} to solve a real-world problem",
                starter_code=f"# Challenge: Advanced {concept_name}\n",
                solution=f"# Advanced solution\n",
                test_cases=[]
            ))
        
        return exercises
    
    def generate_lab(self, concept_name: str, concept_definition: str,
                    topic: str, personalization_context: str = None) -> CompleteLabResult:
        """Generate a template-based lab for a concept."""
        
        try:
            # Determine difficulty
            difficulty = self._determine_difficulty(concept_name, concept_definition)
            
            # Create personalized title
            if personalization_context:
                title = f"Hands-On Lab: {concept_name} in {personalization_context.title()}"
            else:
                title = f"Hands-On Lab: {concept_name}"
            
            # Create exercises
            exercises = self._create_exercises(concept_name, difficulty, personalization_context)
            
            # Create section
            section = LabSection(
                concept=concept_name,
                title=f"Exploring {concept_name}",
                difficulty=difficulty,
                scaffolding_level='medium',
                exercises=exercises,
                learning_objectives=[
                    f"Understand the fundamentals of {concept_name}",
                    f"Apply {concept_name} in practical scenarios",
                    f"Implement solutions using {concept_name}"
                ],
                background=concept_definition
            )
            
            # Create lab
            lab = PersonalizedLab(
                title=title,
                topic=topic,
                difficulty=difficulty,
                estimated_time=self._estimate_time(difficulty, 1),
                sections=[section],
                prerequisites=["Basic programming knowledge", "Understanding of databases"],
                technologies=["Python", "Jupyter Notebook"],
                personalization_context=personalization_context
            )
            
            # Create metadata
            metadata = LabGenerationMetadata(
                concept_name=concept_name,
                concept_definition=concept_definition,
                source_topic=topic,
                model_used="template",
                personalization_applied=personalization_context is not None
            )
            
            return CompleteLabResult(
                lab=lab,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            print(f"❌ Error generating lab for {concept_name}: {e}")
            return CompleteLabResult(
                lab=self._create_minimal_lab(concept_name, topic),
                metadata=LabGenerationMetadata(
                    concept_name=concept_name,
                    concept_definition=concept_definition,
                    source_topic=topic,
                    model_used="template",
                    personalization_applied=False
                ),
                success=False,
                error=str(e)
            )
    
    def _create_minimal_lab(self, concept_name: str, topic: str) -> PersonalizedLab:
        """Create minimal fallback lab."""
        return PersonalizedLab(
            title=f"Introduction to {concept_name}",
            topic=topic,
            difficulty="medium",
            estimated_time=45,
            sections=[
                LabSection(
                    concept=concept_name,
                    title=f"Learning {concept_name}",
                    difficulty="medium",
                    scaffolding_level="medium",
                    exercises=[
                        LabExercise(
                            type="guided",
                            hints=3,
                            description=f"Explore {concept_name}",
                            starter_code="# TODO: Implement\n",
                            solution="# Solution\n",
                            test_cases=[]
                        )
                    ],
                    learning_objectives=[f"Understand {concept_name}"],
                    background=f"This lab introduces {concept_name}"
                )
            ],
            prerequisites=["Basic programming"],
            technologies=["Python"],
            personalization_context=None
        )


def generate_all_labs(
    export_path: str = "../lab_tutor/knowledge_graph_builder/complete_neo4j_export_no_embeddings.json",
    output_dir: str = "batch_output",
    personalization_context: str = None
):
    """
    Generate labs for all concepts in the knowledge graph.
    
    Args:
        export_path: Path to Neo4j export file
        output_dir: Output directory for labs
        personalization_context: Optional personalization context
    """
    
    print("="*80)
    print("LAB GENERATION FOR ALL CONCEPTS")
    print("="*80)
    
    start_time = time.time()
    
    # Load concepts
    print(f"\n📁 Loading concepts from: {export_path}")
    concepts = load_concepts_from_export(export_path)
    total_concepts = len(concepts)
    
    print(f"✅ Loaded {total_concepts} concepts")
    
    if personalization_context:
        print(f"🎯 Personalization context: {personalization_context}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Initialize generator
    generator = TemplateLabGenerator()
    
    # Process each concept
    results = []
    successful = 0
    failed = 0
    
    print(f"\n🚀 Starting lab generation for {total_concepts} concepts...")
    print("="*80)
    
    for i, concept in enumerate(concepts, 1):
        # Progress indicator
        if i % 10 == 0 or i == 1:
            elapsed = time.time() - start_time
            avg_time = elapsed / i if i > 0 else 0
            remaining = avg_time * (total_concepts - i)
            print(f"\n📊 Progress: {i}/{total_concepts} ({i*100//total_concepts}%)")
            print(f"⏱️  Elapsed: {elapsed:.1f}s | Remaining: ~{remaining:.1f}s")
        
        concept_name = concept['name']
        print(f"\n{i}. {concept_name}")
        
        try:
            # Generate lab
            result = generator.generate_lab(
                concept_name=concept['name'],
                concept_definition=concept['definition'],
                topic=concept['topic'],
                personalization_context=personalization_context
            )
            
            # Save output
            saved_files = organize_lab_output(
                lab_result=result,
                output_dir=output_dir,
                concept_name=concept['name']
            )
            
            results.append(result)
            
            if result.success:
                successful += 1
                print(f"   ✅ Success: {result.lab.title}")
            else:
                failed += 1
                print(f"   ⚠️  Fallback used: {result.error}")
                
        except Exception as e:
            failed += 1
            print(f"   ❌ Error: {e}")
    
    # Create summary report
    print(f"\n{'='*80}")
    print("📊 Creating summary report...")
    summary_path = create_summary_report(results, output_dir)
    
    processing_time = time.time() - start_time
    
    # Print final summary
    print(f"\n{'='*80}")
    print("📊 FINAL SUMMARY")
    print(f"{'='*80}")
    print(f"📁 Total concepts: {total_concepts}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"⏱️  Total time: {processing_time:.2f} seconds ({processing_time/60:.1f} minutes)")
    print(f"📄 Summary report: {summary_path}")
    print(f"📁 Output directory: {output_dir}")
    print(f"{'='*80}")
    
    return {
        'total_concepts': total_concepts,
        'successful': successful,
        'failed': failed,
        'processing_time': processing_time,
        'summary_path': str(summary_path),
        'results': results
    }


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate labs for all concepts")
    parser.add_argument('--export-path', type=str,
                       default='../lab_tutor/knowledge_graph_builder/complete_neo4j_export_no_embeddings.json',
                       help='Path to Neo4j export file')
    parser.add_argument('--output-dir', type=str, default='batch_output',
                       help='Output directory')
    parser.add_argument('--personalize', type=str, default=None,
                       help='Personalization context (e.g., gaming, music, sports)')
    
    args = parser.parse_args()
    
    # Generate all labs
    generate_all_labs(
        export_path=args.export_path,
        output_dir=args.output_dir,
        personalization_context=args.personalize
    )

