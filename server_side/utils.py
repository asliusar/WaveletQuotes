import json
from datetime import datetime

import numpy as np


class DateTimeEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        elif isinstance(o, np.ndarray):
            return o.tolist()
        return json.JSONEncoder.default(self, o)


formatDate = '%Y-%m-%d'


def format_date(date):
    startDate = date.split("T")[0]
    return datetime.strptime(startDate, formatDate)
