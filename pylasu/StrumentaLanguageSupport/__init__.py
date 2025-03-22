from . import StrumentaLanguageSupport
from .StrumentaLanguageSupport import (ASTNode, BigDecimal, BigInteger,
                                       Destination, EntityDeclaration,
                                       Expression, Issue, IssueSeverity,
                                       IssueType, LocalDate, LocalDateTime,
                                       LocalTime, Named, NodeDestination,
                                       Origin, Point, Position, PossiblyNamed,
                                       ReferenceByName, Result, Statement,
                                       TextFileDestination, eClass,
                                       eClassifiers)

__all__ = [
    "BigDecimal",
    "BigInteger",
    "LocalDate",
    "LocalTime",
    "LocalDateTime",
    "Point",
    "Position",
    "Origin",
    "Destination",
    "NodeDestination",
    "TextFileDestination",
    "ASTNode",
    "Statement",
    "Expression",
    "EntityDeclaration",
    "IssueType",
    "IssueSeverity",
    "Issue",
    "PossiblyNamed",
    "Named",
    "ReferenceByName",
    "Result",
]

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
ReferenceByName.referenced.eType = ASTNode
#  TODO eGenericType not supported
Result.root.eType = ASTNode
Result.issues.eType = Issue

otherClassifiers = [BigDecimal, BigInteger, IssueType, IssueSeverity]

for classif in otherClassifiers:
    eClassifiers[classif.name] = classif
    classif.ePackage = eClass

for subpack in eSubpackages:
    eClass.eSubpackages.append(subpack.eClass)
