"""
Lab Generation Service using LLM to create personalized coding labs.

This service generates personalized labs for each concept in the knowledge graph,
with customization based on student interests and hobbies.
"""

import os
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from models.lab_models import (
    PersonalizedLab,
    LabSection,
    LabExercise,
    LabGenerationMetadata,
    CompleteLabResult
)

load_dotenv()


class LabGenerationService:
    """
    Service for generating personalized coding labs based on concepts.
    Uses LLM to create engaging, contextual lab exercises.
    """
    
    def __init__(self, model_name: str = "gpt-4", temperature: float = 0.7):
        """
        Initialize the lab generation service.
        
        Args:
            model_name: OpenAI model to use for generation
            temperature: Temperature for generation (0.0-1.0)
        """
        self.model_name = model_name
        self.temperature = temperature
        
        # Initialize LLM
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
        
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=temperature,
            api_key=api_key
        )
        
        # Initialize output parser
        self.parser = JsonOutputParser(pydantic_object=PersonalizedLab)
    
    def _create_lab_prompt(self, concept_name: str, concept_definition: str, 
                          topic: str, personalization_context: Optional[str] = None) -> str:
        """
        Create a prompt for lab generation.
        
        Args:
            concept_name: Name of the concept
            concept_definition: Definition of the concept
            topic: Topic the concept belongs to
            personalization_context: Optional context for personalization (e.g., hobbies)
        
        Returns:
            Formatted prompt string
        """
        base_prompt = f"""You are an expert educator creating hands-on coding labs for big data and database concepts.

Generate a personalized lab for the following concept:

**Concept**: {concept_name}
**Definition**: {concept_definition}
**Topic**: {topic}
"""
        
        if personalization_context:
            base_prompt += f"""
**Personalization Context**: {personalization_context}

Please incorporate this context into the lab examples and scenarios to make it more engaging and relatable.
For example, if the context is "gaming", use gaming-related examples like player databases, leaderboards, etc.
"""
        
        base_prompt += """

Create a comprehensive lab with the following structure:

1. **Title**: An engaging title that captures the essence of the lab
2. **Difficulty**: Choose from 'easy', 'medium', or 'hard' based on concept complexity
3. **Estimated Time**: Realistic time estimate in minutes (15-180)
4. **Sections**: Create 1-3 sections, each with:
   - A specific aspect of the concept to explore
   - Appropriate difficulty level
   - Scaffolding level (low/medium/high) based on complexity
   - 1-3 exercises with:
     * Type: 'guided' (step-by-step), 'challenge' (minimal guidance), or 'exploration' (open-ended)
     * Number of hints (0-5)
     * Description of what to implement
     * Starter code template
     * Reference solution
     * Test cases for validation

5. **Prerequisites**: List any required knowledge
6. **Technologies**: List technologies/tools used (e.g., Python, MongoDB, Jupyter)

Make the lab practical, hands-on, and focused on real-world applications of the concept.
Include code examples that students can actually run and modify.

Return ONLY valid JSON matching this exact structure:
{
  "title": "string",
  "topic": "string",
  "difficulty": "easy|medium|hard",
  "estimated_time": number,
  "sections": [
    {
      "concept": "string",
      "title": "string",
      "difficulty": "easy|medium|hard",
      "scaffolding_level": "low|medium|high",
      "exercises": [
        {
          "type": "guided|challenge|exploration",
          "hints": number,
          "description": "string",
          "starter_code": "string",
          "solution": "string",
          "test_cases": [{"input": "...", "expected": "..."}]
        }
      ],
      "learning_objectives": ["string"],
      "background": "string"
    }
  ],
  "prerequisites": ["string"],
  "technologies": ["string"],
  "personalization_context": "string or null"
}
"""
        return base_prompt
    
    def generate_lab(self, concept_name: str, concept_definition: str, 
                    topic: str, personalization_context: Optional[str] = None) -> CompleteLabResult:
        """
        Generate a personalized lab for a given concept.
        
        Args:
            concept_name: Name of the concept
            concept_definition: Definition of the concept
            topic: Topic the concept belongs to
            personalization_context: Optional context for personalization
        
        Returns:
            CompleteLabResult with generated lab and metadata
        """
        try:
            # Create prompt
            prompt = self._create_lab_prompt(
                concept_name=concept_name,
                concept_definition=concept_definition,
                topic=topic,
                personalization_context=personalization_context
            )
            
            # Generate lab using LLM
            response = self.llm.invoke(prompt)
            
            # Parse response
            lab_data = self.parser.parse(response.content)
            
            # Create PersonalizedLab object
            lab = PersonalizedLab(**lab_data)
            
            # Create metadata
            metadata = LabGenerationMetadata(
                concept_name=concept_name,
                concept_definition=concept_definition,
                source_topic=topic,
                model_used=self.model_name,
                personalization_applied=personalization_context is not None
            )
            
            return CompleteLabResult(
                lab=lab,
                metadata=metadata,
                success=True
            )
            
        except Exception as e:
            print(f"❌ Error generating lab for {concept_name}: {e}")
            
            # Return error result
            return CompleteLabResult(
                lab=self._create_fallback_lab(concept_name, topic),
                metadata=LabGenerationMetadata(
                    concept_name=concept_name,
                    concept_definition=concept_definition,
                    source_topic=topic,
                    model_used=self.model_name,
                    personalization_applied=False
                ),
                success=False,
                error=str(e)
            )
    
    def _create_fallback_lab(self, concept_name: str, topic: str) -> PersonalizedLab:
        """
        Create a basic fallback lab when generation fails.
        
        Args:
            concept_name: Name of the concept
            topic: Topic the concept belongs to
        
        Returns:
            Basic PersonalizedLab object
        """
        return PersonalizedLab(
            title=f"Introduction to {concept_name}",
            topic=topic,
            difficulty="medium",
            estimated_time=45,
            sections=[
                LabSection(
                    concept=concept_name,
                    title=f"Exploring {concept_name}",
                    difficulty="medium",
                    scaffolding_level="medium",
                    exercises=[
                        LabExercise(
                            type="guided",
                            hints=3,
                            description=f"Learn the basics of {concept_name}",
                            starter_code="# TODO: Implement your solution here\n",
                            solution="# Solution will be provided",
                            test_cases=[]
                        )
                    ],
                    learning_objectives=[f"Understand {concept_name}"],
                    background=f"This lab introduces {concept_name}"
                )
            ],
            prerequisites=["Basic programming knowledge"],
            technologies=["Python", "Jupyter Notebook"],
            personalization_context=None
        )
    
    def generate_batch_labs(self, concepts: List[Dict[str, str]], 
                           personalization_context: Optional[str] = None) -> List[CompleteLabResult]:
        """
        Generate labs for multiple concepts.
        
        Args:
            concepts: List of concept dictionaries with 'name', 'definition', and 'topic'
            personalization_context: Optional context for personalization
        
        Returns:
            List of CompleteLabResult objects
        """
        results = []
        total = len(concepts)
        
        print(f"🚀 Generating labs for {total} concepts...")
        
        for i, concept in enumerate(concepts, 1):
            print(f"🔄 Processing {i}/{total}: {concept['name']}")
            
            result = self.generate_lab(
                concept_name=concept['name'],
                concept_definition=concept['definition'],
                topic=concept['topic'],
                personalization_context=personalization_context
            )
            
            results.append(result)
            
            if result.success:
                print(f"✅ Successfully generated lab for {concept['name']}")
            else:
                print(f"⚠️  Used fallback lab for {concept['name']}")
        
        return results

