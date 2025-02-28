from ...ackit import ACK


@ACK.Flags.OPERATOR.REGISTER_UNDO
@ACK.Poll.ACTIVE_OBJECT.MESH
@ACK.Poll.MODE.OBJECT
class ActionOperator(ACK.Register.Types.Ops.Action):
    label = "Test Action"
    tooltip = "Transforms active mesh object location in Z axis"

    enable = ACK.PropsLayout.BOOL(name="Enable")
    z_location = ACK.PropsLayout.FLOAT(name="Z")

    def draw_ui(self, context, layout):
        # print(self.props.__dict__)  # This will show you all properties in the DescriptorPropertyCollection
        row = layout.row()
        row.prop(*self.props.enable, text="Enable Feature")
        row.prop(*self.props.z_location, text="Z Location")

    def action(self, context) -> None:
        if self.enable:
            context.active_object.location.z = self.z_location
            self.report_info(f"Value {self.z_location}")
