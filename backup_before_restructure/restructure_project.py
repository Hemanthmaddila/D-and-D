#!/usr/bin/env python3
"""
Project Restructuring Script for Dungeon Master's Oracle
Safely reorganizes the project following best practices.
"""

import os
import shutil
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class ProjectRestructurer:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.backup_dir = self.project_root / "backup_before_restructure"
        
    def create_backup(self):
        """Create a backup of the current structure."""
        print("🔄 Creating backup of current structure...")
        
        if self.backup_dir.exists():
            shutil.rmtree(self.backup_dir)
        
        # Create backup directory
        self.backup_dir.mkdir()
        
        # Copy important files and directories
        items_to_backup = [
            "src", "sql_schema", "infrastructure", "tests", "data-pipelines",
            "scripts", "docker", "*.md", "*.py", "*.yaml", "*.yml", "Makefile"
        ]
        
        for item in self.project_root.iterdir():
            if item.name.startswith('.') or item.name == 'backup_before_restructure':
                continue
            if item.is_file() or item.is_dir():
                if item.is_dir():
                    shutil.copytree(item, self.backup_dir / item.name)
                else:
                    shutil.copy2(item, self.backup_dir / item.name)
        
        print(f"✅ Backup created at: {self.backup_dir}")

    def create_new_structure(self):
        """Create the new directory structure."""
        print("🏗️  Creating new directory structure...")
        
        directories = [
            "docs",
            "docs/api",
            "config",
            "config/environments", 
            "database",
            "database/schema",
            "database/migrations",
            "database/seeds",
            "database/scripts",
            "infrastructure/terraform",
            "infrastructure/terraform/environments",
            "infrastructure/terraform/environments/dev",
            "infrastructure/terraform/environments/staging", 
            "infrastructure/terraform/environments/prod",
            "infrastructure/docker",
            "data-pipelines/airflow",
            "data-pipelines/airflow/dags",
            "data-pipelines/scripts",
            "tests/unit",
            "tests/integration", 
            "tests/e2e",
            "src/core",
            "src/api/routes",
            "tools",
            "tools/linting",
            "tools/formatting",
            "tools/pre-commit"
        ]
        
        for directory in directories:
            dir_path = self.project_root / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            
            # Create __init__.py files for Python packages
            if directory.startswith(('src/', 'tests/')):
                init_file = dir_path / "__init__.py"
                if not init_file.exists():
                    init_file.write_text("# Package initialization\n")
        
        print("✅ Directory structure created")

    def move_files(self):
        """Move files to their new locations."""
        print("📦 Moving files to new locations...")
        
        # Define file movements: (source, destination)
        movements = [
            # Documentation files
            ("QUICKSTART.md", "docs/quickstart.md"),
            ("DEPLOYMENT_README.md", "docs/deployment.md"),
            ("COMPLETE_TUTORIAL.md", "docs/tutorial.md"),
            ("DOCKER_BEGINNER_GUIDE.md", "docs/docker-guide.md"),
            
            # Configuration files
            ("config.yaml", "config/config.yaml"),
            ("cloudbuild.yaml", "config/cloudbuild.yaml"),
            
            # Test files (move root level tests to integration)
            ("test_env.py", "tests/integration/test_env.py"),
            ("test_gemini_usage.py", "tests/integration/test_gemini_usage.py"),
            ("test_live_api.py", "tests/integration/test_live_api.py"),
            ("test_rag_connection.py", "tests/integration/test_rag_connection.py"),
            
            # Data pipeline scripts
            ("expand_data.py", "data-pipelines/scripts/expand_data.py"),
            ("data_expansion_guide.py", "data-pipelines/scripts/data_expansion_guide.py"),
            
            # Move docker directory
            ("docker/Dockerfile", "infrastructure/docker/Dockerfile"),
        ]
        
        for source, destination in movements:
            source_path = self.project_root / source
            dest_path = self.project_root / destination
            
            if source_path.exists():
                # Create destination directory if it doesn't exist
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                
                # Move the file
                shutil.move(str(source_path), str(dest_path))
                print(f"  ✅ Moved {source} → {destination}")
            else:
                print(f"  ⚠️  File not found: {source}")

    def move_directories(self):
        """Move entire directories to new locations."""
        print("📁 Moving directories...")
        
        directory_movements = [
            # SQL schema to database
            ("sql_schema", "database/temp_sql_schema"),
            
            # Infrastructure reorganization  
            ("infrastructure", "infrastructure/terraform_temp"),
            
            # Data pipelines
            ("data-pipelines/dags", "data-pipelines/airflow/dags"),
            
            # Tests reorganization
            ("tests", "tests/unit_temp"),
        ]
        
        for source, destination in directory_movements:
            source_path = self.project_root / source
            dest_path = self.project_root / destination
            
            if source_path.exists():
                if dest_path.exists():
                    shutil.rmtree(dest_path)
                shutil.move(str(source_path), str(dest_path))
                print(f"  ✅ Moved directory {source} → {destination}")

    def reorganize_moved_directories(self):
        """Reorganize the moved directories into their final structure."""
        print("🔄 Reorganizing moved directories...")
        
        # Reorganize sql_schema → database
        temp_sql = self.project_root / "database/temp_sql_schema"
        if temp_sql.exists():
            # Move files to appropriate subdirectories
            for item in temp_sql.iterdir():
                if item.name.endswith('.sql'):
                    shutil.move(str(item), str(self.project_root / "database/schema" / item.name))
                elif item.name.endswith('.json'):
                    shutil.move(str(item), str(self.project_root / "database/schema" / item.name))
                elif item.name.endswith('.py') and ('setup' in item.name or 'create' in item.name or 'load' in item.name):
                    shutil.move(str(item), str(self.project_root / "database/scripts" / item.name))
                elif item.name.endswith('.py') and ('sample' in item.name or 'schema' in item.name):
                    shutil.move(str(item), str(self.project_root / "database/seeds" / item.name))
                elif item.name == 'README.md':
                    shutil.move(str(item), str(self.project_root / "database" / item.name))
                elif item.name.endswith('.tf'):
                    shutil.move(str(item), str(self.project_root / "database/schema" / item.name))
            
            # Remove temp directory
            if temp_sql.exists():
                shutil.rmtree(temp_sql)
        
        # Reorganize infrastructure
        temp_infra = self.project_root / "infrastructure/terraform_temp"
        if temp_infra.exists():
            for item in temp_infra.iterdir():
                if item.name.endswith('.tf') or item.name.endswith('.tfvars') or item.name.endswith('.example'):
                    shutil.move(str(item), str(self.project_root / "infrastructure/terraform" / item.name))
                elif item.name == 'README.md':
                    shutil.move(str(item), str(self.project_root / "infrastructure" / item.name))
            
            # Remove temp directory
            if temp_infra.exists():
                shutil.rmtree(temp_infra)
        
        # Reorganize tests
        temp_tests = self.project_root / "tests/unit_temp"
        if temp_tests.exists():
            for item in temp_tests.iterdir():
                shutil.move(str(item), str(self.project_root / "tests/unit" / item.name))
            
            # Remove temp directory
            if temp_tests.exists():
                shutil.rmtree(temp_tests)

    def create_documentation_index(self):
        """Create a documentation index file."""
        print("📝 Creating documentation index...")
        
        docs_readme = self.project_root / "docs/README.md"
        content = """# 📚 Documentation

Welcome to the Dungeon Master's Oracle documentation!

## Quick Navigation

- **[🚀 Quick Start](quickstart.md)** - Get up and running in minutes
- **[📖 Complete Tutorial](tutorial.md)** - Comprehensive guide
- **[🚢 Deployment Guide](deployment.md)** - Deploy to production
- **[🐳 Docker Guide](docker-guide.md)** - Container setup
- **[🔌 API Documentation](api/)** - API reference

## Project Structure

This project follows a clean, organized structure:

```
dungeon-masters-oracle/
├── 📚 docs/           # All documentation (you are here!)
├── ⚙️ config/         # Configuration files
├── 💻 src/            # Source code
├── 🗄️ database/       # Database schema and scripts
├── 🏗️ infrastructure/ # Infrastructure as Code
├── 📊 data-pipelines/ # Data processing
├── 🧪 tests/          # All tests
└── 🔧 scripts/        # Utility scripts
```

## Getting Help

- Check the [Quick Start](quickstart.md) for common setup issues
- Review the [Tutorial](tutorial.md) for detailed explanations
- See [Deployment Guide](deployment.md) for production concerns

---

*Built with ❤️ for the D&D community* 🧙‍♂️⚔️🐉
"""
        docs_readme.write_text(content)

    def create_consolidated_requirements(self):
        """Create a consolidated requirements.txt at the root level."""
        print("📋 Creating consolidated requirements...")
        
        # Collect all requirements from different files
        requirements_files = [
            "src/requirements.txt",
            "tests/requirements.txt", 
            "data-pipelines/requirements.txt"
        ]
        
        all_requirements = set()
        
        for req_file in requirements_files:
            req_path = self.project_root / req_file
            if req_path.exists():
                content = req_path.read_text()
                for line in content.split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        all_requirements.add(line)
        
        # Create main requirements.txt
        main_req = self.project_root / "requirements.txt"
        sorted_requirements = sorted(all_requirements)
        content = "# Dungeon Master's Oracle - Main Dependencies\n"
        content += "# Install with: pip install -r requirements.txt\n\n"
        content += "\n".join(sorted_requirements)
        main_req.write_text(content)

    def update_readme(self):
        """Update the main README with new structure references."""
        print("📝 Updating main README...")
        
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            content = readme_path.read_text()
            
            # Update file references to match new structure
            content = content.replace("cd sql_schema", "cd database/scripts")
            content = content.replace("python sql_schema/", "python database/scripts/")
            content = content.replace("See [QUICKSTART.md](QUICKSTART.md)", "See [docs/quickstart.md](docs/quickstart.md)")
            content = content.replace("See [DEPLOYMENT_README.md](DEPLOYMENT_README.md)", "See [docs/deployment.md](docs/deployment.md)")
            
            readme_path.write_text(content)

    def clean_old_files(self):
        """Remove any remaining old files that are no longer needed."""
        print("🧹 Cleaning up old files...")
        
        # Files to remove (they've been moved or are no longer needed)
        files_to_remove = [
            "docker-compose.yml"  # Will be moved to infrastructure/docker/
        ]
        
        for file_name in files_to_remove:
            file_path = self.project_root / file_name
            if file_path.exists():
                file_path.unlink()
                print(f"  🗑️  Removed {file_name}")

    def run_restructure(self):
        """Run the complete restructuring process."""
        print("🎯 Starting project restructuring...")
        print("=" * 50)
        
        try:
            # Step 1: Create backup
            self.create_backup()
            
            # Step 2: Create new structure
            self.create_new_structure()
            
            # Step 3: Move files
            self.move_files()
            
            # Step 4: Move directories
            self.move_directories()
            
            # Step 5: Reorganize moved directories
            self.reorganize_moved_directories()
            
            # Step 6: Create documentation
            self.create_documentation_index()
            
            # Step 7: Consolidate requirements
            self.create_consolidated_requirements()
            
            # Step 8: Update README
            self.update_readme()
            
            # Step 9: Clean up
            self.clean_old_files()
            
            print("=" * 50)
            print("✅ Project restructuring completed successfully!")
            print()
            print("📁 New structure:")
            print("   - docs/           → All documentation")
            print("   - config/         → Configuration files")
            print("   - database/       → Database schema & scripts")
            print("   - infrastructure/ → Terraform & Docker")
            print("   - data-pipelines/ → Data processing")
            print("   - tests/          → Organized test suites")
            print("   - src/            → Source code")
            print("   - scripts/        → Utility scripts")
            print()
            print(f"💾 Backup available at: {self.backup_dir}")
            print("🧪 Run tests to ensure everything works correctly")
            
        except Exception as e:
            print(f"❌ Error during restructuring: {e}")
            print(f"💾 Backup is available at: {self.backup_dir}")
            print("🔄 You can restore from backup if needed")
            sys.exit(1)


def main():
    """Main entry point."""
    print("🎲 Dungeon Master's Oracle - Project Restructuring Tool")
    print()
    
    # Confirm with user
    response = input("This will reorganize your project structure. Continue? (y/N): ")
    if response.lower() != 'y':
        print("❌ Restructuring cancelled")
        sys.exit(0)
    
    # Run restructuring
    restructurer = ProjectRestructurer()
    restructurer.run_restructure()


if __name__ == "__main__":
    main() 