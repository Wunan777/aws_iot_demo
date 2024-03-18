import os
import argparse
import logging
from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt, http
from uuid import uuid4
from utilities.tool import get_client_id
from shadow.index import Shadow
from utilities.view import Render

logging.basicConfig(encoding="utf-8", level=logging.INFO)


def on_update_shadow_accepted(response):
    pass


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
    client_id = get_client_id("controll-app")
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
    # shadow_client = iotshadow.IotShadowClient(mqtt_connection)
    shadow_client = Shadow(
        mqtt_connection,
        shadow_thing_name,
        on_update_shadow_accepted=on_update_shadow_accepted,
        on_update_shadow_rejected=None,
        on_get_shadow_accepted=None,
        on_get_shadow_rejected=None,
        on_shadow_delta_updated=None,
    )

    connected_future.result()
    print("Connected!")

    try:
        # The rest of the sample runs asynchronously.
        # Issue request for shadow's current state.
        # The response will be received by the on_get_accepted() callback
        print("Requesting current shadow state...")
        token = str(uuid4())
        publish_get_future = shadow_client.publish_get_shadow(
            request=iotshadow.GetShadowRequest(
                thing_name=shadow_thing_name, client_token=token
            ),
            qos=mqtt.QoS.AT_LEAST_ONCE,
        )
        publish_get_future.result()

    except Exception as e:
        exit(e)

    while True:
        # Read user input
        os.system("clear")
        print("Please input 1 or 2")
        app_screen = Render.get_app_screen()
        logging.info("\n" + app_screen)

        cmd = input()
        # print("Your input: {}".format(cmd))
        if cmd == "1":
            shadow_client.change_desired_value(desired={"door-status": "locked"})
        elif cmd == "2":
            shadow_client.change_desired_value(desired={"door-status": "unlocked"})
        else:
            print("Invalid input, please try again.")
