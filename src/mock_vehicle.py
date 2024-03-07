import time
from uuid import uuid4
from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt, http
import argparse
from utilities.tool import get_client_id
from shadow.index import Shadow
from model.vehicle import Vehicle


vehicle = Vehicle()


def on_shadow_delta_updated(delta):
    pass


def on_update_shadow_accepted(response):

    # response.state.reported[shadow_property]
    desired = response.state.desired

    desired_door_status = desired["door-status"]
    actual_door_status = vehicle.door_status
    # When desired_status != actual_status,
    #   trigger `mange_door` event.
    if desired_door_status != actual_door_status:
        vehicle.manage_door_status(desired_door_status)
        vehicle.report()
    else:
        # No event trigger, No need to do.
        pass


def on_get_shadow_accepted():
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
    shadow_client = Shadow(mqtt_connection, shadow_thing_name)
    vehicle.conect_shadow(shadow_client)

    try:
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
