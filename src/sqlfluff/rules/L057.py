"""Implementation of Rule L057."""

from typing import Optional

from sqlfluff.core.rules.base import BaseRule, LintResult, RuleContext
from sqlfluff.core.rules.doc_decorators import (
    document_configuration,
)
from sqlfluff.rules.L014 import identifiers_policy_applicable


@document_configuration
class Rule_L057(BaseRule):
    """Do not use special characters in identifiers.

    | **Anti-pattern**
    | Using special characters within identifiers when creating or aliasing objects.

    .. code-block:: sql

        CREATE TABLE DBO.ColumnNames
        (
            [Internal Space] INT,
            [Greater>Than] INT,
            [Less<Than] INT,
            Number# INT
        )

    | **Best practice**
    | Identifiers should include only alphanumerics and underscores.

    .. code-block:: sql

        CREATE TABLE DBO.ColumnNames
        (
            [Internal_Space] INT,
            [GreaterThan] INT,
            [LessThan] INT,
            NumberVal INT
        )

    """

    config_keywords = [
        "quoted_identifiers_policy",
        "unquoted_identifiers_policy",
        "allow_space_in_identifier",
    ]

    def _eval(self, context: RuleContext) -> Optional[LintResult]:
        """Do not use special characters in object names."""
        # Config type hints
        self.quoted_identifiers_policy: str
        self.unquoted_identifiers_policy: str
        self.allow_space_in_identifier: bool

        # Exit early if not a single identifier.
        if context.segment.name not in ("naked_identifier", "quoted_identifier"):
            return None

        if context.segment.name == "naked_identifier":
            # Evaluate unquoted identifiers.
            if identifiers_policy_applicable(
                self.unquoted_identifiers_policy, context.parent_stack
            ) and not (context.segment.raw.replace("_", "").isalnum()):
                return LintResult(anchor=context.segment)
        else:
            # Evaluate quoted identifiers.

            # Strip the quotes.
            identifier = context.segment.raw[1:-1]

            # BigQuery table references are quoted in back ticks so allow dots
            #
            # It also allows a star at the end of table_references for wildcards
            # (https://cloud.google.com/bigquery/docs/querying-wildcard-tables)
            #
            # Strip both out before testing the identifier
            if (
                context.dialect.name in ["bigquery"]
                and context.parent_stack
                and context.parent_stack[-1].name == "TableReferenceSegment"
            ):
                if identifier[-1] == "*":
                    identifier = identifier[:-1]
                identifier = identifier.replace(".", "")

            if identifiers_policy_applicable(
                self.quoted_identifiers_policy, context.parent_stack
            ) and not (
                identifier.replace("_", "").isalnum()
                or (
                    self.allow_space_in_identifier
                    and identifier.replace("_", "").replace(" ", "").isalnum()
                )
            ):
                return LintResult(anchor=context.segment)

        return None
