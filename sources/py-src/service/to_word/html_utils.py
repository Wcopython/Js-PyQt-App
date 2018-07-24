# -*- coding: utf-8 -*
# author luxin

import json
import os.path
from bs4 import BeautifulSoup
from bs4 import Tag
from visio2img import visio2img

from service.to_word.word_utils import WordUtils


class HtmlUtils(object):

    def __init__(self):
        self.__document = None
        self.dict_methods = {"heading": self.__add_heading, "prompt": self.__add_prompt,
                             "paragraph": self.__add_paragraph, "radio": self.__add_radio,
                             "checkbox": self.__add_checkbox, "file": self.__add_file,
                             "table": self.__add_table, "orientation": self.__orientation}
        self.list_img = [".bmp", ".jpg", ".png", ".tiff", ".gif"]
        self.dict_merge = []

    def html_to_word(self, html_code):
        # 初始化word文档
        self.__document = WordUtils()
        # 将html_code转小写
        # html_code = html_code.lower()
        # 解析html
        soup = BeautifulSoup(html_code, "html.parser")
        # 找到章节
        _tags = soup.find_all(attrs={"data-word": "{\"name\":\"chapter\"}"})
        # 处理标签
        for _tag in _tags:
            self.__tag_analysis(_tag)
        # 保存文档
        self.__document.save_document()

    # 分析标签
    def __tag_analysis(self, _tag):
        # 判断是否是标签
        if isinstance(_tag, Tag):
            # 处理标签里的信息
            self.__tag_current(_tag)
            # 处理子标签的信息
            self.__tag_children(_tag)

    # 处理子节点
    def __tag_children(self, _tag):
        # 获取节点的子节点
        _children = _tag.children
        # 循环子节点
        for _child in _children:
            # 分析标签
            self.__tag_analysis(_child)

    # 处理当前标签的信息
    def __tag_current(self, _tag):
        # 判断标签是否有data-word属性
        if _tag.has_attr("data-word"):
            # 将data-word转为dict
            _dict_word = json.loads(_tag["data-word"])
            # 判断dict是否这个key
            key = "name"
            if key in _dict_word:
                key = _dict_word[key]
                if key in self.dict_methods:
                    self.dict_methods[key](_tag, _dict_word)

    # 标题
    def __add_heading(self, _tag, _dict_word):
        level = "1"
        if "level" in _dict_word:
            level = str(_dict_word["level"])

        style_name = "Heading " + level
        self.__document.add_paragraph(_tag.get_text().strip(), style_name)

    # 提示信息
    def __add_prompt(self, _tag, _dict_word):
        style_name = "user_prompt"
        if "style" in _dict_word:
            style_name = _dict_word["style"]
        self.__document.add_paragraph(_tag.get_text().strip(), style_name)

    # 段落
    def __add_paragraph(self, _tag, _dict_word):
        style_name = "user_paragraph"
        if "style" in _dict_word:
            style_name = _dict_word["style"]
        _atp_tags = _tag.find_all(attrs={"data-word": "{\"name\":\"atp\"}"})
        if _atp_tags.__len__() > 0:
            self.__document.add_paragraph("", style_name)
            for _atp in _atp_tags:
                if _atp.name.__eq__("input") or _atp.name.__eq__("textarea"):
                    if _atp.has_attr("value"):
                        self.__document.add_to_paragraph(" " + _atp['value'].strip() + " ", underline=True)
                    else:
                        self.__document.add_to_paragraph("  ", underline=True)
                elif _atp.name.__eq__("span"):
                    self.__document.add_to_paragraph(" " + _atp.get_text().strip(), underline=False)
                else:
                    self.__document.add_to_paragraph(_atp.get_text().strip())
        else:
            if _tag.name.__eq__("textarea") and _tag.has_attr("value"):
                self.__document.add_paragraph(_tag['value'].strip(), style_name)
            else:
                self.__document.add_paragraph(_tag.get_text().strip(), style_name)

    # 单选题
    def __add_radio(self, _tag, _dict_word):
        # 标题
        _title = _tag.find(attrs={"data-word": "{\"name\":\"title\"}"})
        style_name = "user_radio_title"
        _title_word = json.loads(_title["data-word"])
        if "style" in _title_word:
            style_name = _title_word["style"]
        self.__document.add_paragraph(_title.get_text().strip(), style_name)
        # 选项
        for _option in _tag.find_all(attrs={"data-word": "{\"name\":\"option\"}"}):
            style_name = "user_radio_option"
            _option_word = json.loads(_option["data-word"])
            if "style" in _option_word:
                style_name = _option_word["style"]
            words = "○"
            if self.__radio_option_checked(_option):
                words = "●"
            # 先增加一个段落，有数据向段落中追加
            self.__document.add_paragraph(words, style_name)
            _atp_tags = _option.find_all(attrs={"data-word": "{\"name\":\"atp\"}"})
            if _atp_tags.__len__() > 0:
                for _atp in _atp_tags:
                    if _atp.name == "input":
                        if _atp.has_attr("value"):
                            self.__document.add_to_paragraph(" " + _atp["value"].strip() + " ", underline=True)
                        else:
                            self.__document.add_to_paragraph("  ", underline=True)
                    else:
                        self.__document.add_to_paragraph(_atp.get_text().strip())
            else:
                self.__document.add_to_paragraph(_option.get_text().strip())

    # 多选题
    def __add_checkbox(self, _tag, _dict_word):
        # 标题
        _title = _tag.find(attrs={"data-word": "{\"name\":\"title\"}"})
        style_name = "user_radio_title"
        _title_word = json.loads(_title["data-word"])
        if "style" in _title_word:
            style_name = _title_word["style"]
        self.__document.add_paragraph(_title.get_text().strip(), style_name)
        # 选项
        for _option in _tag.find_all(attrs={"data-word": "{\"name\":\"option\"}"}):
            style_name = "user_radio_option"
            _option_word = json.loads(_option["data-word"])
            if "style" in _option_word:
                style_name = _option_word["style"]
            self.__document.add_paragraph("", style_name)
            _atp_tags = _option.find_all(attrs={"data-word": "{\"name\":\"atp\"}"})
            if _atp_tags.__len__() > 0:
                for _atp in _atp_tags:
                    if _atp.name == "input":
                        if _atp.has_attr("value"):
                            self.__document.add_to_paragraph(" " + _atp["value"].strip() + " ", underline=True)
                        else:
                            self.__document.add_to_paragraph("  ", underline=True)
                    else:
                        if self.__tag_is_checkbox(_atp):
                            if self.__checkbox_option_checked(_atp):
                                self.__document.add_to_paragraph("■")
                            else:
                                self.__document.add_to_paragraph("□")
                        self.__document.add_to_paragraph(_atp.get_text().strip())
            else:
                if self.__tag_is_checkbox(_option):
                    if self.__checkbox_option_checked(_option):
                        self.__document.add_to_paragraph("■")
                    else:
                        self.__document.add_to_paragraph("□")
                self.__document.add_to_paragraph(_option.get_text().strip())

    # 图片
    def __add_file(self, _tag, _dict_word):
        # 标题
        _title = _tag.find(attrs={"data-word": "{\"name\":\"title\"}"})
        style_name = "user_file_title"
        _title_word = json.loads(_title["data-word"])
        if "style" in _title_word:
            style_name = _title_word["style"]
        self.__document.add_paragraph(_title.get_text().strip(), style_name)

        # 图片
        _pic_tags = _tag.find_all(attrs={"data-word": "{\"name\":\"img\"}"})
        for _pic in _pic_tags:
            _width = 300
            if _pic.has_attr("data-word"):
                _pic_word = json.loads(_pic["data-word"])
                if "width" in _pic_word:
                    _width = int(_pic_word["width"])
            if _pic.has_attr("word-src"):
                file_path = _pic["word-src"]
                file_suffix = os.path.splitext(file_path)[1]
                if file_suffix in self.list_img:
                    self.__document.add_picture(_pic["word-src"], _width)
                elif file_suffix == ".vsd" or file_suffix == ".vsdx":
                    self.__document.add_picture(self.__visio2img(file_path), _width)
                else:
                    n = 1

    # 表格
    def __add_table(self, _tag, _dict_word):
        # 添加标题
        table_title = _tag.find(attrs={"data-word": "{\"name\":\"title\"}"})
        if table_title is not None:
            self.__document.add_paragraph(table_title.get_text().strip(), "user_table_title")
        # 添加提示
        table_notes = _tag.find(attrs={"data-word": "{\"name\":\"notes\"}"})
        if table_notes is not None:
            self.__document.add_paragraph(table_notes.get_text().strip(), "user_table_notes")
        # 初始化
        self.dict_merge = []
        # 表格行数
        row_size = 0
        # 表格列数
        col_size = 0
        # 查询表格中所有行的标签
        _row_tags = _tag.find_all(attrs={"data-word": "{\"name\":\"tr\"}"})
        # 获取表格行数
        row_size = _row_tags.__len__()
        # 如果表格的行数不为0，则计算表格的列数
        if row_size > 0:
            # 取出表格第一行
            _row_tag = _row_tags[0]
            # 循环行中的每一个标签，计算列数
            for _content in _row_tag.descendants:
                # 判断是否是标签并具有data-word属性
                if isinstance(_content, Tag) and _content.has_attr("data-word"):
                    _content_dict = json.loads(_content["data-word"])
                    # 判断是否是td标签
                    if "name" in _content_dict and _content_dict["name"] == "td":
                        col_size = col_size + 1
                        # 判断合并列
                        if "colspan" in _content_dict:
                            col_size = col_size + int(_content_dict["colspan"]) - 1

        # 表格的行数和列数均大于0，则创建表格
        if row_size > 0 and col_size > 0:
            # 表格样式名
            style_name = "user_table_firstline"
            if "style" in _dict_word:
                style_name = _dict_word["style"]
            # 创建表格
            self.__document.add_table(row_size, col_size, style_name)
            # 循环表格的每一行，合并单元格并填充数据
            for _row_idx in range(row_size):
                # 列的索引
                _col_idx = -1
                # 循环行中的标签
                for _child in _row_tags[_row_idx].descendants:
                    # 找到行中具有data-word属性的标签
                    if isinstance(_child, Tag) and _child.has_attr("data-word"):
                        # 标签的data-word属性
                        _child_dict = json.loads(_child["data-word"])
                        # 判断是否是列标签
                        if "name" in _child_dict and _child_dict["name"] == "td":
                            # 索引自增
                            _col_idx = _col_idx + 1
                            # 行合并
                            _row_span_size = self.__get_rowspan(_child_dict) - 1 if self.__get_rowspan(
                                _child_dict) - 1 > 0 else 0
                            # 列合并
                            _col_span_size = self.__get_colspan(_child_dict) - 1 if self.__get_colspan(
                                _child_dict) - 1 > 0 else 0
                            # 目标单元格
                            _end_row = _row_idx + _row_span_size
                            _end_col = _col_idx + _col_span_size
                            # 判断当前单元格与合并的单元格有交叉
                            while self.__cell_in_merge(_row_idx, _col_idx, _end_row, _end_col) == 0:
                                _col_idx = _col_idx + 1
                                _end_col = _end_col + 1

                            # 合并单元格
                            self.__merge_cell(_row_idx, _col_idx, _end_row, _end_col)
                            # 填充数据
                            self.__insert_cell(_row_idx, _col_idx, _child)
                            # 如果有行合并，记录行合并
                            if _row_idx != _end_row or _col_idx != _end_col:
                                self.dict_merge.append(Merge(_row_idx, _col_idx, _end_row, _end_col))
                            _col_idx = _end_col

    # 判断单选题选项是否选中
    def __radio_option_checked(self, _option_tag):
        if _option_tag.has_attr("class"):
            for css in _option_tag["class"]:
                if css == "checked":
                    return True
        return False

    # 判断多选题选项是否选中
    def __checkbox_option_checked(self, _option_tag):
        if _option_tag.has_attr("class"):
            for css in _option_tag["class"]:
                if css == "checked":
                    return True
        return False

    # 获取rowspan
    def __get_rowspan(self, _col_word):
        if "rowspan" in _col_word:
            return int(_col_word["rowspan"])
        else:
            return 0

    # 获取colspan
    def __get_colspan(self, _col_word):
        if "colspan" in _col_word:
            return int(_col_word["colspan"])
        else:
            return 0

    # 记录单元格合并信息
    def __write_merge(self, start_row, start_col, end_row, end_col):
        self.dict_merge.append(Merge(start_row, start_col, end_row, end_col))

    # 判断当前单元格是否已经合并
    def __cell_in_merge(self, start_row, start_col, end_row, end_col):
        # 返回三种状态，1同一个单元格， 0不是同一个单元格，但是有交叉， -1没有任何交叉
        flag = -1
        for _merge in self.dict_merge:
            if start_row < _merge.start_row or start_row > _merge.end_row or start_col < _merge.start_col or start_col > _merge.end_col:
                if flag < 0:
                    flag = -1
            else:
                if _merge.start_row == start_row and _merge.start_col == start_col and _merge.end_row == end_row and _merge.end_col == end_col:
                    if flag < 1:
                        flag = 1
                else:
                    if flag < 0:
                        flag = 0
        return flag

    # 根据rowspan和colspan合并单元格
    def __merge_cell(self, start_row, start_col, end_row, end_col):
        self.__document.merge_cell(start_row, start_col, end_row, end_col)

    # 填充数据
    def __insert_cell(self, row_num, col_num, col_tag):
        self.__document.insert_cell(row_num, col_num, "")
        atp_tags = col_tag.find_all(attrs={"data-word": "{\"name\":\"atp\"}"})
        if atp_tags.__len__() > 0:
            for tag in atp_tags:
                if self.__tag_is_radio(tag):
                    if self.__radio_option_checked(tag):
                        self.__document.add_to_paragraph("●")
                    else:
                        self.__document.add_to_paragraph("○")
                    self.__document.add_to_paragraph(tag.get_text().strip() + " ")
                elif self.__tag_is_checkbox(tag):
                    if self.__checkbox_option_checked(tag):
                        self.__document.add_to_paragraph("■")
                    else:
                        self.__document.add_to_paragraph("□")
                    self.__document.add_to_paragraph(tag.get_text().strip() + " ")
                elif self.__tag_is_input(tag):
                    if tag.has_attr("value"):
                        self.__document.add_to_paragraph(" " + tag["value"].strip() + " ", underline=True)
                    else:
                        self.__document.add_to_paragraph("  ", underline=True)
                elif self.__tag_is_br(tag):
                    self.__document.cell_add_paragraph(row_num, col_num)
                else:
                    self.__document.insert_cell(row_num, col_num, tag.get_text().strip())
        else:
            if col_tag.name == "input" and col_tag.has_attr("value"):
                self.__document.insert_cell(row_num, col_num, col_tag["value"].strip())
            elif col_tag.name == "select" and col_tag.has_attr("value"):
                self.__document.insert_cell(row_num, col_num, col_tag["value"].strip())
            else:
                self.__document.insert_cell(row_num, col_num, col_tag.get_text().strip())

    # 是否是单选
    def __tag_is_radio(self, tag):
        _flag = False
        if tag.has_attr("class"):
            for str in tag["class"]:
                if str == "radio":
                    _flag = True
                    break
        return _flag

    # 是否是多选
    def __tag_is_checkbox(self, tag):
        _flag = False
        if tag.has_attr("class"):
            for str in tag["class"]:
                if str == "checkbox":
                    _flag = True
                    break
        return _flag

    # 是否是输入框
    def __tag_is_input(self, tag):
        _flag = False
        if tag.name == "input":
            _flag = True
        return _flag

    # 是否是输入框
    def __tag_is_br(self, tag):
        _flag = False
        if tag.name == "br":
            _flag = True
        return _flag

    # 設置紙張方向
    def __orientation(self, _tag, _dict_word):
        if "value" in _dict_word:
            orientation_methods = {"landscape": self.__document.section_landscape,
                                   "portrait": self.__document.section_portrait}
            key = _dict_word['value']
            if key in orientation_methods:
                orientation_methods[key]()

    # visio文件转为图片
    def __visio2img(self, file_path):
        img_path = file_path + ".png"
        visio2img(file_path, img_path, 1, None)
        return img_path


class Merge(object):
    def __init__(self, start_row, start_col, end_row, end_col):
        self.start_row = start_row
        self.start_col = start_col
        self.end_row = end_row
        self.end_col = end_col
