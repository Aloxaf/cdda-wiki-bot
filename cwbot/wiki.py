import typing as t
import re
from collections import defaultdict

import mwclient
from loguru import logger
from .types import Json
from .templates import spell, master

TEMPLATE_HEADER = """<!-- CDDA WIKI BOT START -->
<!-- 这部分内容是 bot 生成的，请不要更改 -->
{text}
<!-- CDDA WIKI BOT END -->"""
TEMPLATE_FOOTER = """<!-- CDDA WIKI BOT START FOOTER -->
<!-- 这部分内容是 bot 生成的，请不要更改 -->
{text}
<!-- CDDA WIKI BOT END FOOTER -->"""
RE_TEMPLATE_HEADER = r"<!-- CDDA WIKI BOT START -->.*<!-- CDDA WIKI BOT END -->"
RE_TEMPLATE_FOOTER = r"<!-- CDDA WIKI BOT START FOOTER -->.*<!-- CDDA WIKI BOT END FOOTER -->"


class WikiBot:
    def __init__(self, host: str, path: str, username: str, password: str):
        self.site = mwclient.Site(host, path=path)
        self.site.login(username, password)

    def update_page(self, name: str, header: str, footer: str = ''):
        """
        更新页面，不修改用户自己添加的内容
        :param name: 页面名称
        :param header: 页面开头
        :param footer: 页面结尾
        :return:
        """
        logger.info("同步页面：{}", name)

        header = TEMPLATE_HEADER.format(text=header)
        footer = TEMPLATE_FOOTER.format(text=footer)

        page = self.site.pages[name]
        if page.exists:
            old_text = page.text()
            # 如果已经存在 header，就更新，反之添加到开头
            if re.search(RE_TEMPLATE_HEADER, old_text, flags=re.DOTALL):
                text = re.sub(RE_TEMPLATE_HEADER, header, old_text, flags=re.DOTALL)
            else:
                text = header + old_text
            # 如果已经存在 footer，就更新，反之添加到结尾
            if re.search(RE_TEMPLATE_FOOTER, text, flags=re.DOTALL):
                text = re.sub(RE_TEMPLATE_FOOTER, footer, text, flags=re.DOTALL)
            else:
                text += footer
        else:
            text = header + footer
        page.edit(text, summary="cdda wiki bot 自动更新", minor=True)

    def create_redirect(self, src: str, dst: str):
        """
        创建重定向页面，当页面已存在时则跳过
        :param src: 原页面
        :param dst: 目标页面
        :return:
        """
        page = self.site.pages[src]
        if not page.exists:
            page.edit(f'#REDIRECT [[{dst}]]', summary="cdda wiki bot 自动更新")

    def update_spells(self, datas: t.List[Json]):
        """
        更新法术页面
        :param datas: 法术的 JSON 数据
        :return:
        """
        # 先扫描一遍生成「模板:法师列表」
        master_template = master.template(datas)

        self.update_page("模板:法术体系", master_template)

        for data in datas:
            if not data.get("id"):
                logger.warning("这个法术没有 ID: {}", data)
                continue

            name, text = spell.template(data)

            if data.get("spell_class"):
                self.update_page(name, text, footer="{{模板:法术体系}}")
            else:
                self.update_page(name, text)

            self.create_redirect(data["id"], name)
