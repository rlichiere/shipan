# TODO




## Mock-up: a rollback tool

This mock-up experiments a way to facilitate the management of a process that must be rollbacked in case of error.



### The tool: `attempt()`

```
# tools.utils_job.py

def attempt(job, history):
   " Attempts to execute the job, otherwise attempts to rollback it."

   try:
      _jobResult = job.execute(*args, **kwargs)

   except Exception as e:
      history.add_log(label='Execution error', failed=True, exc=e)

      if job.is_error_rollbackable(exc=e):

         try:
            _rollbackResult = job.rollback()

         except Exception as e:
            history.add_log(label='Rollback error', failed=True, exc=e)

         else:
            history.add_log(label='Rollback done', failed=True, **_rollbackResult)

      return False

   history.add_log(label='Attempt done', **_jobResult)
   return True
```

### Meta class: `Job`

```
class Job(object):
   " Metaclass for all jobs. "

   rollbackable_errors = ()

   @abstractmethod
   def execute(self, *args, **kwargs):
      # implement custom job, with custom args and kwargs
      return dict()

   @abstractmethod
   def rollback(self, *args, **kwargs):
      # implement rollback of custom job, with custom args and kwargs
      return dict()

   def is_error_rollbackable(self, exc):
      if exc in self.rollbackable_errors:
         return True
      return False
```

### Samples

* Definition of jobs

```
# sample_jobs_declaration.py

class SomeJob(Job):
   " Some rollbackable job "

   rollbackable_errors = (IntegrityError, )

   def execute(*args, **kwargs):
      # some job
      return {'some_job_result_key': 'some_job_result'}

   def rollback(*args, **kwargs):
      # some rollback job
      return {'some_rollback_job_result_key': 'some_rollback_job_result'}

   def detect_exceptions(self):
      pass

class OtherJob(Job):
   " Other rollbackable job "

   def execute(*args, **kwargs):
      # other job
      return {'other_job_result_key': 'other_job_result'}

   def rollback(*args, **kwargs):
      # other rollback job
      return {'other_rollback_job_result_key': 'other_rollback_job_result'}
```

* Sample 1: simple job attempt

```
# sample_usage_1.py
from tools import utils_job
_h = History()

if not attempt(job=SomeJob, history=_h):
   print('Attempt failed')
else:
   print('Attempt successful')

_h.print_logs()
```

* Sample 2: sequence of attempts

```
# sample_usage_2.py
from tools import utils_job

def someComplexJob():
   _h = History()

   if not attempt(job=SomeJob, history=_h):
      return _h

   if not attempt(job=OtherJob, history=_h):
      return _h

   return _h
```
