import traceback
from awsiot import iotshadow
from concurrent.futures import Future
import logging


def exit(msg_or_exception):
    if isinstance(msg_or_exception, Exception):
        print("Exiting sample due to exception.")
        traceback.print_exception(
            msg_or_exception.__class__, msg_or_exception, sys.exc_info()[2]
        )
    else:
        print("Exiting sample:", msg_or_exception)


def on_disconnected(disconnect_future):
    # type: (Future) -> None
    print("Disconnected.")

    # Signal that sample is finished
    # is_sample_done.set()


def on_get_shadow_accepted(response):
    # type: (iotshadow.GetShadowResponse) -> None
    try:
        logging.debug("on_get_shadow_accepted : {}".format(response))
        return

    except Exception as e:
        exit(e)


def on_get_shadow_rejected(error):
    # type: (iotshadow.ErrorResponse) -> None
    try:
        if error.code == 404:
            print("Thing has no shadow document. Creating with defaults...")
        else:
            exit(
                "Get request was rejected. code:{} message:'{}'".format(
                    error.code, error.message
                )
            )

    except Exception as e:
        exit(e)


def on_shadow_delta_updated(delta):
    # type: (iotshadow.ShadowDeltaUpdatedEvent) -> None
    try:
        logging.debug("Received shadow delta event. :{}".format(delta))

    except Exception as e:
        exit(e)


def on_publish_update_shadow(future):
    # type: (Future) -> None
    try:
        future.result()
        print("Update request published.")
    except Exception as e:
        print("Failed to publish update request.")
        exit(e)


def on_update_shadow_accepted(response):
    # type: (iotshadow.UpdateShadowResponse) -> None
    try:
        # check that this is a response to a request from this session
        logging.debug("on_update_shadow_accepted: {}".format(response))
    except Exception as e:
        exit(e)


def on_update_shadow_rejected(error):
    # type: (iotshadow.ErrorResponse) -> None
    print(error)
    try:
        # check that this is a response to a request from this session
        exit(
            "Update request was rejected. code:{} message:'{}'".format(
                error.code, error.message
            )
        )

    except Exception as e:
        exit(e)
