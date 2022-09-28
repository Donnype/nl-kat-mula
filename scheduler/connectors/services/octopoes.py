import random
from typing import List

from octopoes.connector.octopoes import OctopoesAPIConnector
from octopoes.models.types import ALL_TYPES

from scheduler.connectors.errors import exception_handler
from scheduler.models import OOI, ScanProfile, Organisation

from .services import HTTPService


class Octopoes:
    name = "octopoes"
    health_endpoint = None

    def __init__(self, *args, **kwargs):
        pass

    def get_random_objects(self, organisation_id: str, n: int) -> List[OOI]:
        oois = OctopoesAPIConnector().list(ALL_TYPES)

        oois = [OOI(primary_key=ooi.reference, scan_profile=ScanProfile(level=ooi.scan_profile.level, reference=ooi.reference)) for ooi in oois]
        if n >= len(oois):
            return oois

        return random.sample(oois, n)


class OctopoesV1(HTTPService):
    name = "octopoes"
    health_endpoint = None

    def __init__(self, host: str, source: str, orgs: List[Organisation]):
        self.orgs: List[Organisation] = orgs
        super().__init__(host, source)

    @exception_handler
    def get_objects(self, organisation_id: str) -> List[OOI]:
        """Get all oois from octopoes"""
        url = f"{self.host}/{organisation_id}/objects"
        response = self.get(url)
        return [OOI(**ooi) for ooi in response.json()]

    @exception_handler
    def get_random_objects(self, organisation_id: str, n: int) -> List[OOI]:
        """Get `n` random oois from octopoes"""
        url = f"{self.host}/{organisation_id}/objects/random"
        response = self.get(url, params={"amount": str(n)})
        return [OOI(**ooi) for ooi in response.json()]

    @exception_handler
    def get_object(self, organisation_id: str, reference: str) -> OOI:
        """Get an ooi from octopoes"""
        url = f"{self.host}/{organisation_id}"
        response = self.get(url, params={"reference": reference})
        return OOI(**response.json())

    def is_healthy(self) -> bool:
        healthy = True
        for org in self.orgs:
            if not self.is_host_healthy(self.host, f"/{org.id}{self.health_endpoint}"):
                return False

        return healthy
