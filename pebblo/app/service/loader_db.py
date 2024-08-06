
class DBLoaderDoc():
    def __init__(self, data):
        self.data = data
        self.app_name = self.data.get("name")

    def process_request(self):
        pass
    # We can also implement stretegy on loader service, discovery service.