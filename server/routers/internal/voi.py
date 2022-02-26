from .service import Service

class VoiService(Service):
    

    def get_vehicles(self):
        pass

if __name__ == "__main__":
    voice_service = VoiService("TRANSPORTAPIAPPID", "TRANSPORTAPIAPPKEY")