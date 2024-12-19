// ast.h
#ifndef AST_H
#define AST_H

typedef struct ASTNode {
    int nodeType;
    union {
        int ival;
        char *sval;
        struct {
            struct ASTNode *left;
            struct ASTNode *right;
        } children;
    } data;
} ASTNode;

ASTNode *newNode(int nodeType);

#endif
