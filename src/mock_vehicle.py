import time
from uuid import uuid4
from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt, http
import argparse
from utilities.tool import get_client_id
from shadow.index import Shadow
from model.vehicle import Vehicle
import logging

logging.basicConfig(encoding="utf-8", level=logging.INFO)

vehicle = Vehicle(model="tesla-model-s", color="white")


def on_shadow_delta_updated(delta):
    # 如果某个属性位于 reported 部分，但在 desired 部分没有等效值，则不会包含在内。
    # 如果某个属性位于 desired 部分，但在 reported 部分没有等效值，则将包含在内。
    # 如果某个属性已从 reported 部分删除，但仍存在于 desired 部分，则将包含在内。
    logging.debug("on_shadow_delta_updated recv: {}".format(delta))
    desired_door_status = delta.state["door-status"]
    vehicle.manage_door_status(desired_door_status)


def on_update_shadow_accepted(response):
    logging.debug("on_update_shadow_accepted recv:{}".format(response))
    desired = response.state.desired
    desired_door_status = desired["door-status"]
    vehicle.manage_door_status(desired_door_status)


def on_get_shadow_accepted(response):
    logging.debug("on_get_shadow_accepted recv: {}".format(response))
    if response.state:
        if response.state.desired:
            desired = response.state.desired
            desired_door_status = desired["door-status"]
            vehicle.manage_door_status(desired_door_status)


def parse_arguments():
    parser = argparse.ArgumentParser(description="描述您的程序")
    parser.add_argument("--endpoint", help="指定终端点地址")
    parser.add_argument("--cert", help="指定证书路径")
    parser.add_argument("--key", help="指定密钥路径")
    parser.add_argument("--ca_file", help="指定 CA 文件路径")
    parser.add_argument("--thing_name", help="设备名称")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    endpoint = args.endpoint
    cert = args.cert
    key = args.key
    ca_file = args.ca_file
    port = (
        8883  # Connection port. AWS IoT supports 443 and 8883 (optional, default=8883)
    )
    client_id = get_client_id("vehicle")
    shadow_thing_name = args.thing_name

    print(shadow_thing_name)
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        port=port,
        cert_filepath=cert,
        pri_key_filepath=key,
        ca_filepath=ca_file,
        client_id=client_id,
        clean_session=False,
        keep_alive_secs=30,
        http_proxy_options=None,
    )

    connected_future = mqtt_connection.connect()
    connected_future.result()
    print("Connected!")

    # Initilize shadow.
    shadow_client = Shadow(
        mqtt_connection,
        shadow_thing_name,
        on_update_shadow_accepted=on_get_shadow_accepted,
        on_update_shadow_rejected=None,
        on_get_shadow_accepted=on_update_shadow_accepted,
        on_get_shadow_rejected=None,
        on_shadow_delta_updated=on_shadow_delta_updated,
    )
    vehicle.conect_shadow(shadow_client)

    shadow_client.query_remote_shadow()

    # Mock Vehicle online, loop report to the remote.
    while True:
        vehicle.report()
        time.sleep(1)
