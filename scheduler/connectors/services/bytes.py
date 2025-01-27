from typing import Optional

from scheduler.connectors.errors import exception_handler
from scheduler.models import BoefjeMeta

from .services import HTTPService
from boefjes.clients.data import BOEFJE_METAS


class Bytes:
    name = "bytes"

    def __init__(self, *args, **kwargs):
        pass

    def get_last_run_boefje(self, boefje_id: str, input_ooi: str, organization_id: str) -> Optional[BoefjeMeta]:
        boefje_metas = [bm for bm in BOEFJE_METAS.values() if
                            bm.input_ooi == input_ooi and
                            bm.organization == organization_id and
                            bm.boefje.id == boefje_id
                        ]

        if not boefje_metas:
            return None

        boefje_metas = sorted(boefje_metas, key=lambda x: x.ended_at)

        return BoefjeMeta(**boefje_metas.pop(0).dict())

    def get_last_run_boefje_by_organisation_id(self, organization_id: str) -> Optional[BoefjeMeta]:
        url = f"{self.host}/bytes/boefje_meta"
        response = self.get(
            url=url,
            params={
                "organization": organization_id,
                "limit": 1,
                "descending": "true",
            },
        )
        if response.status_code == 200 and response.content:
            return BoefjeMeta(**response.json()[0])

        return None


class BytesV1(HTTPService):
    name = "bytes"

    def __init__(self, host: str, source: str, user: str, password: str, timeout: int = 5):
        self.user: str = user
        self.password: str = password

        super().__init__(host=host, source=source, timeout=timeout)

        self.token = self._get_token(
            user=self.user,
            password=self.password,
        )

        self.headers.update({"Authorization": f"Bearer {self.token}"})

    def _get_token(self, user: str, password: str) -> str:
        url = f"{self.host}/token"
        response = self.post(
            url=url,
            payload={"username": user, "password": password},
            headers={"Content-Type": "application/x-www-form-urlendcoded"},
        )
        return str(response.json()["access_token"])

    @exception_handler
    def get_last_run_boefje(self, boefje_id: str, input_ooi: str, organization_id: str) -> Optional[BoefjeMeta]:
        url = f"{self.host}/bytes/boefje_meta"
        response = self.get(
            url=url,
            params={
                "boefje_id": boefje_id,
                "input_ooi": input_ooi,
                "organization": organization_id,
                "limit": 1,
                "descending": "true",
            },
        )
        if response.status_code == 200 and len(response.json()) > 0:
            return BoefjeMeta(**response.json()[0])

        return None

    @exception_handler
    def get_last_run_boefje_by_organisation_id(self, organization_id: str) -> Optional[BoefjeMeta]:
        url = f"{self.host}/bytes/boefje_meta"
        response = self.get(
            url=url,
            params={
                "organization": organization_id,
                "limit": 1,
                "descending": "true",
            },
        )
        if response.status_code == 200 and response.content:
            return BoefjeMeta(**response.json()[0])

        return None
