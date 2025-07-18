import google.generativeai as genai
import time
import json
from typing import List, Dict, Any, Optional
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
        Extract obligations/requirements from text using enhanced enterprise-focused prompts
        """
        start_time = time.time()
        
        # Enhanced system prompt for enterprise use cases
        system_prompt = """You are an enterprise compliance and requirements intelligence expert specializing in PMO, GRC, and product management. Your role is to extract actionable obligations, requirements, and compliance items from unstructured documents and transform them into structured, traceable data.

Your expertise covers:
- Regulatory compliance (SOX, GDPR, HIPAA, FedRAMP, etc.)
- Contract obligations and vendor requirements
- Product requirements and feature specifications
- Operational procedures and policies
- Risk management and audit requirements

For each extracted item, provide:
- Specific, actionable text that can be mapped to internal processes
- Appropriate categorization for enterprise systems
- Priority based on business impact and regulatory requirements
- Source context for traceability

Categories to use:
- privacy: Data protection, user rights, consent, GDPR, CCPA requirements
- security: Encryption, access controls, security frameworks, SOC2, ISO27001
- payments: Payment processing, PCI DSS, financial regulations
- ux: User experience, accessibility, interface requirements
- compliance: Regulatory compliance, audit requirements, certifications
- legal: Contract terms, legal obligations, liability requirements
- operations: Operational processes, procedures, SLAs, KPIs
- risk: Risk management, mitigation requirements, controls
- other: Anything that doesn't fit the above categories

Priorities:
- high: Critical compliance, legal, or business requirements
- medium: Important operational or process requirements
- low: Nice-to-have or optional requirements

Return ONLY a valid JSON array with no additional text."""

        # Enhanced user prompt with enterprise context
        user_prompt = f"""Extract obligations, requirements, or compliance items from the following enterprise document. Focus on items that can be:
1. Mapped to internal policies, controls, or Jira tickets
2. Tracked for compliance and audit purposes
3. Used for requirement traceability
4. Integrated into project management workflows

Document Title: {request.document_title or 'Unknown'}
Document Type: {request.document_type or 'General'}
Business Context: {getattr(request, 'business_context', 'Enterprise document analysis')}

For each item, provide:
- obligation_text: Specific, actionable requirement or obligation
- category: Best-fit category for enterprise systems
- priority: High/Medium/Low based on business impact
- source_section: Section or heading where found
- business_impact: Brief description of business impact (optional)
- compliance_framework: Relevant compliance framework if applicable (optional)

TEXT:
{request.text}

Return as JSON array:
[
  {{
    "obligation_text": "Implement multi-factor authentication for all user accounts",
    "category": "security",
    "priority": "high",
    "source_section": "Security Requirements",
    "business_impact": "Critical for SOC2 compliance and data protection",
    "compliance_framework": "SOC2, ISO27001"
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
            
            # Parse JSON response
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
                    confidence_score=85,  # Default confidence for Gemini
                    business_impact=item.get("business_impact"),
                    compliance_framework=item.get("compliance_framework")
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

    def analyze_document_structure(self, text: str, document_type: str = "general") -> Dict[str, Any]:
        """
        Analyze document structure and extract metadata for enterprise document management
        """
        system_prompt = """You are an expert in enterprise document analysis and information governance. Analyze the structure and content of documents to extract metadata useful for PMO, compliance, and project management."""

        user_prompt = f"""Analyze the following document and extract structural metadata:

Document Type: {document_type}

TEXT:
{text}

Provide analysis as JSON:
{{
  "document_type": "contract|policy|requirement|procedure|other",
  "key_sections": ["section1", "section2", "section3"],
  "stakeholders": ["role1", "role2"],
  "compliance_areas": ["framework1", "framework2"],
  "risk_level": "low|medium|high",
  "action_items_count": 0,
  "deadlines": ["date1", "date2"],
  "summary": "Brief document summary"
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
            try:
                return json.loads(content)
            except Exception as e:
                print(f"JSON parsing error: {e}")
                return {"error": "Failed to parse document structure"}
                
        except Exception as e:
            print(f"Document structure analysis error: {e}")
            return {"error": "Failed to analyze document structure"}

    def generate_compliance_mapping(self, obligation_text: str, existing_controls: List[str]) -> Dict[str, Any]:
        """
        Generate compliance mapping suggestions for obligations
        """
        system_prompt = """You are a GRC expert specializing in mapping requirements to internal controls and compliance frameworks."""

        user_prompt = f"""Given this obligation: "{obligation_text}"

And these existing internal controls: {existing_controls}

Suggest mappings and identify gaps. Return as JSON:
{{
  "suggested_mappings": [
    {{"obligation": "obligation_text", "control": "control_name", "confidence": 0.85}}
  ],
  "gap_analysis": [
    {{"gap": "description", "risk_level": "high|medium|low", "recommended_action": "action"}}
  ],
  "compliance_frameworks": ["framework1", "framework2"]
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
            try:
                return json.loads(content)
            except Exception as e:
                print(f"Compliance mapping error: {e}")
                return {"error": "Failed to generate compliance mapping"}
                
        except Exception as e:
            print(f"Compliance mapping error: {e}")
            return {"error": "Failed to generate compliance mapping"}

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