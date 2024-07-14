    def get_bulk_player_file(self) -> bytes: <1>
        """Returns a bulk file with player data"""

        self.logger.debug("Entered get bulk player file")

        player_file_path = self.BULK_FILE_BASE_URL + self.BULK_FILE_NAMES["players"] <2>

        response = httpx.get(player_file_path, follow_redirects=True) <3>

        if response.status_code == 200:
            self.logger.debug("File downloaded successfully")
            return response.content <4>
