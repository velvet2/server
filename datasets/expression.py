import fnmatch
import pprint
import datetime
from .filter import func

def applyExpression(target, filter_tree):
    return _filter(target, filter_tree)

def coerceType(left, right, ops):
    # user prefer not to coerce type
    if ops == '===':
        return (left, right)

    return (left, right)

def _filter(target, filter_tree, method_call=False):
    left = None
    right = None
    if filter_tree['type'] == "BinaryExpression":
        left = _filter(target, filter_tree['left'])
        right = _filter(target, filter_tree['right'])

        if isinstance(left, str) and isinstance(right, str) and filter_tree['operator'] == '==':
            return fnmatch.fnmatch(left, right)
        else:
            left, right = coerceType(left, right, filter_tree.get('operator', '==='))
            return _applyOps(left, right, filter_tree.get('operator', None))

    elif filter_tree['type'] == "Compound":
        # Unknown
        return None

    elif filter_tree['type'] == "Identifier":
        if method_call is True:
            # add a check here ?
            left = func.get(filter_tree['name'], None)
            if left is None:
                raise Exception("function %s is not defined" % filter_tree['name'])
            else:
                return left
        else:
            return target.get(filter_tree['name'], None)

    elif filter_tree['type'] == "MemberExpression":
        left = _filter(target, filter_tree['object'])
        # print("LEFT", left)
        if left is None:
            return None;
        elif method_call is True:
            return (left, filter_tree['property']['name'])
        else:
            value = _filter(target, filter_tree['property'])
            return _filter(left, filter_tree['property'])

    elif filter_tree['type'] == "Literal":
        return filter_tree.get('value', None)

    elif filter_tree['type'] == "CallExpression":
        left = _filter(target, filter_tree['callee'], True)
        if callable(left) is False and len(left) == 2:
            # data['City'].sum()
            call_op = getattr(left[0], left[1])
            if callable(call_op) is True:
                return call_op()
            else:
                return None

        else:
            args = []
            for arg in filter_tree['arguments']:
                args.append(_filter(target,  arg))

            return left(*args)

    elif filter_tree['type'] == 'UnaryExpression':
        left = _filter(object, filter_tree['argument'])
        # handle manually
        return None

    elif filter_tree['type'] == 'LogicalExpression':
        left = _filter(target, filter_tree['left']);
        right = _filter(target, filter_tree['right']);
        # return eval(left + filter_tree.operator + right);
        return None

    elif filter_tree['type'] == 'ConditionalExpression':
        left = _filter(target, filter_tree['test'])
        if left :
            return filter_tree['consequent']['value']
        else:
            return filter_tree['alternate']['value']

    elif filter_tree['type'] == 'ArrayExpression':
        return [_filter(target, x) for x in filter_tree['elements']]
    else:
        return None

def _applyOps(left, right, operator):
    if operator == "==":
        return left == right
    elif operator == "===":
        return left == right
    elif operator == ">":
        return left > right
    elif operator == ">=":
        return left >= right
    elif operator == "<":
        return left < right
    elif operator == "<=":
        return left <= right
    elif operator == "+":
        return left + right
    elif operator == "-":
        return left - right
    elif operator == "*":
        return left * right
    elif operator == "/":
        return left / right
    elif operator == "&":
        return left & right
    elif operator == "|":
        return left | right
    elif operator == "%":
        return left % right
    else:
        return None

COMPOUND = 'Compound'
IDENTIFIER = 'Identifier'
MEMBER_EXP = 'MemberExpression'
LITERAL = 'Literal'
THIS_EXP = 'ThisExpression'
CALL_EXP = 'CallExpression'
UNARY_EXP = 'UnaryExpression'
BINARY_EXP = 'BinaryExpression'
LOGICAL_EXP = 'LogicalExpression'
CONDITIONAL_EXP = 'ConditionalExpression'
ARRAY_EXP = 'ArrayExpression'

PERIOD_CODE = 46 # '.'
COMMA_CODE  = 44 # ','
SQUOTE_CODE = 39 # single quote
DQUOTE_CODE = 34 # double quotes
OPAREN_CODE = 40 # (
CPAREN_CODE = 41 # )
OBRACK_CODE = 91 # [
CBRACK_CODE = 93 # ]
QUMARK_CODE = 63 # ?
SEMCOL_CODE = 59 # ;
COLON_CODE  = 58 # :

t = True
unary_ops = {'-': t, '!': t, '~': t, '+': t}
binary_ops = {
    '||': 1, '&&': 2, '|': 3,  '^': 4,  '&': 5,
    '==': 6, '!=': 6, '===': 6, '!==': 6,
    '<': 7,  '>': 7,  '<=': 7,  '>=': 7,
    '<<':8,  '>>': 8, '>>>': 8,
    '+': 9, '-': 9,
    '*': 10, '/': 10, '%': 10
}

this_str = 'this'

def getMaxKeyLen(obj):
    max_len = 0
    for key in obj.keys():
        if len(key) > max_len:
            max_len = len(key)
    return max_len

max_unop_len = getMaxKeyLen(unary_ops)
max_binop_len = getMaxKeyLen(binary_ops)

literals = {
    'true': True,
    'false': False,
    'null': None
}

def binaryPrecedence(op_val):
    return binary_ops.get(op_val, 0)

def createBinaryExpression(operator, left, right):
    if operator == '||' or operator == '&&':
        typ = LOGICAL_EXP
    else:
        typ = BINARY_EXP

    return {
        "type": typ,
        "operator": operator,
        "left": left,
        "right": right
    }

def isDecimalDigit(ch):
    if ch is None:
        return False
    else:
        return ch >= 48 and ch <= 57 # 0...9

def isIdentifierStart(ch):
    if ch is None:
        return False
    else:
        return ch == 36 or ch == 95 or (ch >= 65 and ch <= 90) or (ch >= 97 and ch <= 122) or (ch >= 128 and not binary_ops.get(chr(ch), None))
            # `$` and `_`
            # A...Z
            # a...z
            # any non-ASCII that is not an operator

def isIdentifierPart(ch):
    if ch is None:
        return False
    else:
        return ch == 36 or ch == 95 or (ch >= 65 and ch <= 90) or (ch >= 97 and ch <= 122) or (ch >= 48 and ch <= 57) or (ch >= 128 and not binary_ops.get(chr(ch), None))
            # `$` and `_`
            # A...Z
            # a...z
            # 0...9
            # any non-ASCII that is not an operator

class jsep(object):
    def __init__(self, expression):
        self.index = 0
        self.length = len(expression)
        self.expression = expression
        # begin

        nodes = []
        while self.index < self.length:
            ch_i = self.exprICode(self.index)
            if ch_i == SEMCOL_CODE or ch_i == COMMA_CODE:
                self.index = self.index + 1 # ignore separators
            else:
                node = self.gobbleExpression()
                if node:
                    nodes.append(node)
                elif self.index < self.length:
                    raise Exception('Unexpected "' + self.exprI(self.index) + '"', self.index)

        if len(nodes) == 1:
            self.parsed = nodes[0];
        else:
            self.parsed = {
                "type": COMPOUND,
                "body": nodes
            }

    def exprI(self, ind):
        return self.expression[ind] if ind < self.length else ""

    def exprICode(self, ind):
        return ord(self.expression[ind]) if ind < self.length else None

    def gobbleSpaces(self):
        ch = self.exprICode(self.index);
        while(ch == 32 or ch == 9):
            self.index = self.index + 1
            ch = self.exprICode(self.index)

    def gobbleExpression(self):
        test = self.gobbleBinaryExpression()
        self.gobbleSpaces()
        if self.exprICode(self.index) == QUMARK_CODE:
            self.index = self.index + 1
            consequent = self.gobbleExpression()
            if not consequent:
                raise Exception('Expected expression', self.index)

            self.gobbleSpaces();
            if self.exprICode(self.index) == COLON_CODE:
                self.index = self.index + 1
                alternate = self.gobbleExpression()
                if not alternate:
                    raise Exception('Expected expression', self.index)
                return {
                    "type": CONDITIONAL_EXP,
                    "test": test,
                    "consequent": consequent,
                    "alternate": alternate
                }
            else:
                raise Exception('Expected :', self.index)
        else:
            return test

    def gobbleBinaryOp(self):
        self.gobbleSpaces()
        to_check = self.expression[self.index:self.index+max_binop_len]
        tc_len = len(to_check)
        while tc_len > 0:
            if to_check in binary_ops :
                self.index += tc_len;
                return to_check;

            tc_len = tc_len - 1
            to_check = to_check[0:tc_len]
        return False


    def gobbleBinaryExpression(self):
        left = self.gobbleToken()
        biop = self.gobbleBinaryOp()
        if not biop:
            return left

        biop_info = { "value": biop, "prec": binaryPrecedence(biop)}
        right = self.gobbleToken();
        if not right:
            raise Exception("Expected expression after " + biop, self.index)
        stack = [left, biop_info, right]
        while True:
            biop = self.gobbleBinaryOp()
            prec = binaryPrecedence(biop);
            if prec == 0:
                break;
            biop_info = { "value": biop, "prec": prec };

            while len(stack) > 2 and prec <= stack[len(stack) - 2]['prec']:
                right = stack.pop();
                biop = stack.pop()['value'];
                left = stack.pop();
                node = createBinaryExpression(biop, left, right);
                stack.append(node);

            node = self.gobbleToken();
            if not node:
                raise Exception("Expected expression after " + biop, self.index);
            stack.append(biop_info)
            stack.append(node)

        i = len(stack) - 1
        node = stack[i];
        while i > 1:
            node = createBinaryExpression(stack[i - 1]['value'], stack[i - 2], node);
            i -= 2;

        return node;

    def gobbleToken(self):
        self.gobbleSpaces()
        ch = self.exprICode(self.index)
        if isDecimalDigit(ch) or ch == PERIOD_CODE:
            return self.gobbleNumericLiteral()
        elif ch == SQUOTE_CODE or ch == DQUOTE_CODE:
            return self.gobbleStringLiteral()
        elif isIdentifierStart(ch) or ch == OPAREN_CODE: # { // open parenthesis
            return self.gobbleVariable()
        elif ch == OBRACK_CODE:
            return self.gobbleArray()
        else:
            to_check = self.expression[self.index:self.index+max_unop_len]
            tc_len = len(to_check)
            while tc_len > 0 :
                if to_check in unary_ops:
                    self.index = self.index + tc_len;
                    return {
                        "type": UNARY_EXP,
                        "operator": to_check,
                        "argument": self.gobbleToken(),
                        "prefix": True
                    }
                tc_len = tc_len - 1
                to_check = to_check[0:tc_len]

            return False

    def gobbleNumericLiteral(self):
        number = ''
        while isDecimalDigit(self.exprICode(self.index)):
            number = number + self.exprI(self.index)
            self.index = self.index + 1

        if self.exprICode(self.index) == PERIOD_CODE: # { // can start with a decimal marker
            number += self.exprI(self.index)
            self.index = self.index + 1

            while isDecimalDigit(self.exprICode(self.index)):
                number += self.exprI(self.index)
                self.index = self.index + 1

        ch = self.exprI(self.index)
        if ch == 'e' or ch == 'E':  # exponent marker
            number += self.exprI(self.index)
            self.index = self.index + 1

            ch = self.exprI(self.index)
            if ch == '+' or ch == '-': #  // exponent sign
                number += self.exprI(self.index)
                self.index = self.index + 1

            while isDecimalDigit(self.exprICode(self.index)): #{ //exponent itself
                number += self.exprI(self.index)
                self.index = self.index + 1

            if not isDecimalDigit(self.exprICode(self.index-1)):
                raise Exception('Expected exponent (' + number + self.exprI(self.index) + ')', self.index);

        chCode = self.exprICode(self.index)
        if isIdentifierStart(chCode):
            raise Exception('Variable names cannot start with a number (' + number + self.exprI(self.index) + ')', self.index)
        elif chCode == PERIOD_CODE:
            raise Exception('Unexpected period', self.index)

        return {
            "type": LITERAL,
            "value": float(number),
            "raw": number
        }

    def gobbleStringLiteral(self):
        strr = ''
        quote = self.exprI(self.index)
        self.index = self.index + 1
        closed = False

        while self.index < self.length:
            ch = self.exprI(self.index)
            self.index = self.index + 1
            if ch == quote:
                closed = True
                break
            elif ch == '\\':
                ch = self.exprI(self.index)
                self.index = self.index + 1
                self.index = self.index + 1
                if ch == 'n':
                    strr += '\n'
                elif ch == 'r':
                    strr += '\r'
                elif ch == 't':
                    strr += '\t'
                elif ch == 'b':
                    strr += '\b'
                elif ch == 'f':
                    strr += '\f'
                elif ch == 'v':
                    strr += '\v'
                else:
                    strr += '\\'
            else:
                strr += ch

        if not closed:
            raise Exception('Unclosed quote after "'+strr+'"', self.index);

        return {
            "type": LITERAL,
            "value": strr,
            "raw": quote + strr + quote
        }

    def gobbleIdentifier(self):
        ch = self.exprICode(self.index)
        start = self.index

        if isIdentifierStart(ch):
            self.index = self.index + 1
        else:
            raise Exception('Unexpected ' + self.exprI(self.index), self.index)


        while self.index < self.length:
            ch = self.exprICode(self.index)
            if isIdentifierPart(ch):
                self.index = self.index + 1
            else:
                break

        identifier = self.expression[start:self.index]
        if identifier in literals:
            return {
                "type": LITERAL,
                "value": literals[identifier],
                "raw": identifier
            }
        elif identifier == this_str:
            return { "type": THIS_EXP }
        else:
            return {
                "type": IDENTIFIER,
                "name": identifier
            }

    def gobbleArguments(self, termination):
        args = []
        closed = False
        while self.index < self.length:
            self.gobbleSpaces()
            ch_i = self.exprICode(self.index)
            if ch_i == termination: # // done parsing
                closed = True
                self.index = self.index + 1
                break;
            elif ch_i == COMMA_CODE: # // between expressions
                self.index = self.index + 1
            else:
                node = self.gobbleExpression()
                if not node or node['type'] == COMPOUND:
                    raise Exception('Expected comma', self.index);
                args.append(node)

        if not closed:
            raise Exception('Expected ' + chr(termination), self.index)

        return args

    def gobbleVariable(self):
        ch_i = self.exprICode(self.index)
        node = self.gobbleGroup() if ch_i == OPAREN_CODE else self.gobbleIdentifier()
        self.gobbleSpaces()
        ch_i = self.exprICode(self.index)
        while ch_i == PERIOD_CODE or ch_i == OBRACK_CODE or ch_i == OPAREN_CODE:
            self.index = self.index + 1
            if ch_i == PERIOD_CODE:
                self.gobbleSpaces();
                node = {
                    "type": MEMBER_EXP,
                    "computed": False,
                    "object": node,
                    "property": self.gobbleIdentifier()
                }
            elif  ch_i == OBRACK_CODE:
                node = {
                    "type": MEMBER_EXP,
                    "computed": True,
                    "object": node,
                    "property": self.gobbleExpression()
                }
                self.gobbleSpaces()
                ch_i = self.exprICode(self.index)
                if ch_i != CBRACK_CODE:
                    raise Exception('Unclosed [', self.index)
                self.index = self.index + 1
            elif ch_i == OPAREN_CODE:
                node = {
                    "type": CALL_EXP,
                    'arguments': self.gobbleArguments(CPAREN_CODE),
                    "callee": node
                };

            self.gobbleSpaces()
            ch_i = self.exprICode(self.index)
        return node;

    def gobbleGroup(self):
        self.index = self.index + 1
        node = self.gobbleExpression()
        self.gobbleSpaces()
        if self.exprICode(self.index) == CPAREN_CODE:
            self.index = self.index + 1
            return node
        else:
            raise Exception('Unclosed (', self.index)

    def gobbleArray(self):
        self.index = self.index + 1
        return {
            "type": ARRAY_EXP,
            "elements": self.gobbleArguments(CBRACK_CODE)
        }

    def getParsed(self):
        return self.parsed
# jsep("123")
