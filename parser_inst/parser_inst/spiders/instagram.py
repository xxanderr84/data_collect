import json
from copy import deepcopy
from urllib.parse import urlencode
import scrapy
import re
from scrapy.http import HtmlResponse
from parser_inst.parser_inst.items import ParserInstItem


class InstagramSpider(scrapy.Spider):
    name = 'instagram'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'data_engener'
    inst_pwd = '#PWD_INSTAGRAM_BROWSER:10:1605003620:AfNQAECUm96xANcvtCifwLqJpOvPwoRE8Pd31G' \
               'X6Ih4PT20wNDwzu3DhkAf95C2g6kcXPT3jiOgfLjoOL9nwr3Y9YxhMeOT9E1Z8OCAI5ITGoKJb' \
               'sv5gkz8xynkl+SQ8FGIIGy0t6/3BRpajiMYAKYAMcQ=='
    parse_user = ['elenabogd1', 'hyperbonus']
    graphql_url = 'https://www.instagram.com/graphql/query/?'
    follow_hash = 'd04b0a864b4b54837c0d870b0e77e076'
    followed_hash = 'c76146de99bb02f6415203be841dd25a'

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)
        yield scrapy.FormRequest(
            self.inst_link,
            method='POST',
            callback=self.auth,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def auth(self, response):
        jdata = response.json()
        if jdata['authenticated']:
            for item in self.parse_user:
                yield response.follow(
                    f'/{item}',
                    callback=self.parse_users,
                    cb_kwargs={'username': item}
                )
        pass

    def parse_users(self, response: HtmlResponse, username):
        user_id = self.fetch_user_id(response.text, username)
        variables = {'id': user_id,
                     'include_reel': True,
                     'fetch_mutual': True,
                     'first': 24}
        url_follow = f'{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}'
        url_followed = f'{self.graphql_url}query_hash={self.followed_hash}&{urlencode(variables)}'
        yield response.follow(
            url_follow,
            callback=self.user_follow_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )
        yield response.follow(
            url_followed,
            callback=self.user_followed_parse,
            cb_kwargs={'username': username,
                       'user_id': user_id,
                       'variables': deepcopy(variables)}
        )

    def user_follow_parse(self, response, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data['data']['user']['edge_follow']['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_following = f'{self.graphql_url}query_hash={self.follow_hash}&{urlencode(variables)}'
            yield response.follow(
                url_following,
                callback=self.user_follow_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        follows = j_data['data']['user']['edge_follow']['edges']
        for follow in follows:
            item = ParserInstItem(
                user_id=user_id,
                photo=follow['node']['profile_pic_url'],
                follow_name=follow['node']['username'],
                follow_id=follow['node']['id'],
                follow_full_name=follow['node']['full_name'],
                collection='following'
            )
            yield item

    def user_followed_parse(self, response, username, user_id, variables):
        j_data = json.loads(response.text)
        page_info = j_data['data']['user']['edge_followed_by']['page_info']
        if page_info['has_next_page']:
            variables['after'] = page_info['end_cursor']
            url_followed = f'{self.graphql_url}query_hash={self.followed_hash}&{urlencode(variables)}'
            yield response.follow(
                url_followed,
                callback=self.user_followed_parse,
                cb_kwargs={'username': username,
                           'user_id': user_id,
                           'variables': deepcopy(variables)}
            )
        followeds = j_data['data']['user']['edge_followed_by']['edges']
        for followed in followeds:
            item = ParserInstItem(
                user_id=user_id,
                photo=followed['node']['profile_pic_url'],
                follow_name=followed['node']['username'],
                follow_id=followed['node']['id'],
                follow_full_name=followed['node']['full_name'],
                collection='followers'
            )
            yield item


    # Получаем токен для авторизации
    def fetch_csrf_token(self, text):
        matched = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return matched.split(':').pop().replace(r'"', '')

    # Получаем id желаемого пользователя
    def fetch_user_id(self, text, username):
        matched = re.search(
            '{\"id\":\"\\d+\",\"username\":\"%s\"}' % username, text
        ).group()
        return json.loads(matched).get('id')
