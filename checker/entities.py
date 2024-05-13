from dataclasses import dataclass, field
from typing import List
import uuid

def generate_uid():
    return str(uuid.uuid4())

def addressify(address : list):
    return ', '.join([word for word in address if word])

@dataclass(frozen=True)
class SanctionedEntity:
    """Sanctioned entities are an abstract class for people, companies, and addresses
    The fulltext property is used for searching purposes, and some 'identifiers' additional to names 
    and addresses are added depending upon the relevant authority.
    """
    source: str
    names: List[str] = field(default_factory=list)
    address: List[str] = field(default_factory=list)
    uid: str = field(default_factory=generate_uid)
    description: str = 'Unknown description'

    COLUMN_TITLES = ['Source', 'Names', 'Address', 'Identifier']

    def row_repr(self):
        return [self.source, ' '.join(self.names), addressify(self.address), 'Unknown']

    def serialize(self):
        """Serialize attributes for return over JSON"""
        return {
            'source': self.source,
            'names': self.names,
            'address': self.address,
            'fulltext': self.fulltext,
            'uid': self.uid,
            'description': self.description,
        }
    
    @classmethod
    def filter_fields(cls, data):
        """Filter a dict to only include SanctionedEntity fields"""
        return {
            'source': data['source'],
            'names': data['names'],
            'address': data['address'],
            'uid': data['uid'],
            'description': data['description'],
        }
    
    @classmethod
    def deserialize(cls, data):        
        match data['source']:
            case 'UK':
                return UKSanctionedEntity.deserialize(data)
            case 'EU':
                return EUSanctionedEntity.deserialize(data)
            case 'AU':
                return AUSanctionedEntity.deserialize(data)
            case 'US':
                return USSanctionedEntity.deserialize(data)
            case 'UN':
                return UNSanctionedEntity.deserialize(data)
            case _:
                return cls(**data) 
    
    @property
    def fulltext(self):
        return ' '.join([word for word in self.names + self.address if word])

@dataclass(frozen=True)
class UKSanctionedEntity(SanctionedEntity):
    group_id : str = 'Unknown UK Group ID'

    def row_repr(self):
        base = super().row_repr()
        base[-1] = f"UK Group ID: {self.group_id}"
        return base
    
    def serialize(self):
        """Serialize attributes for return over JSON"""
        return {
            **super().serialize(),
            'group_id': self.group_id,
        }
    
    @classmethod
    def deserialize(cls, data):
        return UKSanctionedEntity(
            **super().filter_fields(data),
            group_id=data['group_id'],
        )
    
    
@dataclass(frozen=True)
class EUSanctionedEntity(SanctionedEntity):
    """Contains extra identifiers for IMO number"""
    reference : str = 'Unknown EU Reference'
    url : str = 'Unknown URL'
    identifiers: List[str] = field(default_factory=list)

    def row_repr(self):
        base = super().row_repr()
        base[-1] = f"EU Reference: {self.reference}"
        return base

    def serialize(self):
        """Serialize attributes for return over JSON"""
        return {
            **super().serialize(),
            'reference': self.reference,
            'url': self.url,
            'identifiers': self.identifiers,
        }
    
    @classmethod
    def deserialize(cls, data):
        return EUSanctionedEntity(
            **super().filter_fields(data),
            reference=data['reference'],
            url=data['url'],
            identifiers=data['identifiers'],
        )
    
    @property
    def fulltext(self):
        return ' '.join([word for word in self.names + self.address + self.identifiers if word])

@dataclass(frozen=True)
class USSanctionedEntity(SanctionedEntity):
    lookup_id: str = 'Unknown US LookupID'
    identifiers: List[str] = field(default_factory=list)

    def row_repr(self):
        base = super().row_repr()
        base[-1] = f"US Lookup ID: {self.lookup_id}"
        return base

    def serialize(self):
        """Serialize attributes for return over JSON"""
        return {
            **super().serialize(),
            'lookup_id': self.lookup_id,
            'identifiers': self.identifiers,
        }
    
    @classmethod
    def deserialize(cls, data):
        return USSanctionedEntity(
            **super().filter_fields(data),
            lookup_id=data['lookup_id'],
            identifiers=data['identifiers'],
        )
    
    @property
    def fulltext(self):
        return ' '.join([word for word in self.names + self.address + self.identifiers if word])
    
@dataclass(frozen=True)
class AUSanctionedEntity(SanctionedEntity):
    reference: str = 'Unknown AU Reference'
    identifiers: List[str] = field(default_factory=list)

    def row_repr(self):
        base = super().row_repr()
        base[-1] = f"AU Reference: {self.reference}"
        return base

    def serialize(self):
        """Serialize attributes for return over JSON"""
        return {
            **super().serialize(),
            'reference': self.reference,
            'identifiers': self.identifiers,
        }
    
    @classmethod
    def deserialize(cls, data):
        return AUSanctionedEntity(
            **super().filter_fields(data),
            reference=data['reference'],
            identifiers=data['identifiers'],
        )
    
    @property
    def fulltext(self):
        return ' '.join([word for word in self.names + self.address + self.identifiers if word])
    
@dataclass(frozen=True)
class UNSanctionedEntity(SanctionedEntity):
    reference : str = 'Unknown UN Reference'
    aliases: List[str] = field(default_factory=list)
    identifiers: List[str] = field(default_factory=list)

    def row_repr(self):
        base = super().row_repr()
        base[-1] = f"UN Reference: {self.reference}"
        return base

    def serialize(self):
        """Serialize attributes for return over JSON"""
        return {
            **super().serialize(),
            'reference': self.reference,
            'aliases': self.aliases,
            'identifiers': self.identifiers,
        }
    
    @classmethod
    def deserialize(cls, data):
        return UNSanctionedEntity(
            **super().filter_fields(data),
            reference=data['reference'],
            aliases=data['aliases'],
            identifiers=data['identifiers'],
        )
    
    @property
    def fulltext(self):
        return ' '.join([word for word in self.names + self.address + self.aliases + self.identifiers if word])