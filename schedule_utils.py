import schedule
import functools


def catch_exceptions(job_func, cancel_on_failure=False):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
            if cancel_on_failure:
                return schedule.CancelJob
    return wrapper


def run_once(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        job_func(*args, **kwargs)
        return schedule.CancelJob
    return wrapper