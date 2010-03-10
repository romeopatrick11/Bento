import os

import ply
import ply.lex
import ply.yacc

from toydist.core.parser.lexer \
    import \
        MyLexer, tokens

from toydist.core.parser.nodes \
    import \
        Node

_PICKLED_PARSETAB = os.path.join(os.path.dirname(__file__), "parsetab")
_OPTIMIZE_LEX = 0
_DEBUG_YACC = 1

class Parser(object):
    def __init__(self, lexer=None):
        if lexer is None:
            self.lexer = MyLexer(stage=5, optimize=_OPTIMIZE_LEX)
        else:
            self.lexer = lexer

        self.parser = ply.yacc.yacc(start="stmt_list",
                                    picklefile=_PICKLED_PARSETAB,
                                    debug=_DEBUG_YACC)

    def parse(self, data):
        return self.parser.parse(data, lexer=self.lexer)

def parse(data):
    parser = Parser()
    return parser.parse(data)

#-------------
#   Grammar
#-------------
def p_stmt_list(p):
    """stmt_list : stmt_list stmt"""
    p[0] = p[1]
    if p[2].type not in ("newline",):
        p[0].children.append(p[2])

def p_stmt_list_term(p):
    """stmt_list : stmt"""
    p[0] = Node("stmt_list", children=[p[1]])

def p_stmt_list_empty(p):
    """stmt_list : empty"""
    pass

def p_stmt_list_newline(p):
    """stmt_list : NEWLINE"""
    pass

def p_stmt(p):
    """stmt : meta_stmt
            | library
            | exec
            | path
            | flag
            | extra_sources
            | data_files
    """
    p[0] = p[1]

def p_empty(p):
    """empty : """
    pass

#----------------
#   Meta data
#----------------
def p_meta_stmt(p):
    """meta_stmt : meta_name_stmt
                 | meta_summary_stmt
                 | meta_description_stmt
                 | meta_version_stmt
                 | meta_url_stmt
                 | meta_download_url_stmt
                 | meta_author_stmt
                 | meta_author_email_stmt
                 | meta_maintainer_stmt
                 | meta_maintainer_email_stmt
                 | meta_license_stmt
                 | meta_platforms_stmt
                 | meta_classifiers_stmt
    """
    p[0] = p[1]

def p_meta_name_stmt(p):
    """meta_name_stmt : NAME_ID COLON WORD
    """
    p[0] = Node("name", value=p[3])

def p_meta_summary_stmt(p):
    """meta_summary_stmt : SUMMARY_ID COLON single_line_value
    """
    p[0] = Node("summary", value=p[3])

def p_meta_url_stmt(p):
    """meta_url_stmt : URL_ID COLON anyword
    """
    p[0] = Node("url", value=p[3].value)

def p_meta_download_url_stmt(p):
    """meta_download_url_stmt : DOWNLOAD_URL_ID COLON anyword
    """
    p[0] = Node("download_url", value=p[3].value)

def p_meta_author_stmt(p):
    """meta_author_stmt : AUTHOR_ID COLON anyword
    """
    p[0] = Node("author", value=p[3].value)

def p_meta_author_email_stmt(p):
    """meta_author_email_stmt : AUTHOR_EMAIL_ID COLON anyword
    """
    p[0] = Node("author_email", value=p[3].value)

def p_meta_maintainer_stmt(p):
    """meta_maintainer_stmt : MAINTAINER_ID COLON anyword
    """
    p[0] = Node("maintainer", value=p[3].value)

def p_meta_maintainer_email_stmt(p):
    """meta_maintainer_email_stmt : MAINTAINER_EMAIL_ID COLON anyword
    """
    p[0] = Node("maintainer_email", value=p[3].value)

def p_meta_license_stmt(p):
    """meta_license_stmt : LICENSE_ID COLON anyword
    """
    p[0] = Node("license", value=p[3].value)

def p_meta_platforms_stmt(p):
    """meta_platforms_stmt : PLATFORMS_ID COLON anyword
    """
    p[0] = Node("platforms", value=p[3].value)

def p_meta_version_stmt(p):
    """meta_version_stmt : VERSION_ID COLON version
    """
    p[0] = Node("version", value=p[3].value)

def p_meta_classifiers_stmt_single_line(p):
    """meta_classifiers_stmt : CLASSIFIERS_ID COLON classifier"""
    p[0] = Node("classifiers", children=[p[3]])

def p_meta_classifiers_stmt_indent(p):
    """meta_classifiers_stmt : CLASSIFIERS_ID COLON NEWLINE INDENT \
                               classifiers_list DEDENT
    """
    p[0] = Node("classifiers", children=[p[5]])

def p_meta_classifiers_stmt(p):
    """meta_classifiers_stmt : CLASSIFIERS_ID COLON classifier NEWLINE \
                               INDENT classifiers_list DEDENT
    """
    p[0] = Node("classifiers", children=[p[3], p[6]])

def p_classifiers_list(p):
    """classifiers_list : classifier NEWLINE classifiers_list
    """
    p[0] = p[3]
    p[0].children.insert(0, p[1])

def p_classifiers_list_term(p):
    """classifiers_list : classifier
    """
    p[0] = Node("classifiers_list", children=[p[1]])

def p_classifier(p):
    """classifier : literal_line"""
    p[0] = p[1]
    p[0].value = "".join(p[0].value)
    p[0].type = "classifier"

#---------------------------------------
# Data files and extra sources handling
#---------------------------------------
def p_extra_sources(p):
    """extra_sources : EXTRA_SOURCES_ID COLON comma_list"""
    p[0] = Node("extra_sources", value=p[3].value)
 
def p_data_files(p):
    """data_files : data_files_declaration INDENT data_files_stmts DEDENT
    """
    p[0] = Node("data_files", children=[p[1]])
    p[0].children.append(p[3])

def p_data_files_declaration(p):
    """data_files_declaration : DATAFILES_ID COLON word"""
    p[0] = Node("data_files_declaration", value=p[3].value)

def p_data_files_stmts(p):
    """data_files_stmts : data_files_stmts data_files_stmt"""
    p[0] = Node("data_files_stmts", children=(p[1].children + [p[2]]))

def p_data_files_stmts_term(p):
    """data_files_stmts : data_files_stmt"""
    p[0] = Node("data_files_stmts", children=[p[1]])

def p_data_files_stmt(p):
    """data_files_stmt : data_files_target
                       | data_files_files
                       | data_files_srcdir
    """
    p[0] = p[1]

def p_data_files_target(p):
    """data_files_target : TARGET_ID COLON anyword"""
    p[0] = Node("target_dir", value=p[3].value)

def p_data_files_srcdir(p):
    """data_files_srcdir : SRCDIR_ID COLON anyword"""
    p[0] = Node("source_dir", value=p[3].value)

def p_data_files_files(p):
    """data_files_files : FILES_ID COLON comma_list"""
    p[0] = Node("files", value=p[3].value)

#---------------------
#   Library section
#---------------------
def p_library(p):
    """library : library_declaration INDENT library_stmts DEDENT
    """
    p[0] = Node("library", children=[p[1]])
    p[0].children.append(p[3])

def p_library_decl_only(p):
    """library : library_declaration
    """
    p[0] = Node("library", children=[p[1]])

def p_library_declaration(p):
    """library_declaration : LIBRARY_ID COLON library_name"""
    p[0] = p[3]

def p_library_name(p):
    """library_name : word
                    |"""
    if len(p) == 1:
        name = "default"
    else:
        name = p[1]
    p[0] = Node("library_name", value=name)

def p_library_stmts(p):
    """library_stmts : library_stmts library_stmt
    """
    children = p[1].children
    children.append(p[2])
    p[0] = Node("library_stmts", children=children)

def p_library_stmts_term(p):
    """library_stmts : library_stmt
    """
    p[0] = Node("library_stmts", children=[p[1]])

def p_library_stmt(p):
    """library_stmt : modules_stmt
                    | packages_stmt
                    | extension_stmt
                    | build_requires_stmt
                    | install_requires_stmt
                    | conditional_stmt
    """
    p[0] = p[1]

def p_packages_stmt(p):
    """packages_stmt : PACKAGES_ID COLON comma_list"""
    p[0] = Node("packages", value=p[3].value)

def p_modules_stmt(p):
    """modules_stmt : MODULES_ID COLON comma_list"""
    p[0] = Node("modules", value=p[3].value)

def p_build_requires_stmt(p):
    """build_requires_stmt : BUILD_REQUIRES_ID COLON comma_list"""
    p[0] = Node("build_requires", value=p[3].value)

def p_install_requires_stmt(p):
    """install_requires_stmt : INSTALL_REQUIRES_ID COLON comma_list"""
    p[0] = Node("install_requires", value=p[3].value)

def p_extension_stmt_content(p):
    """extension_stmt : extension_decl INDENT extension_fields DEDENT"""
    p[0] = Node("extension", children=[p[1]])
    p[0].children.append(p[3])

def p_extension_decl(p):
    """extension_decl : EXTENSION_ID COLON anyword"""
    p[0] = Node("extension_declaration", value=p[3].value)

def p_extension_fields(p):
    """extension_fields : SOURCES_ID COLON comma_list"""
    p[0] = Node("sources", value=p[3].value)

#---------------------
# Conditional handling
#---------------------
def p_conditional_if_only(p):
    """conditional_stmt : IF test COLON INDENT library_stmts DEDENT"""
    p[0] = Node("conditional", value=p[2], children=[p[5]])

def p_conditional_if_else(p):
    """conditional_stmt : IF test COLON INDENT library_stmts DEDENT \
                          ELSE COLON INDENT library_stmts DEDENT
    """
    p[0] = Node("conditional", value=p[2], children=[p[5], p[10]])

def p_test(p):
    """test : bool
            | os_var
            | flag_var"""
    p[0] = p[1]

def p_os_var(p):
    """os_var : OS_OP LPAR word RPAR"""
    p[0] = Node("osvar", value=p[3])

def p_flag_var(p):
    """flag_var : FLAG_OP LPAR word RPAR"""
    p[0] = Node("flagvar", value=p[3])

def p_cond_expr_true(p):
    """bool : TRUE"""
    p[0] = Node("bool", value=True)

def p_cond_expr_false(p):
    """bool : FALSE"""
    p[0] = Node("bool", value=False)

#---------------------
#   Path section
#---------------------
def p_path(p):
    """path : path_declaration INDENT path_stmts DEDENT"""
    p[0] = Node("path", children=[p[1], p[3]])

def p_path_declaration(p):
    """path_declaration : PATH_ID COLON anyword"""
    p[0] = Node("path_declaration", value=p[3].value)

def p_path_stmts(p):
    """path_stmts : path_stmts path_stmt"""
    p[0] = Node("path_stmts", children=(p[1].children + [p[2]]))

def p_path_stmts_term(p):
    """path_stmts : path_stmt"""
    p[0] = Node("path_stmts", children=[p[1]])

def p_path_stmt(p):
    """path_stmt : path_description
                 | path_default"""
    p[0] = p[1]

def p_path_description(p):
    """path_description : DESCRIPTION_ID COLON single_line_value"""
    #"""path_description : meta_description_stmt"""
    p[0] = Node("path_description", value=p[3])

def p_path_default(p):
    """path_default : DEFAULT_ID COLON anyword"""
    p[0] = Node("path_default", value=p[3].value)

#------------------
#   Flag section
#------------------
def p_flag(p):
    """flag : flag_declaration INDENT flag_stmts DEDENT"""
    p[0] = Node("flag", children=[p[1], p[3]])

def p_flag_declaration(p):
    """flag_declaration : FLAG_ID COLON anyword"""
    p[0] = Node("flag_declaration", value=p[3].value)

def p_flag_stmts(p):
    """flag_stmts : flag_stmts flag_stmt"""
    p[0] = Node("flag_stmts", children=(p[1].children + [p[2]]))

def p_flag_stmts_term(p):
    """flag_stmts : flag_stmt"""
    p[0] = Node("flag_stmts", children=[p[1]])

def p_flag_stmt(p):
    """flag_stmt : flag_description
                 | flag_default"""
    p[0] = p[1]

def p_flag_description(p):
    """flag_description : DESCRIPTION_ID COLON single_line_value"""
    #"""flag_description : meta_description_stmt"""
    p[0] = Node("flag_description", value=p[3])

def p_flag_default(p):
    """flag_default : DEFAULT_ID COLON anyword"""
    p[0] = Node("flag_default", value=p[3].value)

#----------------------
#  Executable section
#----------------------
def p_executable(p):
    """exec : exec_decl INDENT exec_stmts DEDENT"""
    p[0] = Node("executable", children=[p[1], p[3]])

def p_exec_declaration(p):
    """exec_decl : EXECUTABLE_ID COLON anyword"""
    p[0] = Node("exec_name", value=p[3].value)

def p_exec_stmts(p):
    """exec_stmts : exec_stmts exec_stmt"""
    p[0] = Node("exec_stmts", children=(p[1].children + [p[2]]))

def p_exec_stmts_term(p):
    """exec_stmts : exec_stmt"""
    p[0] = Node("exec_stmts", children=[p[1]])

def p_exec_stmt(p):
    """exec_stmt : function
                 | module"""
    p[0] = p[1]

def p_exec_module(p):
    """module : MODULE_ID COLON anyword"""
    p[0] = Node("module", value=p[3].value)

def p_exec_function(p):
    """function : FUNCTION_ID COLON anyword"""
    p[0] = Node("function", value=p[3].value)

#-----------------------
#   Literal handling
#-----------------------

def p_comma_list_indented(p):
    """comma_list : indented_comma_list 
    """
    p[0] = Node("comma_list", value=p[1].value)

def p_comma_list(p):
    """comma_list : comma_words
    """
    p[0] = Node("comma_list", value=p[1].value)

def p_indented_comma_list(p):
    """indented_comma_list : comma_words COMMA INDENT comma_words DEDENT
    """
    p[0] = p[1]
    p[0].value.extend(p[4].value)

def p_indented_comma_list_term(p):
    """indented_comma_list : INDENT comma_words DEDENT
    """
    p[0] = p[2]

def p_comma_words(p):
    """comma_words : comma_words COMMA anyword_comma_list
    """
    p[0] = p[1]
    p[0].value.append(p[3].value)

def p_comma_words_term(p):
    """comma_words : anyword_comma_list
    """
    p[0] = Node("comma_words", value=[p[1].value])

# We produce a flat list here to speed things up (should do the same for
# description field)
def p_literal_line(p):
    """literal_line : literal literal_line"""
    p[0] = p[2]
    p[2].value.insert(0, p[1].value)

def p_literal_line_term(p):
    """literal_line : literal"""
    p[0] = Node("literal_line", value=[p[1].value])

def p_single_line(p):
    """single_line_value : WS single_line"""
    p[0] = p[2]

def p_single_line_no_space(p):
    """single_line_value : single_line"""
    p[0] = p[1]

def p_single_line_string(p):
    """single_line : single_line literal"""
    p[0] = p[1] + [p[2]]

def p_single_line_string_term(p):
    """single_line : literal_no_space"""
    p[0] = [p[1]]

def p_meta_description_stmt_start_same_line(p):
    """meta_description_stmt : description_decl single_line_newline \
                               INDENT multi_stmts DEDENT
    """
    p[0] = Node("description", value=(p[2].value + p[4]))

def p_meta_description_stmt_indented_block(p):
    """meta_description_stmt : description_decl NEWLINE \
                               INDENT multi_stmts DEDENT
    """
    p[0] = Node("description", value=p[4])

def p_meta_description_stmt_indented_block2(p):
    """meta_description_stmt : description_decl WS NEWLINE \
                               INDENT multi_stmts DEDENT
    """
    p[0] = Node("description", value=p[5])

def p_meta_description_stmt_single(p):
    """meta_description_stmt : description_decl single_line_value
    """
    p[0] = Node("description", value=p[2])

def p_single_line_newline(p):
    """single_line_newline : single_line_value newline
    """
    p[0] = Node("single_line_newline", value=(p[1] + [p[2]]))

def p_description_decl(p):
    """description_decl : DESCRIPTION_ID COLON"""
    p[0] = Node("description_decl")

def p_indented_block(p):
    """indented_block : indent indented_block_value"""
    p[0] = [p[1]] + p[2]

def p_indented_block_value(p):
    """indented_block_value : multi_stmts dedent"""
    p[0] = p[1] + [p[2]]

def p_multi_stmts(p):
    """multi_stmts : multi_stmt multi_stmts"""
    p[0] = p[1] + p[2]

def p_multi_stmts_term(p):
    """multi_stmts : multi_stmt"""
    p[0] = p[1]

def p_multi_stmt_ind_block(p):
    """multi_stmt : indented_block"""
    p[0] = p[1]

def p_multi_stmt_term(p):
    """multi_stmt : multi_literal"""
    p[0] = [p[1]]

def p_newline(p):
    """newline : NEWLINE"""
    p[0] = Node("newline", value=p[1])

# anyword groks any character stream without space|newline
def p_anyword(p):
    """anyword : anyword literal"""
    p[0] = Node("anyword", value=(p[1].value + p[2].value))

def p_anyword_term(p):
    """anyword : literal"""
    p[0] = p[1]

def p_anyword_comma_list(p):
    """anyword_comma_list : anyword_comma_list anytoken_no_comma"""
    p[0] = Node("anyword_comma_list", value=(p[1].value + p[2].value))

def p_anyword_comma_list_term(p):
    """anyword_comma_list : anytoken_no_comma"""
    p[0] = Node("anyword_comma_list", value=p[1].value)

# Any token but whitespace, newline and comma
def p_anytoken_no_comma(p):
    """anytoken_no_comma : WORD
                         | COLON
                         | LPAR
                         | RPAR
                         | LESS
                         | SLASH
                         | SHARP
                         | EQUAL
                         | GREATER
    """
    p[0] = Node("anytoken", value=p[1])

def p_literal_no_space(p):
    """literal_no_space : anytoken_no_comma
    """
    p[0] = Node("literal", value=p[1].value)

def p_literal_no_space_term(p):
    """literal_no_space : COMMA
    """
    p[0] = Node("literal", value=p[1])

def p_literal(p):
    """literal : literal_no_space
    """
    p[0] = Node("literal", value=p[1].value)

def p_literal_term(p):
    """literal : WS
    """
    p[0] = Node("literal", value=p[1])

def p_multi_literal(p):
    """multi_literal : literal
    """
    p[0] = Node("multi_literal", value=p[1].value)

def p_multi_literal2(p):
    """multi_literal : newline
    """
    p[0] = p[1]

def p_indent(p):
    """indent : INDENT
    """
    p[0] = Node("indent", value=p[1])

def p_dedent(p):
    """dedent : DEDENT
    """
    p[0] = Node("dedent", value=p[1])

def p_word(p):
    """word : WORD"""
    p[0] = Node("word", value=p[1])

def p_version(p):
    """version : WORD"""
    p[0] = Node("version", value=p[1])

#def p_num_part(p):
#    """num_part : int DOT num_part
#                | int
#    """
#    if len(p) == 4:
#        p[0] = Node("num_part", children=[p[1]])
#        p[0].children.append(p[3])
#    elif len(p) == 2:
#        p[0] = p[1]
#    else:
#        raise ValueError("YO")
#
#def p_int(p):
#    """int : INT"""
#    value = int(p[1])
#    p[0] = Node("int", value=value)
#
def p_error(p):
    if p is not None:
        msg = ["Syntax error at line number %d, token %s ('%s')" % \
               (p.lineno, p.type, p.value)]
        if hasattr(p.lexer, "lexdata"):
            data = p.lexer.lexdata.splitlines()
            msg += ["    Line %d -> %s" % (p.lineno, data[p.lineno-1])]
        else:
            msg += ["    Line %d" % (p.lineno)]
        raise SyntaxError("\n".join(msg))
    raise SyntaxError("Unhandled token")
