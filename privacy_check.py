#!/usr/bin/env python3
"""
Privacy & Security Checker for Summer School Chatbot

This script scans the project for potential privacy and security issues
before committing to version control.

Author: Assistant
Date: 2024
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

class PrivacyChecker:
    """Check for sensitive information in project files."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.issues = []
        
        # Patterns that indicate sensitive information
        self.sensitive_patterns = [
            # API Keys and Secrets
            (r'api[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}', "API Key"),
            (r'secret[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}', "Secret Key"),
            (r'access[_-]?token\s*[:=]\s*["\']?[a-zA-Z0-9_-]{20,}', "Access Token"),
            (r'sk-[a-zA-Z0-9]{20,}', "OpenAI API Key"),
            (r'AIza[0-9A-Za-z_-]{35}', "Google API Key"),
            
            # Credentials
            (r'password\s*[:=]\s*["\']?[^"\'\s]{8,}', "Password"),
            (r'credentials\s*[:=]\s*["\']?[^"\'\s]+', "Credentials"),
            
            # Personal Information
            (r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', "Email Address"),
            (r'\b\d{3}-\d{3}-\d{4}\b', "Phone Number"),
            (r'\b\d{3}\.\d{3}\.\d{4}\b', "Phone Number"),
            
            # Private Keys
            (r'-----BEGIN[A-Z ]+PRIVATE KEY-----', "Private Key"),
            (r'-----BEGIN RSA PRIVATE KEY-----', "RSA Private Key"),
        ]
        
        # File extensions to check
        self.check_extensions = {'.py', '.json', '.env', '.txt', '.md', '.yml', '.yaml', '.js', '.ts', '.html'}
        
        # Files and directories to skip
        self.skip_paths = {
            '.git', '__pycache__', 'venv', 'env', '.venv', 'node_modules',
            '.pytest_cache', '.coverage', '.tox', 'build', 'dist',
            '.gitignore', 'privacy_check.py'  # Skip this script itself
        }
        
        # Known safe example files
        self.safe_examples = {
            'config.env.example',
            'google_drive_credentials.json.example',
            '.env.example',
            'credentials.json.example'
        }
    
    def should_check_file(self, file_path: Path) -> bool:
        """Determine if a file should be checked for sensitive content."""
        # Skip if any parent directory is in skip_paths
        for part in file_path.parts:
            if part in self.skip_paths:
                return False
        
        # Skip if it's a known safe example file
        if file_path.name in self.safe_examples:
            return False
        
        # Only check specific file types
        return file_path.suffix.lower() in self.check_extensions
    
    def scan_file(self, file_path: Path) -> List[Tuple[str, str, int]]:
        """Scan a single file for sensitive patterns."""
        issues = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            for line_num, line in enumerate(content.split('\n'), 1):
                for pattern, description in self.sensitive_patterns:
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        # Skip if it's in a comment and looks like an example
                        if ('example' in line.lower() or 
                            'template' in line.lower() or
                            'your_' in line.lower() or
                            'placeholder' in line.lower()):
                            continue
                            
                        issues.append((str(file_path), description, line_num))
                        
        except Exception as e:
            print(f"⚠️ Could not scan {file_path}: {e}")
            
        return issues
    
    def check_git_status(self) -> List[str]:
        """Check what files are staged for commit."""
        try:
            import subprocess
            result = subprocess.run(['git', 'diff', '--cached', '--name-only'], 
                                  capture_output=True, text=True, cwd=self.project_root)
            if result.returncode == 0:
                return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except:
            pass
        return []
    
    def scan_project(self, staged_only: bool = False) -> Dict[str, List]:
        """Scan the entire project or only staged files."""
        results = {
            'critical': [],    # Definite sensitive info
            'warning': [],     # Potential sensitive info
            'info': []         # General security notes
        }
        
        if staged_only:
            staged_files = self.check_git_status()
            files_to_check = [Path(f) for f in staged_files if Path(f).exists()]
        else:
            files_to_check = [
                f for f in self.project_root.rglob('*') 
                if f.is_file() and self.should_check_file(f)
            ]
        
        total_files = len(files_to_check)
        print(f"🔍 Scanning {total_files} files for sensitive information...")
        
        for file_path in files_to_check:
            issues = self.scan_file(file_path)
            for file, description, line_num in issues:
                severity = self.categorize_issue(description)
                results[severity].append({
                    'file': file,
                    'description': description,
                    'line': line_num
                })
        
        return results
    
    def categorize_issue(self, description: str) -> str:
        """Categorize the severity of an issue."""
        critical_keywords = ['API Key', 'Secret Key', 'Access Token', 'Private Key', 'Password']
        warning_keywords = ['Email Address', 'Phone Number']
        
        if any(keyword in description for keyword in critical_keywords):
            return 'critical'
        elif any(keyword in description for keyword in warning_keywords):
            return 'warning'
        else:
            return 'info'
    
    def print_results(self, results: Dict[str, List]):
        """Print scan results in a user-friendly format."""
        total_issues = sum(len(issues) for issues in results.values())
        
        if total_issues == 0:
            print("✅ No sensitive information detected!")
            return True
        
        print(f"\n🚨 Found {total_issues} potential privacy/security issues:")
        
        # Critical issues
        if results['critical']:
            print(f"\n🔴 CRITICAL ({len(results['critical'])} issues):")
            for issue in results['critical']:
                print(f"   {issue['file']}:{issue['line']} - {issue['description']}")
        
        # Warning issues
        if results['warning']:
            print(f"\n🟡 WARNING ({len(results['warning'])} issues):")
            for issue in results['warning']:
                print(f"   {issue['file']}:{issue['line']} - {issue['description']}")
        
        # Info issues
        if results['info']:
            print(f"\n🔵 INFO ({len(results['info'])} issues):")
            for issue in results['info']:
                print(f"   {issue['file']}:{issue['line']} - {issue['description']}")
        
        return len(results['critical']) == 0
    
    def generate_report(self, results: Dict[str, List], output_file: str = "privacy_report.json"):
        """Generate a detailed JSON report."""
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"📄 Detailed report saved to: {output_file}")

def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Check for sensitive information in project files")
    parser.add_argument('--staged', action='store_true', 
                       help='Only check files staged for git commit')
    parser.add_argument('--report', type=str, default=None,
                       help='Generate detailed JSON report')
    parser.add_argument('--strict', action='store_true',
                       help='Exit with error code if any issues found')
    
    args = parser.parse_args()
    
    print("🔒 Privacy & Security Checker")
    print("=" * 50)
    
    checker = PrivacyChecker()
    results = checker.scan_project(staged_only=args.staged)
    
    safe = checker.print_results(results)
    
    if args.report:
        checker.generate_report(results, args.report)
    
    if not safe:
        print("\n⚠️ RECOMMENDATIONS:")
        print("1. Move sensitive data to environment variables")
        print("2. Use .example files for templates")
        print("3. Add sensitive files to .gitignore")
        print("4. Review files before committing")
        
        if args.strict:
            exit(1)
    else:
        print("🎉 Project is ready for sharing!")

if __name__ == "__main__":
    main() 