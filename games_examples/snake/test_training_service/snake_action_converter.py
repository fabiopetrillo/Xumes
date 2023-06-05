from typing import List

from framework.training_service_module.i_action_converter import IActionConverter


class SnakeActionConverter(IActionConverter):

    def convert(self, raws_actions) -> List[str]:
        if raws_actions == 1:
            return ['up']
        elif raws_actions == 2:
            return ['down']
        elif raws_actions == 3:
            return ['left']
        elif raws_actions == 4:
            return ['right']
        return ['nothing']
