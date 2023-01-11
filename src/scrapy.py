import logging
from dataclasses import dataclass
import requests
from typing import Dict, List

from lxml import etree

from email_sender import EmailSender
from util import log_around


@dataclass
class ArticleInfo:
    id: str
    url: str
    title: str


class Spider:
    def __init__(self, public_service_ids: List[str], email_sender: EmailSender) -> None:
        self._public_service_id_to_latest_article_info: Dict[str, ArticleInfo] = dict()
        for public_service_id in public_service_ids:
            self._public_service_id_to_latest_article_info[public_service_id] = \
                self._get_latest_article_link_by_public_service_id(public_service_id)
        self._email_sender: EmailSender = email_sender
        logging.info("Spider 初始化成功")

    @log_around
    def refresh(self) -> None:
        logging.info("爬虫开始工作")
        updated_articles: List[ArticleInfo] = []
        for public_service_id in public_service_ids:
            article_info: ArticleInfo = Spider._get_latest_article_link_by_public_service_id(public_service_id)
            if article_info != self._public_service_id_to_latest_article_info[public_service_id]:
                updated_articles.append(article_info)
                self._public_service_id_to_latest_article_info[public_service_id] = article_info
        if updated_articles:
            def article_info_to_content(article: ArticleInfo) -> str:
                return f'{article.id}: <a herf="{article.url}">{article.title}</a>'

            sub_contents: List[str] = list(map(article_info_to_content, updated_articles))
            content: str = "\n\n".join(sub_contents)
            self._email_sender("微信公众号更新！", content)
        logging.info("爬虫结束工作")

    @staticmethod
    def _get_latest_article_link_by_public_service_id(public_service_id: str) -> ArticleInfo:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36'
        }
        response = requests.get(
            f'https://weixin.sogou.com/weixin?type=1&query={public_service_id}&ie=utf8&s_from=input&_sug_=n&_sug_type_=',
            headers=headers).text
        service_element = etree.HTML(response).xpath('//*[@id="sogou_vr_11002301_box_0"]/div/div[2]/p[1]/a')[0]
        article_element = etree.HTML(response).xpath('//*[@id="sogou_vr_11002301_box_0"]/dl[2]/dd/a')[0]
        return ArticleInfo(service_element.text,
                           f'https://weixin.sogou.com{article_element.attrib.get("href")}',
                           article_element.text)
