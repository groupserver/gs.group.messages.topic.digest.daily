# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2013, 2015 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from gs.group.messages.topic.digest.base import BaseTopicsDigest


class DailyTopicsDigest(BaseTopicsDigest):
    """ Represents the content of a daily digest.

        Dicts in the list provided by topics include the following
        attributes, in addition to the standard attributes:
            num_posts_today - Number of posts made in the topic today
            num_posts_total - Total number of posts in the topic
        """

    def __init__(self, context, siteInfo):
        super(DailyTopicsDigest, self).__init__(context, siteInfo)
        self.__dailyDigestQuery__ = None
        self.__last_author_key__ = 'last_author_id'
        self.__subject_key__ = 'subject'

    def __getTopics__(self):
        if self.__dailyDigestQuery__ is None:
            self.__dailyDigestQuery__ = \
                self.messageQuery.topics_sinse_yesterday(self.siteInfo.id,
                                                         self.groupInfo.id)

        retval = self.__dailyDigestQuery__
        assert type(retval) == list
        return retval

    def __formatTopic__(self, topic):
        topic = super(DailyTopicsDigest, self).__formatTopic__(topic)
        topic['num_posts_today'] = topic['num_posts_day']
        topic['num_posts_total'] = topic['num_posts']
        del topic['num_posts_day']
        del topic['num_posts']
        return topic

    @Lazy
    def show_digest(self):
        """ True if there has been a post made in the group in the previous
            24 hours."""
        retval = (self.post_stats['new_posts'] > 0)
        assert type(retval) == bool
        return retval
