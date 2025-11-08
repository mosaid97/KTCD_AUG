"""
Lab Generation Ingestion Script

This script generates personalized coding labs for all concepts in the knowledge graph.
It follows the same pattern as lab_tutor/knowledge_graph_builder/services/ingestion.py
but focuses on lab generation instead of concept extraction.

Usage:
    python ingestion.py --mode single --concept "NoSQL Database"
    python ingestion.py --mode batch --output-dir batch_output
    python ingestion.py --mode batch --personalize "gaming"
"""

import argparse
import time
from pathlib import Path
from typing import Optional, List

from services.lab_generation_service import LabGenerationService
from utils.file_utils import (
    load_concepts_from_export,
    organize_lab_output,
    create_summary_report
)


class LabIngestionService:
    """
    Service for ingesting concepts and generating labs.
    Similar to the IngestionService in lab_tutor but for lab generation.
    """
    
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize the lab ingestion service.
        
        Args:
            model_name: OpenAI model to use
            temperature: Temperature for generation
        """
        self.lab_generator = LabGenerationService(
            model_name=model_name,
            temperature=temperature
        )
    
    def generate_single_lab(
        self,
        concept_name: str,
        concept_definition: str,
        topic: str,
        output_dir: str = "batch_output",
        personalization_context: Optional[str] = None
    ) -> dict:
        """
        Generate a lab for a single concept.
        
        Args:
            concept_name: Name of the concept
            concept_definition: Definition of the concept
            topic: Topic the concept belongs to
            output_dir: Output directory for the lab
            personalization_context: Optional personalization context
        
        Returns:
            Dictionary with generation results
        """
        try:
            print(f"🔄 Generating lab for: {concept_name}")
            
            # Generate lab
            result = self.lab_generator.generate_lab(
                concept_name=concept_name,
                concept_definition=concept_definition,
                topic=topic,
                personalization_context=personalization_context
            )
            
            # Organize and save output
            saved_files = organize_lab_output(
                lab_result=result,
                output_dir=output_dir,
                concept_name=concept_name
            )
            
            if result.success:
                print(f"✅ Successfully generated lab for {concept_name}")
                print(f"   📁 Saved to: {saved_files['concept_dir']}")
            else:
                print(f"⚠️  Generated fallback lab for {concept_name}")
                print(f"   Error: {result.error}")
            
            return {
                'success': result.success,
                'concept_name': concept_name,
                'topic': topic,
                'saved_files': saved_files,
                'result': result
            }
            
        except Exception as e:
            print(f"❌ Error generating lab for {concept_name}: {e}")
            return {
                'success': False,
                'concept_name': concept_name,
                'topic': topic,
                'error': str(e)
            }
    
    def generate_batch_labs(
        self,
        export_path: str,
        output_dir: str = "batch_output",
        personalization_context: Optional[str] = None,
        limit: Optional[int] = None
    ) -> dict:
        """
        Generate labs for all concepts in the knowledge graph.
        
        Args:
            export_path: Path to complete_neo4j_export_no_embeddings.json
            output_dir: Output directory for labs
            personalization_context: Optional personalization context
            limit: Optional limit on number of concepts to process
        
        Returns:
            Dictionary with batch processing results
        """
        start_time = time.time()
        
        # Load concepts from export
        print(f"📁 Loading concepts from: {export_path}")
        concepts = load_concepts_from_export(export_path)
        
        if limit:
            concepts = concepts[:limit]
            print(f"⚠️  Limited to first {limit} concepts")
        
        total_concepts = len(concepts)
        print(f"🚀 Starting batch lab generation for {total_concepts} concepts")
        
        if personalization_context:
            print(f"🎯 Personalization context: {personalization_context}")
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Process each concept
        results = []
        successful = 0
        failed = 0
        
        for i, concept in enumerate(concepts, 1):
            print(f"\n{'='*60}")
            print(f"Processing {i}/{total_concepts}: {concept['name']}")
            print(f"{'='*60}")
            
            try:
                result = self.generate_single_lab(
                    concept_name=concept['name'],
                    concept_definition=concept['definition'],
                    topic=concept['topic'],
                    output_dir=output_dir,
                    personalization_context=personalization_context
                )
                
                results.append(result['result'])
                
                if result['success']:
                    successful += 1
                else:
                    failed += 1
                    
            except Exception as e:
                failed += 1
                print(f"❌ Error processing {concept['name']}: {e}")
        
        # Create summary report
        print(f"\n{'='*60}")
        print("📊 Creating summary report...")
        print(f"{'='*60}")
        
        summary_path = create_summary_report(results, output_dir)
        
        processing_time = time.time() - start_time
        
        # Print final summary
        print(f"\n{'='*60}")
        print("📊 BATCH LAB GENERATION SUMMARY")
        print(f"{'='*60}")
        print(f"📁 Total concepts: {total_concepts}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Processing time: {processing_time:.2f} seconds")
        print(f"📄 Summary report: {summary_path}")
        print(f"{'='*60}")
        
        return {
            'total_concepts': total_concepts,
            'successful': successful,
            'failed': failed,
            'processing_time': processing_time,
            'summary_path': str(summary_path),
            'results': results
        }


def main():
    """Main entry point for the lab generation script."""
    parser = argparse.ArgumentParser(
        description="Generate personalized coding labs for knowledge graph concepts"
    )
    
    parser.add_argument(
        '--mode',
        type=str,
        choices=['single', 'batch'],
        default='batch',
        help='Generation mode: single concept or batch processing'
    )
    
    parser.add_argument(
        '--concept',
        type=str,
        help='Concept name for single mode'
    )
    
    parser.add_argument(
        '--export-path',
        type=str,
        default='../lab_tutor/knowledge_graph_builder/complete_neo4j_export_no_embeddings.json',
        help='Path to Neo4j export file'
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        default='batch_output',
        help='Output directory for generated labs'
    )
    
    parser.add_argument(
        '--personalize',
        type=str,
        help='Personalization context (e.g., "gaming", "music", "sports")'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of concepts to process (for testing)'
    )
    
    parser.add_argument(
        '--model',
        type=str,
        default='gpt-4',
        help='OpenAI model to use'
    )
    
    parser.add_argument(
        '--temperature',
        type=float,
        default=0.7,
        help='Temperature for generation (0.0-1.0)'
    )
    
    args = parser.parse_args()
    
    # Initialize ingestion service
    ingestion_service = LabIngestionService(
        model_name=args.model,
        temperature=args.temperature
    )
    
    if args.mode == 'single':
        if not args.concept:
            print("❌ Error: --concept required for single mode")
            return
        
        # Load concepts to find the specified one
        concepts = load_concepts_from_export(args.export_path)
        concept_data = next(
            (c for c in concepts if c['name'].lower() == args.concept.lower()),
            None
        )
        
        if not concept_data:
            print(f"❌ Error: Concept '{args.concept}' not found")
            return
        
        # Generate single lab
        ingestion_service.generate_single_lab(
            concept_name=concept_data['name'],
            concept_definition=concept_data['definition'],
            topic=concept_data['topic'],
            output_dir=args.output_dir,
            personalization_context=args.personalize
        )
        
    else:  # batch mode
        # Generate labs for all concepts
        ingestion_service.generate_batch_labs(
            export_path=args.export_path,
            output_dir=args.output_dir,
            personalization_context=args.personalize,
            limit=args.limit
        )


if __name__ == '__main__':
    main()

