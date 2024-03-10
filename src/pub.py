from awscrt import mqtt, http
from awsiot import mqtt_connection_builder
from uuid import uuid4

import time
import json
from utilities.conn_callback_handler import (
    on_connection_interrupted,
    on_connection_resumed,
    on_connection_success,
    on_connection_failure,
    on_connection_closed,
)
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="描述您的程序")
    parser.add_argument("--endpoint", help="指定终端点地址")
    parser.add_argument("--cert", help="指定证书路径")
    parser.add_argument("--key", help="指定密钥路径")
    parser.add_argument("--ca_file", help="指定 CA 文件路径")
    return parser.parse_args()


if __name__ == "__main__":
    # Create the proxy options if the data is present in cmdData
    proxy_options = None

    args = parse_arguments()
    endpoint = args.endpoint
    cert = args.cert
    key = args.key
    ca_file = args.ca_file
    topic = "test/topic1"
    # Connection port. AWS IoT supports 443 and 8883 (optional, default=8883)
    port = 8883
    client_id = "publisher-" + str(uuid4())
    # Create a MQTT connection from the command line data
    mqtt_connection = mqtt_connection_builder.mtls_from_path(
        endpoint=endpoint,
        port=port,
        cert_filepath=cert,
        pri_key_filepath=key,
        ca_filepath=ca_file,
        on_connection_interrupted=on_connection_interrupted,
        on_connection_resumed=on_connection_resumed,
        client_id=client_id,
        clean_session=False,
        # Session
        # 保持活动状态值（以秒为单位），在 CONNECT请求中发送。在此时间间隔内将自动发送 ping。如果服务器在此值的 1.5 倍之后没有收到 ping，假定连接丢失。
        keep_alive_secs=30,
        http_proxy_options=proxy_options,
        on_connection_success=on_connection_success,
        on_connection_failure=on_connection_failure,
        on_connection_closed=on_connection_closed,
    )

    # Connect.
    print("Connecting to {} with client ID '{}'...".format(endpoint, client_id))
    connect_future = mqtt_connection.connect()
    connect_future.result()
    # The function publish is no-blocking, and the return detail as below.
    # Returns:
    # Tuple[concurrent.futures.Future, int]:
    #   Tuple containing a Future and the ID of the PUBLISH packet.
    # ---
    # The QoS determines when the Future completes:
    # For QoS 0, completes as soon as the packet is sent.
    # For QoS 1, completes when PUBACK is received.
    # For QoS 2, completes when PUBCOMP is received.
    while True:
        print("Please input the message: ")
        user_input = input()
        print("Your input: {}".format(user_input))

        # Publish.
        message_json = json.dumps(user_input)

        pub_res = mqtt_connection.publish(
            topic=topic, payload=message_json, qos=mqtt.QoS.AT_LEAST_ONCE
        )

        # Here for the QoS 1,
        # When just after publishing, pub_res state is 'pending'
        # print(pub_res)
        # Or you can use `pub_res[0].result()`, which will block here until the PUBACK is received.
        # time.sleep(10)
        # When PUBACK is received, pub_res state is 'finished'
        # print(pub_res)

    # Disconnect.
    print("Disconnecting...")
    disconnect_future = mqtt_connection.disconnect()
    disconnect_future.result()
    print("Disconnected!")
