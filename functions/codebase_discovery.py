"""
Codebase Discovery
==============================================================
Purpose: Quickly understand unfamiliar codebases - frameworks, entry points, structure
"""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from collections import defaultdict

from utils.codebase_patterns import FRAMEWORK_PATTERNS, BUSINESS_PATTERNS, EXTERNAL_SERVICE_PATTERNS

@dataclass
class DiscoveryResult:
    """Results from codebase discovery."""
    entry_points: List[Dict[str, Any]]
    frameworks: Dict[str, float]
    business_patterns: Dict[str, List[str]]
    external_services: List[str]
    quick_start_guide: List[str]
    total_files_analyzed: int
    project_insights: List[str]

class CodebaseDiscovery:
    """Fast codebase understanding tool."""
    
    def __init__(self):
        self.excluded_dirs = {
            '__pycache__', '.git', '.pytest_cache', '.venv', 'venv', 'env',
            'node_modules', '.tox', 'build', 'dist'
        }
    
    def analyze_codebase(self, project_path: str) -> DiscoveryResult:
        """Main analysis - understand what this codebase does."""
        path = Path(project_path)
        if not path.exists():
            raise FileNotFoundError(f"Project path not found: {project_path}")
        
        # Get Python files
        python_files = self._get_python_files(path)
        if not python_files:
            return self._empty_result()
        
        print(f"🔍 Analyzing {len(python_files)} Python files...")
        
        # Run all detection
        entry_points = self._find_entry_points(python_files)
        frameworks = self._detect_frameworks(python_files)
        business_patterns = self._detect_business_patterns(python_files)
        external_services = self._detect_external_services(python_files)
        
        # Generate insights and guidance
        quick_start = self._generate_quick_start(entry_points, frameworks)
        insights = self._generate_insights(frameworks, business_patterns, external_services)
        
        return DiscoveryResult(
            entry_points=entry_points,
            frameworks=frameworks,
            business_patterns=business_patterns,
            external_services=external_services,
            quick_start_guide=quick_start,
            total_files_analyzed=len(python_files),
            project_insights=insights
        )
    
    def _get_python_files(self, project_path: Path) -> List[Path]:
        """Get Python files, excluding common build/cache directories."""
        python_files = []
        
        for file_path in project_path.rglob("*.py"):
            # Skip excluded directories
            if any(excluded in file_path.parts for excluded in self.excluded_dirs):
                continue
            python_files.append(file_path)
        
        return python_files
    
    def _find_entry_points(self, python_files: List[Path]) -> List[Dict[str, Any]]:
        """Find likely application entry points."""
        entry_points = []
        
        for file_path in python_files:
            confidence = self._calculate_entry_confidence(file_path)
            if confidence > 0.3:
                entry_points.append({
                    'filename': file_path.name,
                    'file_path': str(file_path),
                    'confidence': confidence
                })
        
        # Sort by confidence and return top 5
        entry_points.sort(key=lambda x: x['confidence'], reverse=True)
        return entry_points[:5]
    
    def _calculate_entry_confidence(self, file_path: Path) -> float:
        """Calculate how likely this file is an entry point."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception:
            return 0.0
        
        confidence = 0.0
        
        # Main guard pattern
        if 'if __name__ == "__main__":' in content:
            confidence += 0.6
        
        # Entry point filenames
        filename = file_path.name.lower()
        if filename in ['main.py', 'app.py', 'run.py', 'server.py', 'manage.py']:
            confidence += 0.4
        
        # Application server patterns
        if re.search(r'\.run\s*\(', content):
            confidence += 0.3
        
        # CLI argument handling
        if 'argparse' in content or 'sys.argv' in content:
            confidence += 0.2
        
        return min(confidence, 1.0)
    
    def _detect_frameworks(self, python_files: List[Path]) -> Dict[str, float]:
        """Detect frameworks used in the project."""
        framework_scores = defaultdict(float)
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check each framework
                for framework, patterns in FRAMEWORK_PATTERNS.items():
                    matches = sum(1 for pattern in patterns if pattern in content)
                    if matches > 0:
                        # Score based on pattern matches
                        framework_scores[framework] += min(matches / len(patterns), 1.0)
            except Exception:
                continue
        
        # Normalize scores and filter significant ones
        total_files = len(python_files)
        return {
            framework: score / total_files 
            for framework, score in framework_scores.items() 
            if score > 0.2
        }
    
    def _detect_business_patterns(self, python_files: List[Path]) -> Dict[str, List[str]]:
        """Detect business logic patterns."""
        pattern_files = defaultdict(set)
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read().lower()
                
                # Check each business pattern
                for pattern_name, keywords in BUSINESS_PATTERNS.items():
                    matches = sum(1 for keyword in keywords if keyword in content)
                    if matches >= 1:  # At least one match
                        pattern_files[pattern_name].add(file_path.name)
            except Exception:
                continue
        
        # Return with limited file lists
        return {k: list(v)[:3] for k, v in pattern_files.items() if v}
    
    def _detect_external_services(self, python_files: List[Path]) -> List[str]:
        """Detect external service integrations."""
        services_found = set()
        
        for file_path in python_files:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                # Check each service pattern
                for service, patterns in EXTERNAL_SERVICE_PATTERNS.items():
                    if any(pattern in content for pattern in patterns):
                        services_found.add(service)
            except Exception:
                continue
        
        return sorted(services_found)
    
    def _generate_quick_start(self, entry_points: List[Dict], frameworks: Dict[str, float]) -> List[str]:
        """Generate quick start instructions."""
        guide = []
        
        # Entry point guidance
        if entry_points:
            primary = entry_points[0]
            guide.append(f"🚀 Primary entry point: {primary['filename']}")
            guide.append(f"   Try running: python {primary['filename']}")
        else:
            guide.append("⚠️ No clear entry point found")
            guide.append("   Look for files named main.py, app.py, or run.py")
        
        # Framework-specific instructions
        if frameworks:
            top_framework = max(frameworks.items(), key=lambda x: x[1])[0]
            guide.append(f"🔧 Detected framework: {top_framework}")
            
            framework_commands = {
                'django': "   Django: python manage.py runserver",
                'flask': "   Flask: python app.py or flask run", 
                'fastapi': "   FastAPI: uvicorn main:app --reload",
                'streamlit': "   Streamlit: streamlit run app.py"
            }
            
            if top_framework in framework_commands:
                guide.append(framework_commands[top_framework])
        
        guide.append("📦 Install dependencies: pip install -r requirements.txt")
        return guide
    
    def _generate_insights(self, frameworks: Dict[str, float], 
                          business_patterns: Dict[str, List[str]], 
                          external_services: List[str]) -> List[str]:
        """Generate project insights."""
        insights = []
        
        # Framework insights
        if frameworks:
            primary_fw = max(frameworks.items(), key=lambda x: x[1])[0]
            insights.append(f"🎯 This appears to be a {primary_fw} application")
            
            framework_purposes = {
                'django': 'web application with database models',
                'flask': 'lightweight web service or API',
                'fastapi': 'modern REST API with automatic documentation',
                'streamlit': 'data science dashboard or interactive app',
                'tkinter': 'desktop GUI application',
                'pandas': 'data analysis or processing tool',
                'pygame': 'game or interactive multimedia application'
            }
            
            if primary_fw in framework_purposes:
                insights.append(f"   Purpose: {framework_purposes[primary_fw]}")
        
        # Business logic insights
        if business_patterns:
            patterns = list(business_patterns.keys())
            insights.append(f"💼 Business logic includes: {', '.join(patterns[:3])}")
            
            if 'user_authentication' in patterns:
                insights.append("   🔒 Has user login/authentication system")
            if 'payment_processing' in patterns:
                insights.append("   💳 Processes payments or billing")
            if 'api_service' in patterns:
                insights.append("   🌐 Provides API endpoints")
        
        # External service insights
        if external_services:
            insights.append(f"🔌 External integrations: {', '.join(external_services[:3])}")
        
        if not insights:
            insights.append("🤔 Project structure suggests a Python utility or library")
        
        return insights
    
    def _empty_result(self) -> DiscoveryResult:
        """Return empty result when no files found."""
        return DiscoveryResult(
            entry_points=[],
            frameworks={},
            business_patterns={},
            external_services=[],
            quick_start_guide=["No Python files found"],
            total_files_analyzed=0,
            project_insights=["Unable to analyze project"]
        )


# Simple public API
def analyze_codebase(project_path: str) -> DiscoveryResult:
    """Analyze codebase for discovery insights."""
    discovery = CodebaseDiscovery()
    return discovery.analyze_codebase(project_path)


def create_discovery_report(result: DiscoveryResult) -> str:
    """Create formatted discovery report."""
    lines = [
        "🗺️ CODEBASE DISCOVERY REPORT", "=" * 50, f"📁 Files analyzed: {result.total_files_analyzed}",
        ""
    ]
    
    # Project insights
    if result.project_insights:
        lines.append("🎯 PROJECT INSIGHTS:")
        for insight in result.project_insights:
            lines.append(f"  {insight}")
        lines.append("")
    
    # Entry points
    if result.entry_points:
        lines.append("🚪 ENTRY POINTS:")
        for ep in result.entry_points:
            confidence = f"{ep['confidence']:.0%}"
            lines.append(f"  • {ep['filename']} ({confidence} confidence)")
        lines.append("")
    
    # Quick start
    if result.quick_start_guide:
        lines.append("🚀 QUICK START GUIDE:")
        for instruction in result.quick_start_guide:
            lines.append(f"  {instruction}")
        lines.append("")
    
    # Frameworks
    if result.frameworks:
        lines.append("🔧 FRAMEWORKS DETECTED:")
        for framework, confidence in sorted(result.frameworks.items(), key=lambda x: x[1], reverse=True):
            lines.append(f"  • {framework.title()}: {confidence:.0%}")
        lines.append("")
    
    # Business patterns
    if result.business_patterns:
        lines.append("💼 BUSINESS LOGIC:")
        for pattern, files in result.business_patterns.items():
            pattern_name = pattern.replace('_', ' ').title()
            lines.append(f"  • {pattern_name}: {len(files)} files")
        lines.append("")
    
    # External services
    if result.external_services:
        lines.append("🔌 EXTERNAL SERVICES:")
        for service in result.external_services:
            lines.append(f"  • {service.replace('_', ' ').title()}")
    
    return "\n".join(lines)


# CLI interface
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python codebase_discovery.py <project_path>")
        sys.exit(1)
    
    try:
        result = analyze_codebase(sys.argv[1])
        print(create_discovery_report(result))
        sys.exit(0)
    except Exception as e:
        print(f"Discovery failed: {e}")
        sys.exit(1)