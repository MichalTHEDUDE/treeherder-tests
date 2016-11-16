# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import itertools
import random

from pypom import Page, Region
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from pages.base import Base


class TreeherderPage(Base):

    _active_watched_repo_locator = (By.CSS_SELECTOR, '#watched-repo-navbar button.active')
    _clear_filter_locator = (By.ID, 'quick-filter-clear-button')
    _close_the_job_panel_locator = (By.CSS_SELECTOR, '.info-panel-navbar-controls > li:nth-child(2)')
    _filter_panel_all_failures_locator = (By.CSS_SELECTOR, '.pull-right input')
    _filter_panel_body_locator = (By.CSS_SELECTOR, '.th-top-nav-options-panel')
    _filter_panel_busted_failures_locator = (By.ID, 'busted')
    _filter_panel_exception_failures_locator = (By.ID, 'exception')
    _filter_panel_locator = (By.CSS_SELECTOR, 'span.navbar-right > span:nth-child(4)')
    _filter_panel_reset_locator = (By.CSS_SELECTOR, '.pull-right span:nth-child(3)')
    _filter_panel_testfailed_failures_locator = (By.ID, 'testfailed')
    _info_panel_content_locator = (By.ID, 'info-panel-content')
    _keyboard_shortcuts_locator = (By.CSS_SELECTOR, '#onscreen-shortcuts')
    _mozilla_central_repo_locator = (By.CSS_SELECTOR, '#th-global-navbar-top a[href*="mozilla-central"]')
    _next_ten_locator = (By.CSS_SELECTOR, 'div.btn:nth-child(1)')
    _next_twenty_locator = (By.CSS_SELECTOR, 'div.btn:nth-child(2)')
    _next_fifty_locator = (By.CSS_SELECTOR, 'div.btn:nth-child(3)')
    _quick_filter_locator = (By.ID, 'quick-filter')
    _related_bug_input_locator = (By.ID, 'related-bug-input')
    _repos_menu_locator = (By.ID, 'repoLabel')
    _result_sets_locator = (By.CSS_SELECTOR, '.result-set:not(.row)')
    _unchecked_repos_links_locator = (By.CSS_SELECTOR, '#repoLabel + .dropdown-menu .dropdown-checkbox:not([checked]) + .dropdown-link')
    _unclassified_failure_count_locator = (By.ID, 'unclassified-failure-count')
    _unclassified_failure_filter_locator = (By.CSS_SELECTOR, '.btn-unclassified-failures')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.unclassified_failure_count > 0)
        return self

    @property
    def active_watched_repo(self):
        return self.find_element(*self._active_watched_repo_locator).text

    @property
    def all_emails(self):
        return list(itertools.chain.from_iterable([r.emails for r in self.result_sets]))

    @property
    def all_jobs(self):
        return list(itertools.chain.from_iterable([r.jobs for r in self.result_sets]))

    @property
    def all_pending_jobs(self):
        return list(itertools.chain.from_iterable([r.pending_jobs for r in self.result_sets]))

    @property
    def all_running_jobs(self):
        return list(itertools.chain.from_iterable([r.running_jobs for r in self.result_sets]))

    @property
    def checkbox_busted_is_selected(self):
        return self.find_element(*self._filter_panel_busted_failures_locator).is_selected()

    @property
    def checkbox_exception_is_selected(self):
        return self.find_element(*self._filter_panel_exception_failures_locator).is_selected()

    @property
    def checkbox_testfailed_is_selected(self):
        return self.find_element(*self._filter_panel_testfailed_failures_locator).is_selected()

    @property
    def filter_panel_is_opened(self):
        el = self.find_element(*self._filter_panel_body_locator)
        return el.is_displayed()

    @property
    def get_search_box_text(self):
        el = self.find_element(*self._quick_filter_locator)
        return el.get_attribute('value')

    @property
    def job_details(self):
        return self.JobDetails(self)

    @property
    def job_details_panel_is_opened(self):
        el = self.find_element(*self._info_panel_content_locator)
        return el.is_displayed()

    @property
    def keyboard_shortcuts_panel_is_displayed(self):
        el = self.find_element(*self._keyboard_shortcuts_locator)
        return el.is_displayed()

    @property
    def pinboard(self):
        return self.Pinboard(self)

    @property
    def random_email_name(self):
        random_email_name = random.choice(self.all_emails)
        return random_email_name.get_name

    @property
    def result_sets(self):
        return [self.ResultSet(self, el) for el in self.find_elements(*self._result_sets_locator)]

    @property
    def unchecked_repos(self):
        return self.find_elements(*self._unchecked_repos_links_locator)

    @property
    def unclassified_failure_count(self):
        return int(self.find_element(*self._unclassified_failure_count_locator).text)

    def clear_filter(self):
        self.selenium.find_element(*self._clear_filter_locator).click()

    def clear_filter_by_shortcut(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys(Keys.CONTROL + Keys.SHIFT + 'f')

    def click_on_filters_panel(self):
        self.find_element(*self._filter_panel_locator).click()

    def click_on_active_watched_repo(self):
        self.find_element(*self._active_watched_repo_locator).click()

    def click_on_in_progress_button(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys('i')

    def close_the_job_panel(self):
        self.find_element(*self._close_the_job_panel_locator).click()

    def close_all_panels(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys(Keys.ESCAPE)

    def deselect_all_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_all_failures_locator).click()

    def deselect_busted_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_busted_failures_locator).click()

    def deselect_exception_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_exception_failures_locator).click()

    def deselect_testfailed_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_testfailed_failures_locator).click()

    def display_keyboard_shortcuts(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys(Keys.SHIFT + '?')

    def filter_by_using_quick_filter(self, term):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys('f' + term)
        el.send_keys(Keys.RETURN)

    def filter_by(self, term):
        el = self.selenium.find_element(*self._quick_filter_locator)
        el.send_keys(term)
        el.send_keys(Keys.RETURN)
        self.wait.until(lambda s: self.result_sets)

    def filter_unclassified_jobs(self):
        self.find_element(*self._unclassified_failure_filter_locator).click()

    def get_next_ten_results(self):
        self.find_element(*self._next_ten_locator).click()
        self.wait.until(lambda s: len(self.result_sets) == 20)

    def get_next_twenty_results(self):
        self.find_element(*self._next_twenty_locator).click()
        self.wait.until(lambda s: len(self.result_sets) == 30)

    def get_next_fifty_results(self):
        self.find_element(*self._next_fifty_locator).click()
        self.wait.until(lambda s: len(self.result_sets) == 60)

    def open_next_unclassified_failure(self):
        el = self.find_element(*self._result_sets_locator)
        self.wait.until(EC.visibility_of(el))
        el.send_keys('n')
        self.wait.until(lambda s: self.job_details.job_result_status)

    def open_perfherder_page(self):
        self.header.switch_page_using_dropdown()

        from perfherder import PerfherderPage
        return PerfherderPage(self.selenium, self.base_url).wait_for_page_to_load()

    def open_repos_menu(self):
        self.find_element(*self._repos_menu_locator).click()

    def pin_job_and_enter_bug_number(self, bug_number):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys('b')
        el = self.find_element(*self._related_bug_input_locator)
        el.send_keys(bug_number + Keys.RETURN)

    def pin_random_job(self, driver):
        random_job = random.choice(self.all_jobs).click()
        ActionChains(driver).key_down(Keys.CONTROL).click(random_job).perform()

    def pin_using_spacebar(self):
        el = self.find_element(*self._result_sets_locator)
        self.wait.until(EC.visibility_of(el))
        el.send_keys(Keys.SPACE)
        self.wait.until(lambda _: self.pinboard.is_pinboard_open)

    def reset_filters(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_reset_locator).click()

    def select_mozilla_central_repo(self):
        # Fix me: https://github.com/mozilla/treeherder-tests/issues/43
        self.open_repos_menu()
        self.find_element(*self._mozilla_central_repo_locator).click()
        self.wait_for_page_to_load()

    def select_busted_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_busted_failures_locator).click()

    def select_exception_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_exception_failures_locator).click()

    def select_testfailed_failures(self):
        """Filters Panel must be opened"""
        self.find_element(*self._filter_panel_testfailed_failures_locator).click()

    def select_next_job(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys(Keys.ARROW_RIGHT)

    def select_previous_job(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys(Keys.ARROW_LEFT)

    def select_previous_unclassified_failure(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys('p')

    def select_random_email(self):
        random_email = random.choice(self.all_emails)
        random_email.click()

    def select_random_job(self):
        random_job = random.choice(self.all_jobs)
        random_job.click()

    def select_random_repo(self):
        self.open_repos_menu()
        repo = random.choice(self.unchecked_repos)
        repo_name = repo.text
        repo.click()
        self.wait.until(lambda s: self._active_watched_repo_locator == repo_name)
        return repo_name

    def show_only_unclassified_failures(self):
        el = self.find_element(*self._result_sets_locator)
        el.send_keys('u')

    class ResultSet(Region):

        _datestamp_locator = (By.CSS_SELECTOR, '.result-set-title-left > span a')
        _dropdown_toggle_locator = (By.CLASS_NAME, 'dropdown-toggle')
        _email_locator = (By.CSS_SELECTOR, '.result-set-title-left > th-author > span > a')
        _expanded_group_content_locator = (By.CSS_SELECTOR, '.group-job-list[style="display: inline;"]')
        _group_content_locator = (By.CSS_SELECTOR, 'span.group-count-list .btn')
        _jobs_locator = (By.CSS_SELECTOR, '.job-btn.filter-shown')
        _jobs_running_locator = (By.CSS_SELECTOR, '.job-btn.btn-dkgray.filter-shown')
        _jobs_pending_locator = (By.CSS_SELECTOR, '.job-btn.btn-ltgray.filter-shown')
        _pin_all_jobs_locator = (By.CLASS_NAME, 'pin-all-jobs-btn')
        _platform_locator = (By.CLASS_NAME, 'platform')
        _set_bottom_of_range_locator = (By.CSS_SELECTOR, '.open ul > li:nth-child(8) > a')
        _set_top_of_range_locator = (By.CSS_SELECTOR, '.open ul > li:nth-child(7) > a')

        @property
        def builds(self):
            return [self.Build(self.page, root=el) for el in self.find_elements(*self._platform_locator)]

        @property
        def datestamp(self):
            return self.find_element(*self._datestamp_locator).text

        @property
        def emails(self):
            return [self.Email(self.page, root=el) for el in self.find_elements(*self._email_locator)]

        @property
        def email_name(self):
            return self.find_element(*self._email_locator).text

        @property
        def find_expanded_group_content(self):
            return self.is_element_displayed(*self._expanded_group_content_locator)

        @property
        def jobs(self):
            return [self.Job(self.page, root=el) for el in self.find_elements(*self._jobs_locator)]

        @property
        def pending_jobs(self):
            return [self.Job(self.page, root=el) for el in self.find_elements(*self._jobs_pending_locator)]

        @property
        def running_jobs(self):
            return [self.Job(self.page, root=el) for el in self.find_elements(*self._jobs_running_locator)]

        def expand_group_count(self):
            self.find_element(*self._group_content_locator).click()
            self.wait.until(lambda s: self.is_element_displayed(*self._expanded_group_content_locator))

        def pin_all_jobs(self):
            return self.find_element(*self._pin_all_jobs_locator).click()

        def set_as_bottom_of_range(self):
            self.find_element(*self._dropdown_toggle_locator).click()
            self.find_element(*self._set_bottom_of_range_locator).click()

        def set_as_top_of_range(self):
            self.find_element(*self._dropdown_toggle_locator).click()
            self.find_element(*self._set_top_of_range_locator).click()

        def view(self):
            return self.find_element(*self._datestamp_locator).click()

        class Build(Region):

            _platform_name_locator = (By.CSS_SELECTOR, 'td:nth-child(1) > span:nth-child(1)')

            @property
            def platform_name(self):
                return self.find_element(*self._platform_name_locator).text

        class Email(Region):

            @property
            def get_name(self):
                return self.root.text

            def click(self):
                self.root.click()

        class Job(Region):

            @property
            def symbol(self):
                return self.root.text

            def click(self):
                self.root.click()
                self.wait.until(lambda _: self.page.job_details.job_result_status)

    class JobDetails(Region):

        _active_tab_header_locator = (By.CSS_SELECTOR, '#job-tabs-navbar > nav > ul > li.active > a')
        _job_details_panel_locator = (By.ID, 'job-details-panel')
        _job_keyword_locator = (By.CSS_SELECTOR, '#job-details-pane > ul > li > a:nth-last-child(1)')
        _job_result_status_locator = (By.CSS_SELECTOR, '#result-status-pane > div:nth-child(1) > span:nth-child(2)')
        _logviewer_button_locator = (By.ID, 'logviewer-btn')
        _pin_job_locator = (By.ID, 'pin-job-btn')

        def wait_for_region_to_load(self):
            el = self.find_element(*self._job_result_status_locator)
            self.wait.until(EC.visibility_of(el))

        @property
        def active_tab_name(self):
            return self.find_element(*self._active_tab_header_locator).text

        @property
        def job_keyword_name(self):
            return self.find_element(*self._job_keyword_locator).text

        @property
        def job_result_status(self):
            return self.find_element(*self._job_result_status_locator).text

        def filter_by_job_keyword(self):
            self.find_element(*self._job_keyword_locator).click()

        def open_logviewer(self):
            self.find_element(*self._job_details_panel_locator).send_keys('l')
            window_handles = self.selenium.window_handles
            for handle in window_handles:
                self.selenium.switch_to.window(handle)
            return LogviewerPage(self.selenium, self.page.base_url).wait_for_page_to_load()

        def pin_job(self):
            el = self.find_element(*self._pin_job_locator)
            self.wait.until(EC.visibility_of(el))
            el.click()

        def select_next_panel_tab(self):
            el = self.find_element(*self._job_details_panel_locator)
            el.send_keys('t')

    class Pinboard(Region):

        _root_locator = (By.ID, 'pinboard-panel')
        _clear_all_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .dropdown-menu li:nth-child(4)')
        _jobs_locator = (By.CLASS_NAME, 'pinned-job')
        _open_save_menu_locator = (By.CSS_SELECTOR, '#pinboard-controls .save-btn-dropdown')
        _pinboard_remove_job_locator = (By.CSS_SELECTOR, '#pinned-job-list .pinned-job-close-btn')
        _pinboard_related_bugs_locator = (By.CSS_SELECTOR, '.pinboard-related-bugs-btn a em')

        @property
        def is_pinboard_open(self):
            return self.root.is_displayed()

        @property
        def jobs(self):
            return [self.Job(self.page, el) for el in self.find_elements(*self._jobs_locator)]

        @property
        def related_bugs(self):
            return [el.text for el in self.find_elements(*self._pinboard_related_bugs_locator)]

        @property
        def selected_job(self):
            return next(j for j in self.jobs if j.is_selected)

        def clear_pinboard(self):
            el = self.find_element(*self._open_save_menu_locator)
            el.click()
            self.wait.until(lambda _: el.get_attribute('aria-expanded') == 'true')
            self.find_element(*self._clear_all_menu_locator).click()

        def clear_pinboard_using_keyboard_shortcut(self):
            el = self.find_element(*self._root_locator)
            el.send_keys(Keys.CONTROL + Keys.SHIFT + 'u')

        class Job(Region):

            @property
            def is_selected(self):
                return 'selected-job' in self.root.get_attribute('class')

            @property
            def symbol(self):
                return self.root.text


class LogviewerPage(Page):

    _job_header_locator = (By.CSS_SELECTOR, 'div.job-header')

    def wait_for_page_to_load(self):
        self.wait.until(lambda s: self.is_job_status_visible)
        return self

    @property
    def is_job_status_visible(self):
        return self.is_element_displayed(*self._job_header_locator)
