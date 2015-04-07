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
from logging import getLogger
log = getLogger('gs.group.messages.topic.digest.daily')
from zope.cachedescriptors.property import Lazy
from gs.content.email.base import TextMixin
from gs.group.messages.topic.digest.base import TopicsDigestMessage
from .topicsdigest import DailyTopicsDigest


class DailyMessage(TopicsDigestMessage):
    @Lazy
    def digest(self):
        retval = DailyTopicsDigest(self.context, self.siteInfo)
        return retval


class DailyMessageText(DailyMessage, TextMixin):
    def __init__(self, group, request):
        super(DailyMessageText, self).__init__(group, request)
        f = 'gs-group-messages-topic-digest-daily-{0}-{1}.txt'
        filename = f.format(self.siteInfo.id, self.groupInfo.id)
        self.set_header(filename)
