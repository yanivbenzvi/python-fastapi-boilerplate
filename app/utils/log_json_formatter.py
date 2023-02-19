import json

from pythonjsonlogger import jsonlogger

DATE_FORMAT_TIMEZONE = "%Y-%m-%dT%H:%M:%S.%fZ"


class JsonFormatter(jsonlogger.JsonFormatter):
    EXTRA_PREFIX = "extra_"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # update the timestamp format
        log_record["timestamp"] = log_record["timestamp"].utcnow().strftime(DATE_FORMAT_TIMEZONE)
        log_record["level"] = record.levelname
        log_record["type"] = "log"
        log_record["level_num"] = record.levelno
        log_record["logger_name"] = record.name
        trace = self._get_trace_id()

        if trace:
            log_record["trace_id"] = trace

        self.set_extra_keys(record, log_record, self._skip_fields)

    @staticmethod
    def is_private_key(key):
        return hasattr(key, "startswith") and key.startswith("_")

    @staticmethod
    def is_extra_key(key):
        return hasattr(key, "startswith") and key.startswith(JsonFormatter.EXTRA_PREFIX)

    @staticmethod
    def set_extra_keys(record, log_record, reserved):
        """
        Add the extra data to the log record.
        prefix will be added to all custom tags.
        """
        record_items = list(record.__dict__.items())
        records_filtered_reserved = [item for item in record_items if item[0] not in reserved]
        records_filtered_private_attr = [item for item in records_filtered_reserved if
                                         not JsonFormatter.is_private_key(item[0])]

        for key, value in records_filtered_private_attr:
            if not JsonFormatter.is_extra_key(key):
                if isinstance(value, (dict, list)):
                    value = json.dumps(value)
                new_key_name = f"{JsonFormatter.EXTRA_PREFIX}{key}"
                log_record[new_key_name] = value
                log_record.pop(key, None)

    @staticmethod
    def _get_trace_id():
        """
        The trace id can be used for tracing logs across multiple services.
        It's fetched from the headers of the request.
        Should be implemented according to the tracing mechanism of the service.
        e.g in flask or fastapi:
        trace_id = request.headers.get("X-Trace-Id")
        """

        return "example_trace_id"