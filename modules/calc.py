"""
calc module — safe math expression evaluator
evaluates arithmetic expressions using ast parsing
only allows numbers, operators, and math functions
"""
import ast
import math
import operator
from pyrogram import Client

commands = ["calc", "math", "calculate"]

# safe operators for ast-based evaluation
SAFE_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

# allowed math functions
SAFE_FUNCS = {
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "radians": math.radians,
    "degrees": math.degrees,
    "log": math.log,
    "log10": math.log10,
    "log2": math.log2,
    "exp": math.exp,
    "abs": abs,
    "round": round,
    "floor": math.floor,
    "ceil": math.ceil,
    "pi": math.pi,
    "e": math.e,
    "tau": math.tau,
}


def _safe_eval(expr: str):
    """Evaluate a math expression safely using AST."""
    tree = ast.parse(expr.strip(), mode="eval")

    def _eval_node(node):
        if isinstance(node, ast.Expression):
            return _eval_node(node.body)
        elif isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"unsupported constant: {node.value}")
        elif isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"unsupported operator: {op_type.__name__}")
            return SAFE_OPERATORS[op_type](_eval_node(node.left), _eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type not in SAFE_OPERATORS:
                raise ValueError(f"unsupported unary operator: {op_type.__name__}")
            return SAFE_OPERATORS[op_type](_eval_node(node.operand))
        elif isinstance(node, ast.Call):
            func_name = node.func.id if isinstance(node.func, ast.Name) else None
            if func_name not in SAFE_FUNCS:
                raise ValueError(f"unsupported function: {func_name}")
            args = [_eval_node(arg) for arg in node.args]
            return SAFE_FUNCS[func_name](*args)
        elif isinstance(node, ast.Name):
            if node.id in ("pi", "e", "tau"):
                return SAFE_FUNCS[node.id]
            raise ValueError(f"unknown identifier: {node.id}")
        raise ValueError(f"unsupported syntax: {type(node).__name__}")

    return _eval_node(tree)


async def handle(app: Client, client: Client, message, args):
    if not args:
        await app.send_message(
            message.chat.id,
            "🧮 **calc** — evaluate math expressions\n"
            "Usage: `.calc 2 + 2 * 3`\n"
            "Functions: sqrt, sin, cos, tan, log, abs, round, floor, ceil\n"
            "Constants: pi, e, tau",
        )
        return

    expression = " ".join(args)
    try:
        result = _safe_eval(expression)
        # format: remove trailing zeros from floats
        if isinstance(result, float):
            formatted = f"{result:g}"
        else:
            formatted = str(result)
        await app.send_message(
            message.chat.id,
            f"🧮 **{expression}**\n= `{formatted}`",
        )
    except ValueError as e:
        await app.send_message(
            message.chat.id,
            f"📛 **Error:** {e}",
        )
    except Exception:
        await app.send_message(
            message.chat.id,
            "📛 **Error:** invalid expression",
        )
