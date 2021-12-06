from typing import TYPE_CHECKING, Any, Dict, Union

# Auto Generated Rules. Do not change manually
from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from typing import Optional

    from ansiblelint.file_utils import Lintable


class OctalPermissionsRule(AnsibleLintRule):
    id = 'risky-octal'
    shortdesc = 'Octal file permissions must contain leading zero or be a string'
    description = 'Numeric file permissions without leading zero can behave in unexpected ways. See https://docs.ansible.com/ansible/latest/collections/ansible/builtin/blockinfile_module.html for more details'
    tag = 'Formatting'

    _modules = ['blockinfile']

    def is_invalid_permission(self, mode: int) -> bool:
        # sensible file permission modes don't
        # have write bit set when read bit is
        # not set and don't have execute bit set
        # when user execute bit is not set.
        # also, user permissions are more generous than
        # group permissions and user and group permissions
        # are more generous than world permissions

        other_write_without_read = (
                mode % 8 and mode % 8 < 4 and not (mode % 8 == 1 and (mode >> 6) % 2 == 1)
        )
        group_write_without_read = (
                (mode >> 3) % 8
                and (mode >> 3) % 8 < 4
                and not ((mode >> 3) % 8 == 1 and (mode >> 6) % 2 == 1)
        )
        user_write_without_read = (
                (mode >> 6) % 8 and (mode >> 6) % 8 < 4 and not (mode >> 6) % 8 == 1
        )
        other_more_generous_than_group = mode % 8 > (mode >> 3) % 8
        other_more_generous_than_user = mode % 8 > (mode >> 6) % 8
        group_more_generous_than_user = (mode >> 3) % 8 > (mode >> 6) % 8

        return bool(
            other_write_without_read
            or group_write_without_read
            or user_write_without_read
            or other_more_generous_than_group
            or other_more_generous_than_user
            or group_more_generous_than_user
        )

    def matchtask(
            self, task: Dict[str, Any], file: 'Optional[Lintable]' = None
    ) -> Union[bool, str]:
        if task["action"]["__ansible_module__"] in self._modules:
            mode = task['action'].get('mode', None)

            if isinstance(mode, str):
                return False

            if isinstance(mode, int):
                return self.is_invalid_permission(mode)
        return False
