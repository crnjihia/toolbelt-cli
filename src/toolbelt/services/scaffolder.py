"""Project scaffolding service using Jinja2 templates."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import jinja2

TEMPLATE_ROOT = Path(__file__).parent.parent / "templates"


class Scaffolder:
    """Render project templates and write files to disk."""

    def __init__(
        self,
        project_type: str,
        project_name: str,
        author: str,
        license: str,
        include_ci: bool,
        include_docker: bool,
        destination: Path,
    ) -> None:
        self.project_type = project_type.lower()
        self.project_name = project_name
        self.author = author
        self.license = license
        self.include_ci = include_ci
        self.include_docker = include_docker
        self.destination = destination

        tmpl_dir = TEMPLATE_ROOT / self.project_type
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(str(tmpl_dir)),
            autoescape=False,
            keep_trailing_newline=True,
        )
        self.context: dict[str, Any] = {
            "project_name": project_name,
            "author": author,
            "license": license,
            "include_ci": include_ci,
            "include_docker": include_docker,
        }

    def _render_template(self, template_posix_path: str) -> str:
        template = self.env.get_template(template_posix_path)
        return template.render(**self.context)

    def _write_file(self, relative_path: Path, content: str) -> None:
        target = self.destination / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    def run(self) -> None:
        """Run the scaffolding process."""
        tmpl_root = TEMPLATE_ROOT / self.project_type
        if not tmpl_root.exists():
            raise FileNotFoundError(f"Template directory not found: {tmpl_root}")

        for root, _, files in os.walk(tmpl_root):
            for fname in files:
                full_src = Path(root) / fname
                rel_src = full_src.relative_to(tmpl_root)
                rel_posix = rel_src.as_posix()

                # Filter optional files
                if "ci.yml" in rel_posix and not self.include_ci:
                    continue
                if "Dockerfile" in rel_posix and not self.include_docker:
                    continue
                if "LICENSE" in rel_posix and self.license.lower() == "none":
                    continue

                # Render content
                if fname.endswith(".j2"):
                    content = self._render_template(rel_posix)
                else:
                    content = full_src.read_text(encoding="utf-8")

                # Resolve path placeholders like {{project_name}}
                rendered_rel_path = rel_posix.replace(
                    "{{project_name}}", self.project_name
                )
                if rendered_rel_path.endswith(".j2"):
                    rendered_rel_path = rendered_rel_path[:-3]

                self._write_file(Path(rendered_rel_path), content)
