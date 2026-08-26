from __future__ import annotations

import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "validate-skill.yml"


class WorkflowPolicyTests(unittest.TestCase):
    def test_validation_workflow_cancels_redundant_runs(self) -> None:
        workflow = WORKFLOW.read_text(encoding="utf-8")
        self.assertRegex(
            workflow,
            re.compile(
                r"^concurrency:\n"
                r"  group: \$\{\{ github\.workflow \}\}-\$\{\{ github\.ref \}\}\n"
                r"  cancel-in-progress: true$",
                re.MULTILINE,
            ),
        )


if __name__ == "__main__":
    unittest.main()
