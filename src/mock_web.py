import time
import argparse
from awsiot import mqtt_connection_builder
from utilities.tool import get_client_id
from shadow.index import Shadow
import logging
a = ("                 _________________________________________                                "+"\n"+
"               .'  _____________________________________  '.                              "+"\n"+
"              "| .'                                     '. |                              "+"\n"+
"              "| |                                       | |                              "+"\n"+
"              "| |  {                                    | |                              "+"\n"+
"              "| |    cout << "Vopec_" << endl;          | |                              "+"\n"+
"              "| |    return 0;                          | |                              "+"\n"+
"              "| |  }                                    | |                              "+"\n"+
"              "| |                                       | |                              "+"\n"+
"              "| '._____________________________________.' |`*.                           "+"\n"+
"              "'._________________________________________.'   `.                         "+"\n"+
"               """"""""""""""""""|.   .|""""""""""""""""""      '                         "+"\n"+
"          ----------------------__|   |__------------------------`--------------          "+"\n"+
"         /                     /_________\.......-----------.     `.            \         "+"\n"+
"        /       _________________________________________    )       `.          \        "+"\n"+
"       /      "/ .-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.  ---  \_.'         _;___       \       "+"\n"+
"      /      "/ .---.-.-.-.-.-.-.-.-.-.-.-.-.-.-.--.  .-. \          /" \  \       \      "+"\n"+
"     /      "/ .-.-. .---.-.-.-.-.--.-.-.-.-.-`__`. .-.-.-.\         \""    \       \     "+"\n"+
"    /      "/ .-.-. .-----.-.-.-.-.-.-.-.-.-.-.-----. .-.-. \         \""    \       \    "+"\n"+
"   /      ":-------------------------------------------------:         \""    \       \   "+"\n"+
"  /       "`---._.-------------------------------------._.---'          '=---='        \  "+"\n"+
" /                                                                                      \ "+"\n"+
"------------------------------------------------------------------------------------------"+"\n")

#         _______________________________________
#        |,---"-----------------------------"---,|
#        ||___    16 bit....................    ||
#        ||====\ :HHHHHHHHHHHHHHHHHHHHHHHHHHH   ||
#        ||=====):H c> pb#                  H   ||
#        ||====/ :H                         H   ||
#        ||"""   :H                         H   ||
#        ||PORTFO:H                         H   ||
#        ||      :HHHHHHHHHHHHHHHHHHHHHHHHHHH   ||
#        ||_____,_________________________,_____||
#        |)_____)-----.| /I\ATARI |.------(_____(|
#      //"""""""|_____|=----------=|______|"""""""\
#     // _| _| _| _| _| _| _| _| _| _| _| _| _| _| \
#    // ___| _| _| _| _| _| _| _| _| _| _| _|  |  | \
#   |/ ___| _| _| _| _| _| _| _| _| _| _| _| ______| \
#   / __| _| _| _| _| _| _| _| _| _| _| _| _| _| ___| \
#  / _| _| _| _| ________________________| _| _| _| _| \
# |------"--------------------------------------"-------|
# `-----------------------------------------------------'
# pb

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
    client_id = get_client_id("vehicle-controll-app")
    thing_name = args.thing_name

    # Same-name variables: shadow_thing_name,
    # In aws iot core shadow service, there
    shadow_thing_name = thing_name

    print(thing_name)
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

    shadow_client = Shadow(mqtt_connection, thing_name)

    print("Hi, I'm monitor website, will monitor the device: {}.".format(thing_name))
    print("Monitoring ....")

    shadow_client.query_remote_shadow()

    while True:
        time.sleep(86400 * 1)
