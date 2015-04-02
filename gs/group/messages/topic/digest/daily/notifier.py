# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014, 2015 E-Democracy.org and Contributors.
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
from logging import getLogger
log = getLogger('gs.group.messages.topic.digest.daily.notifier')
from zope.component import createObject, getMultiAdapter
from zope.cachedescriptors.property import Lazy
from .topicsdigest import DailyTopicsDigest


class DailyDigestNotifier(object):
    weight = 10  # Used to determine the "best" notifier
    baseTemplate = 'gs-group-messages-topic-digest-daily'

    def __init__(self, group, request):
        self.context = self.group = group
        self.request = request

    @Lazy
    def siteInfo(self):
        retval = createObject('groupserver.SiteInfo', self.group)
        return retval

    @Lazy
    def groupInfo(self):
        retval = createObject('groupserver.GroupInfo', self.group)
        if not retval:
            msg = 'Could not create the GroupInfo from %s' % self.group
            raise ValueError(msg)
        return retval

    @Lazy
    def topicsDigest(self):
        retval = DailyTopicsDigest(self.context, self.siteInfo)
        return retval

    @Lazy
    def canSend(self):
        '''``True`` if we can send the daily digest; ``False`` otherwise.'''
        retval = self.topicsDigest.show_digest
        return retval

    @Lazy
    def text(self):
        'The daily digest of topics in plain-text (Unicode) form'
        templateName = '{0}.txt'.format(self.baseTemplate)
        textTemplate = getMultiAdapter((self.group, self.request),
                                       name=templateName)
        retval = textTemplate(topicsDigest=self.topicsDigest)
        assert retval
        return retval

    @Lazy
    def html(self):
        'The daily digest of topics in HTML form'
        templateName = '{0}.html'.format(self.baseTemplate)
        htmlTemplate = getMultiAdapter((self.group, self.request),
                                       name=templateName)
        retval = htmlTemplate(topicsDigest=self.topicsDigest)
        assert retval
        return retval

    @Lazy
    def subject(self):
        m = '{groupShortName} topic digest: {new_posts} new posts, '\
            '{new_topics} new topics'
        shortName = self.groupInfo.get_property('short_name',
                                                self.groupInfo.name)
        digestStats = self.topicsDigest.post_stats
        retval = m.format(groupShortName=shortName,
                          new_posts=digestStats['new_posts'],
                          new_topics=digestStats['new_topics'])
        assert retval
        return retval
