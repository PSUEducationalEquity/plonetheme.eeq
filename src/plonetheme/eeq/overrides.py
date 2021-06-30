from datetime import datetime
from zope.component import adapter
from zope.interface import implementer
from zope.schema._bootstrapfields import Field
from zope.schema._bootstrapfields import Orderable
from zope.schema.interfaces import IDatetime
from plone.app.z3cform.interfaces import IDatetimeWidget
from plone.app.z3cform.converters import DatetimeWidgetConverter


class ITileDatetime(IDatetime):
    """Datetime field to render in a tile"""


@implementer(ITileDatetime)
class TileDatetime(Orderable, Field):
    __doc__ = ITileDatetime.__doc__
    _type = datetime

    def __init__(self, *args, **kw):
        super(TileDatetime, self).__init__(*args, **kw)


@adapter(ITileDatetime, IDatetimeWidget)
class TileDatetimeWidgetConverter(DatetimeWidgetConverter):
    """Data converter for datetime fields in tiles.

    Since `plone.app.blocks.layoutbehavior.LayoutAwareTileDataStorage.__setitem__`
    invokes `json_compatible` before storing its data we need to skip the datetime to string
    conversion that the default converter does.
    """

    def toWidgetValue(self, value):
        """Converts from field value to widget.
        Overridden because we're being passed a string, but the parent class
        expects a datetime object.
        The format is also changed so that the patterns library datetime widget
        can use it: '2021-06-01T03:40:00' → '2021-06-30 09:00'.

        :param value: Field value.
        :type value: str or None (mysteriously not a datetime)

        :returns: Datetime in format `Y-m-d H:M`
        :rtype: string
        """
        return value and value.replace("T", " ")[:16]
