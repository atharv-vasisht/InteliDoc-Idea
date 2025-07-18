from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict, Any
import time
from app.services.cross_platform_agent import cross_platform_agent
from app.core.database import get_async_db

router = APIRouter()

@router.get("/monitor")
async def monitor_all_platforms():
    """
    Monitor all enterprise platforms and collect data
    """
    try:
        items = await cross_platform_agent.monitor_platforms()
        
        # Convert to serializable format
        platform_data = {}
        for platform in cross_platform_agent.platforms.keys():
            platform_items = [item for item in items if item.platform == platform]
            platform_data[platform.value] = {
                "name": cross_platform_agent.platforms[platform],
                "items_count": len(platform_items),
                "data_types": list(set([item.data_type.value for item in platform_items])),
                "users": list(set([item.user_id for item in platform_items])),
                "last_activity": max([item.timestamp for item in platform_items]).isoformat() if platform_items else None,
                "items": [
                    {
                        "data_type": item.data_type.value,
                        "content_preview": item.content[:150] + "..." if len(item.content) > 150 else item.content,
                        "user_id": item.user_id,
                        "timestamp": item.timestamp.isoformat(),
                        "confidence_score": item.confidence_score,
                        "metadata": item.metadata
                    }
                    for item in platform_items
                ]
            }
        
        return {
            "status": "success",
            "platforms_monitored": len(cross_platform_agent.platforms),
            "total_items_collected": len(items),
            "platform_data": platform_data,
            "monitoring_timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Platform monitoring failed: {str(e)}")

@router.get("/grc-validation")
async def perform_grc_cross_validation():
    """
    Perform GRC cross-validation across all platforms
    """
    try:
        # Collect data from all platforms
        items = await cross_platform_agent.monitor_platforms()
        
        # Perform GRC cross-validation
        discrepancies = await cross_platform_agent.cross_validate_grc(items)
        
        return {
            "status": "success",
            "discrepancies_found": len(discrepancies),
            "discrepancies": [
                {
                    "severity": d.severity,
                    "description": d.description,
                    "platforms_involved": [p.value for p in d.platforms_involved],
                    "compliance_framework": d.compliance_framework,
                    "risk_level": d.risk_level,
                    "recommended_action": d.recommended_action,
                    "detected_at": d.detected_at.isoformat(),
                    "items_count": len(d.items),
                    "items": [
                        {
                            "platform": item.platform.value,
                            "platform_name": cross_platform_agent.platforms[item.platform],
                            "data_type": item.data_type.value,
                            "content_preview": item.content[:100] + "..." if len(item.content) > 100 else item.content,
                            "user_id": item.user_id,
                            "timestamp": item.timestamp.isoformat()
                        }
                        for item in d.items
                    ]
                }
                for d in discrepancies
            ],
            "validation_timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GRC validation failed: {str(e)}")

@router.get("/intelligence-report")
async def generate_intelligence_report():
    """
    Generate comprehensive cross-platform intelligence report
    """
    try:
        report = await cross_platform_agent.generate_cross_platform_report()
        return report
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Report generation failed: {str(e)}")

@router.get("/activity-feed")
async def get_platform_activity_feed():
    """
    Get real-time activity feed across all platforms
    """
    try:
        activity_feed = await cross_platform_agent.get_platform_activity_feed()
        return {
            "status": "success",
            "activities_count": len(activity_feed),
            "activity_feed": activity_feed,
            "feed_timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Activity feed failed: {str(e)}")

@router.get("/platform/{platform_name}")
async def get_platform_details(platform_name: str):
    """
    Get detailed information about a specific platform
    """
    try:
        # Find platform by name
        platform = None
        for p_type, p_name in cross_platform_agent.platforms.items():
            if p_name.lower().replace(" ", "_") == platform_name.lower().replace(" ", "_"):
                platform = p_type
                break
        
        if not platform:
            raise HTTPException(status_code=404, detail=f"Platform '{platform_name}' not found")
        
        # Get platform data
        items = await cross_platform_agent.monitor_platforms()
        platform_items = [item for item in items if item.platform == platform]
        
        # Calculate platform metrics
        data_type_counts = {}
        user_activity = {}
        recent_activity = []
        
        for item in platform_items:
            # Count data types
            data_type = item.data_type.value
            data_type_counts[data_type] = data_type_counts.get(data_type, 0) + 1
            
            # Track user activity
            user_activity[item.user_id] = user_activity.get(item.user_id, 0) + 1
            
            # Recent activity
            recent_activity.append({
                "data_type": item.data_type.value,
                "content_preview": item.content[:100] + "..." if len(item.content) > 100 else item.content,
                "user_id": item.user_id,
                "timestamp": item.timestamp.isoformat(),
                "confidence_score": item.confidence_score,
                "metadata": item.metadata
            })
        
        # Sort recent activity by timestamp
        recent_activity.sort(key=lambda x: x["timestamp"], reverse=True)
        
        return {
            "platform_name": cross_platform_agent.platforms[platform],
            "platform_type": platform.value,
            "total_items": len(platform_items),
            "data_type_distribution": data_type_counts,
            "user_activity": user_activity,
            "recent_activity": recent_activity[:10],  # Last 10 activities
            "last_activity": max([item.timestamp for item in platform_items]).isoformat() if platform_items else None,
            "average_confidence": sum([item.confidence_score for item in platform_items]) / len(platform_items) if platform_items else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Platform details failed: {str(e)}")

@router.get("/discrepancies/summary")
async def get_discrepancies_summary():
    """
    Get summary of all GRC discrepancies
    """
    try:
        items = await cross_platform_agent.monitor_platforms()
        discrepancies = await cross_platform_agent.cross_validate_grc(items)
        
        # Group by severity
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        framework_counts = {}
        platform_counts = {}
        
        for d in discrepancies:
            severity_counts[d.severity] += 1
            
            # Count by compliance framework
            framework = d.compliance_framework
            framework_counts[framework] = framework_counts.get(framework, 0) + 1
            
            # Count by platform
            for platform in d.platforms_involved:
                platform_name = cross_platform_agent.platforms[platform]
                platform_counts[platform_name] = platform_counts.get(platform_name, 0) + 1
        
        return {
            "total_discrepancies": len(discrepancies),
            "severity_distribution": severity_counts,
            "compliance_framework_distribution": framework_counts,
            "platform_distribution": platform_counts,
            "risk_levels": {
                "high_risk": len([d for d in discrepancies if d.risk_level == "high"]),
                "medium_risk": len([d for d in discrepancies if d.risk_level == "medium"]),
                "low_risk": len([d for d in discrepancies if d.risk_level == "low"])
            },
            "summary_timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Discrepancies summary failed: {str(e)}")

@router.post("/simulate-platform-event")
async def simulate_platform_event(platform: str, event_type: str, content: str):
    """
    Simulate a new event on a specific platform for testing
    """
    try:
        # This would normally add to the simulated data
        # For MVP, we'll just return a success response
        return {
            "status": "success",
            "message": f"Simulated {event_type} event on {platform}",
            "content_preview": content[:100] + "..." if len(content) > 100 else content,
            "simulation_timestamp": time.time()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Event simulation failed: {str(e)}") 