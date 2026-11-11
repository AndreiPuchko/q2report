#    Copyright (C) 2021 Andrei Puchko
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

import ast
from decimal import Decimal
import datetime
import re

class WHITE_LIST_BROKEN(Exception):
    pass



def is_sub_list(sublst, lst):
    return len([x for x in sublst if x in lst]) == len(sublst)


def int_(toInt):
    try:
        return int(f"{toInt}")
    except Exception:
        return int(num(toInt))


def float_(toFloat):
    try:
        return float(f"{toFloat}")
    except Exception:
        return float(num(toFloat))


def num(tonum):
    try:
        return Decimal(f"{tonum}")
    except Exception:
        return 0


def today():
    return datetime.date.today()


class dotdict(dict):
    """dot.notation access to dictionary attributes"""

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def set_dict_default(_dict, _key, _value):
    """set only key does not exist"""

    if not _dict.get(_key):
        _dict[_key] = _value


inch = num(72.0)
cm = num(28.35)
mm = cm * num(0.1)
pica = num(12.0)
pt = num(1.0)
twip = num(20.0)

reMultiSpaceDelete = re.compile(r"[\s]+")
reDecimal = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$")
reNumber = re.compile(r"\d+")


class Q2Heap:
    pass


class TotalControlTransformer(ast.NodeTransformer):
    def __init__(self):
        self.placeholders = {}
        self.counter = 0

    def _next_ph(self, type_str, original_value):
        ph_name = f"ph_{self.counter:04d}"
        self.counter += 1
        self.placeholders[ph_name] = {"type": type_str, "value": original_value}
        return ph_name

    def _parse_rep_chain(self, node):
        """
        Рекурсивный хелпер.
        """
        # Базовый случай: перемнная
        if isinstance(node, ast.Name):
            return node.id

        # Случай 1: Атрибут (.supplier)
        if isinstance(node, ast.Attribute):
            base = self._parse_rep_chain(node.value)
            if base is not None:
                if node.attr.startswith("_"):
                    raise WHITE_LIST_BROKEN(f"Access to private attribute banned: {node.attr}")
                return f"{base}.{node.attr}"

        # Случай 2: Индекс ([0] или ['phone'])
        if isinstance(node, ast.Subscript):
            base = self._parse_rep_chain(node.value)
            if base is not None:
                # Извлекаем сам индекс (поддерживаем только числа и строки)
                if isinstance(node.slice, ast.Constant):
                    idx_val = node.slice.value
                    if isinstance(idx_val, str) and idx_val.startswith("_"):
                        raise WHITE_LIST_BROKEN(f"Access to private keys banned: {idx_val}")
                    return f"{base}[{repr(idx_val)}]"
                else:
                    raise WHITE_LIST_BROKEN("Dynamic/complex expressions inside brackets [] are not allowed")

        # Случай 3: Вызов метода на объекте rep (.get('phone'))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            base = self._parse_rep_chain(node.func.value)
            if base is not None:
                method_name = node.func.attr
                # Собираем аргументы метода (только константы для безопасности)
                args_repr = []
                for arg in node.args:
                    if isinstance(arg, ast.Constant):
                        args_repr.append(repr(arg.value))
                    else:
                        raise WHITE_LIST_BROKEN("Only constant arguments are allowed in data methods")

                args_str = ", ".join(args_repr)
                return f"{base}.{method_name}({args_str})"

        return None

    def visit_Attribute(self, node):
        chain = self._parse_rep_chain(node)
        if chain is not None:
            ph_name = self._next_ph("data_chain", chain)
            return ast.Name(id=ph_name, ctx=ast.Load())
        return self.generic_visit(node)

    def visit_Subscript(self, node):
        chain = self._parse_rep_chain(node)
        if chain is not None:
            ph_name = self._next_ph("data_chain", chain)
            return ast.Name(id=ph_name, ctx=ast.Load())
        return self.generic_visit(node)

    def visit_Call(self, node):
        # Проверяем, не является ли весь этот вызов цепочкой данных (напр. rep.d.get('phone'))
        chain = self._parse_rep_chain(node)
        if chain is not None:
            ph_name = self._next_ph("data_chain", chain)
            return ast.Name(id=ph_name, ctx=ast.Load())

        # Если это обычный вызов функции (напр. round(...)), обрабатываем внутренности
        node.args = [self.visit(arg) for arg in node.args]
        node.keywords = [self.visit(kw) for kw in node.keywords]

        if isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name.startswith("__"):
                raise WHITE_LIST_BROKEN(f"Dunder functions are forbidden: {func_name}")

            ph_name = self._next_ph("function", func_name)
            node.func = ast.Name(id=ph_name, ctx=ast.Load())

        return node

    def visit_Name(self, node):
        # Перехватываем изолированные переменные (price, qt)
        if node.id.startswith("__"):
            raise WHITE_LIST_BROKEN(f"Dunder names are strictly forbidden: {node.id}")

        ph_name = self._next_ph("variable", node.id)
        return ast.Name(id=ph_name, ctx=ast.Load())
