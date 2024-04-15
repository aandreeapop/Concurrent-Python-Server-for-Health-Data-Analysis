from queue import Queue, Empty
from threading import Thread, Event
import pandas as pd
import time

import os
import json


class ThreadPool:
    def __init__(self):
        # Verifica daca valoarea pentru 'TP_NUM_OF_THREADS' este definita
        if 'TP_NUM_OF_THREADS' in os.environ:
            self.num_threads = int(os.environ['TP_NUM_OF_THREADS'])
        else:
            # Dacă nu este definita, foloseste numarul de nuclee CPU ca valoare implicita
            self.num_threads = os.cpu_count()

        self.task_queue = Queue()
        self.jobs = {}
        self.jobs_type = {}
        self.shutdown = False

        # Crearea și pornirea thread-urilor din pool
        self.threads = []
        for _ in range(self.num_threads):
            thread = TaskRunner(self.task_queue, self.jobs_type, self.jobs)
            thread.start()
            self.threads.append(thread)

    def stop(self):
        self.shutdown = True
        for thread in self.threads:
            thread.stop()

class TaskRunner(Thread):
    def __init__(self, task_queue, jobs_type, jobs):
        super().__init__()
        self.task_queue = task_queue
        self.graceful_shutdown = Event()
        self.jobs_type = jobs_type
        self.jobs = jobs

    def run(self):
        while not self.graceful_shutdown.is_set():
            try:
                # Așteptarea unei sarcini din coadă
                job_id = self.task_queue.get(timeout=1)
            except Empty:
                # Continuarea execuției în cazul în care nu există sarcini în coadă
                continue
            self.execute_task(job_id)

    # Executarea task-ului prin marcarea statusului cu "done"
    def execute_task(self, job_id):
        self.jobs[job_id] = "done"

    def stop(self):
        self.graceful_shutdown.set()
