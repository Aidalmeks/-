%{
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "ast.h" 

void yyerror(const char *s);
int yylex();
%}

%union {
    int ival;
    char *sval;
}

%token MAIN IF THEN ELSE END WHILE SCAN PRINT
%token IDENT NUMBER
%token EQ NEQ LT LTE GT GTE PLUS MINUS MUL DIV ASSIGN
%token LPAREN RPAREN LBRACE RBRACE SEMICOLON COMMA

%type <node> program stmt_list stmt assign_stmt if_stmt while_stmt scan_stmt print_stmt bool_expr expr term factor

%%

program:
    MAIN LBRACE stmt_list RBRACE {
        printf("Parsed a program.\n");
    }
    ;

stmt_list:
    stmt SEMICOLON {
        // handle single stmt
    }
    | stmt_list stmt SEMICOLON {
        // handle multiple stmts
    }
    ;

stmt:
    assign_stmt
    | if_stmt
    | while_stmt
    | scan_stmt
    | print_stmt
    ;

assign_stmt:
    IDENT ASSIGN expr {
        // handle assignment
    }
    ;

if_stmt:
    IF LPAREN bool_expr RPAREN THEN LBRACE stmt_list RBRACE END {
        // handle if statement
    }
    | IF LPAREN bool_expr RPAREN THEN LBRACE stmt_list RBRACE ELSE LBRACE stmt_list RBRACE END {
        // handle if-else statement
    }
    ;

while_stmt:
    WHILE LPAREN bool_expr RPAREN LBRACE stmt_list RBRACE {
        // handle while statement
    }
    ;

scan_stmt:
    SCAN LPAREN IDENT {
        // handle scan with one identifier
    }
    | SCAN LPAREN IDENT COMMA IDENT {
        // handle scan with multiple identifiers
    }
    ;

print_stmt:
    PRINT LPAREN expr {
        // handle print with one expression
    }
    | PRINT LPAREN expr COMMA expr {
        // handle print with multiple expressions
    }
    ;

bool_expr:
    expr EQ expr
    | expr NEQ expr
    | expr LT expr
    | expr LTE expr
    | expr GT expr
    | expr GTE expr
    ;

expr:
    PLUS term {
        // handle positive term
    }
    | MINUS term {
        // handle negative term
    }
    | term {
        // handle single term
    }
    | expr PLUS term {
        // handle addition
    }
    | expr MINUS term {
        // handle subtraction
    }
    ;

term:
    factor {
        // handle single factor
    }
    | term MUL factor {
        // handle multiplication
    }
    | term DIV factor {
        // handle division
    }
    ;

factor:
    IDENT {
        // handle identifier
    }
    | NUMBER {
        // handle number
    }
    | LPAREN expr RPAREN {
        // handle expression in parentheses
    }
    ;

%%

void yyerror(const char *s) {
    fprintf(stderr, "Error: %s\n", s);
}

ASTNode *newNode(int nodeType) {
    ASTNode *node = (ASTNode *)malloc(sizeof(ASTNode));
    node->nodeType = nodeType;
    return node;
}

int main() {
    return yyparse();
}
