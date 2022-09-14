from dataclasses import dataclass, field
from typing import List

from pyecore.resources import Resource

from pylasu import StrumentaLanguageSupport as starlasu
from pylasu.emf.model import to_eobject
from pylasu.playground.transpilation_trace_ecore import TranspilationTrace as ETranspilationTrace
from pylasu.validation.validation import Result, Issue


@dataclass
class TranspilationTrace:
    original_code: str
    source_result: Result
    target_result: Result
    generated_code: str
    issues: List[Issue] = field(default_factory=list)

    def to_eobject(self, resource: Resource):
        mappings = {}
        return ETranspilationTrace(
            original_code=self.original_code,
            source_result=starlasu.Result(root=to_eobject(self.source_result.root, resource, mappings)),
            target_result=starlasu.Result(root=to_eobject(self.target_result.root, resource, mappings)),
            generated_code=self.generated_code
        )
