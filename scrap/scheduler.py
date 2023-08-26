from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.events import EVENT_JOB_ERROR
import logging

logger = logging.getLogger('main')


class Scheduler:
    def __init__(self, interval):
        self.interval = interval
        self.scheduler = None
        self.fail_counter = 0

    def listener(self, event):
        logger.exception(f'Job {event.job_id} raised {event.exception.__class__.__name__}')
        self.fail_counter += 1
        self.scheduler.shutdown()

    def start_up(self, func):
        if self.scheduler is None:
            self.scheduler = BackgroundScheduler(job_defaults={'max_instances': 1})
            self.scheduler.add_listener(self.listener, EVENT_JOB_ERROR)
            self.scheduler.add_job(func, 'interval', seconds=self.interval)
            self.scheduler.start()
        else:
            raise

    def shut_down(self):
        if self.scheduler is None:
            raise
        else:
            if self.scheduler.state:
                self.scheduler.shutdown()
