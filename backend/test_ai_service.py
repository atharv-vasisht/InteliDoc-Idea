import asyncio
from app.services.ai_service import ai_service
from app.schemas.ai import ExtractionRequest, SummarizationRequest

def test_ai_extraction():
    """Test the AI extraction service with sample document text"""
    
    # Sample document text that should contain obligations
    sample_text = """
    DATA PROTECTION REQUIREMENTS
    
    Section 1: Security Measures
    All customer data must be encrypted in transit and at rest using AES-256 encryption. 
    Multi-factor authentication must be implemented for all user accounts.
    Access logs must be maintained for all data access and modifications.
    
    Section 2: Privacy Compliance
    Users must be provided with the ability to delete their personal data upon request.
    Consent must be obtained before collecting any personal information.
    Data retention policies must be clearly communicated to users.
    
    Section 3: Payment Processing
    All payment transactions must be PCI DSS compliant.
    Credit card information must be tokenized and never stored in plain text.
    Payment processing must include fraud detection mechanisms.
    
    Section 4: User Experience
    The application must be accessible to users with disabilities (WCAG 2.1 AA compliance).
    Error messages must be clear and actionable.
    Loading times must not exceed 3 seconds for critical user flows.
    """
    
    print("🧪 Testing AI Document Intelligence Service")
    print("=" * 50)
    
    # Test 1: Obligation Extraction
    print("\n1️⃣ Testing Obligation Extraction...")
    try:
        request = ExtractionRequest(
            text=sample_text,
            document_title="Sample Data Protection Policy",
            document_type="regulation"
        )
        
        obligations = ai_service.extract_obligations(request)
        
        print(f"✅ Successfully extracted {len(obligations)} obligations:")
        for i, obligation in enumerate(obligations, 1):
            print(f"   {i}. {obligation.obligation_text}")
            print(f"      Category: {obligation.category.value}")
            print(f"      Priority: {obligation.priority.value if obligation.priority else 'N/A'}")
            print(f"      Source: {obligation.source_section}")
            print()
            
    except Exception as e:
        print(f"❌ Obligation extraction failed: {e}")
        return False
    
    # Test 2: Text Summarization
    print("\n2️⃣ Testing Text Summarization...")
    try:
        summary_request = SummarizationRequest(
            text=sample_text,
            max_length=200
        )
        
        summary_result = ai_service.summarize_text(summary_request)
        
        print("✅ Summary generated successfully:")
        print(f"   Summary: {summary_result['summary']}")
        print(f"   Key Points: {summary_result['key_points']}")
        print(f"   Processing Time: {summary_result['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"❌ Summarization failed: {e}")
        return False
    
    print("\n🎉 All AI service tests passed!")
    return True

if __name__ == "__main__":
    test_ai_extraction() 