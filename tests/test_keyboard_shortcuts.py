# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import random

from pages.treeherder import TreeherderPage


def test_close_open_panels(base_url, selenium):
    """Shortcut: 'esc'
    Open Treeherder page, open Filters panel, select random job, close all
    panels using 'esc' button, verify if all panels are closed"""
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
    word mozilla"""
    page = TreeherderPage(selenium, base_url).open()
    assert page.get_search_box_text == ''

    page.filter_by_using_quick_filter('mozilla')

    assert page.get_search_box_text == 'mozilla'


def test_clear_the_quick_filter_shortcut(base_url, selenium):
    """Shortcut: CTRL + SHIFT + 'f'
    Open Treeherder page, filter by 'mozilla', verify if filter box contain
    word 'mozilla', clear the quick filter using CTRL + SHIFT + f shortcut,
    verify if search box is empty"""
    page = TreeherderPage(selenium, base_url).open()

    page.filter_by_using_quick_filter('mozilla')
    assert page.get_search_box_text == 'mozilla'

    page.clear_filter_by_shortcut()

    assert page.get_search_box_text == ''


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


def test_previous_job_shortcut(base_url, selenium):
    """Shortcut: 'Left Arrow'
    Open Treeherder page, select random job, select previous job, take
    job keyword, go back to next job and select previous job using Left Arrow
    shortcut, verify if job keywords match"""
    page = TreeherderPage(selenium, base_url).open()
    all_jobs = page.all_jobs

    # Check number of jobs
    num_of_jobs = len(all_jobs) - 1
    rnd_number = random.randint(0, num_of_jobs)
    previous_job = rnd_number - 1

    if rnd_number == 0:
        previous_job = num_of_jobs

    # Select random job and job to the left
    all_jobs[rnd_number].click()
    all_jobs[previous_job].click()
    page.job_details.wait_for_region_to_load()
    assumed_job_keyword = page.job_details.job_keyword_name

    all_jobs[rnd_number].click()
    page.job_details.wait_for_region_to_load()

    page.select_previous_job()
    page.job_details.wait_for_region_to_load()

    assert page.job_details.job_keyword_name == assumed_job_keyword


def test_previous_unclassified_failure_shortcut(base_url, selenium):
    """Shortcut: 'p'
    Open Treeherder page, show only unclassified failures, select random
    failure, select previous failure, take job keyword, go back to next failure
    and select previous unclassified failure using 'p' button shortcut,
    verify if job keywords match"""
    page = TreeherderPage(selenium, base_url).open()
    page.show_only_unclassified_failures()
    all_unclassified_failures = page.all_jobs

    # Check number of unclassified failures
    num_of_unclass_failures = len(all_unclassified_failures) - 1
    rnd_number = random.randint(0, num_of_unclass_failures)
    previous_failure = rnd_number - 1

    if rnd_number == 0:
        previous_failure = num_of_unclass_failures

    # Select random unclassified failure
    all_unclassified_failures[rnd_number].click()
    all_unclassified_failures[previous_failure].click()
    assumed_job_keyword = page.job_details.job_keyword_name

    all_unclassified_failures[rnd_number].click()
    page.job_details.wait_for_region_to_load()

    page.select_previous_unclassified_failure()
    page.job_details.wait_for_region_to_load()

    assert page.job_details.job_keyword_name == assumed_job_keyword


def test_select_next_info_tab_shortcut(base_url, selenium):
    """Shortcut: 't'
    Open Treeherder page, select random job, get active tab name, depending on
    tab header name verify if next tab have assumed value, change tabs using
    't' keyboard shortcut"""
    page = TreeherderPage(selenium, base_url).open()
    page.select_random_job()

    active_tab_name = page.job_details.active_tab_name

    if active_tab_name == 'Job details':
        next_tab_name = 'Failure summary'
        page.job_details.select_next_panel_tab()
        assert page.job_details.active_tab_name == next_tab_name

    if active_tab_name == 'Failure summary':
        next_tab_name = 'Annotations'
        page.job_details.select_next_panel_tab()
        assert page.job_details.active_tab_name == next_tab_name

    if active_tab_name == 'Performance':
        next_tab_name = 'Job details'
        page.job_details.select_next_panel_tab()
        assert page.job_details.active_tab_name == next_tab_name


def test_toggle_pinning_job_during_clicking_shortcut(base_url, selenium, driver):
    """Shortcut: CTRL/CMD + job
    Open Treeherder page, pin two random jobs, verify if number of pinned jobs
    is greater that 1"""
    page = TreeherderPage(selenium, base_url).open()
    assert 0 == len(page.pinboard.jobs)

    page.pin_random_job(driver)
    page.pin_random_job(driver)

    assert len(page.pinboard.jobs) > 1


def test_pin_job_and_enter_bug_number(base_url, selenium):
    """Shortcut: b
    Open Treeherder page, select random job, pin job using 'b' shortcut and
    enter bug number, do it once again, verify if there is one pinned job and
    entered bugs are in related bugs field"""
    page = TreeherderPage(selenium, base_url).open()
    page.select_random_job()

    bug_number = u'1729'
    page.pin_job_and_enter_bug_number(bug_number)

    bug_number = u'87539319'
    page.pin_job_and_enter_bug_number(bug_number)

    assert len(page.pinboard.jobs) == 1
    assert bug_number in page.pinboard.related_bugs


def test_clear_the_pinboard_shortcut(base_url, selenium, driver):
    """Shortcut: CTRL + SHIFT + 'u'
    Open Treeherder page, pin two random jobs, verify if number of pinned jobs
    is greater that 1, clear the pinboard using CTRL + SHIFT + 'u' shortcut,
    verify if number of pinned jobs is zero"""
    page = TreeherderPage(selenium, base_url).open()

    page.pin_random_job(driver)
    page.pin_random_job(driver)
    assert len(page.pinboard.jobs) > 1

    page.pinboard.clear_pinboard_using_keyboard_shortcut()

    assert len(page.pinboard.jobs) == 0


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
