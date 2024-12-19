%{
#include "parser.tab.h"
#include "ast.h" // Include the ASTNode definition
%}

%%
"main"               { return MAIN; }
"if"                 { return IF; }
"then"               { return THEN; }
"else"               { return ELSE; }
"end"                { return END; }
"while"              { return WHILE; }
"scan"               { return SCAN; }
"print"              { return PRINT; }
[a-zA-Z_][a-zA-Z0-9_]*  { yylval.sval = strdup(yytext); return IDENT; }
[0-9]+               { yylval.ival = atoi(yytext); return NUMBER; }
"=="                 { return EQ; }
"!="                 { return NEQ; }
"<="                 { return LTE; }
">="                 { return GTE; }
"<"                  { return LT; }
">"                  { return GT; }
"+"                  { return PLUS; }
"-"                  { return MINUS; }
"*"                  { return MUL; }
"/"                  { return DIV; }
"="                  { return ASSIGN; }
"("                  { return LPAREN; }
")"                  { return RPAREN; }
"{"                  { return LBRACE; }
"}"                  { return RBRACE; }
";"                  { return SEMICOLON; }
","                  { return COMMA; }
[ \t\n]+             { /* ignore whitespace */ }
.                    { fprintf(stderr, "Unknown character: %c\n", yytext[0]); }
%%

int yywrap() {
    return 1;
}
