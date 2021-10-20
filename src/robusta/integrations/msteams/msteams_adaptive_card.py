
from enum import Enum
from typing import Awaitable


class CardElements(Enum):
    TEXT = 'text',
    IMAGE = 'image',
    SECTION = 'section'
    



class AdaptiveCardFontSize(Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    EXTRA_LARGE = "extraLarge"


class MsTeamsAdaptiveCard:

    curr_card = ''

    def get_msg(self):
        __BODY =  """{{
                        "type":"message",
                        "attachments":[
                        {{
                            "contentType":"application/vnd.microsoft.card.adaptive",
                            "contentUrl":null,
                            "content":{{
                                "$schema":"http://adaptivecards.io/schemas/adaptive-card.json",
                                "type":"AdaptiveCard",
                                "version":"1.2",
                                "msTeams": {{ "width": "full" }},
                                "body":[
                                    {0}  
                                ]
                            }}
                        }}
                        ]
                    }}"""
        print(__BODY.format(self.curr_card))
        return __BODY.format(self.curr_card)

    def set_text_block(self, text : str, font_size : AdaptiveCardFontSize):
        block = ''' {{
                "type": "TextBlock",
                "text": "{0}",
                "size": "{1}"
                }}, '''
        self.curr_card += block.format(text, font_size.value)

    def get_text_block(self, text : str, font_size : AdaptiveCardFontSize):
        block = ''' {{
                "type": "TextBlock",
                "text": "{0}",
                "size": "{1}"
                }}, '''
        return block.format(text, font_size.value)



    def get_section_separator(self):
        block = '''
            {{
        "type": "Container",
        "minHeight": "50px",
        "style": "default",
        "items": []
        }},'''
        return block

    def set_image(self):
        pass