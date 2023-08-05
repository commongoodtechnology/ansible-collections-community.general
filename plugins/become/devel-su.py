# -*- coding: utf-8 -*-
# Copyright (c) 2023, Institute for Common Good Technology <https://commongoodtechnology.org/>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
    name: devel-su
    short_description: Sailfish OS sudo
    description:
        - This become plugins allows your remote/login user to execute commands as root via the devel-su utility.
    author: Institute for Common Good Technology
    options:
        become_exe:
            description: devel-su executable
            default: devel-su
            ini:
              - section: privilege_escalation
                key: become_exe
              - section: develsu_become_plugin
                key: executable
            vars:
              - name: ansible_become_exe
              - name: ansible_develsu_exe
            env:
              - name: ANSIBLE_BECOME_EXE
              - name: ANSIBLE_DEVELSU_EXE
        become_flags:
            description: Options to pass to devel-su
            default: ''
            ini:
              - section: privilege_escalation
                key: become_flags
              - section: develsu_become_plugin
                key: flags
            vars:
              - name: ansible_become_flags
              - name: ansible_develsu_flags
            env:
              - name: ANSIBLE_BECOME_FLAGS
              - name: ANSIBLE_DEVELSU_FLAGS
        become_pass:
            description: develsu password
            required: false
            vars:
              - name: ansible_develsu_pass
              - name: ansible_become_pass
              - name: ansible_become_password
            env:
              - name: ANSIBLE_BECOME_PASS
              - name: ANSIBLE_DEVELSU_PASS
            ini:
              - section: develsu_become_plugin
                key: password
'''

from ansible.plugins.become import BecomeBase


class BecomeModule(BecomeBase):

    name = 'community.general.devel_su'

    # messages for detecting prompted password issues
    fail = ('Password incorrect',)
    missing = ('No password given',)

    def check_password_prompt(self, b_output):
        ''' checks if the expected password prompt exists in b_output '''

        # the prompt is not localized
        return b_output.startswith(b"Password:")

    def build_become_command(self, cmd, shell):

        super(BecomeModule, self).build_become_command(cmd, shell)

        # Ansible needs to know we wait for a prompt, otherwise we get a
        # "Timeout (12s) waiting for privilege escalation prompt:"
        self.prompt = True

        if not cmd:
            return cmd

        exe = self.get_option('become_exe')

        flags = self.get_option('become_flags')
        return '%s %s %s' % (exe, flags, self._build_success_command(cmd, shell))

