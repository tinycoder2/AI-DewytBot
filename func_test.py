from cal_setup import get_calendar_service
from datetime import datetime
import pytz

# test_start = datetime.strptime('Apr 23 2022 3:00PM','%b %d %Y %I:%M%p')

def check_conflict(new_start):
    day_start = new_start.replace(hour=00,minute=00)
    day_end = day_start.replace(day=day_start.day+1)

    service = get_calendar_service()

    day_start = day_start.isoformat(timespec='milliseconds')+'Z'
    day_end = day_end.isoformat(timespec='milliseconds')+'Z'

    body = {
      "timeMin": day_start,
      "timeMax": day_end,
      "timeZone": "Asia/Kolkata",
      "items": [{"id": 'primary'}]
    }

    eventsResult = service.freebusy().query(body=body).execute()
    events = eventsResult['calendars']['primary']['busy']
    check = new_start.astimezone(tz=pytz.timezone('Asia/Kolkata'))
    for event in events:
        event_start = datetime.fromisoformat(event['start'])
        event_end = datetime.fromisoformat(event['end'])
        if event_start<=check<=event_end:
            return (event_start,event_end)
    return False




