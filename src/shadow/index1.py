class Shadow(iotshadow.IotShadowClient):

    def __init__(self, mqtt_connection, shadow_thing_name):
        super().__init__(mqtt_connection)
        self.shadow_thing_name = shadow_thing_name
        self.subscribe_topic()

    def subscribe_topic(self):
        '''
            Subscribe to necessary topics.
            Note that is **is** important to wait for "accepted/rejected" subscriptions, to succeed before publishing the corresponding "request".
        '''
        # 1) Subscribe `update shadow` response.
        print("Subscribing to Update responses...")
        update_accepted_subscribed_future, _ = (
            self.subscribe_to_update_shadow_accepted(
                request=iotshadow.UpdateShadowSubscriptionRequest(
                    thing_name=self.shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_update_shadow_accepted,
            )
        )

        update_rejected_subscribed_future, _ = (
            self.subscribe_to_update_shadow_rejected(
                request=iotshadow.UpdateShadowSubscriptionRequest(
                    thing_name=self.shadow_thing_name
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
            self.subscribe_to_get_shadow_accepted(
                request=iotshadow.GetShadowSubscriptionRequest(
                    thing_name=self.shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_get_shadow_accepted,
            )
        )

        get_rejected_subscribed_future, _ = (
            self.subscribe_to_get_shadow_rejected(
                request=iotshadow.GetShadowSubscriptionRequest(
                    thing_name=self.shadow_thing_name
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
            self.subscribe_to_shadow_delta_updated_events(
                request=iotshadow.ShadowDeltaUpdatedSubscriptionRequest(
                    thing_name=self.shadow_thing_name
                ),
                qos=mqtt.QoS.AT_LEAST_ONCE,
                callback=on_shadow_delta_updated,
            )
        )
        # Wait for subscription to succeed
        delta_subscribed_future.result()
