import __builtin__


class ContextElement(object):
    def __init__(self, type, id, attrs=None):
        if attrs is None:
            self.attrs = {}
        else:
            self.attrs = attrs
        self.type = type
        self.id = id

    def __setattr__(self, name, value):
        if name in ["attrs", "type", "id"]:
            self.__dict__[name] = value
        else:
            self.attrs[name] = value

    def __getattr__(self, name):
        return self.attrs[name]

    def to_dict_attr(self, k, v):
        return {"name": k,
                "value": str(v),
                "type": type(v).__name__}

    def to_dict(self):
        if self.type is None or self.id is None:
            return {}
        a = [self.to_dict_attr(k, v) for k, v in self.attrs.items()]
        return {"type": self.type,
                "id": self.id,
                "attributes": a}

    @classmethod
    def from_dict(cls, d):
        e = ContextElement(type=d.get("type", None), id=d.get("id", None))
        for a in d.get("attributes", []):
            typ = a.get("type", None)
            if typ is not None and typ not in ("dict", "NoneType"):
                t = getattr(__builtin__, typ)
                if a.get("name", None):
                    setattr(e, a["name"], t(a.get("value", None)))
        return e

    @classmethod
    def from_model(cls, m, serializer):
        t = "%s.%s" % (m._meta.app_label, m._meta.model_name)
        attrs = serializer(m).data
        return ContextElement(type=t, id=m.id, attrs=attrs)

    def __str__(self):
        return "<ContextElement type=%s, id=%s attrs=%s>" \
            % (self.type, self.id, self.attrs)

    __repr__ = __str__
