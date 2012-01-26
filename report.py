import datetime
import sys

import readability

from auth import API_KEY, API_SECRET, XAUTH_TOKEN


api = readability.oauth(API_KEY, API_SECRET, token=XAUTH_TOKEN)


def parse_date(raw_date):
    return datetime.datetime.strptime(raw_date, '%Y-%m-%d')


def get_archives(archived_since, archived_until=None):
    if not archived_until:
        archived_until = archived_since + datetime.timedelta(days=1)
    filters = {
        'archived_since': archived_since,
        'archived_until': archived_until,
    }
    user = api.get_me()
    return user.bookmarks(**filters)


def word_count_by_date(bookmarks):
    pass


def get_unread():
    return api.get_me().bookmarks(archive=False)


def main():
    today = datetime.datetime.combine(datetime.date.today(), datetime.time())
    archived_since = today
    archived_until = None
    if len(sys.argv) > 1:
        archived_since = parse_date(sys.argv[1])
    if len(sys.argv) > 2:
        archived_until = parse_date(sys.argv[2])

    archives = get_archives(archived_since, archived_until)
    unread = get_unread()

    print 'Articles read:'
    for bookmark in archives:
        if bookmark.favorite:
            print '  *',
        else:
            print '  -',
        print bookmark.article.title.encode('utf8'),
        print '(%d words)' % bookmark.article.word_count
    print '============'
    print 'Total articles: %d' % len(archives)
    print 'Total words: %d' % sum([b.article.word_count for b in archives])
    print '============'
    print 'Unread articles: %d' % len(unread)
    print 'Unread words: %d' % sum([b.article.word_count for b in unread])


if __name__ == '__main__':
    main()
