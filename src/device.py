from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt, http
from uuid import uuid4
from shadow.callback_handler import (
    on_update_shadow_accepted,
    on_update_shadow_rejected,
    on_get_shadow_accepted,
    on_get_shadow_rejected,
    on_shadow_delta_updated,
)
import argparse
import time


def parse_arguments():
    parser = argparse.ArgumentParser(description="描述您的程序")
    parser.add_argument("--endpoint", help="指定终端点地址")
    parser.add_argument("--cert", help="指定证书路径")
    parser.add_argument("--key", help="指定密钥路径")
    parser.add_argument("--ca_file", help="指定 CA 文件路径")
    parser.add_argument("--shadow_thing_name", help="设备影子名称")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    endpoint = args.endpoint
    cert = args.cert
    key = args.key
    ca_file = args.ca_file
    # Connection port. AWS IoT supports 443 and 8883 (optional, default=8883)
    port = 8883
    client_id = "device-001"
    shadow_thing_name = args.shadow_thing_name
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
    shadow_client = iotshadow.IotShadowClient(mqtt_connection)
    connected_future.result()
    print("Connected!")

    try:
        # Subscribe to necessary topics.
        # Note that is **is** important to wait for "accepted/rejected" subscriptions
        # to succeed before publishing the corresponding "request".

        # 1) Subscribe `update shadow` response.
        print("Subscribing to Update responses...")
        update_accepted_subscribed_future, _ = (
            shadow_client.subscribe_to_update_shadow_accepted(
                request=iotshadow.UpdateShadowSubscriptionRequest(
                    thing_name=shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_update_shadow_accepted,
            )
        )

        update_rejected_subscribed_future, _ = (
            shadow_client.subscribe_to_update_shadow_rejected(
                request=iotshadow.UpdateShadowSubscriptionRequest(
                    thing_name=shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_update_shadow_rejected,
            )
        )

        # Wait for subscriptions to succeed
        update_accepted_subscribed_future.result()
        update_rejected_subscribed_future.result()

        # 2) Subscribe `get shadow` response.
        print("Subscribing to Get responses...")
        get_accepted_subscribed_future, _ = (
            shadow_client.subscribe_to_get_shadow_accepted(
                request=iotshadow.GetShadowSubscriptionRequest(
                    thing_name=shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_get_shadow_accepted,
            )
        )

        get_rejected_subscribed_future, _ = (
            shadow_client.subscribe_to_get_shadow_rejected(
                request=iotshadow.GetShadowSubscriptionRequest(
                    thing_name=shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_get_shadow_rejected,
            )
        )

        # Wait for subscriptions to succeed
        get_accepted_subscribed_future.result()
        get_rejected_subscribed_future.result()

        # 3) Subscribe `Delta` event,
        # When the shadow `desired val` and `reported val` not same, the `Delta` event will be pubilshed.
        print("Subscribing to Delta events...")
        delta_subscribed_future, _ = (
            shadow_client.subscribe_to_shadow_delta_updated_events(
                request=iotshadow.ShadowDeltaUpdatedSubscriptionRequest(
                    thing_name=shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_shadow_delta_updated,
            )
        )

        # Wait for subscription to succeed
        delta_subscribed_future.result()

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
        time.sleep(1)
