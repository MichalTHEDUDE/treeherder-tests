# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from pages.treeherder import TreeherderPage


def test_next_job_shortcut(base_url, selenium):
    """Open Treeherder page, select random job, select job next to it and take
    job keyword, go back to previous job and select next job using Right arrow
    shortcut, verify if job keyword match"""
    page = TreeherderPage(selenium, base_url).open()
    all_jobs = page.all_jobs

    # Check number of jobs
    num_of_jobs = len(all_jobs) - 1
    rnd_number = random.randint(0, num_of_jobs)
    next_job = rnd_number + 1

    if rnd_number == num_of_jobs:
        next_job = 0

    # Select random job and job next to it
    all_jobs[rnd_number].click()
    all_jobs[next_job].click()
    page.job_details.wait_for_region_to_load()
    assumed_job_keyword = page.job_details.job_keyword_name

    all_jobs[rnd_number].click()
    page.job_details.wait_for_region_to_load()

    page.select_next_job()
    page.job_details.wait_for_region_to_load()

    assert page.job_details.job_keyword_name == assumed_job_keyword


def test_display_onscreen_keyboard_shortcuts(base_url, selenium):
    """Open Treeherder page, display keyboard shortcuts using SHIFT + '?',
    verify if keyboard shortcut panel is displayed"""
    page = TreeherderPage(selenium, base_url).open()
    page.display_keyboard_shortcuts()

    assert page.keyboard_shortcuts_panel_is_displayed
