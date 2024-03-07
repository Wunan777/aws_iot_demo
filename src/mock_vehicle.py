import time
from uuid import uuid4
from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt, http
import argparse
from utilities.tool import get_client_id
from shadow.index import Shadow


def on_shadow_delta_updated
def parse_arguments():
    parser = argparse.ArgumentParser(description="描述您的程序")
    parser.add_argument("--endpoint", help="指定终端点地址")
    parser.add_argument("--cert", help="指定证书路径")
    parser.add_argument("--key", help="指定密钥路径")
    parser.add_argument("--ca_file", help="指定 CA 文件路径")
    parser.add_argument("--thing_name", help="设备名称")
    return parser.parse_args()


class Vehicle:
    def __init__(self) -> None:
        self.model = "tesla-model-s"
        self.color = "white"
        self.speed = 0
        self.location = "0.0,0.0"
        self.door_status = "unlocked"


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
    shadow_client = Shadow(mqtt_connection, shadow_thing_name)

    connected_future.result()
    print("Connected!")

    vehicle = Vehicle()
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
        time.sleep(86400)
