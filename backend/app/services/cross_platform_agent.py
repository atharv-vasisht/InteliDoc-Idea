import asyncio
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum

class PlatformType(Enum):
    M365 = "microsoft_365"
    SAP = "sap"
    SALESFORCE = "salesforce"
    JIRA = "jira"
    SHAREPOINT = "sharepoint"
    TEAMS = "teams"
    OUTLOOK = "outlook"
    ONEDRIVE = "onedrive"

class DataType(Enum):
    DOCUMENT = "document"
    EMAIL = "email"
    TASK = "task"
    OPPORTUNITY = "opportunity"
    CONTRACT = "contract"
    POLICY = "policy"
    COMPLIANCE = "compliance"
    USER_ACTIVITY = "user_activity"

@dataclass
class CrossPlatformItem:
    platform: PlatformType
    data_type: DataType
    content: str
    metadata: Dict[str, Any]
    timestamp: datetime
    user_id: str
    source_id: str
    confidence_score: float

@dataclass
class GRCDiscrepancy:
    severity: str  # high, medium, low
    description: str
    platforms_involved: List[PlatformType]
    items: List[CrossPlatformItem]
    compliance_framework: str
    risk_level: str
    recommended_action: str
    detected_at: datetime

class CrossPlatformAgent:
    """
    MVP Cross-Platform AI Agent that monitors and cross-validates data across enterprise platforms
    """
    
    def __init__(self):
        self.platforms = {
            PlatformType.M365: "Microsoft 365",
            PlatformType.SAP: "SAP ERP",
            PlatformType.SALESFORCE: "Salesforce CRM",
            PlatformType.JIRA: "Jira Project Management",
            PlatformType.SHAREPOINT: "SharePoint Document Management",
            PlatformType.TEAMS: "Microsoft Teams",
            PlatformType.OUTLOOK: "Outlook Email",
            PlatformType.ONEDRIVE: "OneDrive File Storage"
        }
        
        # Simulated data for MVP demonstration
        self.simulated_data = self._generate_simulated_data()
        
    def _generate_simulated_data(self) -> List[CrossPlatformItem]:
        """Generate realistic simulated data across platforms for MVP demonstration"""
        return [
            # M365 - SharePoint Document
            CrossPlatformItem(
                platform=PlatformType.SHAREPOINT,
                data_type=DataType.DOCUMENT,
                content="Vendor Security Requirements: All vendors must implement MFA and data encryption. Vendor access must be reviewed quarterly.",
                metadata={
                    "title": "Vendor Security Policy v2.1",
                    "author": "Security Team",
                    "department": "IT Security",
                    "last_modified": "2024-01-15",
                    "tags": ["security", "vendor", "compliance"]
                },
                timestamp=datetime.now() - timedelta(days=2),
                user_id="security.team@company.com",
                source_id="sharepoint_doc_001",
                confidence_score=0.95
            ),
            
            # SAP - Contract Data
            CrossPlatformItem(
                platform=PlatformType.SAP,
                data_type=DataType.CONTRACT,
                content="Contract with Vendor ABC: Payment terms 30 days, security requirements: basic authentication only, data retention: 2 years",
                metadata={
                    "contract_id": "CON-2024-001",
                    "vendor_name": "Vendor ABC",
                    "contract_value": "$500,000",
                    "start_date": "2024-01-01",
                    "end_date": "2024-12-31",
                    "department": "Procurement"
                },
                timestamp=datetime.now() - timedelta(days=5),
                user_id="procurement@company.com",
                source_id="sap_contract_001",
                confidence_score=0.92
            ),
            
            # Salesforce - Opportunity
            CrossPlatformItem(
                platform=PlatformType.SALESFORCE,
                data_type=DataType.OPPORTUNITY,
                content="Enterprise deal with Client XYZ: Requires SOC2 compliance, data residency in EU, 24/7 support",
                metadata={
                    "opportunity_id": "OPP-2024-003",
                    "client_name": "Client XYZ",
                    "deal_value": "$2,500,000",
                    "stage": "Proposal",
                    "probability": "75%",
                    "expected_close": "2024-03-15"
                },
                timestamp=datetime.now() - timedelta(days=1),
                user_id="sales.rep@company.com",
                source_id="salesforce_opp_001",
                confidence_score=0.88
            ),
            
            # Jira - Task
            CrossPlatformItem(
                platform=PlatformType.JIRA,
                data_type=DataType.TASK,
                content="Implement SOC2 compliance controls for Client XYZ deal. Required: MFA, audit logging, data encryption",
                metadata={
                    "issue_key": "PROJ-123",
                    "issue_type": "Task",
                    "priority": "High",
                    "assignee": "dev.team@company.com",
                    "project": "Compliance Implementation",
                    "due_date": "2024-02-15"
                },
                timestamp=datetime.now() - timedelta(hours=6),
                user_id="project.manager@company.com",
                source_id="jira_task_001",
                confidence_score=0.90
            ),
            
            # Teams - Chat Message
            CrossPlatformItem(
                platform=PlatformType.TEAMS,
                data_type=DataType.USER_ACTIVITY,
                content="Team discussion: Client XYZ requires GDPR compliance. Need to update our data processing agreements.",
                metadata={
                    "channel": "Sales Team",
                    "message_type": "chat",
                    "participants": ["sales.rep@company.com", "legal.team@company.com"],
                    "thread_id": "thread_001"
                },
                timestamp=datetime.now() - timedelta(hours=2),
                user_id="sales.rep@company.com",
                source_id="teams_chat_001",
                confidence_score=0.85
            ),
            
            # Outlook - Email
            CrossPlatformItem(
                platform=PlatformType.OUTLOOK,
                data_type=DataType.EMAIL,
                content="Subject: Vendor ABC Security Review - URGENT\n\nVendor ABC's current security setup doesn't meet our MFA requirements. Need immediate remediation.",
                metadata={
                    "subject": "Vendor ABC Security Review - URGENT",
                    "sender": "security.team@company.com",
                    "recipients": ["procurement@company.com", "vendor.abc@company.com"],
                    "priority": "High",
                    "has_attachments": True
                },
                timestamp=datetime.now() - timedelta(hours=1),
                user_id="security.team@company.com",
                source_id="outlook_email_001",
                confidence_score=0.93
            ),
            
            # OneDrive - Policy Document
            CrossPlatformItem(
                platform=PlatformType.ONEDRIVE,
                data_type=DataType.POLICY,
                content="Data Retention Policy: Customer data must be retained for 7 years. Vendor data: 3 years. All data must be encrypted at rest.",
                metadata={
                    "title": "Data Retention Policy v1.2",
                    "author": "Legal Team",
                    "department": "Legal",
                    "last_modified": "2024-01-10",
                    "version": "1.2"
                },
                timestamp=datetime.now() - timedelta(days=3),
                user_id="legal.team@company.com",
                source_id="onedrive_policy_001",
                confidence_score=0.94
            )
        ]
    
    async def monitor_platforms(self) -> List[CrossPlatformItem]:
        """
        Simulate monitoring all enterprise platforms and collecting data
        """
        print("🔍 Cross-Platform Agent: Monitoring enterprise platforms...")
        
        # Simulate async data collection from multiple platforms
        tasks = []
        for platform in self.platforms.keys():
            task = self._collect_platform_data(platform)
            tasks.append(task)
        
        # Wait for all platform data collection
        results = await asyncio.gather(*tasks)
        
        # Flatten results
        all_items = []
        for result in results:
            all_items.extend(result)
        
        print(f"✅ Collected {len(all_items)} items across {len(self.platforms)} platforms")
        return all_items
    
    async def _collect_platform_data(self, platform: PlatformType) -> List[CrossPlatformItem]:
        """Simulate collecting data from a specific platform"""
        await asyncio.sleep(0.1)  # Simulate API call delay
        
        # Filter simulated data for this platform
        platform_items = [item for item in self.simulated_data if item.platform == platform]
        
        print(f"📊 {self.platforms[platform]}: Collected {len(platform_items)} items")
        return platform_items
    
    async def cross_validate_grc(self, items: List[CrossPlatformItem]) -> List[GRCDiscrepancy]:
        """
        Cross-validate data across platforms for GRC discrepancies
        """
        print("🔍 Cross-Platform Agent: Performing GRC cross-validation...")
        
        discrepancies = []
        
        # Check for security requirement inconsistencies
        security_discrepancy = self._check_security_requirements(items)
        if security_discrepancy:
            discrepancies.append(security_discrepancy)
        
        # Check for compliance framework gaps
        compliance_discrepancy = self._check_compliance_frameworks(items)
        if compliance_discrepancy:
            discrepancies.append(compliance_discrepancy)
        
        # Check for data retention inconsistencies
        retention_discrepancy = self._check_data_retention(items)
        if retention_discrepancy:
            discrepancies.append(retention_discrepancy)
        
        # Check for vendor management gaps
        vendor_discrepancy = self._check_vendor_management(items)
        if vendor_discrepancy:
            discrepancies.append(vendor_discrepancy)
        
        print(f"⚠️  Found {len(discrepancies)} GRC discrepancies across platforms")
        return discrepancies
    
    def _check_security_requirements(self, items: List[CrossPlatformItem]) -> Optional[GRCDiscrepancy]:
        """Check for security requirement inconsistencies across platforms"""
        security_items = [item for item in items if "security" in item.content.lower() or "mfa" in item.content.lower()]
        
        # Find MFA requirement inconsistencies
        mfa_required = []
        mfa_not_required = []
        
        for item in security_items:
            if "mfa" in item.content.lower() and "required" in item.content.lower():
                mfa_required.append(item)
            elif "basic authentication" in item.content.lower():
                mfa_not_required.append(item)
        
        if mfa_required and mfa_not_required:
            return GRCDiscrepancy(
                severity="high",
                description="Inconsistent MFA requirements detected across platforms. Policy requires MFA but vendor contract allows basic authentication.",
                platforms_involved=[item.platform for item in mfa_required + mfa_not_required],
                items=mfa_required + mfa_not_required,
                compliance_framework="SOC2, ISO27001",
                risk_level="high",
                recommended_action="Update vendor contract to require MFA and conduct security review",
                detected_at=datetime.now()
            )
        
        return None
    
    def _check_compliance_frameworks(self, items: List[CrossPlatformItem]) -> Optional[GRCDiscrepancy]:
        """Check for compliance framework gaps"""
        compliance_items = [item for item in items if "soc2" in item.content.lower() or "gdpr" in item.content.lower()]
        
        soc2_mentioned = [item for item in compliance_items if "soc2" in item.content.lower()]
        gdpr_mentioned = [item for item in compliance_items if "gdpr" in item.content.lower()]
        
        if soc2_mentioned and not gdpr_mentioned:
            return GRCDiscrepancy(
                severity="medium",
                description="SOC2 compliance mentioned but GDPR requirements not addressed in EU client deal",
                platforms_involved=[item.platform for item in soc2_mentioned],
                items=soc2_mentioned,
                compliance_framework="GDPR",
                risk_level="medium",
                recommended_action="Review GDPR compliance requirements for EU client deal",
                detected_at=datetime.now()
            )
        
        return None
    
    def _check_data_retention(self, items: List[CrossPlatformItem]) -> Optional[GRCDiscrepancy]:
        """Check for data retention inconsistencies"""
        retention_items = [item for item in items if "retention" in item.content.lower()]
        
        if len(retention_items) >= 2:
            # Check for different retention periods mentioned
            retention_periods = []
            for item in retention_items:
                if "7 years" in item.content:
                    retention_periods.append(("7 years", item))
                elif "3 years" in item.content:
                    retention_periods.append(("3 years", item))
                elif "2 years" in item.content:
                    retention_periods.append(("2 years", item))
            
            if len(set([period[0] for period in retention_periods])) > 1:
                return GRCDiscrepancy(
                    severity="medium",
                    description="Inconsistent data retention periods specified across documents",
                    platforms_involved=[item.platform for item in retention_items],
                    items=retention_items,
                    compliance_framework="Data Retention Policy",
                    risk_level="medium",
                    recommended_action="Standardize data retention periods across all contracts and policies",
                    detected_at=datetime.now()
                )
        
        return None
    
    def _check_vendor_management(self, items: List[CrossPlatformItem]) -> Optional[GRCDiscrepancy]:
        """Check for vendor management gaps"""
        vendor_items = [item for item in items if "vendor" in item.content.lower()]
        
        if vendor_items:
            # Check if vendor security review is mentioned but not completed
            security_review_mentioned = [item for item in vendor_items if "security review" in item.content.lower()]
            urgent_issues = [item for item in vendor_items if "urgent" in item.content.lower()]
            
            if security_review_mentioned and urgent_issues:
                return GRCDiscrepancy(
                    severity="high",
                    description="Vendor security review identified urgent issues requiring immediate attention",
                    platforms_involved=[item.platform for item in vendor_items],
                    items=vendor_items,
                    compliance_framework="Vendor Management",
                    risk_level="high",
                    recommended_action="Immediate vendor security remediation and quarterly review implementation",
                    detected_at=datetime.now()
                )
        
        return None
    
    async def generate_cross_platform_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive cross-platform intelligence report
        """
        print("📊 Cross-Platform Agent: Generating intelligence report...")
        
        # Collect data from all platforms
        items = await self.monitor_platforms()
        
        # Perform GRC cross-validation
        discrepancies = await self.cross_validate_grc(items)
        
        # Generate platform summary
        platform_summary = {}
        for platform in self.platforms.keys():
            platform_items = [item for item in items if item.platform == platform]
            platform_summary[platform.value] = {
                "name": self.platforms[platform],
                "items_count": len(platform_items),
                "data_types": list(set([item.data_type.value for item in platform_items])),
                "users": list(set([item.user_id for item in platform_items])),
                "last_activity": max([item.timestamp for item in platform_items]).isoformat() if platform_items else None
            }
        
        # Generate risk assessment
        risk_assessment = {
            "overall_risk": "medium",
            "high_risk_discrepancies": len([d for d in discrepancies if d.severity == "high"]),
            "medium_risk_discrepancies": len([d for d in discrepancies if d.severity == "medium"]),
            "low_risk_discrepancies": len([d for d in discrepancies if d.severity == "low"]),
            "platforms_monitored": len(self.platforms),
            "total_items_analyzed": len(items)
        }
        
        return {
            "report_generated_at": datetime.now().isoformat(),
            "platform_summary": platform_summary,
            "grc_discrepancies": [
                {
                    "severity": d.severity,
                    "description": d.description,
                    "platforms_involved": [p.value for p in d.platforms_involved],
                    "compliance_framework": d.compliance_framework,
                    "risk_level": d.risk_level,
                    "recommended_action": d.recommended_action,
                    "detected_at": d.detected_at.isoformat(),
                    "items_count": len(d.items)
                }
                for d in discrepancies
            ],
            "risk_assessment": risk_assessment,
            "intelligence_insights": [
                "Cross-platform security requirements need standardization",
                "Vendor management process requires immediate attention",
                "GDPR compliance gaps identified in EU client deals",
                "Data retention policies show inconsistencies across systems"
            ]
        }
    
    async def get_platform_activity_feed(self) -> List[Dict[str, Any]]:
        """
        Get real-time activity feed across all platforms
        """
        items = await self.monitor_platforms()
        
        # Sort by timestamp (most recent first)
        items.sort(key=lambda x: x.timestamp, reverse=True)
        
        activity_feed = []
        for item in items[:20]:  # Last 20 activities
            activity_feed.append({
                "platform": item.platform.value,
                "platform_name": self.platforms[item.platform],
                "data_type": item.data_type.value,
                "content_preview": item.content[:100] + "..." if len(item.content) > 100 else item.content,
                "user_id": item.user_id,
                "timestamp": item.timestamp.isoformat(),
                "confidence_score": item.confidence_score,
                "metadata": item.metadata
            })
        
        return activity_feed

# Global instance for the cross-platform agent
cross_platform_agent = CrossPlatformAgent() 