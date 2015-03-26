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
    last_author_key = 'last_author_id'
    subject_key = 'subject'

    def __init__(self, context, siteInfo):
        super(DailyTopicsDigest, self).__init__(context, siteInfo)

    def get_topics(self):
        retval = self.messageQuery.topics_sinse_yesterday(self.siteInfo.id,
                                                          self.groupInfo.id)
        assert type(retval) == list
        return retval

    def format_topic(self, topic):
        topic = super(DailyTopicsDigest, self).format_topic(topic)
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
