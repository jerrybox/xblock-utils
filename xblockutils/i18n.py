# -*- coding: utf-8 -*-
#
# Copyright (C) 2018 OpenCraft
# License: AGPLv3

"""
This module contains a mixin that allows XBlocks to use locally translated text in python and HTML code.

Requires the i18n runtime service to be loaded on the XBlock:

    @XBlock.needs('i18n')
    MyXBlock(XBlock):
        ...

Translations files should be provided in the locale_path and domain configured by the i18n runtime's translator object.
See e.g. edx-platform's ModuleI18nService.
"""

# Imports ###########################################################

import logging

from django.utils.translation import trans_real, get_language

from xblock.exceptions import NoSuchServiceError

# Globals ###########################################################

log = logging.getLogger(__name__)

# Classes ###########################################################


class TranslationServiceMixin(object):
    """     
    Mixin which allows XBlocks to use locally translated strings.
            
    No-op if the XBlock doesn't enable the `i18n` service.
    """     
    def __init__(self, *args, **kwargs):
        """ 
        Adds the runtime `i18n` service translator to the currently selected language's translation processor.
        """
        super(TranslationServiceMixin, self).__init__(*args, **kwargs)
        try:
            i18n_service = self.runtime.service(self, "i18n")
            translation = trans_real.translation(get_language())
            translation.merge(i18n_service.translator)

        except NoSuchServiceError:
            log.warning("XBlock needs the i18n runtime service enabled to perform translations.")
    
    def _(self, text): 
        """ Translate text using the runtime `i18n` service"""
        try:
            i18n_service = self.runtime.service(self, "i18n")
            return i18n_service.ugettext(text)
        except NoSuchServiceError:
            return text
