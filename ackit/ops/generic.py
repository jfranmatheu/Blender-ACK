from ..ackit import types, props, Poll, Property
from ..ackit.utils.operator import OpsReturn


@Poll.ACTIVE_OBJECT.ANY
class GenericOperator(types.Operator):
    new_name = Property.STRING(name="Object Name")

    def invoke(self, context, event) -> None:
        context.active_object.location.z = self.new_name
        self.report({'INFO'}, f"New Name {self.new_name}")
