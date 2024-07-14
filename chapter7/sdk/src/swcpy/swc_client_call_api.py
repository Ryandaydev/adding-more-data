    def call_api(self, <1>
            api_endpoint: str, <2>
            api_params: dict = None <3>
        ) -> httpx.Response: <4>
        """Makes API call and logs errors."""

        if api_params: 
            api_params = {key: val for key, val in api_params.items() if val is not None} <5>

        try:
            with httpx.Client(base_url=self.swc_base_url) as client:  <6>
                self.logger.debug(f"base_url: {self.swc_base_url}, api_endpoint: {api_endpoint}, api_params: {api_params}") <7>
                response = client.get(api_endpoint, params=api_params)
                self.logger.debug(f"Response JSON: {response.json()}")
                return response
        except httpx.HTTPStatusError as e:
            self.logger.error(
                f"HTTP status error occurred: {e.response.status_code} {e.response.text}"
            )
            raise
        except httpx.RequestError as e:
            self.logger.error(f"Request error occurred: {str(e)}")
            raise