from ...ackit import ACK
from ...ackit.enums.operator import OpsReturn


@ACK.Poll.ACTIVE_OBJECT.ANY
class GenericOperator(ACK.Ops.Generic):
    new_name = ACK.PropTyped.String("Object Name").default("Best Name Ever")

    def invoke(self, context, event) -> set[str]:
        context.active_object.name = self.new_name
        self.report({'INFO'}, f"New Name {self.new_name}")
        return OpsReturn.FINISH
