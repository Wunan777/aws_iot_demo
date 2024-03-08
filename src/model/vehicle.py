import logging
from uuid import uuid4
from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt


locekd_car_image = (
    "                     _..-------++._                      \n"
    + "                 _.-'/ |      _||  \"--._              \n"
    + "           __.--'`._/_\j_____/_||___\    `----.        \n"
    + "      _.--'_____    |    locked        _____  /        \n"
    + "    _j    /,---.\   |        =o |   /,---.\   |_       \n"
    + "   [__]==// .-. \\==`===========/==// .-. \\=[__]      \n"
    + "     `-._|\ `-' /|___\_________/___|\ `-' /|_.'        \n"
    + "           `---'                     `---'             \n"
)


unlocekd_car_image = (
    "                     _..-------++._                      \n"
    + "                 _.-'/ |      _||  \"--._              \n"
    + "           __.--'`._/_\j_____/_||___\    `----.        \n"
    + "      _.--'_____    | unlocked|   _____       /        \n"
    + "    _j    /,---.\   |         o |   /,---.\   |_       \n"
    + "   [__]==// .-. \\==`===========/==// .-. \\=[__]      \n"
    + "     `-._|\ `-' /|___\_________/___|\ `-' /|_.'        \n"
    + "           `---'                     `---'             \n"
)


def on_publish_update_shadow(future):
    # type: (Future) -> None
    try:
        future.result()
        logging.debug("on_publish_update_shadow: Update request published.")
    except Exception as e:
        logging.error("Failed to publish update request.")
        exit(e)


class Vehicle:
    def __init__(self, model, color) -> None:

        self.model = model
        self.color = color

        self.door_status = "unlocked"
        self.speed = 0
        self.location = "0.0,0.0"

        self.shadow = None

    def lock_door(
        self,
    ):
        self.door_status = "locked"
        logging.info("\n" + locekd_car_image)

    def unlock_door(self):
        self.door_status = "unlocked"
        logging.info("\n" + unlocekd_car_image)

    def manage_door_status(self, desired_door_status):
        if self.door_status == desired_door_status:
            logging.info(
                "manage_door_status: vehicle_door_status - {}, is same as desired_door_status, no need to operation.".format(
                    desired_door_status
                )
            )
            return
        logging.debug(
            "manage_door_status desired_door_status: {}".format(desired_door_status)
        )
        if desired_door_status == "locked":
            self.lock_door()
        elif desired_door_status == "unlocked":
            self.unlock_door()
        else:
            logging.info("Invalid desired door-status: {}".format(desired_door_status))

        self.report()

    def conect_shadow(self, shadow):
        self.shadow = shadow

    def report(
        self,
    ):
        """
        @Des: report current status, sync to the remote.
        """
        if not self.shadow:
            raise Exception("The vehicle shadow not exist, can not report.")
        shadow_property = "door-status"
        reported = {shadow_property: self.door_status}
        token = str(uuid4())
        thing_name = self.shadow.shadow_thing_name
        request = iotshadow.UpdateShadowRequest(
            thing_name=thing_name,
            state=iotshadow.ShadowState(
                reported=reported,
            ),
            client_token=token,
        )
        logging.debug("vehicle report: {}".format(reported))
        future = self.shadow.publish_update_shadow(request, mqtt.QoS.AT_LEAST_ONCE)
        # future.result()
        future.add_done_callback(on_publish_update_shadow)
