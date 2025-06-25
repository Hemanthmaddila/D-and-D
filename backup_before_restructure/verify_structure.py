#!/usr/bin/env python3
"""
Verification script to check if project restructuring was successful.
"""

import os
from pathlib import Path


def check_structure():
    """Check if the new project structure is in place."""
    print("🔍 Verifying project structure...")
    
    expected_structure = {
        "directories": [
            "docs",
            "config", 
            "database",
            "database/schema",
            "database/scripts",
            "database/seeds",
            "infrastructure",
            "infrastructure/terraform",
            "infrastructure/docker",
            "data-pipelines",
            "data-pipelines/airflow",
            "data-pipelines/scripts",
            "tests",
            "tests/unit",
            "tests/integration",
            "src",
            "src/core",
            "src/api",
            "scripts"
        ],
        "files": [
            "docs/README.md",
            "docs/quickstart.md",
            "docs/deployment.md",
            "docs/tutorial.md",
            "docs/docker-guide.md",
            "config/config.yaml",
            "requirements.txt",
            "README.md"
        ]
    }
    
    project_root = Path(".")
    issues = []
    successes = []
    
    # Check directories
    print("\n📁 Checking directories...")
    for directory in expected_structure["directories"]:
        dir_path = project_root / directory
        if dir_path.exists() and dir_path.is_dir():
            successes.append(f"✅ {directory}/")
        else:
            issues.append(f"❌ Missing directory: {directory}/")
    
    # Check files
    print("\n📄 Checking files...")
    for file_path in expected_structure["files"]:
        file_path_obj = project_root / file_path
        if file_path_obj.exists() and file_path_obj.is_file():
            successes.append(f"✅ {file_path}")
        else:
            issues.append(f"❌ Missing file: {file_path}")
    
    # Print results
    print(f"\n📊 Results:")
    print(f"   ✅ Successful: {len(successes)}")
    print(f"   ❌ Issues: {len(issues)}")
    
    if issues:
        print("\n⚠️  Issues found:")
        for issue in issues:
            print(f"   {issue}")
    
    if successes:
        print(f"\n✅ Structure verification {'completed successfully!' if not issues else 'completed with issues.'}")
        
    return len(issues) == 0


def check_imports():
    """Check if Python imports still work after restructuring."""
    print("\n🐍 Checking Python imports...")
    
    try:
        # Test if we can import from the restructured modules
        import sys
        sys.path.append("src")
        
        # Try importing common modules
        imports_to_test = [
            ("src.api.main", "FastAPI app"),
            ("src.rag_engine.hybrid_rag", "RAG engine")
        ]
        
        for module_name, description in imports_to_test:
            try:
                __import__(module_name)
                print(f"   ✅ {description} import successful")
            except ImportError as e:
                print(f"   ⚠️  {description} import issue: {e}")
            except Exception as e:
                print(f"   ⚠️  {description} import error: {e}")
                
    except Exception as e:
        print(f"   ❌ Import testing error: {e}")


def main():
    """Main verification function."""
    print("🧪 Project Structure Verification Tool")
    print("=" * 50)
    
    structure_ok = check_structure()
    check_imports()
    
    print("\n" + "=" * 50)
    if structure_ok:
        print("🎉 Project restructuring verification completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Run tests: python -m pytest tests/")
        print("   2. Test the API: python -m uvicorn src.api.main:app --reload")
        print("   3. Check documentation: open docs/README.md")
        print("   4. Update any remaining imports in your code")
    else:
        print("⚠️  Some issues were found. Please review and fix them.")
        print("💾 You can restore from backup if needed: backup_before_restructure/")


if __name__ == "__main__":
    main() 