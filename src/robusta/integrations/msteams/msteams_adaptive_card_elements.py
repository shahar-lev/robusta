
class MsTeamsAdaptiveCardElements:
    __type = 'type'

    def image_set(self, images_list : list[map]) -> map:
        block = {}
        block[self.__type] =  "ImageSet"
        block["imageSize"] = "large"
        block["images"]=  images_list
        return block

    def action(self, title : str, target_elements : list[map]):
        block = {}
        block["selectAction"] = {}
        block["selectAction"]["type"] = "Action.ToggleVisibility"
        block["title"]["type"] = "Action.ToggleVisibility"
        block["title"]["title"] = title
        block["title"]["targetElements"] = target_elements

        return block

    def present_image(self, url : str) -> map:
        block = {}
        block[self.__type] = "Image"
        block["url"] = url
        block["msTeams"] = { "allowExpand": True }    
        return block      

    def text_block(self, text : str, isSubtle : bool = None, wrap: bool = None, weight: str = None):
        block = {}
        block[self.__type] = "TextBlock" 
        block["text"] = text 
        if isSubtle is not None:
            block["isSubtle"] = isSubtle 
        if wrap is not None:
            block["wrap"] = wrap 
        if weight is not None:
            block["weight"] = weight 
        return block

    def container(self, key : str = None, items : list[map] = []):
        block = {}
        block[self.__type] = "Container"
        block["style"] = "accent"
        block["isVisible"] = False
        if key is not None:
            block["id"] = key
        block["bleed"] = True
        block["items"] = items
        return block

    def column(self, width_number: int = None, width_strech : bool = None, isVisible : bool = True, key : str = None, items : list[map] = []):
        block = {}
        block[self.__type] = "Column"
        if width_number is not None:
            block["width"] = str(width_number) + "px"
        if width_strech is not None:
            block["width"] = "stretch"
        block["isVisible"] = isVisible
        block["isVisible"] = isVisible
        if key is not None:
            block["id"] = key
        block["items"] = items

    def action_toggle_target_elements(self, visible_keys : list[bool], invisible_keys : list[bool]):
        pass

        