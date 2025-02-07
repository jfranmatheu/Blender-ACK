from ...ackit import ACK


@ACK.Deco.Options.OPERATOR.REGISTER
@ACK.Deco.Options.OPERATOR.UNDO
@ACK.Deco.Poll.ACTIVE_OBJECT.MESH
@ACK.Deco.Poll.MODE.OBJECT
class ActionOperator(ACK.Types.Ops.ACTION):
    use_something = ACK.Props.Typed.BoolProperty(name="Use Something")
    my_value = ACK.Props.Typed.FloatProperty(name="Value")

    def draw_ui(self, context, layout):
        # print(self.props.__dict__)  # This will show you all properties in the DescriptorPropertyCollection
        row = layout.row()
        row.prop(*self.props.use_something, text="Enable Feature")
        row.prop(*self.props.my_value, text="Nice value")

    def action(self, context) -> None:
        if self.use_something:
            context.active_object.location.z = self.my_value
            self.report({'INFO'}, f"Value {self.my_value}")
