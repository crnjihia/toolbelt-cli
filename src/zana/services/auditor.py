"""Repository auditing service."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from rich.console import Console
from rich.prompt import Confirm, Prompt

MIT_TEMPLATE = """MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

APACHE_TEMPLATE = """                                 Apache License
                           Version 2.0, January 2004
                        http://www.apache.org/licenses/

   Copyright (c) {year} {author}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

DEFAULT_GITIGNORE = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
.env
.venv
env/
venv/
ENV/

# Node
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Java
target/
*.class

# IDE
.idea/
.vscode/
*.swp
"""


class AuditResult:
    """Individual audit check result."""

    def __init__(self, name: str, passed: bool, details: str = "") -> None:
        self.name = name
        self.passed = passed
        self.details = details

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "status": "✅" if self.passed else "❌",
            "details": self.details,
        }


class Auditor:
    """Inspects a repository path for standards, files, and conventions."""

    def __init__(self, repo_path: Path, console: Console | None = None) -> None:
        self.repo_path = repo_path.resolve()
        self.console = console or Console()

    def _file_content(self, relative_path: str) -> str | None:
        target = self.repo_path / relative_path
        if target.is_file():
            try:
                return target.read_text(encoding="utf-8")
            except Exception:
                return None
        return None

    def fix_missing(self, interactive: bool = True) -> None:
        """Prompt to fix missing .gitignore and LICENSE."""
        gitignore_path = self.repo_path / ".gitignore"
        license_path = self.repo_path / "LICENSE"

        if not gitignore_path.exists():
            create_gi = True
            if interactive:
                try:
                    create_gi = Confirm.ask(
                        "Missing .gitignore. Create default .gitignore?", default=True
                    )
                except Exception:
                    create_gi = True
            if create_gi:
                gitignore_path.write_text(DEFAULT_GITIGNORE, encoding="utf-8")
                self.console.print("[green]Created .gitignore[/green]")

        if not license_path.exists():
            create_lic = True
            choice = "MIT"
            if interactive:
                try:
                    create_lic = Confirm.ask(
                        "Missing LICENSE file. Create one?", default=True
                    )
                    if create_lic:
                        choice = Prompt.ask(
                            "Select license",
                            choices=["MIT", "Apache-2.0"],
                            default="MIT",
                        )
                except Exception:
                    create_lic = True
                    choice = "MIT"
            if create_lic:
                template = APACHE_TEMPLATE if choice == "Apache-2.0" else MIT_TEMPLATE
                content = template.format(year="2026", author="Author")
                license_path.write_text(content, encoding="utf-8")
                self.console.print(f"[green]Created LICENSE ({choice})[/green]")

    def run(self, fix: bool = False, interactive: bool = True) -> list[AuditResult]:
        """Run all audit checks."""
        if fix:
            self.fix_missing(interactive=interactive)

        results: list[AuditResult] = []

        # 1. README.md exists
        readme_content = self._file_content("README.md")
        if readme_content is not None:
            line_count = len(readme_content.splitlines())
            results.append(AuditResult("README.md exists", True, f"{line_count} lines"))
        else:
            results.append(AuditResult("README.md exists", False, "file missing"))

        # 2. README has Install
        if readme_content and re.search(
            r"##\s+Install(ation)?", readme_content, re.IGNORECASE
        ):
            results.append(
                AuditResult("README has Install", True, 'found "## Installation"')
            )
        else:
            results.append(
                AuditResult(
                    "README has Install", False, 'missing "## Installation" section'
                )
            )

        # 3. README has Usage
        if readme_content and re.search(r"##\s+Usage", readme_content, re.IGNORECASE):
            results.append(AuditResult("README has Usage", True, 'found "## Usage"'))
        else:
            results.append(
                AuditResult("README has Usage", False, 'missing "## Usage" section')
            )

        # 4. README has License
        if readme_content and re.search(r"##\s+License", readme_content, re.IGNORECASE):
            results.append(
                AuditResult("README has License", True, 'found "## License"')
            )
        else:
            results.append(
                AuditResult("README has License", False, "no License section")
            )

        # 5. LICENSE file
        license_content = self._file_content("LICENSE")
        if license_content is not None:
            if "Apache" in license_content:
                lic_type = "Apache-2.0"
            elif "MIT" in license_content:
                lic_type = "MIT"
            else:
                first_line = (
                    license_content.strip().splitlines()[0][:20]
                    if license_content.strip()
                    else "Found"
                )
                lic_type = first_line
            results.append(AuditResult("LICENSE file", True, lic_type))
        else:
            results.append(AuditResult("LICENSE file", False, "missing"))

        # 6. .gitignore exists
        gitignore_content = self._file_content(".gitignore")
        if gitignore_content is not None:
            entries = [
                line
                for line in gitignore_content.splitlines()
                if line.strip() and not line.strip().startswith("#")
            ]
            results.append(
                AuditResult(".gitignore exists", True, f"{len(entries)} entries")
            )
        else:
            results.append(AuditResult(".gitignore exists", False, "file missing"))

        # 7. .gitignore has __pycache__
        if gitignore_content is not None and "__pycache__" in gitignore_content:
            results.append(AuditResult(".gitignore has __pycache__", True, ""))
        else:
            results.append(
                AuditResult(
                    ".gitignore has __pycache__", False, 'missing "__pycache__"'
                )
            )

        # 8. Tests directory
        tests_dir = self.repo_path / "tests"
        test_dir = self.repo_path / "test"
        src_test_dir = self.repo_path / "src" / "test"
        has_tests = (
            (tests_dir.is_dir() and any(tests_dir.iterdir()))
            or (test_dir.is_dir() and any(test_dir.iterdir()))
            or (src_test_dir.is_dir() and any(src_test_dir.iterdir()))
        )
        if has_tests:
            results.append(AuditResult("Tests directory", True, "tests/ found"))
        else:
            results.append(AuditResult("Tests directory", False, "missing"))

        # 9. CI config
        ci_yml = self.repo_path / ".github" / "workflows" / "ci.yml"
        ci_yaml = self.repo_path / ".github" / "workflows" / "ci.yaml"
        workflows_dir = self.repo_path / ".github" / "workflows"
        has_ci = (
            ci_yml.exists()
            or ci_yaml.exists()
            or (workflows_dir.is_dir() and any(workflows_dir.glob("*.y*ml")))
        )
        if has_ci:
            results.append(AuditResult("CI config", True, ".github/workflows/ci.yml"))
        else:
            results.append(AuditResult("CI config", False, "missing"))

        # 10. pyproject.toml
        pyproject = self.repo_path / "pyproject.toml"
        if pyproject.is_file():
            results.append(AuditResult("pyproject.toml", True, ""))
        else:
            results.append(AuditResult("pyproject.toml", False, "missing"))

        return results
