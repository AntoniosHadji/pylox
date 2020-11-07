import subprocess

EXPECT_FAIL_65 = [
    'prefix_operator',
    'grouping',
    'infix_operator',
    'to_this',
    'inherit_self',
    'local_inherit_self',
    'return_value',
    'parenthesized_superclass',
    'missing_argument',
    'var_in_body',
    'fun_in_body',
    'class_in_body',
    'trailing_dot',
    'leading_dot',
    'decimal_point_at_eof',
    'use_nil_as_var',
    'use_local_in_initializer',
    'use_this_as_var',
    'duplicate_local',
    'duplicate_parameter',
    'collide_with_parameter',
    'use_false_as_var',
    'unterminated',
    'parenthesized',
    'no_superclass_bind',
    'super_without_dot',
    'super_at_top_level',
    'no_reuse_constants',
    'super_without_name',
    'no_superclass_call',
    'super_in_top_level_function',
    'too_many_constants',
    'too_many_upvalues',
    'too_many_locals',
    'loop_too_large',
    'trees',
    'this_at_top_level',
    'this_in_top_level_function',
    'statement_initializer',
    'statement_increment',
    'statement_condition',
    'gunexpected_character',
    'too_many_arguments',
    'too_many_parameters',
    'missing_comma_in_parameters',
    'fun_in_then',
    'fun_in_else',
    'var_in_else',
    'class_in_then',
    'body_must_be_block',
    'class_in_else',
    'var_in_then',
    'at_top_level',
]
EXPECT_FAIL_70 = [
    'undefined',
    'object',
    'bool',
    'nil',
    'string',
    'num',
    'extra_arguments',
    'missing_arguments',
    'default_arguments',
    'get_on_string',
    'no_superclass_method',
    'error_after_multiline',
    'undefined_local',
    'undefined_global',
    'less_nonnum_num',
    'multiply_num_nonnum',
    'add_bool_num',
    'add_bool_nil',
    'greater_or_equal_num_nonnum',
    'greater_or_equal_nonnum_num',
    'less_num_nonnum',
    'add_nil_nil',
    'less_or_equal_nonnum_num',
    'negate_nonnum',
    'less_or_equal_num_nonnum',
    'add_bool_string',
    'subtract_num_nonnum',
    'multiply_nonnum_num',
    'add_string_nil',
    'subtract_nonnum_num',
    'divide_num_nonnum',
    'add_num_nil',
    'divide_nonnum_num',
    'greater_num_nonnum',
    'greater_nonnum_num',
    'inherit_from_function',
    'refer_to_name',
    'local_mutual_recursion',
    'not_found',
    'stack_overflow',
    'inherit_from_number',
    'inherit_from_nil',
    'set_on_class',
    'get_on_function',
    'call_nonfunction_field',
    'get_on_nil',
    'set_on_num',
    'set_on_string',
    'get_on_bool',
    'get_on_class',
    'set_on_bool',
    'set_evaluation_order',
    'get_on_num',
    'set_on_nil',
    'set_on_function',
]


def test_indirectly_inherited():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/indirectly_inherited.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_closure():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/closure.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_call_same_method():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/call_same_method.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_super_in_closure_in_inherited_method():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/super_in_closure_in_inherited_method.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_parenthesized():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/parenthesized.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_no_superclass_method():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/no_superclass_method.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_super_in_top_level_function():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/super_in_top_level_function.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_no_superclass_call():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/no_superclass_call.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_super_in_inherited_method():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/super_in_inherited_method.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_super_without_name():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/super_without_name.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_constructor():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/constructor.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_super_at_top_level():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/super_at_top_level.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_extra_arguments():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/extra_arguments.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_bound_method():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/bound_method.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_missing_arguments():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/missing_arguments.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_super_without_dot():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/super_without_dot.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_reassign_superclass():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/reassign_superclass.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_call_other_method():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/call_other_method.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_no_superclass_bind():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/no_superclass_bind.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_this_in_superclass_method():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/super/this_in_superclass_method.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode
