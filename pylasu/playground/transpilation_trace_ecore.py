from io import BytesIO, IOBase

from pyecore.ecore import EAttribute, EObject, EReference, EString, MetaEClass
from pyecore.resources import URI, ResourceSet
from pyecore.resources.json import JsonResource as BaseJsonResource

from pylasu import StrumentaLanguageSupport as starlasu

nsURI = "https://strumenta.com/kolasu/transpilation/v1"
name = "StrumentaLanguageSupportTranspilation"


class JsonResource(BaseJsonResource):

    def open_out_stream(self, other=None):
        if isinstance(other, IOBase):
            return other
        else:
            return super().open_out_stream(other)


class TranspilationTrace(EObject, metaclass=MetaEClass):
    # Note: we use camelCase here because Pyecore's JSON serialization doesn't handle having different names for
    # Python attributes and their corresponding Ecore structural features.
    originalCode = EAttribute(eType=EString)
    sourceResult = EReference(containment=True, eType=starlasu.Result)
    targetResult = EReference(containment=True, eType=starlasu.Result)
    generatedCode = EAttribute(eType=EString)
    issues = EReference(containment=True, eType=starlasu.Issue, upper=-1)

    def __init__(
        self,
        *,
        original_code=None,
        source_result=None,
        target_result=None,
        generated_code=None,
        issues=None,
    ):
        super().__init__()
        if original_code is not None:
            self.originalCode = original_code
        if source_result is not None:
            self.sourceResult = source_result
        if target_result is not None:
            self.targetResult = target_result
        if generated_code is not None:
            self.generatedCode = generated_code
        if issues:
            self.issues.extend(issues)

    def save_as_json(self, name, *packages):
        rset = ResourceSet()
        rset.resource_factory["json"] = JsonResource
        resource = rset.create_resource(URI(name))
        for pkg in packages:
            package_resource = rset.create_resource(URI(pkg.nsURI))
            package_resource.contents.append(pkg)
        resource.contents.append(self)
        with BytesIO() as out:
            resource.save(out)
            return out.getvalue().decode("utf-8")
