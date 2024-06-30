class LaunchRecord:
    def __init__(self, \
            launch_id: str, \
            name: str, \
            latitude: str, \
            longitude: str, \
            net: int, \
            sunrise_timestamp: int, \
            hours_of_sunlight: float, \
            raan: float = None) -> None:
        
        self.launch_id = launch_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.net = net
        self.sunrise_timestamp = sunrise_timestamp
        self.hours_of_sunlight = hours_of_sunlight
        self.raan = raan

    def empty_record():
        return LaunchRecord("<none>", "", "", "", 0, 0, 0.0)
        
