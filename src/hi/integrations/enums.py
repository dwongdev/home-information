from typing import Dict, FrozenSet, Optional

from hi.apps.attribute.enums import AttributeValueType
from hi.apps.common.enums import LabeledEnum


class IntegrationCapability( LabeledEnum ):

    CONNECT = ( 'Connect', 'Live mirror of an upstream system.' )
    IMPORT = ( 'Import', 'One-shot pull of upstream items into HI.' )
    ATTRIBUTE_REFERENCE = (
        'Attribute Reference',
        'Search-and-attach external documents as Entity/Location attributes.',
    )


ALL_CAPABILITIES = frozenset( IntegrationCapability )


class IntegrationDisableMode( LabeledEnum ):

    SAFE = ( 'Delete Safe',
             'Delete entities without user data; preserve those with user data' )
    ALL  = ( 'Delete All',
             'Hard-delete all entities regardless of user data' )

    @classmethod
    def default(cls):
        return cls.SAFE


class IntegrationAttributeType( LabeledEnum ):
    """Base for per-integration attribute-type enums."""

    def __init__( self,
                  label             : str,
                  description       : str,
                  value_type        : AttributeValueType,
                  value_range_dict  : Dict[ str, str ],
                  is_editable       : bool,
                  is_required       : bool,
                  initial_value     : str                                              = '',
                  capabilities      : Optional[ FrozenSet[ IntegrationCapability ] ]   = None ):
        super().__init__( label, description )
        self.value_type = value_type
        self.value_range_dict = value_range_dict
        self.is_editable = is_editable
        self.is_required = is_required
        self.initial_value = initial_value
        self.capabilities = capabilities if capabilities is not None else ALL_CAPABILITIES
        return
