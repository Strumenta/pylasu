"""Definition of meta model 'StrumentaLanguageSupport'."""
from functools import partial
import pyecore.ecore as Ecore
from pyecore.ecore import *


name = 'StrumentaLanguageSupport'
nsURI = 'https://strumenta.com/kolasu/v2'
nsPrefix = ''

eClass = EPackage(name=name, nsURI=nsURI, nsPrefix=nsPrefix)

eClassifiers = {}
getEClassifier = partial(Ecore.getEClassifier, searchspace=eClassifiers)
IssueType = EEnum('IssueType', literals=['LEXICAL', 'SYNTACTIC', 'SEMANTIC'])

IssueSeverity = EEnum('IssueSeverity', literals=['ERROR', 'WARNING', 'INFO'])


BigDecimal = EDataType('BigDecimal', instanceClassName='java.math.BigDecimal')

BigInteger = EDataType('BigInteger', instanceClassName='java.math.BigInteger')


class LocalDate(EObject, metaclass=MetaEClass):

    year = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    month = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    dayOfMonth = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)

    def __init__(self, *, year=None, month=None, dayOfMonth=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if year is not None:
            self.year = year

        if month is not None:
            self.month = month

        if dayOfMonth is not None:
            self.dayOfMonth = dayOfMonth


class LocalTime(EObject, metaclass=MetaEClass):

    hour = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    minute = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    second = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    nanosecond = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)

    def __init__(self, *, hour=None, minute=None, second=None, nanosecond=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if hour is not None:
            self.hour = hour

        if minute is not None:
            self.minute = minute

        if second is not None:
            self.second = second

        if nanosecond is not None:
            self.nanosecond = nanosecond


class LocalDateTime(EObject, metaclass=MetaEClass):

    date = EReference(ordered=True, unique=True, containment=True, derived=False)
    time = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, date=None, time=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if date is not None:
            self.date = date

        if time is not None:
            self.time = time


class Point(EObject, metaclass=MetaEClass):

    line = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)
    column = EAttribute(eType=EInt, unique=True, derived=False, changeable=True)

    def __init__(self, *, line=None, column=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if line is not None:
            self.line = line

        if column is not None:
            self.column = column


class Position(EObject, metaclass=MetaEClass):

    start = EReference(ordered=True, unique=True, containment=True, derived=False)
    end = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, start=None, end=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if start is not None:
            self.start = start

        if end is not None:
            self.end = end


@abstract
class Origin(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


@abstract
class Destination(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Statement(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Expression(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class EntityDeclaration(EObject, metaclass=MetaEClass):

    def __init__(self):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()


class Issue(EObject, metaclass=MetaEClass):

    type = EAttribute(eType=IssueType, unique=True, derived=False, changeable=True)
    message = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    severity = EAttribute(eType=IssueSeverity, unique=True, derived=False, changeable=True)
    position = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, type=None, message=None, severity=None, position=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if type is not None:
            self.type = type

        if message is not None:
            self.message = message

        if severity is not None:
            self.severity = severity

        if position is not None:
            self.position = position


class PossiblyNamed(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name


class ReferenceByName(EObject, metaclass=MetaEClass):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)
    referenced = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, name=None, referenced=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if name is not None:
            self.name = name

        if referenced is not None:
            self.referenced = referenced


class Result(EObject, metaclass=MetaEClass):

    root = EReference(ordered=True, unique=True, containment=True, derived=False)
    issues = EReference(ordered=True, unique=True, containment=True, derived=False, upper=-1)

    def __init__(self, *, root=None, issues=None):
        # if kwargs:
        #    raise AttributeError('unexpected arguments: {}'.format(kwargs))

        super().__init__()

        if root is not None:
            self.root = root

        if issues:
            self.issues.extend(issues)


class NodeDestination(Destination):

    node = EReference(ordered=True, unique=True, containment=False, derived=False)

    def __init__(self, *, node=None, **kwargs):

        super().__init__(**kwargs)

        if node is not None:
            self.node = node


class TextFileDestination(Destination):

    position = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, position=None, **kwargs):

        super().__init__(**kwargs)

        if position is not None:
            self.position = position


@abstract
class ASTNode(Origin):

    position = EReference(ordered=True, unique=True, containment=True, derived=False)
    origin = EReference(ordered=True, unique=True, containment=False, derived=False)
    destination = EReference(ordered=True, unique=True, containment=True, derived=False)

    def __init__(self, *, position=None, origin=None, destination=None, **kwargs):

        super().__init__(**kwargs)

        if position is not None:
            self.position = position

        if origin is not None:
            self.origin = origin

        if destination is not None:
            self.destination = destination


class Named(PossiblyNamed):

    name = EAttribute(eType=EString, unique=True, derived=False, changeable=True)

    def __init__(self, *, name=None, **kwargs):

        super().__init__(**kwargs)

        if name is not None:
            self.name = name
