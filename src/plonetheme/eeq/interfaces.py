# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""

from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from plone.supermodel import model
from plone.app.textfield import RichText
from zope import schema


class IPlonethemeEeqLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""

class ISettings(model.Schema):
    top_banner_body = schema.Text(
        title="Banner to display at the top of the site",
        description="You can use the placeholder <pre>${portal_url}</pre> to refer to assets",
        default="""
            <div class="container-fluid constrain-width banner">
                <div class="row py-3 banner-content">
                    <div class="col-xs-12 col-md-10 col-lg-8 offset-md-1 offset-lg-2">
                        <img alt="Important message follows"
                            class="float-left mr-3"
                            src="${portal_url}/++theme++psu-educational-equity/images/alert-icon-dark.png" />
                        <p>
                            <strong>Coronavirus updates:</strong>
                            To keep up with the latest from Penn State about the global
                            coronavirus outbreak, visit
                            <a href="https://sites.psu.edu/virusinfo/">
                                <b>the Coronavirus information website</b>
                            </a>.
                        </p>
                    </div>
                </div>
            </div>
        """,
    )
    top_banner_publication_date = schema.Date(
        title="Only publish after this date",
        description="This date is the first day the banner will be shown",
        required=False
    )
    top_banner_retire_date = schema.Date(
        title="Do not publish after this date",
        description="This date is the first day the banner will be hidden",
        required=False
    )
