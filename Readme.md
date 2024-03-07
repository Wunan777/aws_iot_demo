# Deme for aws ioT core.

# Demo1: `Message pub - sub`

## Publish

```
python3 src/pub.py --endpoint ${endpoint} --cert ${cert_path} --key ${key_path} --ca_file ${ca_file_path}
```

## Subscribe

```
python3 src/sub.py --endpoint ${endpoint} --cert ${cert_path} --key ${key_path} --ca_file ${ca_file_path}
```

# Demo2: `Device shadow`

## Scenario:

In this scenario, device is the vehicle, and we will controll the vehicle with the `vehicle controll app`.
Press the `door unlock button` in the `vehicle controll app` to unlock the `vehicle`.

## Steps:

- step1: The vechile on online.

```
python3 src/device.py --endpoint ${endpoint} --cert ${cert_path} --key ${key_path} --ca_file ${ca_file_path} --thing_name=${vehicle_id}
```

- step2: Mock the door unlocking operation in `vehicle controll app`,

```
python3 src/mock_app.py --endpoint ${endpoint} --cert ${cert_path} --key ${key_path} --ca_file ${ca_file_path} --thing_name=${vehicle_id}
```

- step3: Mock the `vehicle monitor platform` website, for the purpose of monitoring multi-end sync.

```
python3 src/mock_app.py --endpoint ${endpoint} --cert ${cert_path} --key ${key_path} --ca_file ${ca_file_path} --thing_name=${vehicle_id}
```

"--endpoint",
"a2ht2a7mp6bug7-ats.iot.us-east-1.amazonaws.com",
"--cert",
"/Users/nanwu/Documents/GitHub/aws_iot_demo/light01_cert/light01.pem.crt",
"--key",
"/Users/nanwu/Documents/GitHub/aws_iot_demo/light01_cert/light01-private.pem.key",
"--ca_file",
"/Users/nanwu/certs/AmazonRootCA1.pem",
"--thing_name",
"light01",
"--shadow_property",
"color"
python3 pub.py --endpoint "a2ht2a7mp6bug7-ats.iot.us-east-1.amazonaws.com" --cert "/Users/nanwu/Documents/GitHub/aws_iot_demo/light01_cert/light01.pem.crt" --key "/Users/nanwu/Documents/GitHub/aws_iot_demo/light01_cert/light01-private.pem.key" --ca_file "/Users/nanwu/certs/AmazonRootCA1.pem"
