import tempfile
import base64
import os
from uuid import uuid1
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from PIL import Image

from ...core.reporting.blocks import *
from .msteams_elements.msteams_images_element import MsTeamsImagesElement
from cairosvg import svg2png

# TODO: in read me write that you CANT !!!! UPLOAD files to msteams sharepoint !!!! put the references
class MsTeamsAdaptiveCardFilesImage:

    def __init__(self):
        self.url_map_list = []

    def create_files_for_presentation(self, file_blocks: list[FileBlock]) -> map:
        url_list = []        
        for file_block in file_blocks:
            if not self.__file_is_image(file_block.filename):
                continue
            data_url = self.__convert_bytes_to_base_64_url(file_block.filename, file_block.contents)
            url_list.append(data_url)
        if len(url_list) == 0:
            return []
        return MsTeamsImagesElement(url_list)

    def get_url_map_list(self):
        return self.url_map_list

    def __get_tmp_file_path(self):
        tmp_dir_path = tempfile.gettempdir() 
        return tmp_dir_path + '/' + str(uuid.uuid1())

    def __file_is_jpg(self, file_name: str):
        return file_name.lower().endswith('.jpg')
    def __file_is_png(self, file_name: str):
        return file_name.lower().endswith('.png')
    def __file_is_svg(self, file_name: str):
        return file_name.lower().endswith('.svg')
    
    def __file_is_image(self, file_name: str):
        return self.__file_is_jpg(file_name) \
            or self.__file_is_png(file_name) \
            or self.__file_is_svg(file_name) \

    def __convert_bytes_to_base_64_url(self, file_name: str, bytes: bytes):
        if self.__file_is_jpg(file_name):
            return self.__jpg_convert_bytes_to_base_64_url(bytes)
        if self.__file_is_png(file_name):
            return self.__png_convert_bytes_to_base_64_url(bytes)
        return self.__svg_convert_bytes_to_jpg(bytes)

    def __jpg_convert_bytes_to_base_64_url(self, bytes : bytes):
        b64_string = base64.b64encode(bytes).decode("utf-8") 
        return 'data:image/jpeg;base64,{0}'.format(b64_string)

    #msteams cant read parsing of url to 'data:image/png;base64,...
    def __png_convert_bytes_to_base_64_url(self, bytes : bytes):
        png_file_path = self.__get_tmp_file_path() + '.png'
        jpg_file_path = self.__get_tmp_file_path() + '.jpg'
        with open(png_file_path, 'wb') as f:
            f.write(bytes)

        im = Image.open(png_file_path)
        rgb_im = im.convert('RGB')
        rgb_im.save(jpg_file_path)
        with open(jpg_file_path, 'rb') as f:
            jpg_bytes = f.read()

        os.remove(png_file_path)
        os.remove(jpg_file_path)

        return self.__jpg_convert_bytes_to_base_64_url(jpg_bytes)

    #msteams cant read parsing of url to svg image
    def __svg_convert_bytes_to_jpg(self, bytes : bytes):

        return self.__png_convert_bytes_to_base_64_url(svg2png(bytestring=bytes))