"""
Pydantic models for lab generation and structure.

These models define the expected output structure for generating personalized
coding labs based on concepts from the knowledge graph.
"""

from typing import List, Optional, Literal
from pydantic import BaseModel, Field


class LabExercise(BaseModel):
    """A single exercise within a lab section."""
    
    type: Literal['guided', 'challenge', 'exploration'] = Field(
        description="Type of exercise: 'guided' (step-by-step), 'challenge' (minimal guidance), "
                   "'exploration' (open-ended)"
    )
    hints: int = Field(
        description="Number of hints available for this exercise (0-5)",
        ge=0,
        le=5
    )
    description: Optional[str] = Field(
        default=None,
        description="Brief description of the exercise"
    )
    starter_code: Optional[str] = Field(
        default=None,
        description="Initial code template for the exercise"
    )
    solution: Optional[str] = Field(
        default=None,
        description="Reference solution for the exercise"
    )
    test_cases: Optional[List[dict]] = Field(
        default=None,
        description="Test cases to validate the solution"
    )


class LabSection(BaseModel):
    """A section of the lab focusing on a specific concept."""
    
    concept: str = Field(
        description="The concept name this section covers"
    )
    title: str = Field(
        description="Engaging title for this lab section"
    )
    difficulty: Literal['easy', 'medium', 'hard'] = Field(
        description="Difficulty level of this section"
    )
    scaffolding_level: Literal['low', 'medium', 'high'] = Field(
        description="Amount of guidance provided: 'low' (minimal), 'medium' (moderate), 'high' (detailed)"
    )
    exercises: List[LabExercise] = Field(
        description="List of exercises in this section",
        min_length=1
    )
    learning_objectives: Optional[List[str]] = Field(
        default=None,
        description="What students should learn from this section"
    )
    background: Optional[str] = Field(
        default=None,
        description="Background information about the concept"
    )


class PersonalizedLab(BaseModel):
    """Complete personalized lab structure."""
    
    title: str = Field(
        description="Main title of the lab"
    )
    topic: str = Field(
        description="The topic this lab belongs to"
    )
    difficulty: Literal['easy', 'medium', 'hard'] = Field(
        description="Overall difficulty level of the lab"
    )
    estimated_time: int = Field(
        description="Estimated time to complete the lab in minutes",
        ge=15,
        le=180
    )
    sections: List[LabSection] = Field(
        description="List of lab sections, each focusing on a concept",
        min_length=1
    )
    prerequisites: Optional[List[str]] = Field(
        default=None,
        description="Prerequisites needed before starting this lab"
    )
    technologies: Optional[List[str]] = Field(
        default=None,
        description="Technologies/tools used in this lab"
    )
    personalization_context: Optional[str] = Field(
        default=None,
        description="Context used for personalization (e.g., student hobbies)"
    )


class LabGenerationMetadata(BaseModel):
    """Metadata about the lab generation process."""
    
    concept_name: str = Field(
        description="The concept this lab was generated for"
    )
    concept_definition: str = Field(
        description="Definition of the concept"
    )
    source_topic: str = Field(
        description="The topic this concept belongs to"
    )
    model_used: Optional[str] = Field(
        default="gpt-4",
        description="LLM model used for generation"
    )
    personalization_applied: bool = Field(
        default=False,
        description="Whether personalization was applied"
    )


class CompleteLabResult(BaseModel):
    """Complete lab generation result including both content and metadata."""
    
    lab: PersonalizedLab = Field(
        description="The generated lab content"
    )
    metadata: LabGenerationMetadata = Field(
        description="Lab generation metadata"
    )
    success: bool = Field(
        default=True,
        description="Lab generation success status"
    )
    error: Optional[str] = Field(
        default=None,
        description="Error message if generation failed"
    )

