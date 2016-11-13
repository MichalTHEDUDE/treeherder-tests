# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from pages.treeherder import TreeherderPage


def test_next_job_shortcut(base_url, selenium):
    """Shortcut: 'Rigth Arrow'
    Open Treeherder page, select random job, select job next to it and take
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
    """Shortcut: SHIFT + '?'
    Open Treeherder page, display keyboard shortcuts using SHIFT + '?',
    verify if keyboard shortcut panel is displayed"""
    page = TreeherderPage(selenium, base_url).open()
    page.display_keyboard_shortcuts()

    assert page.keyboard_shortcuts_panel_is_displayed


def test_toggle_pending_and_running_jobs(base_url, selenium):
    """Shortcut: 'i'
    Open Treeherder page, count number of in progress jobs (pending and
    running), click on 'in progress' button using 'i' keyboard shortcut,
    verify that number of in progress jobs is euqal to zero"""
    page = TreeherderPage(selenium, base_url).open()

    num_of_pending_jobs = len(page.all_pending_jobs)
    num_of_running_jobs = len(page.all_running_jobs)

    assert num_of_pending_jobs > 1
    assert num_of_running_jobs > 1

    page.click_on_in_progress_button()

    num_of_pending_jobs = len(page.all_pending_jobs)
    num_of_running_jobs = len(page.all_running_jobs)

    assert num_of_pending_jobs == 0
    assert num_of_running_jobs == 0


def test_show_only_unclassified_failures(base_url, selenium):
    """Shortcut: 'u'
    Open Treeherder page, show only unclassified failures using 'u' button,
    verify number of unclassified failures"""
    page = TreeherderPage(selenium, base_url).open()
    page.show_only_unclassified_failures()

    unclassified_jobs = len(page.all_jobs)

    assert unclassified_jobs == page.unclassified_failure_count
