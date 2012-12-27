from __future__ import absolute_import
import os

import readability

from readables.backends import BaseBackend

API_KEY = os.environ['READABILITY_API_KEY']
API_SECRET = os.environ['READABILITY_API_SECRET']

# XAUTH_TOKEN = readability.xauth(API_KEY, API_SECRET, USERNAME, PASSWORD)
XAUTH_TOKEN = (
    os.environ['READABILITY_XAUTH_TOKEN_0'],
    os.environ['READABILITY_XAUTH_TOKEN_1'],
)


class Backend(BaseBackend):
    def get_token(self):
        return XAUTH_TOKEN

    def _get_user(self):
        token = self.get_token()
        self.api = readability.oauth(API_KEY, API_SECRET, token=token)
        return self.api.get_me()

    def _get_bookmarks(self, **filters):
        return self._get_user().bookmarks(**filters)

    def _get_archives(self):
        return self._get_bookmarks(archived_since=self.start_date,
                                   archived_until=self.end_date)

    def get_report(self):
        archives = self._get_archives()
        return {
            'n_words': sum([b.article.word_count for b in archives]),
            'n_articles': len(archives),
            'longest_article': None,
            'most_esoteric_article': None,
            'articles_per_day': None,
            'top_sites': None,
            'words_by_language': None,
            'topics': None,
        }
