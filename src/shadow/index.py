import math
import time
import argparse
from awsiot import iotshadow, mqtt_connection_builder
from awscrt import mqtt
from uuid import uuid4
import utilities.shadow_callback_handler as defalut_callback_handler


class Shadow(iotshadow.IotShadowClient):
    def __init__(
        self,
        mqtt_connection,
        shadow_thing_name,
        on_update_shadow_accepted=None,
        on_update_shadow_rejected=None,
        on_get_shadow_accepted=None,
        on_get_shadow_rejected=None,
        on_shadow_delta_updated=None,
    ):
        super().__init__(mqtt_connection)
        self.shadow_thing_name = shadow_thing_name

        self.on_update_shadow_accepted = (
            on_update_shadow_accepted
            if on_update_shadow_accepted
            else defalut_callback_handler.on_update_shadow_accepted
        )
        self.on_update_shadow_rejected = (
            on_update_shadow_rejected
            if on_update_shadow_rejected
            else defalut_callback_handler.on_update_shadow_rejected
        )
        self.on_get_shadow_accepted = (
            on_get_shadow_accepted
            if on_get_shadow_accepted
            else defalut_callback_handler.on_get_shadow_accepted
        )
        self.on_get_shadow_rejected = (
            on_get_shadow_rejected
            if on_get_shadow_rejected
            else defalut_callback_handler.on_get_shadow_rejected
        )
        self.on_shadow_delta_updated = (
            on_shadow_delta_updated
            if on_shadow_delta_updated
            else defalut_callback_handler.on_shadow_delta_updated
        )

        self.subscribe_topic()

    def subscribe_topic(self):
        """
        Subscribe to necessary topics.
        Note that is **is** important to wait for "accepted/rejected" subscriptions, to succeed before publishing the corresponding "request".
        """
        # 1) Subscribe `update shadow` response.
        print("Subscribing to Update responses...")
        update_accepted_subscribed_future, _ = self.subscribe_to_update_shadow_accepted(
            request=iotshadow.UpdateShadowSubscriptionRequest(
                thing_name=self.shadow_thing_name
            ),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.on_update_shadow_accepted,
        )

        update_rejected_subscribed_future, _ = self.subscribe_to_update_shadow_rejected(
            request=iotshadow.UpdateShadowSubscriptionRequest(
                thing_name=self.shadow_thing_name
            ),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.on_update_shadow_rejected,
        )
        # Wait for subscriptions to succeed
        update_accepted_subscribed_future.result()
        update_rejected_subscribed_future.result()

        # 2) Subscribe `get shadow` response.
        print("Subscribing to Get responses...")
        get_accepted_subscribed_future, _ = self.subscribe_to_get_shadow_accepted(
            request=iotshadow.GetShadowSubscriptionRequest(
                thing_name=self.shadow_thing_name
            ),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.on_get_shadow_accepted,
        )

        get_rejected_subscribed_future, _ = self.subscribe_to_get_shadow_rejected(
            request=iotshadow.GetShadowSubscriptionRequest(
                thing_name=self.shadow_thing_name
            ),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.on_get_shadow_rejected,
        )
        # Wait for subscriptions to succeed
        get_accepted_subscribed_future.result()
        get_rejected_subscribed_future.result()

        # 3) Subscribe `Delta` event,
        # When the shadow `desired val` and `reported val` not same, the `Delta` event will be pubilshed.
        print("Subscribing to Delta events...")
        delta_subscribed_future, _ = self.subscribe_to_shadow_delta_updated_events(
            request=iotshadow.ShadowDeltaUpdatedSubscriptionRequest(
                thing_name=self.shadow_thing_name
            ),
            qos=mqtt.QoS.AT_LEAST_ONCE,
            callback=self.on_shadow_delta_updated,
        )
        # Wait for subscription to succeed
        delta_subscribed_future.result()

    def change_desired_value(self, desired=None):

        if desired is None:
            raise Exception("change_shadow_value error: desired is None.")

        token = str(uuid4())
        request = iotshadow.UpdateShadowRequest(
            thing_name=self.shadow_thing_name,
            state=iotshadow.ShadowState(
                desired=desired,
            ),
            client_token=token,
        )

        future = self.publish_update_shadow(request, mqtt.QoS.AT_LEAST_ONCE)
        future.result()
