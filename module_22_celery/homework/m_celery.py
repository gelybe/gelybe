"""
В этом файле будут Celery-задачи
"""
from zipimport import zipimporter

from celery import Celery
from image import blur_image
from mail import send_email
from celery.schedules import crontab

celery = Celery(__name__, broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")


@celery.task
def task_blur(*args):
    blur_image(*args)
    return f"Processed {args[0]}"


class Subscribers:
    emails = []
    tasks = {}
    filename = "test_photo_1.jpg"

    def subscribe(self, mail):
        if mail not in self.tasks:
            self.emails.append(mail)
            task_id = self.setup_periodic_tasks(mail)
            self.tasks[mail] = task_id
            return f"{mail} подписался на рассылку!"
        return f"{mail} уже был подписан на рассылку"

    def unsubscribe(self, mail):
        if mail not in self.tasks:
            return f"{mail} не был подписан на рассылку"
        self.emails.remove(mail)
        task_id = self.tasks.pop(mail, None)
        if task_id:
            celery.control.revoke(task_id, terminate=True)
        return f"{mail} отписался от рассылки"

    def setup_periodic_tasks(self, mail):
        task = celery.add_periodic_task(
            crontab(hour=10, minute=10, day_of_week=1),
            self.send_mail.s(mail),
            name=f"send_email_{mail}"
        )
        return task

    @celery.task
    def send_mail(self, mail):
        index = self.emails.index(mail) if mail in self.emails else None
        if index is not None:
            send_email(index, mail, self.filename)
            return "Письмо отправлено"
        return "Подписчик не найден"

    @celery.task
    def send_mail(self, mail):
        index = self.emails.index(mail) if mail in self.emails else None
        if index is not None:
            send_email(index, mail, self.filename)
            return "Письмо отправлено"
        return "Подписчик не найден"

subscribers_object = Subscribers()