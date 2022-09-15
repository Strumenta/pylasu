from dataclasses import dataclass, field
from io import BytesIO
from typing import List

from pyecore.resources import Resource, ResourceSet, URI

from pylasu import StrumentaLanguageSupport as starlasu
from pylasu.emf.model import to_eobject
from pylasu.playground.transpilation_trace_ecore import TranspilationTrace as ETranspilationTrace, JsonResource
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

    def save_as_json(self, name, *packages):
        rset = ResourceSet()
        rset.resource_factory['json'] = JsonResource
        resource = rset.create_resource(URI(name))
        for pkg in packages:
            package_resource = rset.create_resource(URI(pkg.nsURI))
            package_resource.contents.append(pkg)
        resource.contents.append(self.to_eobject(resource))
        with BytesIO() as out:
            resource.save(out)
            return out.getvalue().decode('utf-8')
