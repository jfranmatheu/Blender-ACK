from ...ackit import ACK


@ACK.Poll.ACTIVE_OBJECT.ANY
class GenericOperator(ACK.Types.Ops.Generic):
    new_name = ACK.Props.Typed.STRING(name="Object Name", default="Best Name Ever")

    def invoke(self, context, event) -> None:
        context.active_object.name = self.new_name
        self.report({'INFO'}, f"New Name {self.new_name}")
        return ACK.Returns.Operator.FINISH
