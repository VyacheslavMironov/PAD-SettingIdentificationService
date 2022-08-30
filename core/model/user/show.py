from abc import ABC, abstractmethod


class AbstractUserInfo(ABC):
    @abstractmethod
    def abstract_access_token(self):
        pass

    @abstractmethod
    def abstract_role(self):
        pass

    @abstractmethod
    def abstract_organization_id(self):
        pass
