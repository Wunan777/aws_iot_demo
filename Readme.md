# Deme for aws ioT core.

## Publish

```
python3 src/pub.py --endpoint ${endpoint} --cert ${cert_path} --key ${key_path} --ca_file ${ca_file_path}
```

## Subscribe

```
python3 src/sub.py --endpoint ${endpoint} --cert ${cert_path} --key ${key_path} --ca_file ${ca_file_path}
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