import os
import subprocess
from typing import Optional, Tuple
from .types import Proposal, EdgeDef
import uuid


class TheBrain:
    """
    The Logic Core. Analyzes diffs and proposes relationships.
    Uses LLM to understand intent behind code changes.
    """

    def __init__(self, config: dict):
        self.config = config
        self.provider = config.get('brain', {}).get('provider', 'mock')
        self.api_key = os.environ.get('ANTHROPIC_API_KEY') or os.environ.get('OPENAI_API_KEY')

    def get_diff(self, file_path: str) -> Optional[str]:
        """Get the git diff for a file."""
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", file_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(file_path) or "."
            )
            if result.stdout.strip():
                return result.stdout

            # Try unstaged diff
            result = subprocess.run(
                ["git", "diff", file_path],
                capture_output=True,
                text=True,
                cwd=os.path.dirname(file_path) or "."
            )
            return result.stdout if result.stdout.strip() else None
        except Exception:
            return None

    def analyze_intent(self, file_path: str, diff: Optional[str] = None) -> Proposal:
        """
        Analyze a code change and propose a relationship.
        Returns a Proposal for human confirmation.
        """
        if diff is None:
            diff = self.get_diff(file_path)

        work_unit_id = str(uuid.uuid4())[:8]
        filename = os.path.basename(file_path)

        if self.provider == 'mock' or not self.api_key:
            return self._mock_analysis(filename, diff, work_unit_id)
        elif self.provider == 'anthropic':
            return self._anthropic_analysis(filename, diff, work_unit_id)
        else:
            return self._mock_analysis(filename, diff, work_unit_id)

    def _mock_analysis(self, filename: str, diff: Optional[str], work_unit_id: str) -> Proposal:
        """Mock LLM analysis for testing without API."""
        # Simple heuristic-based intent detection
        intent = self._guess_intent(filename, diff)

        return Proposal(
            work_unit_id=work_unit_id,
            confidence=0.7,
            edge=EdgeDef(
                source=filename,
                target=intent,
                edge_type="implements"
            ),
            rationale=f"Detected modification in {filename}. This appears to be related to: {intent}",
            diff_summary=self._summarize_diff(diff) if diff else "No diff available"
        )

    def _guess_intent(self, filename: str, diff: Optional[str]) -> str:
        """Simple heuristic to guess intent from filename and diff."""
        filename_lower = filename.lower()

        # Check filename patterns
        if "test" in filename_lower:
            return "Testing & Quality"
        elif "config" in filename_lower or "yaml" in filename_lower:
            return "Configuration"
        elif "ui" in filename_lower or "voice" in filename_lower or "view" in filename_lower:
            return "User Interface"
        elif "api" in filename_lower or "client" in filename_lower:
            return "API Integration"
        elif "model" in filename_lower or "type" in filename_lower:
            return "Data Modeling"
        elif "util" in filename_lower or "helper" in filename_lower:
            return "Utilities"

        # Check diff content if available
        if diff:
            diff_lower = diff.lower()
            if "fix" in diff_lower or "bug" in diff_lower:
                return "Bug Fix"
            elif "add" in diff_lower or "new" in diff_lower:
                return "New Feature"
            elif "refactor" in diff_lower or "clean" in diff_lower:
                return "Refactoring"
            elif "import" in diff_lower:
                return "Dependency Update"

        return "General Development"

    def _summarize_diff(self, diff: str) -> str:
        """Create a brief summary of the diff."""
        lines = diff.split('\n')
        additions = sum(1 for l in lines if l.startswith('+') and not l.startswith('+++'))
        deletions = sum(1 for l in lines if l.startswith('-') and not l.startswith('---'))
        return f"+{additions}/-{deletions} lines changed"

    def _anthropic_analysis(self, filename: str, diff: Optional[str], work_unit_id: str) -> Proposal:
        """Use Claude API for intent analysis."""
        try:
            import anthropic

            client = anthropic.Anthropic(api_key=self.api_key)

            prompt = f"""Analyze this code change and determine the developer's intent.

File: {filename}
Diff:
{diff or 'No diff available - new file or unstaged changes'}

Respond in this exact format:
INTENT: [2-4 word description of the intent]
CONFIDENCE: [0.0-1.0]
RATIONALE: [One sentence explanation]
EDGE_TYPE: [implements|modifies|deprecates|relates_to]"""

            message = client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=200,
                messages=[{"role": "user", "content": prompt}]
            )

            response = message.content[0].text
            return self._parse_llm_response(filename, response, work_unit_id, diff)

        except Exception as e:
            # Fallback to mock if API fails
            return self._mock_analysis(filename, diff, work_unit_id)

    def _parse_llm_response(self, filename: str, response: str, work_unit_id: str, diff: Optional[str]) -> Proposal:
        """Parse LLM response into a Proposal."""
        lines = response.strip().split('\n')

        intent = "General Development"
        confidence = 0.7
        rationale = "Analysis performed by AI"
        edge_type = "relates_to"

        for line in lines:
            if line.startswith("INTENT:"):
                intent = line.replace("INTENT:", "").strip()
            elif line.startswith("CONFIDENCE:"):
                try:
                    confidence = float(line.replace("CONFIDENCE:", "").strip())
                except ValueError:
                    pass
            elif line.startswith("RATIONALE:"):
                rationale = line.replace("RATIONALE:", "").strip()
            elif line.startswith("EDGE_TYPE:"):
                edge_type = line.replace("EDGE_TYPE:", "").strip().lower()
                if edge_type not in ["implements", "modifies", "deprecates", "relates_to"]:
                    edge_type = "relates_to"

        return Proposal(
            work_unit_id=work_unit_id,
            confidence=confidence,
            edge=EdgeDef(
                source=filename,
                target=intent,
                edge_type=edge_type
            ),
            rationale=rationale,
            diff_summary=self._summarize_diff(diff) if diff else "No diff available"
        )
