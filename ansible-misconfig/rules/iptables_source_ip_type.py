import re
from typing import TYPE_CHECKING, Any, Dict, Union

# Auto Generated Rules. Do not change manually
from ansiblelint.rules import AnsibleLintRule

if TYPE_CHECKING:
    from typing import Optional

    from ansiblelint.file_utils import Lintable


class IPTypeRule(AnsibleLintRule):
    id = 'risky-octal'
    shortdesc = 'IP address must be in valid format'
    description = 'IP address must be in valid format. See https://docs.ansible.com/ansible/latest/collections/ansible/builtin/iptables_module.html for more details'
    tag = 'Formatting'

    _modules = ['iptables']

    def is_invalid_ip(self, ip: str) -> bool:
        return bool(re.match(
            "^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(:((6553[0-5])|(655[0-2][0-9])|(65[0-4][0-9]{2})|(6[0-4][0-9]{3})|([1-5][0-9]{4})|([0-5]{0,5})|([0-9]{1,4})))?$",
            ip))

    def matchtask(
            self, task: Dict[str, Any], file: 'Optional[Lintable]' = None
    ) -> Union[bool, str]:
        if task["action"]["__ansible_module__"] in self._modules:
            ip = task['action'].get('source', None)

            if isinstance(ip, str):
                return self.is_invalid_ip(ip)
        return False
