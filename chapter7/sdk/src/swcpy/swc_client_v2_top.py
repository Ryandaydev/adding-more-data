import httpx
import swcpy.swc_config as config <1>
from .schemas import League, Team, Player, Performance <2>
from typing import List <3>
import backoff <4>
import logging <5>
logger = logging.getLogger(__name__)

class SWCClient:
    """Interacts with the Sports World Central API.

        This SDK class simplifies the process of using the SWC fantasy
        football API. It supports all the functions of SWC API and returns
        validated datatypes.

    Typical usage example:

        client = SWCClient()
        response = client.get_health_check()

    """

    HEALTH_CHECK_ENDPOINT = "/" <6>
    LIST_LEAGUES_ENDPOINT = "/v0/leagues/"
    LIST_PLAYERS_ENDPOINT = "/v0/players/"
    LIST_PERFORMANCES_ENDPOINT = "/v0/performances/"
    LIST_TEAMS_ENDPOINT = "/v0/teams/"
    GET_COUNTS_ENDPOINT = "/v0/counts/"

    BULK_FILE_BASE_URL = (
        "https://raw.githubusercontent.com/[github ID]"
        + "/portfolio-project/main/bulk/"
    )

    #BULK_FILE_BASE_URL = ("https://raw.githubusercontent.com/Ryandaydev/adding-more-data/chapter7-work/bulk/")

    def __init__(self, input_config: config.SWCConfig): <7>
        """Class constructor that sets varibles from configuration object."""

        self.logger.debug(f"Bulk file base URL: {self.BULK_FILE_BASE_URL}")

        self.logger.debug(f"Input config: {input_config}")

        self.swc_base_url = input_config.swc_base_url
        self.backoff = input_config.swc_backoff
        self.backoff_max_time = input_config.swc_backoff_max_time
        self.bulk_file_format = input_config.swc_bulk_file_format

        self.BULK_FILE_NAMES = { <7>
            "players": "player_data",
            "leagues": "league_data",
            "performances": "performance_data",
            "teams": "team_data",
            "team_players": "team_player_data",
        }

        if self.backoff: <8>
            self.call_api = backoff.on_exception(
                wait_gen=backoff.expo,
                exception=(httpx.RequestError, httpx.HTTPStatusError),
                max_time=self.backoff_max_time,
                jitter=backoff.random_jitter,
            )(self.call_api)

        if self.bulk_file_format.lower() == "parquet": <9>
            self.BULK_FILE_NAMES = {
                key: value + ".parquet" for key, value in self.BULK_FILE_NAMES.items()
            }
        else:
            self.BULK_FILE_NAMES = {
                key: value + ".csv" for key, value in self.BULK_FILE_NAMES.items()
            }

        self.logger.debug(f"Bulk file dictionary: {self.BULK_FILE_NAMES}")
