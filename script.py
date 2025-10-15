import zipfile
import os
from pathlib import Path

# Create a ZIP file with all the project files
zip_filename = "rag-knowledge-base-complete.zip"

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
    "demo_document.md",
    "PROJECT_STRUCTURE.md"
]

# Create the ZIP file
with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path in files_to_zip:
        if os.path.exists(file_path):
            zipf.write(file_path, file_path)
            print(f"✅ Added {file_path}")
        else:
            print(f"❌ File not found: {file_path}")

print(f"\n📦 Created {zip_filename} with {len(files_to_zip)} files")
print(f"📁 ZIP file size: {os.path.getsize(zip_filename) / 1024:.1f} KB")

# Verify ZIP contents
print(f"\n📋 ZIP Contents:")
with zipfile.ZipFile(zip_filename, 'r') as zipf:
    for file_info in zipf.filelist:
        print(f"  - {file_info.filename} ({file_info.file_size} bytes)")

print(f"\n🎉 Ready for GitHub upload!")
print(f"📥 Download: {zip_filename}")
print(f"\n🚀 GitHub Upload Instructions:")
print("1. Download the ZIP file")
print("2. Extract all files to your local directory") 
print("3. Create new GitHub repository")
print("4. Upload all extracted files to the repository")
print("5. Your RAG system is ready to deploy!")