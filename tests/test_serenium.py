#!/usr/bin/env python3
"""
Unit tests for Serenium Package Builder
"""

import unittest
import sys
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
import yaml

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from serenium import SereniumBuilder, PackageConfig, ValidationError
from themes import Theme, TerminalTheme

class TestPackageConfig(unittest.TestCase):
    """Test PackageConfig dataclass"""
    
    def test_default_config(self):
        """Test default configuration values"""
        config = PackageConfig()
        self.assertEqual(config.version, "1.0.0")
        self.assertEqual(config.maintainer, "Serenium Team")
        self.assertEqual(config.email, "team@serenium.org")
        self.assertFalse(config.is_metapackage)
        self.assertEqual(config.tools, [])
        self.assertEqual(config.dependencies, [])

class TestSereniumBuilder(unittest.TestCase):
    """Test SereniumBuilder class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = tempfile.mkdtemp()
        self.builder = SereniumBuilder(Theme.SERENIUM)
        self.builder.output_dir = Path(self.temp_dir)
        
    def tearDown(self):
        """Clean up test fixtures"""
        shutil.rmtree(self.temp_dir)
    
    def test_validate_package_name_valid(self):
        """Test valid package name validation"""
        valid_names = ["serenium-tool", "test123", "my_package", "a"]
        for name in valid_names:
            self.assertTrue(self.builder.validate_package_name(name))
    
    def test_validate_package_name_invalid(self):
        """Test invalid package name validation"""
        invalid_names = ["", "Test Package", "package!", "a" * 256]  # Too long
        
        for name in invalid_names:
            with self.assertRaises(ValidationError):
                self.builder.validate_package_name(name)
    
    def test_validate_package_name_valid_edge_cases(self):
        """Test edge cases for valid package names"""
        valid_names = ["a", "package-123", "my_package", "test123package", "123package", "package@name"]
        for name in valid_names:
            self.assertTrue(self.builder.validate_package_name(name))
    
    def test_validate_version_valid(self):
        """Test valid version validation"""
        valid_versions = ["1.0.0", "0.1.0", "10.20.30", "1.0.0-alpha"]
        for version in valid_versions:
            self.assertTrue(self.builder.validate_version(version))
    
    def test_validate_version_invalid(self):
        """Test invalid version validation"""
        invalid_versions = ["", "1.0", "v1.0.0", "not-a-version"]
        for version in invalid_versions:
            with self.assertRaises(ValidationError):
                self.builder.validate_version(version)
    
    def test_validate_version_valid_edge_cases(self):
        """Test edge cases for valid versions"""
        valid_versions = ["1.0.0-alpha", "2.1.3-beta.2", "10.20.30"]
        for version in valid_versions:
            self.assertTrue(self.builder.validate_version(version))
    
    def test_validate_email_valid(self):
        """Test valid email validation"""
        valid_emails = ["test@example.com", "user.name@domain.org", 
                       "user+tag@example.co.uk", ""]
        for email in valid_emails:
            self.assertTrue(self.builder.validate_email(email))
    
    def test_validate_email_invalid(self):
        """Test invalid email validation"""
        invalid_emails = ["invalid", "@example.com", "test@", "test.example.com"]
        for email in invalid_emails:
            with self.assertRaises(ValidationError):
                self.builder.validate_email(email)
    
    def test_sanitize_input(self):
        """Test input sanitization"""
        test_cases = [
            ("  test  ", "test"),
            ("test\x00\x01", "test"),
            ("", ""),
            ("normal text", "normal text")
        ]
        
        for input_text, expected in test_cases:
            result = self.builder.sanitize_input(input_text)
            self.assertEqual(result, expected)
    
    def test_load_config_from_file_yaml(self):
        """Test loading configuration from YAML file"""
        config_data = {
            'name': 'test-package',
            'version': '2.0.0',
            'description': 'Test package'
        }
        
        config_file = Path(self.temp_dir) / "test_config.yaml"
        with open(config_file, 'w') as f:
            yaml.dump(config_data, f)
        
        self.builder.load_config_from_file(str(config_file))
        
        self.assertEqual(self.builder.config.name, 'test-package')
        self.assertEqual(self.builder.config.version, '2.0.0')
        self.assertEqual(self.builder.config.description, 'Test package')
    
    def test_load_config_from_file_json(self):
        """Test loading configuration from JSON file"""
        config_data = {
            'name': 'test-package',
            'version': '2.0.0',
            'description': 'Test package'
        }
        
        config_file = Path(self.temp_dir) / "test_config.json"
        with open(config_file, 'w') as f:
            import json
            json.dump(config_data, f)
        
        self.builder.load_config_from_file(str(config_file))
        
        self.assertEqual(self.builder.config.name, 'test-package')
        self.assertEqual(self.builder.config.version, '2.0.0')
        self.assertEqual(self.builder.config.description, 'Test package')
    
    def test_load_config_from_file_not_found(self):
        """Test loading non-existent configuration file"""
        with self.assertRaises(FileNotFoundError):
            self.builder.load_config_from_file("nonexistent.yaml")
    
    def test_load_config_from_file_invalid_format(self):
        """Test loading configuration file with invalid format"""
        config_file = Path(self.temp_dir) / "test_config.txt"
        config_file.write_text("invalid content")
        
        with self.assertRaises(ValidationError):
            self.builder.load_config_from_file(str(config_file))
    
    def test_create_debian_structure(self):
        """Test Debian structure creation"""
        self.builder.config.name = "test-package"
        self.builder.config.version = "1.0.0"
        self.builder.config.description = "Test package"
        self.builder.config.maintainer = "Test Maintainer"
        self.builder.config.email = "test@example.com"
        self.builder.config.dependencies = ["python3"]
        
        package_path = self.builder.output_dir / "test-package-1.0.0"
        self.builder.create_debian_structure(package_path)
        
        # Check if Debian directory structure is created
        debian_dir = package_path / "debian"
        self.assertTrue(debian_dir.exists())
        self.assertTrue((debian_dir / "changelog").exists())
        self.assertTrue((debian_dir / "control").exists())
        self.assertTrue((debian_dir / "rules").exists())
        self.assertTrue((debian_dir / "compat").exists())
        self.assertTrue((debian_dir / "source" / "format").exists())
        
        # Check file permissions
        rules_file = debian_dir / "rules"
        self.assertEqual(oct(rules_file.stat().st_mode)[-3:], "755")
    
    def test_create_desktop_entry(self):
        """Test desktop entry creation"""
        self.builder.config.name = "test-package"
        self.builder.config.create_desktop = True
        self.builder.config.desktop_name = "Test Package"
        self.builder.config.desktop_comment = "A test package"
        self.builder.config.desktop_icon = "test-icon"
        self.builder.config.desktop_categories = "System"
        
        package_path = self.builder.output_dir / "test-package-1.0.0"
        self.builder.create_desktop_entry(package_path)
        
        desktop_file = package_path / "usr" / "share" / "applications" / "test-package.desktop"
        self.assertTrue(desktop_file.exists())
        
        content = desktop_file.read_text()
        self.assertIn("Name=Test Package", content)
        self.assertIn("Comment=A test package", content)
        self.assertIn("Icon=test-icon", content)
    
    def test_create_package_files(self):
        """Test package files creation"""
        self.builder.config.name = "test-package"
        self.builder.config.description = "Test package"
        self.builder.config.tools = ["tool1", "tool2"]
        
        package_path = self.builder.output_dir / "test-package-1.0.0"
        self.builder.create_package_files(package_path)
        
        launcher_file = package_path / "usr" / "bin" / "test-package"
        self.assertTrue(launcher_file.exists())
        
        content = launcher_file.read_text()
        self.assertIn("test-package - Test package", content)
        self.assertIn("tool1", content)
        self.assertIn("tool2", content)
        
        # Check file permissions
        self.assertEqual(oct(launcher_file.stat().st_mode)[-3:], "755")
    
    def test_create_build_script(self):
        """Test build script creation"""
        self.builder.config.name = "test-package"
        self.builder.config.version = "1.0.0"
        
        package_path = self.builder.output_dir / "test-package-1.0.0"
        package_path.mkdir(parents=True, exist_ok=True)
        self.builder.create_build_script(package_path)
        
        build_file = package_path / "build.sh"
        self.assertTrue(build_file.exists())
        
        content = build_file.read_text()
        self.assertIn("PACKAGE_NAME=\"test-package\"", content)
        self.assertIn("PACKAGE_VERSION=\"1.0.0\"", content)
        self.assertIn("dpkg-buildpackage", content)
        
        # Check file permissions
        self.assertEqual(oct(build_file.stat().st_mode)[-3:], "755")
    
    def test_create_readme(self):
        """Test README creation"""
        self.builder.config.name = "test-package"
        self.builder.config.version = "1.0.0"
        self.builder.config.description = "Test package"
        self.builder.config.maintainer = "Test Maintainer"
        self.builder.config.email = "test@example.com"
        self.builder.config.tools = ["tool1"]
        self.builder.config.dependencies = ["dep1"]
        
        package_path = self.builder.output_dir / "test-package-1.0.0"
        package_path.mkdir(parents=True, exist_ok=True)
        self.builder.create_readme(package_path)
        
        readme_file = package_path / "README.md"
        self.assertTrue(readme_file.exists())
        
        content = readme_file.read_text()
        self.assertIn("# test-package", content)
        self.assertIn("Test package", content)
        self.assertIn("tool1", content)
        self.assertIn("dep1", content)
    
    def test_save_config(self):
        """Test configuration saving"""
        self.builder.config.name = "test-package"
        self.builder.config.version = "1.0.0"
        self.builder.config.description = "Test package"
        
        package_path = self.builder.output_dir / "test-package-1.0.0"
        package_path.mkdir(parents=True, exist_ok=True)
        self.builder.save_config(package_path)
        
        config_file = package_path / "serenium-config.yaml"
        self.assertTrue(config_file.exists())
        
        with open(config_file, 'r') as f:
            loaded_config = yaml.safe_load(f)
        
        self.assertEqual(loaded_config['name'], 'test-package')
        self.assertEqual(loaded_config['version'], '1.0.0')
        self.assertEqual(loaded_config['description'], 'Test package')
    
    def test_build_package_integration(self):
        """Test complete package build integration"""
        self.builder.config.name = "integration-test"
        self.builder.config.version = "1.0.0"
        self.builder.config.description = "Integration test package"
        self.builder.config.maintainer = "Test Maintainer"
        self.builder.config.email = "test@example.com"
        self.builder.config.is_metapackage = False
        self.builder.config.tools = ["test-tool"]
        self.builder.config.create_desktop = True
        self.builder.config.desktop_name = "Test Tool"
        self.builder.config.desktop_comment = "Test comment"
        self.builder.config.dependencies = ["python3"]
        self.builder.config.menu_section = "01-System"
        
        # Mock user input for directory overwrite
        with patch('builtins.input', return_value='y'):
            self.builder.build_package()
        
        package_path = self.builder.output_dir / "integration-test-1.0.0"
        self.assertTrue(package_path.exists())
        
        # Check all components are created
        self.assertTrue((package_path / "debian").exists())
        self.assertTrue((package_path / "usr" / "bin" / "integration-test").exists())
        self.assertTrue((package_path / "usr" / "share" / "applications" / "integration-test.desktop").exists())
        self.assertTrue((package_path / "usr" / "share" / "serenium-menu" / "applications" / "01-System").exists())
        self.assertTrue((package_path / "build.sh").exists())
        self.assertTrue((package_path / "README.md").exists())
        self.assertTrue((package_path / "serenium-config.yaml").exists())

class TestTerminalTheme(unittest.TestCase):
    """Test TerminalTheme class"""
    
    def test_theme_initialization(self):
        """Test theme initialization"""
        theme = TerminalTheme(Theme.SERENIUM)
        self.assertEqual(theme.theme, Theme.SERENIUM)
        self.assertIsNotNone(theme.colors)
    
    def test_colorize_methods(self):
        """Test color formatting methods"""
        theme = TerminalTheme(Theme.SERENIUM)
        
        # Test various formatting methods
        self.assertIsInstance(theme.success("test"), str)
        self.assertIsInstance(theme.error("test"), str)
        self.assertIsInstance(theme.warning("test"), str)
        self.assertIsInstance(theme.info("test"), str)
        self.assertIsInstance(theme.title("test"), str)
        self.assertIsInstance(theme.prompt("test"), str)
        self.assertIsInstance(theme.muted("test"), str)
        self.assertIsInstance(theme.highlight("test"), str)
    
    def test_box_formatting(self):
        """Test box formatting"""
        theme = TerminalTheme(Theme.SERENIUM)
        box = theme.box("Test content")
        self.assertIn("Test content", box)
        self.assertIn("┌", box)
        self.assertIn("┐", box)
        self.assertIn("└", box)
        self.assertIn("┘", box)
    
    def test_progress_bar(self):
        """Test progress bar"""
        theme = TerminalTheme(Theme.SERENIUM)
        
        # Test normal progress
        progress = theme.progress_bar(5, 10)
        self.assertIn("[", progress)
        self.assertIn("]", progress)
        self.assertIn("50%", progress)
        
        # Test zero total
        progress = theme.progress_bar(1, 0)
        self.assertEqual(progress, "[N/A]")

if __name__ == '__main__':
    unittest.main()
