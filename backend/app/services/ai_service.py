import google.generativeai as genai
import time
import json
from typing import List, Dict, Any
from app.core.config import settings
from app.schemas.ai import ExtractionRequest, ExtractedObligation, SummarizationRequest
from app.models.obligation import CategoryEnum, PriorityEnum
import re
import os

class AIService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = settings.GEMINI_MODEL
        self.max_tokens = settings.GEMINI_MAX_TOKENS
        self.temperature = settings.GEMINI_TEMPERATURE

    def extract_obligations(self, request: ExtractionRequest) -> List[ExtractedObligation]:
        """
        Extract obligations/requirements from text using GPT-4
        """
        start_time = time.time()
        
        # System prompt based on the business plan design
        system_prompt = """You are a compliance and requirements extraction expert. Given unstructured text, your job is to extract clear, actionable obligations or requirements, classify them by category, and return them as structured JSON.

Your task is to identify specific, actionable obligations or requirements that can be mapped to internal processes, policies, or backlog items. Focus on concrete, implementable items rather than general statements.

Categories to use:
- privacy: Data protection, user rights, consent requirements
- security: Encryption, access controls, security measures
- payments: Payment processing, financial requirements
- ux: User experience, interface requirements
- compliance: Regulatory compliance, audit requirements
- legal: Legal obligations, contract terms
- operations: Operational processes, procedures
- other: Anything that doesn't fit the above categories

Priorities:
- high: Critical, must-have requirements
- medium: Important but not critical
- low: Nice-to-have or optional requirements

Return ONLY a valid JSON array with no additional text or explanation. Do not include markdown, code blocks, or any text before or after the JSON array."""

        # User prompt template
        user_prompt = f"""Extract obligations or requirements from the following text. For each, provide:

- obligation_text: The extracted obligation or requirement (be specific and actionable)
- category: A best-guess category (privacy, security, payments, ux, compliance, legal, operations, other)
- priority: High/Medium/Low (if indicated in text, otherwise use Medium)
- source_section: Which section or heading it was found in (if possible)

Document Title: {request.document_title or 'Unknown'}
Document Type: {request.document_type or 'General'}

TEXT:
{request.text}

Return the results as a JSON array like this:
[
  {{
    "obligation_text": "Ensure all customer data is encrypted in transit.",
    "category": "security",
    "priority": "high",
    "source_section": "Data Protection Requirements"
  }}
]"""

        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                f"{system_prompt}\n\n{user_prompt}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            )
            
            content = response.text.strip()
            print("Gemini raw response:", content)
            
            # Direct JSON parse as before
            try:
                obligations_data = json.loads(content)
            except Exception as e:
                print(f"JSON parsing error: {e}\nRaw response: {content}")
                return []
            if not isinstance(obligations_data, list):
                obligations_data = [obligations_data]
                
                extracted_obligations = []
                for item in obligations_data:
                    # Validate and convert category
                    category_str = item.get("category", "other").lower()
                    category = self._map_category(category_str)
                    
                    # Validate and convert priority
                    priority_str = item.get("priority", "medium").lower()
                    priority = self._map_priority(priority_str)
                    
                    extracted_obligations.append(ExtractedObligation(
                        obligation_text=item.get("obligation_text", ""),
                        category=category,
                        priority=priority,
                        source_section=item.get("source_section"),
                        confidence_score=85  # Default confidence for Gemini
                    ))
                
                return extracted_obligations
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            return []

    def summarize_text(self, request: SummarizationRequest) -> Dict[str, Any]:
        """
        Generate a summary of the provided text
        """
        start_time = time.time()
        
        system_prompt = """You are an expert at summarizing documents and extracting key points. Provide clear, concise summaries that capture the main requirements, obligations, and important details."""

        user_prompt = f"""Summarize the following text in {request.max_length} words or less. Also extract 3-5 key points.

TEXT:
{request.text}

Provide your response as JSON:
{{
  "summary": "Your summary here",
  "key_points": ["Point 1", "Point 2", "Point 3"]
}}"""

        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(
                f"{system_prompt}\n\n{user_prompt}",
                generation_config=genai.types.GenerationConfig(
                    max_output_tokens=1000,
                    temperature=0.3
                )
            )
            
            content = response.text.strip()
            print("Gemini raw response:", content)
            
            try:
                result = json.loads(content)
                return {
                    "summary": result.get("summary", ""),
                    "key_points": result.get("key_points", []),
                    "processing_time": time.time() - start_time
                }
            except Exception as e:
                # Fallback: treat as plain text
                print(f"JSON parsing error: {e}\nRaw response: {content}")
                return {
                    "summary": content,
                    "key_points": [],
                    "processing_time": time.time() - start_time
                }
                
        except Exception as e:
            print(f"Gemini API error: {e}")
            return {
                "summary": "Error generating summary",
                "key_points": [],
                "processing_time": time.time() - start_time
            }

    def analyze_and_propose_reorg(self, folder_path: str) -> dict:
        """Scan folder, summarize files, and propose a reorganization plan using Gemini."""
        folder_tree = {}
        file_summaries = {}
        # Recursively scan folder
        for root, dirs, files in os.walk(folder_path):
            rel_root = os.path.relpath(root, folder_path)
            folder_tree[rel_root] = files
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(2000)  # Read first 2KB for summary
                except Exception as e:
                    content = f"[Error reading file: {e}]"
                # Summarize file
                summary_prompt = f"Summarize the following file for project management, compliance, and PMO context.\n\nFILENAME: {file}\nCONTENT:\n{content}\n\nReturn a 1-2 sentence summary."
                try:
                    model = genai.GenerativeModel(self.model)
                    response = model.generate_content(summary_prompt)
                    summary = response.text.strip()
                except Exception as e:
                    summary = f"[AI summary error: {e}]"
                file_summaries[file_path] = summary
        # Build prompt for reorganization
        reorg_prompt = (
            "You are an expert in project management and compliance document organization. "
            "Given the following folder structure and file summaries, propose a new, more organized structure and naming convention. "
            "Output a JSON diff of moves, renames, and new files to create. "
            "Do not include markdown or code blocks.\n\n"
            f"FOLDER TREE: {folder_tree}\n\nFILE SUMMARIES: {file_summaries}\n\n"
            "Return a JSON array of changes, where each change is an object with 'action' (move, rename, create), 'source', 'destination', and 'details' fields as needed."
        )
        try:
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(reorg_prompt)
            plan = response.text.strip()
            try:
                plan_json = json.loads(plan)
            except Exception as e:
                print(f"JSON parsing error in reorg plan: {e}\nRaw response: {plan}")
                plan_json = plan
            return {
                "folder_tree": folder_tree,
                "file_summaries": file_summaries,
                "proposed_changes": plan_json
            }
        except Exception as e:
            print(f"Gemini API error in reorg: {e}")
            return {"error": str(e)}

    def _map_category(self, category_str: str) -> CategoryEnum:
        """Map string category to CategoryEnum"""
        category_mapping = {
            "privacy": CategoryEnum.PRIVACY,
            "security": CategoryEnum.SECURITY,
            "payments": CategoryEnum.PAYMENTS,
            "ux": CategoryEnum.UX,
            "compliance": CategoryEnum.COMPLIANCE,
            "legal": CategoryEnum.LEGAL,
            "operations": CategoryEnum.OPERATIONS,
            "other": CategoryEnum.OTHER
        }
        return category_mapping.get(category_str.lower(), CategoryEnum.OTHER)

    def _map_priority(self, priority_str: str) -> PriorityEnum:
        """Map string priority to PriorityEnum"""
        priority_mapping = {
            "high": PriorityEnum.HIGH,
            "medium": PriorityEnum.MEDIUM,
            "low": PriorityEnum.LOW
        }
        return priority_mapping.get(priority_str.lower(), PriorityEnum.MEDIUM)

# Create singleton instance
ai_service = AIService() 