# -*- coding: utf-8 -*-
"""
Experiment scenario 3
Individual student’s progress could slow down the exercises solving

Selenium (or cypress) answering an exercise:
* /coach/#/{id}/learners/{id}/{id}/item/{id}/0/0
* /learn/#/topics/c/88557704d182447f8c86f7a51181dc06
    * CK-12 Testing → Making 10 → Make 10 (grids and number bonds)
Endpoints:
* /learn/#/topics/{id} : JavaScript (Phet or similars) while Selenium is running.


Channels    Learners        Classrooms     Requests/s   Database
================================================================
Exercise       25               2              20        sqlite
Video          25               2              20        sqlite
"""
from __future__ import print_function, unicode_literals

from locust import HttpLocust, TaskSet, task

try:
    from test_scaffolding import launch
except ImportError:
    # the test is being run out of velox environment
    # and velox package is not installed
    import os
    import sys
    sys.path.append(os.path.join(os.getcwd(), 'src'))
    from test_scaffolding import launch


class UserBehavior(TaskSet):

    @task(1)
    def get_something_else(self):
        self.client.get('/')


class WebsiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 0
    max_wait = 0


def run(base_url='http://kolibridemo.learningequality.org', users=3):
    launch(WebsiteUser, base_url, users, 3)


if __name__ == '__main__':
    run()
