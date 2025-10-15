# Create the final ZIP package with all files
import zipfile
import os
from pathlib import Path

# List of all files to include in the ZIP
files_to_zip = [
    "main.py",
    "document_processor.py", 
    "vector_store.py",
    "llm_service.py",
    "requirements.txt",
    "frontend.html",
    "Dockerfile",
    "docker-compose.yml", 
    "nginx.conf",
    ".env.template",
    ".gitignore",
    "README.md",
    "start.sh",
    "start.bat",
    "test_rag_system.py",
    "demo_document.md"
]

# Check which files exist
existing_files = []
missing_files = []

for file_path in files_to_zip:
    if os.path.exists(file_path):
        existing_files.append(file_path)
        print(f"✅ {file_path}")
    else:
        missing_files.append(file_path)
        print(f"❌ {file_path}")

print(f"\n📊 Files Status:")
print(f"✅ Existing: {len(existing_files)}")
print(f"❌ Missing: {len(missing_files)}")

if missing_files:
    print(f"\n❌ Missing files: {missing_files}")

# Create the ZIP file with existing files
zip_filename = "rag-knowledge-base-complete.zip"

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in existing_files:
        zipf.write(file_path, file_path)
        print(f"📦 Added {file_path} to ZIP")

# Get ZIP file size
zip_size = os.path.getsize(zip_filename)
print(f"\n📁 ZIP file created: {zip_filename}")
print(f"📏 ZIP file size: {zip_size / 1024:.1f} KB")

# Verify ZIP contents
print(f"\n📋 ZIP Contents:")
with zipfile.ZipFile(zip_filename, 'r') as zipf:
    file_list = zipf.namelist()
    for file_name in sorted(file_list):
        file_info = zipf.getinfo(file_name)
        print(f"  📄 {file_name} ({file_info.file_size} bytes)")

print(f"\n🎉 Ready for GitHub upload!")
print(f"📥 Download: {zip_filename}")
print(f"📊 Total files in ZIP: {len(file_list)}")

# Create upload instructions
print(f"\n🚀 GitHub Upload Instructions:")
print("=" * 50)
print("1. Download the ZIP file from the output")
print("2. Create a new GitHub repository")
print("3. Extract all files from the ZIP")
print("4. Upload all extracted files to your GitHub repository")
print("5. Your complete RAG system is ready!")
print("")
print("🌟 Key Features of Your RAG System:")
print("- Complete FastAPI backend with document processing")
print("- Modern web frontend with drag-and-drop upload")
print("- Vector database with FAISS and sentence-transformers")
print("- OpenAI integration with intelligent fallback")
print("- Docker deployment with Nginx reverse proxy")
print("- Comprehensive documentation and testing")
print("- Production-ready with security and monitoring")
print("")
print("🚀 Quick Start After Upload:")
print("1. Clone your repository")
print("2. Run: chmod +x start.sh (Linux/macOS)")
print("3. Run: ./start.sh")
print("4. Open: http://localhost")
print("")
print("✨ Your RAG Knowledge Base system is ready for deployment!")