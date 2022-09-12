
from .StrumentaLanguageSupport import getEClassifier, eClassifiers
from .StrumentaLanguageSupport import name, nsURI, nsPrefix, eClass
from .StrumentaLanguageSupport import BigDecimal, BigInteger, LocalDate, LocalTime, LocalDateTime, Point, Position, Origin, Destination, NodeDestination, TextFileDestination, ASTNode, Statement, Expression, EntityDeclaration, IssueType, IssueSeverity, Issue, PossiblyNamed, Named, ReferenceByName, Result


from . import StrumentaLanguageSupport

__all__ = ['BigDecimal', 'BigInteger', 'LocalDate', 'LocalTime', 'LocalDateTime', 'Point', 'Position', 'Origin', 'Destination', 'NodeDestination', 'TextFileDestination',
           'ASTNode', 'Statement', 'Expression', 'EntityDeclaration', 'IssueType', 'IssueSeverity', 'Issue', 'PossiblyNamed', 'Named', 'ReferenceByName', 'Result']

eSubpackages = []
eSuperPackage = None
StrumentaLanguageSupport.eSubpackages = eSubpackages
StrumentaLanguageSupport.eSuperPackage = eSuperPackage

LocalDateTime.date.eType = LocalDate
LocalDateTime.time.eType = LocalTime
Position.start.eType = Point
Position.end.eType = Point
NodeDestination.node.eType = ASTNode
TextFileDestination.position.eType = Position
ASTNode.position.eType = Position
ASTNode.origin.eType = Origin
ASTNode.destination.eType = Destination
Issue.position.eType = Position
#  TODO eGenericType not supported ReferenceByName.referenced.eType =
#  TODO eGenericType not supported
Result.root.eType = ASTNode
Result.issues.eType = Issue

otherClassifiers = [BigDecimal, BigInteger, IssueType, IssueSeverity]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for classif in eClassifiers.values():
    eClass.eClassifiers.append(classif.eClass)

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
