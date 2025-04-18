from ...ackit import ACK


@ACK.Ops.Flags.REGISTER_UNDO
@ACK.Poll.ACTIVE_OBJECT.MESH
@ACK.Poll.MODE.OBJECT
class ActionOperator(ACK.Ops.Action):
    label = "Test Action"
    tooltip = "Transforms active mesh object location in Z axis"

    enable = ACK.PropTyped.Bool("Enable")
    z_location = ACK.PropTyped.Float("Z")

    def draw_ui(self, context, layout):
        # print(self.props.__dict__)  # This will show you all properties in the DescriptorPropertyCollection
        row = layout.row()
        row.prop(self, 'enable', text="Enable Feature")
        row.prop(self, 'z_location', text="Z Location")

    def action(self, context) -> None:
        if self.enable:
            context.active_object.location.z = self.z_location
            self.report_info(f"Value {self.z_location}")
