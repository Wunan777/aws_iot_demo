from uuid import uuid4
from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt


class Vehicle:
    def __init__(
        self,
    ) -> None:

        self.model = "tesla-model-s"
        self.color = "white"
        self.speed = 0
        self.location = "0.0,0.0"
        self.door_status = "unlocked"

        self.shadow = None
        self.shadow_thing_name = ""

    def lock_door(
        self,
    ):
        self.door_status = "locked"

    def unlock_door(self):
        self.door_status = "unlocked"

    def manage_door_status(self, desired_door_status):

        if desired_door_status == "locked":
            self.lock_door()
        elif desired_door_status == "unlocked":
            self.unlock_door()
        else:
            print("Invalid desired door-status: {}".format(desired_door_status))

        # Report vehicle status.
        self.report({"door-status": self.door_status})

    def conect_shadow(self, thing_name, shadow):
        self.shadow = shadow

    def report(
        self,
    ):
        """
        @Des: report current status, sync to the remote.
        """
        if not self.shadow:
            raise Exception("The vehicle shadow not exist, can not report.")

        reported = {"door_status": self.door_status}
        token = str(uuid4())
        thing_name = self.shadow.shadow_thing_name
        request = iotshadow.UpdateShadowRequest(
            thing_name=thing_name,
            state=iotshadow.ShadowState(
                reported=reported,
            ),
            client_token=token,
        )

        future = self.publish_update_shadow(request, mqtt.QoS.AT_LEAST_ONCE)
        future.result()
