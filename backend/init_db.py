#!/usr/bin/env python3
"""
Database initialization script for InteliDoc
Creates tables and sample data
"""

import asyncio
import os
import sys
from sqlalchemy import text
from app.core.database import async_engine, sync_engine
from app.models import User, Document, Obligation, Mapping
from app.core.database import Base

async def init_database():
    """Initialize the database with tables and sample data"""
    
    print("🗄️  Initializing database...")
    
    # Create tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("✅ Tables created successfully")
    
    # Insert sample data
    async with async_engine.begin() as conn:
        # Create sample user
        await conn.execute(text("""
            INSERT INTO users (email, hashed_password, full_name, is_active, is_superuser)
            VALUES ('admin@intelidoc.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/HS.iK8i', 'Admin User', true, true)
            ON CONFLICT (email) DO NOTHING
        """))
        
        # Create sample document
        await conn.execute(text("""
            INSERT INTO documents (title, filename, file_path, file_size, file_type, uploaded_by)
            VALUES ('Sample Regulation Document', 'sample_regulation.pdf', '/uploads/sample.pdf', 1024000, 'pdf', 1)
            ON CONFLICT DO NOTHING
        """))
        
        # Create sample obligations
        sample_obligations = [
            {
                'text': 'Ensure all customer data is encrypted in transit and at rest.',
                'category': 'security',
                'priority': 'high',
                'source_section': 'Data Protection Requirements',
                'document_id': 1,
                'extracted_by': 1
            },
            {
                'text': 'Provide users with the ability to delete their data upon request.',
                'category': 'privacy',
                'priority': 'medium',
                'source_section': 'User Rights',
                'document_id': 1,
                'extracted_by': 1
            },
            {
                'text': 'Implement multi-factor authentication for all user accounts.',
                'category': 'security',
                'priority': 'high',
                'source_section': 'Authentication Requirements',
                'document_id': 1,
                'extracted_by': 1
            },
            {
                'text': 'Maintain audit logs for all data access and modifications.',
                'category': 'compliance',
                'priority': 'medium',
                'source_section': 'Audit Requirements',
                'document_id': 1,
                'extracted_by': 1
            }
        ]
        
        for obligation in sample_obligations:
            await conn.execute(text("""
                INSERT INTO obligations (text, category, priority, source_section, document_id, extracted_by)
                VALUES (:text, :category, :priority, :source_section, :document_id, :extracted_by)
                ON CONFLICT DO NOTHING
            """), obligation)
        
        # Create sample mappings
        sample_mappings = [
            {
                'obligation_id': 1,
                'mapping_type': 'policy',
                'external_id': 'POL-001',
                'external_name': 'Data Encryption Policy',
                'external_url': 'https://company.com/policies/data-encryption',
                'mapped_by': 1
            },
            {
                'obligation_id': 2,
                'mapping_type': 'jira_ticket',
                'external_id': 'PROD-123',
                'external_name': 'Implement Data Deletion Feature',
                'external_url': 'https://company.atlassian.net/browse/PROD-123',
                'mapped_by': 1
            }
        ]
        
        for mapping in sample_mappings:
            await conn.execute(text("""
                INSERT INTO mappings (obligation_id, mapping_type, external_id, external_name, external_url, mapped_by)
                VALUES (:obligation_id, :mapping_type, :external_id, :external_name, :external_url, :mapped_by)
                ON CONFLICT DO NOTHING
            """), mapping)
    
    print("✅ Sample data inserted successfully")
    print("🎉 Database initialization complete!")

if __name__ == "__main__":
    asyncio.run(init_database()) 