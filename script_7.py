# Create the remaining files

files_content = {}

# Test script
files_content['test_rag_system.py'] = '''#!/usr/bin/env python3
"""
Simple test script for the RAG Knowledge Base system
Tests basic functionality without requiring external dependencies
"""

import asyncio
import aiohttp
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"

async def test_health_check():
    """Test if the API is responding"""
    print("🔍 Testing health check...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/health") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Health check passed: {data}")
                    return True
                else:
                    print(f"❌ Health check failed with status {response.status}")
                    return False
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return False

async def test_document_upload():
    """Test document upload functionality"""
    print("📄 Testing document upload...")
    
    # Create a test document
    test_doc_path = Path("test_document.txt")
    test_content = """
    This is a test document for the RAG system.
    
    The system should be able to process this document and answer questions about it.
    
    Key information:
    - This document was created for testing purposes
    - It contains multiple paragraphs and sections
    - The RAG system uses this content to generate responses
    - Vector embeddings are created from this text
    
    Technical details:
    - The document processing pipeline extracts text
    - Text is chunked into smaller pieces
    - Each chunk is converted to vector embeddings
    - Embeddings are stored in a FAISS index
    
    This allows for semantic search and intelligent question answering.
    """
    
    with open(test_doc_path, 'w') as f:
        f.write(test_content)
    
    async with aiohttp.ClientSession() as session:
        try:
            with open(test_doc_path, 'rb') as file:
                form_data = aiohttp.FormData()
                form_data.add_field('file', file, filename='test_document.txt', content_type='text/plain')
                
                async with session.post(f"{BASE_URL}/upload", data=form_data) as response:
                    if response.status == 200:
                        data = await response.json()
                        print(f"✅ Document upload successful: {data}")
                        return data.get('doc_id')
                    else:
                        error_data = await response.text()
                        print(f"❌ Document upload failed with status {response.status}: {error_data}")
                        return None
        except Exception as e:
            print(f"❌ Document upload failed: {e}")
            return None
        finally:
            # Clean up test file
            if test_doc_path.exists():
                test_doc_path.unlink()

async def test_query():
    """Test query functionality"""
    print("❓ Testing query...")
    
    test_query = "What is this document about?"
    
    async with aiohttp.ClientSession() as session:
        try:
            query_data = {
                "query": test_query,
                "top_k": 3
            }
            
            headers = {"Content-Type": "application/json"}
            
            async with session.post(f"{BASE_URL}/query", 
                                  data=json.dumps(query_data), 
                                  headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Query successful!")
                    print(f"📝 Response: {data['response'][:200]}...")
                    print(f"📚 Found {len(data['sources'])} sources")
                    return True
                else:
                    error_data = await response.text()
                    print(f"❌ Query failed with status {response.status}: {error_data}")
                    return False
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return False

async def test_list_documents():
    """Test document listing"""
    print("📋 Testing document listing...")
    
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(f"{BASE_URL}/documents") as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ Document listing successful: Found {len(data)} documents")
                    return data
                else:
                    error_data = await response.text()
                    print(f"❌ Document listing failed with status {response.status}: {error_data}")
                    return None
        except Exception as e:
            print(f"❌ Document listing failed: {e}")
            return None

async def run_all_tests():
    """Run all tests"""
    print("🚀 Starting RAG Knowledge Base Tests")
    print("=" * 50)
    
    # Wait a moment for system to be ready
    print("⏳ Waiting for system to be ready...")
    await asyncio.sleep(2)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Health check
    if await test_health_check():
        tests_passed += 1
    
    print()
    
    # Test 2: Document upload
    doc_id = await test_document_upload()
    if doc_id:
        tests_passed += 1
    
    print()
    
    # Test 3: Query (only if upload succeeded)
    if doc_id:
        if await test_query():
            tests_passed += 1
    else:
        print("⏭️ Skipping query test (upload failed)")
    
    print()
    
    # Test 4: List documents
    if await test_list_documents():
        tests_passed += 1
    
    print()
    print("=" * 50)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your RAG system is working correctly.")
    else:
        print("❌ Some tests failed. Check the output above for details.")
    
    return tests_passed == total_tests

if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\\n❌ Tests interrupted by user")
        exit(1)
    except Exception as e:
        print(f"❌ Test runner failed: {e}")
        exit(1)'''

# Demo document
files_content['demo_document.md'] = '''# Machine Learning Fundamentals

## Introduction

Machine Learning (ML) is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed for every task. This document provides an overview of key concepts and applications.

## Core Concepts

### Supervised Learning

Supervised learning uses labeled training data to learn a mapping from inputs to outputs. Common algorithms include:

- **Linear Regression**: Predicts continuous values
- **Logistic Regression**: Predicts categorical outcomes  
- **Decision Trees**: Uses tree-like models for decisions
- **Random Forest**: Combines multiple decision trees
- **Support Vector Machines**: Finds optimal boundaries between classes
- **Neural Networks**: Inspired by biological neural networks

### Unsupervised Learning

Unsupervised learning finds patterns in data without labeled examples:

- **K-Means Clustering**: Groups similar data points
- **Hierarchical Clustering**: Creates tree-like cluster structures
- **Principal Component Analysis (PCA)**: Reduces data dimensions
- **Association Rules**: Finds relationships between variables

### Reinforcement Learning

Reinforcement learning involves agents learning through interaction with an environment, receiving rewards or penalties for actions taken.

## Applications

### Healthcare
- Medical image analysis for disease diagnosis
- Drug discovery and development
- Personalized treatment recommendations
- Epidemic prediction and tracking

### Finance
- Fraud detection and prevention
- Algorithmic trading
- Credit scoring and risk assessment
- Robo-advisors for investment management

### Technology
- Recommendation systems (Netflix, Amazon)
- Search engine optimization
- Natural language processing
- Computer vision and image recognition

### Transportation
- Autonomous vehicles
- Route optimization
- Predictive maintenance
- Traffic management systems

## Data Processing Pipeline

### Data Collection
Gathering relevant data from various sources including databases, APIs, sensors, and web scraping.

### Data Cleaning
Removing inconsistencies, handling missing values, and standardizing formats.

### Feature Engineering
Creating meaningful features that help models learn patterns more effectively.

### Model Training
Using algorithms to learn patterns from the training data.

### Evaluation
Testing model performance using metrics like accuracy, precision, recall, and F1-score.

### Deployment
Implementing models in production environments for real-world use.

## Challenges and Considerations

### Data Quality
Poor quality data leads to poor model performance. Common issues include:
- Missing or incomplete data
- Biased datasets
- Inconsistent data formats
- Outdated information

### Ethical Considerations
- Bias in algorithms and training data
- Privacy and data protection
- Transparency and explainability
- Fairness across different groups

### Technical Challenges
- Scalability for large datasets
- Model interpretability
- Overfitting and generalization
- Computational resource requirements

## Future Trends

### Automated Machine Learning (AutoML)
Tools that automatically select algorithms, tune parameters, and optimize models.

### Federated Learning
Training models across distributed datasets without centralizing data.

### Explainable AI
Making AI decisions more transparent and interpretable.

### Edge Computing
Running ML models on devices rather than in the cloud for faster response times.

## Conclusion

Machine learning continues to evolve rapidly, offering new opportunities to solve complex problems across various industries. Success depends on understanding both the technical aspects and the broader implications of deploying ML systems.

The key to successful machine learning projects is combining domain expertise, high-quality data, appropriate algorithms, and careful evaluation of results.'''

# Create files
for filename, content in files_content.items():
    with open(filename, 'w') as f:
        f.write(content)
    print(f"✅ Created {filename}")

print("Created test script and demo document")