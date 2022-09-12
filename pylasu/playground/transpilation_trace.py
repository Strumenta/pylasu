from pyecore.ecore import *

from pylasu.StrumentaLanguageSupport import Result, Issue

TRANSPILATION_METAMODEL = EPackage(
    name="StrumentaLanguageSupportTranspilation", nsURI="https://strumenta.com/kolasu/transpilation/v1")


class TranspilationTrace(EObject, metaclass=MetaEClass):
    original_code: EAttribute(name="originalCode", eType=EString)
    source_result = EReference(name="sourceResult", containment=True, eType=Result)
    target_result = EReference(name="targetResult", containment=True, eType=Result)
    generated_code: EAttribute(name="generatedCode", eType=EString)
    issues = EReference(containment=True, eType=Issue, upper=-1)

    def __init__(self, *, original_code=None, source_result=None, target_result=None, generated_code=None, issues=None):
        super().__init__()
        if original_code is not None:
            self.original_code = original_code
        if source_result is not None:
            self.source_result = source_result
        if target_result is not None:
            self.target_result = target_result
        if generated_code is not None:
            self.generated_code = generated_code
        if issues:
            self.issues.extend(issues)


TRANSPILATION_METAMODEL.eContents.append(TranspilationTrace)
