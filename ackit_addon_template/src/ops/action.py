from ...ackit import ACK


@ACK.Flags.OPERATOR.REGISTER
@ACK.Flags.OPERATOR.UNDO
@ACK.Poll.ACTIVE_OBJECT.MESH
@ACK.Poll.MODE.OBJECT
class ActionOperator(ACK.Types.Ops.Action):
    use_something = ACK.Props.Typed.BOOL(name="Use Something")
    my_value = ACK.Props.Typed.FLOAT(name="Value")

    def draw_ui(self, context, layout):
        # print(self.props.__dict__)  # This will show you all properties in the DescriptorPropertyCollection
        row = layout.row()
        row.prop(*self.props.use_something, text="Enable Feature")
        row.prop(*self.props.my_value, text="Nice value")

    def action(self, context) -> None:
        if self.use_something:
            context.active_object.location.z = self.my_value
            self.report({'INFO'}, f"Value {self.my_value}")
