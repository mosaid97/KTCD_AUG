"""
Utility functions for file operations in lab generation.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Optional


def sanitize_filename(name: str, max_length: int = 100) -> str:
    """
    Sanitize a string to be used as a filename.
    
    Args:
        name: Original name
        max_length: Maximum length for the filename
    
    Returns:
        Sanitized filename
    """
    # Replace spaces with underscores
    sanitized = name.replace(' ', '_')
    
    # Remove or replace invalid characters
    sanitized = re.sub(r'[^\w\-_.]', '', sanitized)
    
    # Remove multiple consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # Trim to max length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    
    # Remove trailing underscores or dots
    sanitized = sanitized.rstrip('_.')
    
    return sanitized


def create_output_directory(base_dir: str, concept_name: str) -> Path:
    """
    Create output directory for a concept's lab.
    
    Args:
        base_dir: Base output directory
        concept_name: Name of the concept
    
    Returns:
        Path to the created directory
    """
    # Sanitize concept name for directory
    sanitized_name = sanitize_filename(concept_name)
    
    # Create directory path
    output_dir = Path(base_dir) / sanitized_name
    
    # Create directory if it doesn't exist
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return output_dir


def save_lab_json(lab_data: Dict[str, Any], output_path: Path, filename: str = "lab.json") -> Path:
    """
    Save lab data as JSON file.
    
    Args:
        lab_data: Lab data dictionary
        output_path: Output directory path
        filename: Name of the JSON file
    
    Returns:
        Path to the saved file
    """
    file_path = output_path / filename
    
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(lab_data, f, indent=2, ensure_ascii=False)
    
    return file_path


def load_concepts_from_export(export_path: str) -> list:
    """
    Load all concepts from the Neo4j export file.
    
    Args:
        export_path: Path to the complete_neo4j_export_no_embeddings.json file
    
    Returns:
        List of concept dictionaries with 'name', 'definition', and 'topic'
    """
    with open(export_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    concepts = []
    
    # Extract concepts from theories
    for theory in data.get('theories', []):
        topic = theory.get('topic', 'Unknown')
        
        for concept in theory.get('concepts', []):
            concepts.append({
                'name': concept.get('name', ''),
                'definition': concept.get('definition', ''),
                'topic': topic,
                'text_evidence': concept.get('text_evidence', '')
            })
    
    return concepts


def organize_lab_output(lab_result, output_dir: str, concept_name: str) -> Dict[str, str]:
    """
    Organize and save lab output in a structured format.
    
    Args:
        lab_result: CompleteLabResult object
        output_dir: Base output directory
        concept_name: Name of the concept
    
    Returns:
        Dictionary with paths to saved files
    """
    # Create concept-specific directory
    concept_dir = create_output_directory(output_dir, concept_name)
    
    # Prepare lab data for JSON export
    lab_data = {
        'lab': lab_result.lab.model_dump(),
        'metadata': lab_result.metadata.model_dump(),
        'success': lab_result.success
    }
    
    if lab_result.error:
        lab_data['error'] = lab_result.error
    
    # Save lab JSON
    lab_file = save_lab_json(lab_data, concept_dir, f"{sanitize_filename(concept_name)}_lab.json")
    
    # Save simplified version (just the lab content)
    simplified_data = lab_result.lab.model_dump()
    simplified_file = save_lab_json(simplified_data, concept_dir, "lab_content.json")
    
    return {
        'concept_dir': str(concept_dir),
        'full_lab_file': str(lab_file),
        'simplified_file': str(simplified_file)
    }


def create_summary_report(results: list, output_dir: str) -> Path:
    """
    Create a summary report of all generated labs.
    
    Args:
        results: List of CompleteLabResult objects
        output_dir: Output directory for the report
    
    Returns:
        Path to the summary report file
    """
    summary = {
        'total_labs': len(results),
        'successful': sum(1 for r in results if r.success),
        'failed': sum(1 for r in results if not r.success),
        'labs': []
    }
    
    for result in results:
        lab_info = {
            'concept': result.metadata.concept_name,
            'topic': result.metadata.source_topic,
            'title': result.lab.title,
            'difficulty': result.lab.difficulty,
            'estimated_time': result.lab.estimated_time,
            'num_sections': len(result.lab.sections),
            'success': result.success
        }
        
        if result.error:
            lab_info['error'] = result.error
        
        summary['labs'].append(lab_info)
    
    # Save summary
    summary_path = Path(output_dir) / 'generation_summary.json'
    with open(summary_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    return summary_path

