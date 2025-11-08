"""
Test script for lab generation system.

This script demonstrates how to use the lab generation system
and creates a few sample labs for testing.
"""

import json
from pathlib import Path

from services.lab_generation_service import LabGenerationService
from utils.file_utils import (
    load_concepts_from_export,
    organize_lab_output,
    create_summary_report
)


def test_single_concept():
    """Test generating a lab for a single concept."""
    print("="*60)
    print("TEST 1: Single Concept Lab Generation")
    print("="*60)
    
    # Initialize service
    lab_service = LabGenerationService(model_name="gpt-4", temperature=0.7)
    
    # Test concept
    concept_name = "NoSQL Database"
    concept_definition = "non-relational databases based on distributed file systems"
    topic = "Introduction to NoSQL Databases"
    
    print(f"\nGenerating lab for: {concept_name}")
    print(f"Topic: {topic}")
    
    # Generate lab
    result = lab_service.generate_lab(
        concept_name=concept_name,
        concept_definition=concept_definition,
        topic=topic,
        personalization_context="gaming"
    )
    
    # Print results
    if result.success:
        print("\n✅ Lab generated successfully!")
        print(f"Title: {result.lab.title}")
        print(f"Difficulty: {result.lab.difficulty}")
        print(f"Estimated Time: {result.lab.estimated_time} minutes")
        print(f"Number of Sections: {len(result.lab.sections)}")
        
        # Print first section details
        if result.lab.sections:
            section = result.lab.sections[0]
            print(f"\nFirst Section:")
            print(f"  Title: {section.title}")
            print(f"  Difficulty: {section.difficulty}")
            print(f"  Scaffolding: {section.scaffolding_level}")
            print(f"  Exercises: {len(section.exercises)}")
    else:
        print(f"\n❌ Lab generation failed: {result.error}")
    
    return result


def test_batch_concepts():
    """Test generating labs for multiple concepts."""
    print("\n" + "="*60)
    print("TEST 2: Batch Concept Lab Generation")
    print("="*60)
    
    # Load concepts from export
    export_path = "../lab_tutor/knowledge_graph_builder/complete_neo4j_export_no_embeddings.json"
    
    if not Path(export_path).exists():
        print(f"❌ Export file not found: {export_path}")
        return None
    
    concepts = load_concepts_from_export(export_path)
    
    # Test with first 3 concepts
    test_concepts = concepts[:3]
    
    print(f"\nLoaded {len(concepts)} total concepts")
    print(f"Testing with first {len(test_concepts)} concepts:")
    for i, c in enumerate(test_concepts, 1):
        print(f"  {i}. {c['name']} (Topic: {c['topic']})")
    
    # Initialize service
    lab_service = LabGenerationService(model_name="gpt-4", temperature=0.7)
    
    # Generate labs
    results = []
    for i, concept in enumerate(test_concepts, 1):
        print(f"\n{'='*60}")
        print(f"Generating lab {i}/{len(test_concepts)}: {concept['name']}")
        print(f"{'='*60}")
        
        result = lab_service.generate_lab(
            concept_name=concept['name'],
            concept_definition=concept['definition'],
            topic=concept['topic'],
            personalization_context="sports"
        )
        
        results.append(result)
        
        if result.success:
            print(f"✅ Success: {result.lab.title}")
        else:
            print(f"⚠️  Fallback used: {result.error}")
    
    # Print summary
    print("\n" + "="*60)
    print("BATCH GENERATION SUMMARY")
    print("="*60)
    successful = sum(1 for r in results if r.success)
    print(f"Total: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(results) - successful}")
    
    return results


def test_save_output():
    """Test saving lab output to files."""
    print("\n" + "="*60)
    print("TEST 3: Save Lab Output")
    print("="*60)
    
    # Generate a sample lab
    lab_service = LabGenerationService(model_name="gpt-4", temperature=0.7)
    
    result = lab_service.generate_lab(
        concept_name="CAP Theorem",
        concept_definition="Consistency, Availability, Partition tolerance theorem",
        topic="NoSQL Databases: CAP Theorem and BASE Transaction Model",
        personalization_context="music"
    )
    
    # Save output
    output_dir = "test_output"
    saved_files = organize_lab_output(
        lab_result=result,
        output_dir=output_dir,
        concept_name="CAP Theorem"
    )
    
    print(f"\n✅ Lab saved successfully!")
    print(f"Directory: {saved_files['concept_dir']}")
    print(f"Full lab file: {saved_files['full_lab_file']}")
    print(f"Simplified file: {saved_files['simplified_file']}")
    
    # Verify files exist
    for key, path in saved_files.items():
        if key != 'concept_dir':
            exists = Path(path).exists()
            status = "✅" if exists else "❌"
            print(f"{status} {Path(path).name}")
    
    return saved_files


def test_load_and_display():
    """Test loading and displaying a generated lab."""
    print("\n" + "="*60)
    print("TEST 4: Load and Display Lab")
    print("="*60)
    
    # Check if test output exists
    test_file = "test_output/CAP_Theorem/lab_content.json"
    
    if not Path(test_file).exists():
        print(f"❌ Test file not found: {test_file}")
        print("   Run test_save_output() first")
        return None
    
    # Load lab
    with open(test_file, 'r') as f:
        lab_data = json.load(f)
    
    print(f"\n📄 Lab: {lab_data['title']}")
    print(f"📚 Topic: {lab_data['topic']}")
    print(f"⏱️  Time: {lab_data['estimated_time']} minutes")
    print(f"📊 Difficulty: {lab_data['difficulty']}")
    print(f"🎯 Personalization: {lab_data.get('personalization_context', 'None')}")
    
    print(f"\n📋 Sections ({len(lab_data['sections'])}):")
    for i, section in enumerate(lab_data['sections'], 1):
        print(f"\n  {i}. {section['title']}")
        print(f"     Concept: {section['concept']}")
        print(f"     Difficulty: {section['difficulty']}")
        print(f"     Scaffolding: {section['scaffolding_level']}")
        print(f"     Exercises: {len(section['exercises'])}")
        
        for j, exercise in enumerate(section['exercises'], 1):
            print(f"       {j}. Type: {exercise['type']}, Hints: {exercise['hints']}")
    
    print(f"\n🔧 Technologies: {', '.join(lab_data.get('technologies', []))}")
    print(f"📚 Prerequisites: {', '.join(lab_data.get('prerequisites', []))}")
    
    return lab_data


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("LAB GENERATION SYSTEM - TEST SUITE")
    print("="*60)
    
    try:
        # Test 1: Single concept
        print("\n🧪 Running Test 1...")
        result1 = test_single_concept()
        
        # Test 2: Batch concepts (commented out to save API calls)
        # print("\n🧪 Running Test 2...")
        # result2 = test_batch_concepts()
        
        # Test 3: Save output
        print("\n🧪 Running Test 3...")
        result3 = test_save_output()
        
        # Test 4: Load and display
        print("\n🧪 Running Test 4...")
        result4 = test_load_and_display()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

