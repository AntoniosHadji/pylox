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


def test_or_truth():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/logical_operator/or_truth.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_and_truth():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/logical_operator/and_truth.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_and():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/logical_operator/and.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode


def test_or():
    test_file = '/mnt/projects/csdiy/compilers-8/bradfield/loxPy/tests/logical_operator/or.lox'  # noqa: E501
    resultp = subprocess.run(['python3', 'lox.py', test_file], capture_output=True)
    resultj = subprocess.run(['../craftinginterpreters/jlox', test_file], capture_output=True)
    assert resultp.returncode == resultj.returncode
