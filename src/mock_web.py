import time
import argparse
from awsiot import mqtt_connection_builder
from utilities.tool import get_client_id
from shadow.index import Shadow
import logging
import os
from utilities.view import Render


def render_website_view(response):
    try:
        reported = response.state.reported
        door_status = reported["door-status"]
        website_view = Render.get_monitor_website_view("", "", door_status)
        # os.system("clear")
        logging.info(website_view)
    except Exception as err:
        print(err)


def on_shadow_delta_updated(delta):
    # 如果某个属性位于 reported 部分，但在 desired 部分没有等效值，则不会包含在内。
    # 如果某个属性位于 desired 部分，但在 reported 部分没有等效值，则将包含在内。
    # 如果某个属性已从 reported 部分删除，但仍存在于 desired 部分，则将包含在内。
    # monitor website: No need to deal with the delta.
    pass


def on_update_shadow_accepted(response):
    # logging.debug("on_update_shadow_accepted recv:{}".format(response))
    # desired = response.state.desired
    # desired_door_status = desired["door-status"]
    # vehicle.manage_door_status(desired_door_status)
    print(123)
    print(223)
    print(response)

    # awsiot.iotshadow.UpdateShadowResponse(
    #     client_token="87d771d9-70bb-4cee-ad4c-c3b93abbc3d3",
    #     metadata=awsiot.iotshadow.ShadowMetadata(
    #         desired=None, reported={"door-status": {"timestamp": 1709918914}}
    #     ),
    #     state=awsiot.iotshadow.ShadowState(
    #         desired=None,
    #         desired_is_nullable=False,
    #         reported={"door-status": "unlocked"},
    #         reported_is_nullable=False,
    #     ),
    #     timestamp=datetime.datetime(2024, 3, 9, 1, 28, 34),
    #     version=21237,
    # )
    print(response.state)
    print(response.state.reported)
    try:
        reported = response.state.reported
        door_status = reported.get("door-status")
        print(door_status)
        website_view = Render.get_monitor_website_view("", "", door_status)
        print(website_view)
        # os.system("clear")
        logging.info(website_view)
        render_website_view(response)
    except Exception as err:
        print(err)


def on_get_shadow_accepted(response):
    render_website_view(response)


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
    # Connection port. AWS IoT supports 443 and 8883 (optional, default=8883)
    port = 8883
    client_id = get_client_id("monitor-website")
    thing_name = args.thing_name

    # Same-name variables: shadow_thing_name,
    # In aws iot core shadow service, there
    shadow_thing_name = thing_name

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
    print("mqtt Connected!")

    shadow_client = Shadow(
        mqtt_connection,
        thing_name,
        on_update_shadow_accepted=on_update_shadow_accepted,
        on_update_shadow_rejected=None,
        on_get_shadow_accepted=None,
        on_get_shadow_rejected=None,
        on_shadow_delta_updated=None,
    )

    print("Hi, I'm monitor website, will monitor the device: {}.".format(thing_name))
    print("Monitoring ....")

    shadow_client.query_remote_shadow()

    while True:
        time.sleep(1)
