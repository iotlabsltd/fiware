from .element import ContextElement


class UpdateContext(object):
    def __init__(self, elements, action="UPDATE"):
        self.elements = elements
        self.action = action  # UPDATE|APPEND

    def to_dict(self):
        return {
            "ContextElements": [e.to_dict() for e in self.elements],
            "updateAction": self.action,
        }

    @classmethod
    def from_dict(cls, d):
        elements = [ContextElement.from_dict(e) for e in d.get("contextElements", [])]
        action = d.get("updateAction", "UPDATE")
        return UpdateContext(elements, action)


class QueryContext(object):
    def __init__(self, entities, attr_names=None):
        self.entities = entities
        self.attr_names = attr_names if attr_names else []

    def to_dict(self):
        return {
            "entities": self.entities,
            "attributes": self.attr_names,
        }

    @classmethod
    def from_dict(cls, d):
        ret = QueryContext(d.get("entities", {}),
                           d.get("attributes", {}))
        return ret


class ContextResponses(object):
    def __init__(self, elements):
        self.elements = elements if elements else []
        # (ContextElement, status_code, reason)

    @classmethod
    def from_dict(cls, d):
        ret = ContextResponses(None)
        resp = d.get("contextResponses", None)
        if not resp:
            return None

        for r in resp:
            e = r.get("contextElement", None)
            if e is None:
                continue
            sc = r.get("statusCode", None)
            if sc is None:
                continue
            ce = ContextElement.from_dict(e)
            ret.elements.append((ce,
                                 int(sc.get("code", "500")),
                                 sc.get("reasonPhrase", "")))
        return ret

    def to_dict(self):
        return {"contextResponses":
                [{"contextElement": e[0].to_dict(),
                  "statusCode": {"code": str(e[1]), "reasonPhrase": e[2]}}
                 for e in self.elements]}
