#!/usr/bin/env python3
"""
Serenium - Advanced Package Builder
A production-ready tool to scaffold new packages with proper Debian packaging.
"""

import os
import sys
import json
import logging
import argparse
import subprocess
import yaml
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Union
from dataclasses import dataclass, field
from themes import TerminalTheme, Theme, select_theme_interactive, get_ascii_art

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('serenium.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class PackageConfig:
    """Package configuration data structure"""
    name: str = ""
    version: str = "1.0.0"
    description: str = ""
    long_description: str = ""
    is_metapackage: bool = False
    tools: List[str] = field(default_factory=list)
    create_desktop: bool = False
    desktop_name: str = ""
    desktop_comment: str = ""
    desktop_icon: str = "applications-system"
    desktop_categories: str = "System"
    dependencies: List[str] = field(default_factory=list)
    menu_section: str = "99-Misc"
    maintainer: str = "Serenium Team"
    email: str = "team@serenium.org"
    output_dir: str = "."

class ValidationError(Exception):
    """Custom exception for validation errors"""
    pass

class SereniumBuilder:
    """Main package builder class"""
    
    def __init__(self, theme: Theme = Theme.SERENIUM, config_file: Optional[str] = None):
        self.config = PackageConfig()
        self.output_dir = Path.cwd()
        self.theme = TerminalTheme(theme)
        self.steps_total = 7
        self.steps_completed = 0
        self.config_file = config_file
        
        # Load config from file if provided
        if config_file:
            self.load_config_from_file(config_file)
    
    def validate_package_name(self, name: str) -> bool:
        """Validate package name according to Debian standards"""
        if not name:
            raise ValidationError("Package name cannot be empty")
        
        if len(name) > 255:
            raise ValidationError("Package name too long (max 255 characters)")
        
        # Check for invalid characters
        invalid_chars = set('!#$&*|;:"<>?/\\[]{}')
        if any(char in invalid_chars for char in name):
            raise ValidationError(f"Package name contains invalid characters: {invalid_chars}")
        
        # Must start with alphanumeric
        if not name[0].isalnum():
            raise ValidationError("Package name must start with alphanumeric character")
        
        # No spaces allowed
        if ' ' in name:
            raise ValidationError("Package name cannot contain spaces")
        
        return True
    
    def validate_version(self, version: str) -> bool:
        """Validate version according to Debian standards"""
        if not version:
            raise ValidationError("Version cannot be empty")
        
        # Basic version format check (semantic versioning)
        import re
        if not re.match(r'^\d+\.\d+\.\d+', version):
            raise ValidationError("Version must follow semantic versioning (e.g., 1.0.0)")
        
        return True
    
    def validate_email(self, email: str) -> bool:
        """Basic email validation"""
        if not email:
            return True  # Optional field
        
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            raise ValidationError("Invalid email format")
        
        return True
    
    def sanitize_input(self, text: str) -> str:
        """Sanitize user input"""
        if not text:
            return ""
        
        # Remove potentially dangerous characters
        dangerous_chars = ['\x00', '\x01', '\x02', '\x03', '\x04', '\x05']
        for char in dangerous_chars:
            text = text.replace(char, '')
        
        return text.strip()
    
    def load_config_from_file(self, config_file: str):
        """Load configuration from YAML or JSON file"""
        config_path = Path(config_file)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        try:
            with open(config_path, 'r') as f:
                if config_path.suffix.lower() in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                elif config_path.suffix.lower() == '.json':
                    data = json.load(f)
                else:
                    raise ValidationError("Unsupported config file format. Use .yaml, .yml, or .json")
            
            # Update config with loaded data
            for key, value in data.items():
                if hasattr(self.config, key):
                    setattr(self.config, key, value)
            
            logger.info(f"Configuration loaded from {config_file}")
            
        except Exception as e:
            logger.error(f"Failed to load configuration: {e}")
            raise ValidationError(f"Failed to load configuration: {e}")
    
    def get_user_input(self) -> PackageConfig:
        """Interactive prompt for package information"""
        print(get_ascii_art(self.theme.theme))
        print(self.theme.header("Serenium Package Builder"))
        print()
        
        # Basic package information
        print(self.theme.list_item("Package Configuration", "📋"))
        print(self.theme.separator())
        
        while True:
            try:
                name = self.sanitize_input(input(self.theme.prompt("Package name (e.g., serenium-toolkit): ")))
                self.validate_package_name(name)
                self.config.name = name
                break
            except ValidationError as e:
                print(self.theme.error(str(e)))
        
        while True:
            version = self.sanitize_input(input(self.theme.prompt("Version (e.g., 1.0.0): ")) or "1.0.0")
            try:
                self.validate_version(version)
                self.config.version = version
                break
            except ValidationError as e:
                print(self.theme.error(str(e)))
        
        self.config.description = self.sanitize_input(input(self.theme.prompt("Short description: ")))
        long_desc = self.sanitize_input(input(self.theme.prompt("Long description (optional): ")))
        self.config.long_description = long_desc or self.config.description
        
        # Package type
        print()
        print(self.theme.list_item("Package Type Selection", "📦"))
        print(self.theme.separator())
        print(self.theme.list_item("1. Regular package (with files)", "📁"))
        print(self.theme.list_item("2. Metapackage (dependencies only)", "🔗"))
        
        while True:
            package_type = input(self.theme.prompt("Choose type [1/2]: ")).strip()
            if package_type in ["1", "2"]:
                self.config.is_metapackage = package_type == "2"
                break
            else:
                print(self.theme.error("Please enter 1 or 2"))
        
        if not self.config.is_metapackage:
            # Tools and files for regular packages
            print()
            print(self.theme.list_item("Tools and Files", "🛠️"))
            print(self.theme.separator())
            tools_input = self.sanitize_input(input(self.theme.prompt("Tools to include (comma-separated, e.g., nmap, wireshark, john): ")))
            self.config.tools = [t.strip() for t in tools_input.split(',') if t.strip()] if tools_input else []
            
            # Desktop entry
            print()
            print(self.theme.list_item("Desktop Entry Configuration", "🖥️"))
            print(self.theme.separator())
            create_desktop = input(self.theme.prompt("Create desktop entry? [y/N]: ")).strip().lower()
            self.config.create_desktop = create_desktop == 'y'
            
            if self.config.create_desktop:
                self.config.desktop_name = self.sanitize_input(input(self.theme.prompt("Desktop entry name: ")))
                self.config.desktop_comment = self.sanitize_input(input(self.theme.prompt("Desktop comment: ")))
                self.config.desktop_icon = self.sanitize_input(input(self.theme.prompt("Icon name (optional): ")) or "applications-system")
                self.config.desktop_categories = self.sanitize_input(input(self.theme.prompt("Categories (e.g., System;Security): ")) or "System")
        else:
            self.config.tools = []
            self.config.create_desktop = False
        
        # Dependencies
        print()
        print(self.theme.list_item("Dependencies", "📦"))
        print(self.theme.separator())
        deps_input = self.sanitize_input(input(self.theme.prompt("Dependencies (comma-separated, e.g., python3, git): ")))
        self.config.dependencies = [d.strip() for d in deps_input.split(',') if d.strip()] if deps_input else []
        
        # Menu placement
        print()
        print(self.theme.list_item("Menu Placement", "📂"))
        print(self.theme.separator())
        self.config.menu_section = self.sanitize_input(input(self.theme.prompt("Menu section (e.g., 01-System): ")) or "99-Misc")
        
        # Maintainer info
        print()
        print(self.theme.list_item("Maintainer Information", "👤"))
        print(self.theme.separator())
        self.config.maintainer = self.sanitize_input(input(self.theme.prompt("Maintainer name: ")) or "Serenium Team")
        
        while True:
            email = self.sanitize_input(input(self.theme.prompt("Maintainer email: ")) or "team@serenium.org")
            try:
                self.validate_email(email)
                self.config.email = email
                break
            except ValidationError as e:
                print(self.theme.error(str(e)))
        
        return self.config
    
    def create_debian_structure(self, package_path: Path):
        """Create Debian packaging structure"""
        logger.info("Creating Debian packaging structure")
        
        debian_dir = package_path / "debian"
        debian_dir.mkdir(parents=True, exist_ok=True)
        
        # Create debian/changelog
        changelog = f"""{self.config.name} ({self.config.version}) unstable; urgency=medium

  * Initial release
  * {self.config.description}

 -- {self.config.maintainer} <{self.config.email}>  {datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')}
"""
        (debian_dir / "changelog").write_text(changelog)
        
        # Create debian/control
        if self.config.is_metapackage:
            control = f"""Source: {self.config.name}
Section: metapackages
Priority: optional
Maintainer: {self.config.maintainer} <{self.config.email}>
Build-Depends: debhelper-compat (= 13)
Standards-Version: 4.6.0

Package: {self.config.name}
Architecture: all
Depends: {', '.join(self.config.dependencies) if self.config.dependencies else '${{misc:Depends}}'}
Description: {self.config.description}
 {self.config.long_description}
"""
        else:
            control = f"""Source: {self.config.name}
Section: misc
Priority: optional
Maintainer: {self.config.maintainer} <{self.config.email}>
Build-Depends: debhelper-compat (= 13)
Standards-Version: 4.6.0

Package: {self.config.name}
Architecture: all
Depends: {', '.join(self.config.dependencies) if self.config.dependencies else '${{misc:Depends}}'}
Description: {self.config.description}
 {self.config.long_description}
"""
        (debian_dir / "control").write_text(control)
        
        # Create debian/rules
        rules = """#!/usr/bin/make -f
%:
	dh $@
"""
        (debian_dir / "rules").write_text(rules)
        (debian_dir / "rules").chmod(0o755)
        
        # Create debian/compat
        (debian_dir / "compat").write_text("13")
        
        # Create debian/source/format
        source_dir = debian_dir / "source"
        source_dir.mkdir(exist_ok=True)
        (source_dir / "format").write_text("3.0 (native)")
    
    def create_desktop_entry(self, package_path: Path):
        """Create desktop entry file"""
        if not self.config.create_desktop:
            return
            
        logger.info("Creating desktop entry")
        
        desktop_dir = package_path / "usr" / "share" / "applications"
        desktop_dir.mkdir(parents=True, exist_ok=True)
        
        desktop_entry = f"""[Desktop Entry]
Name={self.config.desktop_name}
Comment={self.config.desktop_comment}
Exec={self.config.name}
Icon={self.config.desktop_icon}
Terminal=false
Type=Application
Categories={self.config.desktop_categories}
StartupNotify=true
"""
        desktop_file = desktop_dir / f"{self.config.name}.desktop"
        desktop_file.write_text(desktop_entry)
    
    def create_menu_structure(self, package_path: Path):
        """Create menu structure"""
        logger.info("Creating menu structure")
        
        menu_dir = package_path / "usr" / "share" / "serenium-menu" / "applications" / self.config.menu_section
        menu_dir.mkdir(parents=True, exist_ok=True)
        
        if self.config.create_desktop:
            # Create symlink in menu structure
            desktop_file = menu_dir / f"{self.config.name}.desktop"
            target_path = Path("../../../applications") / f"{self.config.name}.desktop"
            desktop_file.symlink_to(target_path)
    
    def create_package_files(self, package_path: Path):
        """Create package files and directory structure"""
        if self.config.is_metapackage:
            return  # Metapackages don't need files
            
        logger.info("Creating package files")
        
        # Create basic directory structure
        usr_bin = package_path / "usr" / "bin"
        usr_bin.mkdir(parents=True, exist_ok=True)
        
        # Create a simple launcher script if tools are specified
        if self.config.tools:
            launcher_script = f"""#!/bin/bash
# {self.config.name} launcher
# Generated by Serenium Package Builder

echo "{self.config.name} - {self.config.description}"
echo ""
echo "Available tools:"
"""
            for tool in self.config.tools:
                launcher_script += f"echo '  - {tool}'\n"
            
            launcher_script += """
echo ""
echo "Use 'dpkg -L serenium-toolkit' to see all installed files."
"""
            launcher_file = usr_bin / self.config.name
            launcher_file.write_text(launcher_script)
            launcher_file.chmod(0o755)
    
    def create_build_script(self, package_path: Path):
        """Create build script for the package"""
        logger.info("Creating build script")
        
        build_script = f"""#!/bin/bash
# Build script for {self.config.name}
# Generated by Serenium Package Builder

set -e

PACKAGE_NAME="{self.config.name}"
PACKAGE_VERSION="{self.config.version}"

echo "Building $PACKAGE_NAME version $PACKAGE_VERSION..."

# Clean previous builds
rm -f ../${{PACKAGE_NAME}}_*.deb ../${{PACKAGE_NAME}}_*.tar.gz ../${{PACKAGE_NAME}}_*.dsc ../${{PACKAGE_NAME}}_*.changes

# Build the package
dpkg-buildpackage -us -uc -b

echo "Build complete!"
echo "Package file: ../${{PACKAGE_NAME}}_${{PACKAGE_VERSION}}_all.deb"
echo ""
echo "To install:"
echo "  sudo dpkg -i ../${{PACKAGE_NAME}}_${{PACKAGE_VERSION}}_all.deb"
echo "  sudo apt-get install -f  # Fix dependencies if needed"
"""
        build_file = package_path / "build.sh"
        build_file.write_text(build_script)
        build_file.chmod(0o755)
    
    def create_readme(self, package_path: Path):
        """Create README file"""
        logger.info("Creating README")
        
        readme = f"""# {self.config.name}

{self.config.description}

## Package Information
- **Version**: {self.config.version}
- **Type**: {'Metapackage' if self.config.is_metapackage else 'Regular Package'}
- **Maintainer**: {self.config.maintainer} <{self.config.email}>

"""
        
        if self.config.tools:
            readme += "## Included Tools\n"
            for tool in self.config.tools:
                readme += f"- {tool}\n"
            readme += "\n"
        
        if self.config.dependencies:
            readme += "## Dependencies\n"
            for dep in self.config.dependencies:
                readme += f"- {dep}\n"
            readme += "\n"
        
        readme += """## Building

To build this package:

```bash
./build.sh
```

## Installation

To install the built package:

```bash
sudo dpkg -i ../{package_name}_{package_version}_all.deb
sudo apt-get install -f  # Fix dependencies if needed
```

## Removal

To remove this package:

```bash
sudo apt-get remove {package_name}
```

---
Generated by Serenium Package Builder
""".format(package_name=self.config.name, package_version=self.config.version)
        
        (package_path / "README.md").write_text(readme)
    
    def save_config(self, package_path: Path):
        """Save configuration to file"""
        config_data = {
            'name': self.config.name,
            'version': self.config.version,
            'description': self.config.description,
            'long_description': self.config.long_description,
            'is_metapackage': self.config.is_metapackage,
            'tools': self.config.tools,
            'create_desktop': self.config.create_desktop,
            'desktop_name': self.config.desktop_name,
            'desktop_comment': self.config.desktop_comment,
            'desktop_icon': self.config.desktop_icon,
            'desktop_categories': self.config.desktop_categories,
            'dependencies': self.config.dependencies,
            'menu_section': self.config.menu_section,
            'maintainer': self.config.maintainer,
            'email': self.config.email
        }
        
        config_file = package_path / "serenium-config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False, indent=2)
    
    def build_package(self):
        """Main function to build the complete package"""
        print()
        print(self.theme.header("Building Package Structure"))
        print()
        
        # Create package directory
        package_name = f"{self.config.name}-{self.config.version}"
        package_path = self.output_dir / package_name
        
        if package_path.exists():
            response = input(self.theme.warning(f"Directory {package_path} already exists. Overwrite? [y/N]: ") + " ").strip().lower()
            if response != 'y':
                print(self.theme.error("Build aborted by user."))
                return
            import shutil
            shutil.rmtree(package_path)
        
        package_path.mkdir(parents=True, exist_ok=True)
        
        try:
            # Create all components with progress feedback
            self._update_progress("Creating Debian packaging structure")
            self.create_debian_structure(package_path)
            
            self._update_progress("Creating package files")
            self.create_package_files(package_path)
            
            self._update_progress("Creating desktop entry")
            self.create_desktop_entry(package_path)
            
            self._update_progress("Setting up menu structure")
            self.create_menu_structure(package_path)
            
            self._update_progress("Creating build script")
            self.create_build_script(package_path)
            
            self._update_progress("Generating documentation")
            self.create_readme(package_path)
            
            self._update_progress("Saving configuration")
            self.save_config(package_path)
            
            self._update_progress("Finalizing package")
            
            print()
            print(self.theme.success(f"Package scaffold created at: {package_path}"))
            print()
            print(self.theme.box(self._format_package_summary()))
            
            print()
            print(self.theme.header("Next Steps"))
            print(self.theme.list_item(f"Navigate to package directory:", "📁"))
            print(f"   {self.theme.highlight(f'cd {package_path}')}")
            print()
            print(self.theme.list_item(f"Build the package:", "🔨"))
            print(f"   {self.theme.highlight('./build.sh')}")
            print()
            print(self.theme.footer("Happy packaging! ⚡"))
            
            logger.info(f"Package {self.config.name} version {self.config.version} created successfully")
            
        except Exception as e:
            logger.error(f"Failed to build package: {e}")
            print(self.theme.error(f"Build failed: {e}"))
            raise
    
    def _update_progress(self, step: str):
        """Update progress indicator"""
        self.steps_completed += 1
        progress_bar = self.theme.progress_bar(self.steps_completed, self.steps_total)
        print(f"{progress_bar} {self.theme.muted(step)}")
    
    def _format_package_summary(self) -> str:
        """Format package summary for display"""
        summary = []
        summary.append(f"Package: {self.theme.highlight(self.config.name)}")
        summary.append(f"Version: {self.theme.highlight(self.config.version)}")
        summary.append(f"Type: {self.theme.highlight('Metapackage' if self.config.is_metapackage else 'Regular Package')}")
        
        if self.config.tools:
            summary.append(f"Tools: {self.theme.highlight(', '.join(self.config.tools))}")
        
        if self.config.dependencies:
            summary.append(f"Dependencies: {self.theme.highlight(', '.join(self.config.dependencies))}")
        
        if self.config.create_desktop:
            summary.append(f"Desktop Entry: {self.theme.highlight(self.config.desktop_name)}")
        
        summary.append(f"Menu Section: {self.theme.highlight(self.config.menu_section)}")
        
        return "\n".join(summary)

def create_sample_config():
    """Create a sample configuration file"""
    sample_config = {
        'name': 'sample-package',
        'version': '1.0.0',
        'description': 'A sample package created with Serenium',
        'long_description': 'This is a longer description of what the package does and its purpose.',
        'is_metapackage': False,
        'tools': ['tool1', 'tool2'],
        'create_desktop': True,
        'desktop_name': 'Sample Package',
        'desktop_comment': 'Launch the sample package',
        'desktop_icon': 'applications-system',
        'desktop_categories': 'System',
        'dependencies': ['python3', 'python3-yaml'],
        'menu_section': '01-System',
        'maintainer': 'Your Name',
        'email': 'your.email@example.com'
    }
    
    with open('sample-config.yaml', 'w') as f:
        yaml.dump(sample_config, f, default_flow_style=False, indent=2)
    
    print("Sample configuration created: sample-config.yaml")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Serenium Package Builder - Production-ready package scaffolding tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                           # Interactive mode
  %(prog)s --config config.yaml      # Use configuration file
  %(prog)s --theme ocean             # Use specific theme
  %(prog)s --create-sample-config    # Create sample configuration file
        """
    )
    
    parser.add_argument('--config', '-c', 
                       help='Configuration file (YAML or JSON)')
    parser.add_argument('--theme', '-t', 
                       choices=[t.value for t in Theme],
                       default='serenium',
                       help='Terminal theme (default: serenium)')
    parser.add_argument('--create-sample-config', 
                       action='store_true',
                       help='Create a sample configuration file and exit')
    parser.add_argument('--version', '-v',
                       action='version',
                       version='Serenium 1.0.0')
    
    args = parser.parse_args()
    
    if args.create_sample_config:
        create_sample_config()
        return
    
    print("\033[2J\033[H")  # Clear screen
    
    # Theme selection
    print("\n" + "=" * 60)
    print("⚡ Welcome to Serenium Package Builder")
    print("=" * 60)
    
    use_theme = input("\nWould you like to select a theme? [Y/n]: ").strip().lower()
    
    if use_theme in ['', 'y', 'yes']:
        theme = select_theme_interactive()
        
        # Show theme preview
        temp_theme = TerminalTheme(theme)
        print("\nTheme Preview:")
        temp_theme.show_theme_preview()
        
        confirm = input("\nUse this theme? [Y/n]: ").strip().lower()
        if confirm in ['', 'y', 'yes']:
            selected_theme = theme
        else:
            selected_theme = Theme.SERENIUM
            print("\nUsing default Serenium theme.")
    else:
        selected_theme = Theme.SERENIUM
        print("\nUsing default Serenium theme.")
    
    try:
        builder = SereniumBuilder(selected_theme, args.config)
        
        # If config file is provided and has all required info, skip interactive prompts
        if args.config and builder.config.name and builder.config.description:
            print(f"\n{builder.theme.info('Using configuration from file')}")
            builder.build_package()
        else:
            builder.get_user_input()
            builder.build_package()
            
    except KeyboardInterrupt:
        print("\n\n" + TerminalTheme(selected_theme).error("Build cancelled by user."))
        sys.exit(1)
    except Exception as e:
        print("\n\n" + TerminalTheme(selected_theme).error(f"Error: {e}"))
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
