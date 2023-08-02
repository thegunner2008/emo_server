# from fastapi_scheduler import SchedulerAdmin
# def delete_all_redis_data():
#     redis_client.flushall()
#
# # create scheduler instance
# scheduler = Scheduler()
#
# # add job to scheduler
# @scheduler.cron('0 3 * * *')
# def scheduled_job():
#     delete_all_redis_data()
#
# # start scheduler
# scheduler.start()