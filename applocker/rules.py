from sys import modules
from xml.etree.ElementTree import Element
from applocker.conditions import (FilePublisherCondition, FilePathCondition,
                                  FileHashCondition)


CONDITIONS = (FilePublisherCondition, FilePathCondition, FileHashCondition)


class _Rule(Element):
    def __init__(self, *, id=None, name, description='', user_or_group_sid,
                 action, conditions=[]):
        super(_Rule, self).__init__(self.__class__.__name__)
        self.id = id
        self.name = name
        self.description = description
        self.user_or_group_sid = user_or_group_sid
        self.action = action
        self.conditions = conditions

    @property
    def id(self):
        return self.get('Id')

    @id.setter
    def id(self, id):
        self.set('Id', id)

    @property
    def name(self):
        return self.get('Name')

    @name.setter
    def name(self, name):
        self.set('Name', name)

    @property
    def description(self):
        return self.get('Description')

    @description.setter
    def description(self, description):
        self.set('Description', description)

    @property
    def user_or_group_sid(self):
        return self.get('UserOrGroupSid')

    @user_or_group_sid.setter
    def user_or_group_sid(self, user_or_group_sid):
        self.set('UserOrGroupSid', user_or_group_sid)

    @property
    def action(self):
        return self.get('Action')

    @action.setter
    def action(self, action):
        self.set('Action', action)

    class _Conditions(Element):
        def __init__(self):
            super(_Rule._Conditions, self).__init__('Conditions')

    @property
    def conditions(self):
        return self.find('Conditions')

    @conditions.setter
    def conditions(self, conditions):
        new_conditions = self._Conditions()

        for condition in conditions:
            if isinstance(condition, CONDITIONS):
                new_conditions.append(condition)
            elif isinstance(condition, Element):
                new_conditions.append(
                    getattr(
                        modules[__name__],
                        condition.tag
                    ).from_element(condition)
                )

        self.append(new_conditions)

    @classmethod
    def from_element(cls, element):
        return cls(
            id=element.get('Id'),
            name=element.get('Name'),
            description=element.get('Description'),
            user_or_group_sid=element.get('UserOrGroupSid'),
            action=element.get('Action'),
            conditions=element.find('Conditions')
        )


class FilePublisherRule(_Rule):
    pass


class FilePathRule(_Rule):
    pass


class FileHashRule(_Rule):
    pass


RULES = (FilePublisherRule, FilePathRule, FileHashRule)


class RuleCollection(Element):
    def __init__(self, *, type, enforcement_mode, rules=[]):
        super(RuleCollection, self).__init__('RuleCollection')
        self.type = type
        self.enforcement_mode = enforcement_mode
        self.rules = rules

    @property
    def type(self):
        return self.get('Type')

    @type.setter
    def type(self, type):
        self.set('Type', type)

    @property
    def enforcement_mode(self):
        return self.get('EnforcementMode')

    @enforcement_mode.setter
    def enforcement_mode(self, enforcement_mode):
        self.set('EnforcementMode', enforcement_mode)

    @property
    def rules(self):
        return list(self)

    @rules.setter
    def rules(self, rules):
        for rule in rules:
            if isinstance(rule, RULES):
                self.append(rule)
            elif isinstance(rule, Element):
                self.append(
                    getattr(modules[__name__], rule.tag).from_element(rule)
                )

    @classmethod
    def from_element(cls, element):
        return cls(
            type=element.get('Type'),
            enforcement_mode=element.get('EnforcementMode'),
            rules=list(element)
        )
