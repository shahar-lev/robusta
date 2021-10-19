import json
import logging
import tempfile
import pymsteams

from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.reporting.callbacks import PlaybookCallbackRequest
from ...core.reporting.consts import SlackAnnotations
from ...core.model.env_vars import TARGET_ID
from .msteams_adaptive_card import MsTeamsAdaptiveCard

ACTION_TRIGGER_PLAYBOOK = "trigger_playbook"
MsTeamsBlock = Dict[str, Any]

class MsTeamsImplementation:
    current_header_string = ''
    current_section_string = ''

    def __init__(self, msteams_hookurl: str, title: str, description: str):
        try:
            self.adaptive_card = MsTeamsAdaptiveCard()

            self.adaptive_card.set_text_block(self.__new_line_replacer(title))
            if description is not None:
                self.adaptive_card.set_text_block(self.__new_line_replacer(description))
        except Exception as e:
            logging.error(f"Cannot connect to MsTeams Channel: {e}")
            raise e

    def new_card_section(self):
        section = pymsteams.cardsection()
        section.activityImage("http://i.imgur.com/c4jt321l.png")
        if self.current_header_string != '':
            section.activityTitle(self.__new_line_replacer(self.current_section_string))
        if self.current_section_string != '':
            section.activityText(self.__new_line_replacer(self.current_section_string))

        if self.current_section_string == '' and self.current_header_string == '':
            return

        self.myTeamsMessage.addSection(section)
        self.current_header_string = ''
        self.current_section_string = ''

    def send(self):
        try:
            self.myTeamsMessage.send()
        except Exception as e:
            logging.error(f"error sending message to msteams\ne={e}\n")
        

    def diff(self, block: KubernetesDiffBlock):
        data = ''
        for d in block.diffs:
            data = f"*{d.formatted_path}*: {d.other_value} :arrow_right: {d.value}"
            data += '\n'
        self.current_section_string += self.__new_line_replacer(data + '\n\n')


    def markdown_block(self, block: BaseBlock):
        if not block.text:
            return
        self.current_section_string += self.__apply_length_limit(block.text) + self.__new_line_replacer('\n\n')

    def divider_block(self, block: BaseBlock):
        self.current_section_string += self.__new_line_replacer('\n\n')

    def header_block(self, block: BaseBlock):
        self.current_header_string += self.__apply_length_limit(block.text, 150) + self.__new_line_replacer('\n\n')

    def get_action_block_for_choices(self, choices: Dict[str, Callable] = None, context=""):
        if choices is None:
          return
        '''
        buttons = []
        for (i, (text, callback)) in enumerate(choices.items()):
            buttons.append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": text,
                    },
                    "style": "primary",
                    "action_id": f"{ACTION_TRIGGER_PLAYBOOK}_{i}",
                    "value": PlaybookCallbackRequest.create_for_func(
                        callback, context, text
                    ).json(),
                }
            )

        return [{"type": "actions", "elements": buttons}]
        '''

    def __apply_length_limit(self, msg: str, max_length: int = 3000):
        if len(msg) <= max_length:
            return msg
        truncator = "..."
        return self.__new_line_replacer(msg[: max_length - len(truncator)] + truncator)

    def __new_line_replacer(self, text : str):
        return text.replace('\n', '<br>')
