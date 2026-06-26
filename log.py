import logging

logging.basicConfig(
    level=logging.DEBUG,
    datefmt="%m/%d/%Y %I:%M:%S %p",
    format=(
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "%(asctime)s.%(msecs)03d | %(levelname)-8s\n"
        "Module : %(name)s\n"
        "Source : %(funcName)s:%(lineno)d\n"
        "Process: %(processName)s | Thread: %(threadName)s | Task: %(taskName)s\n"
        "Message: %(message)s\n"
    ),
)


