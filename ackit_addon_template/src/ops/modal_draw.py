from ...ackit import ACK
from ...ackit.enums.operator import OpsReturn
from ...ackit.utils.event import IsEventType, IsEventValue

import blf


# @ModalFlags.USE_MOUSE
@ACK.Ops.add_modal_flag.DRAW_POST_PIXEL.VIEW_3D
@ACK.Poll.ACTIVE_OBJECT.ANY
class ModalDrawOperator(ACK.Ops.Modal):
    def modal_enter(self, context, event):
        self.text = "Hello, world!"

    def modal_update(self, context, event) -> OpsReturn:
        if event.type == 'ESC':
            return OpsReturn.FINISH
        if event.unicode:
            self.text += event.unicode
            self.tag_redraw(context)
            return OpsReturn.RUN
        elif IsEventType.BACK_SPACE and IsEventValue.RELEASE and self.text != '':
            self.text = self.text[:-1]
            self.tag_redraw(context)
            return OpsReturn.RUN
        return OpsReturn.PASS

    def draw_2d(self, context):
        blf.size(0, 12)
        blf.position(0, 100, 50, 0)
        blf.color(0, 1, 0, 0, 1)
        blf.draw(0, self.text)
