# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from pages.treeherder import TreeherderPage


def test_close_open_panels(base_url, selenium):
    """Shortcut: 'esc'

    Open Treeherder page, open Filters panel, select random job, close all
    panels using 'esc' button, verify if all panels are closed
    """
    page = TreeherderPage(selenium, base_url).open()

    page.click_on_filters_panel()
    page.select_random_job()

    assert page.filter_panel_is_opened
    assert page.job_details_panel_is_opened

    page.close_all_panels()

    assert not page.filter_panel_is_opened
    assert not page.job_details_panel_is_opened


def test_enter_quick_filter_shortcut(base_url, selenium):
    """Shortcut: 'f'

    Open Treeherder page, verify if search box is empty, enter search box
    filter using 'f' shortcut, type 'mozilla', verify if filter box contain
    word mozilla
    """
    page = TreeherderPage(selenium, base_url).open()
    assert page.search_term == ''

    page.filter_by('mozilla', method='keyboard')
    assert page.search_term == 'mozilla'


def test_clear_the_quick_filter_shortcut(base_url, selenium):
    """Shortcut: CTRL + SHIFT + 'f'

    Open Treeherder page, filter by 'mozilla', verify if filter box contain
    word 'mozilla', clear the quick filter using CTRL + SHIFT + f shortcut,
    verify if search box is empty
    """
    page = TreeherderPage(selenium, base_url).open()

    page.filter_by('mozilla', method='keyboard')
    assert page.search_term == 'mozilla'

    page.clear_filter(method='keyboard')
    assert page.search_term == ''


def test_next_job_shortcut(base_url, selenium):
    """Shortcut: 'Right Arrow'

    Open Treeherder page, select random job, select job next to it and take
    job keyword, go back to previous job and select next job using Right arrow
    shortcut, verify if job keyword match
    """
    page = TreeherderPage(selenium, base_url).open()
    all_jobs = page.all_jobs

    # Check number of jobs
    number_of_jobs = len(all_jobs)
    random_index = random.randint(1, number_of_jobs - 1)
    next_job = random_index + 1

    # Select random job and job next to it
    all_jobs[next_job].click()
    assumed_job_keyword = page.job_details.job_keyword_name

    all_jobs[random_index].click()
    page.select_next_job()

    assert page.job_details.job_keyword_name == assumed_job_keyword


def test_previous_job_shortcut(base_url, selenium):
    """Shortcut: 'Left Arrow'

    Open Treeherder page, select random job, select previous job, take
    job keyword, go back to next job and select previous job using Left Arrow
    shortcut, verify if job keywords match
    """
    page = TreeherderPage(selenium, base_url).open()
    all_jobs = page.all_jobs

    # Check number of jobs
    number_of_jobs = len(all_jobs)
    random_index = random.randint(1, number_of_jobs - 1)
    previous_job = random_index - 1

    # Select random job and job to the left
    all_jobs[previous_job].click()
    assumed_job_keyword = page.job_details.job_keyword_name

    all_jobs[random_index].click()
    page.select_previous_job()

    assert page.job_details.job_keyword_name == assumed_job_keyword


def test_previous_unclassified_failure_shortcut(base_url, selenium):
    """Shortcut: 'p'

    Open Treeherder page, show only unclassified failures, select random
    failure, select previous failure, take job keyword, go back to next failure
    and select previous unclassified failure using 'p' button shortcut,
    verify if job keywords match
    """
    page = TreeherderPage(selenium, base_url).open()
    page.show_only_unclassified_failures()
    all_unclassified_failures = page.all_jobs

    # Check number of unclassified failures
    number_of_unclassified_failures = len(all_unclassified_failures)
    rnd_number = random.randint(1, number_of_unclassified_failures - 1)
    previous_failure = rnd_number - 1

    # Select random unclassified failure
    all_unclassified_failures[previous_failure].click()
    assumed_job_keyword = page.job_details.job_keyword_name

    all_unclassified_failures[rnd_number].click()
    page.select_previous_unclassified_failure()

    assert page.job_details.job_keyword_name == assumed_job_keyword


def test_select_next_info_tab_shortcut(base_url, selenium):
    """Shortcut: 't'

    Open Treeherder page, select random job, get active tab name, depending on
    tab header name verify if next tab have assumed value, change tabs using
    't' keyboard shortcut
    """
    page = TreeherderPage(selenium, base_url).open()
    page.select_random_job()

    while page.job_details.active_tab_name != 'Job details':
        page.select_random_job()

    tabs_list = ['Failure summary', 'Annotations', 'Similar jobs', 'Job details']

    for tab in tabs_list:
        page.job_details.select_next_panel_tab()
        assert page.job_details.active_tab_name == tab


def test_toggle_pinning_job_during_clicking_shortcut(base_url, selenium, driver):
    """Shortcut: CTRL/CMD + job

    Open Treeherder page, pin two random jobs, verify if number of pinned jobs
    is greater that 1
    """
    page = TreeherderPage(selenium, base_url).open()
    assert 0 == len(page.pinboard.jobs)

    page.pin_random_job(driver)

    assert len(page.pinboard.jobs) == 1


def test_clear_the_pinboard_shortcut(base_url, selenium, driver):
    """Shortcut: CTRL + SHIFT + 'u'

    Open Treeherder page, pin two random jobs, verify if number of pinned jobs
    is greater that 1, clear the pinboard using CTRL + SHIFT + 'u' shortcut,
    verify if number of pinned jobs is zero
    """
    page = TreeherderPage(selenium, base_url).open()

    page.pin_random_job(driver)
    assert len(page.pinboard.jobs) == 1

    page.pinboard.clear_pinboard(method='keyboard')

    assert len(page.pinboard.jobs) == 0


def test_display_onscreen_keyboard_shortcuts(base_url, selenium):
    """Shortcut: SHIFT + '?'

    Open Treeherder page, display keyboard shortcuts using SHIFT + '?',
    verify if keyboard shortcut panel is displayed
    """
    page = TreeherderPage(selenium, base_url).open()
    page.display_keyboard_shortcuts()

    assert page.keyboard_shortcuts_panel_is_displayed


def test_toggle_pending_and_running_jobs(base_url, selenium):
    """Shortcut: 'i'

    Open Treeherder page, count number of in progress jobs (pending and
    running), click on 'in progress' button using 'i' keyboard shortcut,
    verify that number of in progress jobs is euqal to zero
    """
    page = TreeherderPage(selenium, base_url).open()

    assert len(page.all_pending_jobs) > 1
    assert len(page.all_running_jobs) > 1

    page.toggle_jobs_in_progress(option='hide')

    assert len(page.all_pending_jobs) == 0
    assert len(page.all_running_jobs) == 0


def test_show_only_unclassified_failures(base_url, selenium):
    """Shortcut: 'u'

    Open Treeherder page, show only unclassified failures using 'u' button,
    verify number of unclassified failures
    """
    page = TreeherderPage(selenium, base_url).open()
    page.show_only_unclassified_failures()

    unclassified_jobs = len(page.all_jobs)

    assert unclassified_jobs == page.unclassified_failure_count
