from __future__ import annotations

from workshop_b2.models import Device, Site, Country, Tag


class CountryModel(Country):
    pass


class SiteModel(Site):
    pass


class DeviceModel(Device):
    site: SiteModel | None = None


class TagModel(Tag):
    pass
