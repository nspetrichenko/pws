"""
В коде должно быть минимум три основных класса HTML, TopLevelTag и Tag.
Класс HTML определяет, куда сохранять вывод: на экран через print или в файл.
Объекты класса TopLevelTag скорее всего не содержат внутреннего текста и всегда парные.
Объекта класса Tag могут быть непарные или быть парные и содержать текст внутри себя.

Должна быть возможность задать атрибуты в Tag, 
но в данном задании для TopLevelTag это необязательное условие.
"""


class TopLevelTag:
    def __init__(self, tag, **kwargs):
        self.tag = tag
        self.children = []

    def __iadd__(self, other):
        self.children.append(other)
        return self

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        html = "<%s>\n" % self.tag
        for child in self.children:
            html += str(child)
        html += "\n</%s>" % self.tag
        return html

# с наследованием
class HTML(TopLevelTag):
    def __init__(self, output=None):
        self.tag = "html"
        self.output = output
        self.children = []

    #__iadd__
    #__enter__
    def __exit__(self, *args, **kwargs):
        if self.output is not None: 
            with open(self.output, "w") as fp:
                fp.write(str(self))
        else:
            print(self)
    # __str__

# с наследованием
class Tag(TopLevelTag):
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        self.tag = tag
        self.text = ""
        self.attributes = {}

        self.is_single = is_single
        self.children = []

        if klass is not None: 
            self.attributes["class"] = " ".join(klass)

        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value

        #__enter__, __exit__, __iadd__

    def __str__(self):
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)

        if self.children:
            opening = "<{tag} {attrs}>".format(tag=self.tag, attrs=attrs)
            if self.text:
                internal = "%s" % self.text
            else:
                internal = ""
            for child in self.children:
                internal += str(child)
            ending = "</%s>" % self.tag
            return opening + internal + ending
        else:
            if self.is_single:
                return "<{tag} {attrs}/>".format(tag=self.tag, attrs=attrs)
            else:
                return "<{tag} {attrs}>{text}</{tag}>".format(
                    tag=self.tag, attrs=attrs, text=self.text
                )


def main(output=None):
    """
    функция на вход принимает один опциональный аргумент, который регулирует направление результата
    """
    with HTML(output=None) as doc:
        with TopLevelTag("head") as head:
            with Tag("title") as title:
                title.text = "Титул"
                head += title
            doc += head

        with TopLevelTag("body") as body:
            with Tag("h1", klass=("main-header",)) as h1:
                h1.text = "Заголовок"
                body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                with Tag("p") as paragraph:
                    paragraph.text = "Параграф"
                    div += paragraph

                with Tag("img", is_single=True, src="/picture.jpg") as img:
                    div += img

                body += div
                doc += body


if __name__ == "__main__":
    main()
