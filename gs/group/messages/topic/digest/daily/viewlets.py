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
from textwrap import fill
from gs.group.messages.topic.digest.base import TopicsDigestViewlet
from .topicsdigest import DailyTopicsDigest


class DailyTopicsDigestViewlet(TopicsDigestViewlet):
    """ Viewlet used to pull data for daily topics digests. """

    def __init__(self, context, request, view, manager):
        super(DailyTopicsDigestViewlet, self).__init__(context, request,
                                                       view, manager)
        self.__topicsDigest__ = DailyTopicsDigest(self.context,
                                                  self.siteInfo)


class DailyTopicsDigestViewletTxt(DailyTopicsDigestViewlet):
    def summary(self):
        if self.topicsDigest.post_stats['new_posts'] == 1:
            postStats = 'there has been a new post'
        else:
            s = 'there have been {0} new posts'
            postStats = s.format(self.topicsDigest.post_stats['new_posts'])

        newTopicStats = ''
        if self.topicsDigest.post_stats['new_topics'] == 1:
            newTopicStats = 'a new topic'
        elif self.topicsDigest.post_stats['new_topics'] >= 1:
            s = '{0} new topics'
            newTopicStats = s.format(
                self.topicsDigest.post_stats['new_topics'])

        existingTopicStats = ''
        if self.topicsDigest.post_stats['existing_topics'] == 1:
            existingTopicStats = 'an existing topic'
        elif self.topicsDigest.post_stats['existing_topics'] >= 1:
            s = '{0} existing topics'
            existingTopicStats = s.format(
                self.topicsDigest.post_stats['existing_topics'])

        if newTopicStats and existingTopicStats:
            topicStats = ' and '.join((newTopicStats, existingTopicStats))
        elif newTopicStats:
            topicStats = newTopicStats
        else:
            topicStats = existingTopicStats

        r = 'Since yesterday {0} made to {1} in {2}.'
        summary = r.format(postStats, topicStats, self.groupInfo.name)
        retval = fill(summary, 72)
        return retval
