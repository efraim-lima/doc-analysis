import os

# Broker settings
broker_url = os.getenv('BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('RESULT_BACKEND', 'redis://localhost:6379/0')

# Task settings
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'
enable_utc = True
timezone = 'UTC'

# Task execution settings
task_time_limit = 3600  # 1 hour
task_soft_time_limit = 3000  # 50 minutes

# Concurrency settings
worker_concurrency = 4  # Number of worker processes
worker_prefetch_multiplier = 1  # Number of tasks prefetched per worker

# Retry settings
task_acks_late = True
task_reject_on_worker_lost = True

# Logging settings
worker_redirect_stdouts = False
worker_redirect_stdouts_level = 'INFO' 