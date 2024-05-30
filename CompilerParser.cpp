#include "CompilerParser.h"
#include <iostream>


/**
 * Constructor for the CompilerParser
 * @param tokens A linked list of tokens to be parsed
 */
CompilerParser::CompilerParser(std::list<Token*> _tokens) {
    tokens = _tokens;
}

/**
 * Generates a parse tree for a single program
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileProgram() {
    ParseTree* p_tree = new ParseTree("class", "class");
    p_tree->addChild(mustBe("keyword", "class")); // "class"
    p_tree->addChild(mustBe("identifier", "Main")); // className (which is Main)
    p_tree->addChild(mustBe("symbol", "{")); // "{"
    while(have("keyword", "static") || have("keyword", "field")) p_tree->addChild(compileClassVarDec()); // classVarDec*
    while(have("keyword", "function") || have("keyword", "constructor") || have("keyword", "method")) p_tree->addChild(compileSubroutine()); // subroutineDec*
    p_tree->addChild(mustBe("symbol", "}")); // "}"
    return p_tree;
}

/**
 * Generates a parse tree for a single class
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileClass() {
    ParseTree* p_tree = new ParseTree("class", "class");
    p_tree->addChild(mustBe("keyword", "class")); // "class"
    p_tree->addChild(mustBe("identifier")); // className
    p_tree->addChild(mustBe("symbol", "{")); // "{"
    while(have("keyword", "static") || have("keyword", "field")) p_tree->addChild(compileClassVarDec()); // classVarDec*
    while(have("keyword", "function") || have("keyword", "constructor") || have("keyword", "method")) p_tree->addChild(compileSubroutine()); // subroutineDec*
    p_tree->addChild(mustBe("symbol", "}")); // "}"
    return p_tree;
}

/**
 * Generates a parse tree for a static variable declaration or field declaration
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileClassVarDec() {
    ParseTree* p_tree = new ParseTree("classVarDec", "classVarDec");
    if(have("keyword", "static") || have("keyword", "field")){
        p_tree->addChild(current());
        next();
    }; // ("static" | "field")
    if(have("identifier") || have("keyword", "int") || have("keyword", "char") || have("keyword", "boolean")){
        p_tree->addChild(current());
        next();
    }; // type
    p_tree->addChild(mustBe("identifier")); // varName
    while(have("symbol", ",")) {
        p_tree->addChild(mustBe("symbol", ","));
        p_tree->addChild(mustBe("identifier"));
    } // ("," varName)*
    p_tree->addChild(mustBe("symbol", ";")); // ";"
    return p_tree;
}

/**
 * Generates a parse tree for a method, function, or constructor
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileSubroutine() {
    ParseTree* p_tree = new ParseTree("subroutine", "subroutine");
    if(have("keyword", "constructor") || have("keyword", "function") || have("keyword", "method")) {
        p_tree->addChild(current());
        next();
    } // ("constructor" | "function" | "method")
    if(have("keyword", "void") || have("identifier") || have("keyword", "int") || have("keyword", "char") || have("keyword", "boolean")) {
        p_tree->addChild(current());
        next();
    } // ("void" | "type")
    p_tree->addChild(mustBe("identifier")); // subroutineName
    p_tree->addChild(mustBe("symbol", "(")); // "("
    if(have("identifier") || have("keyword", "int") || have("keyword", "char") || have("keyword", "boolean")) p_tree->addChild(compileParameterList()); // parameterList
    p_tree->addChild(mustBe("symbol", ")")); // ")"
    p_tree->addChild(compileSubroutineBody()); // subroutineBody
    return p_tree;
}

/**
 * Generates a parse tree for a subroutine's parameters
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileParameterList() {
    return NULL;
}

/**
 * Generates a parse tree for a subroutine's body
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileSubroutineBody() {
    ParseTree* p_tree = new ParseTree("subroutineBody", "subroutineBody");
    Token* token = mustBe("symbol", "{");
    p_tree->addChild(token);
    if(have("keyword", "var")) p_tree->addChild(compileVarDec());
    if(have("keyword", "let")) p_tree->addChild(compileStatements());
    token = mustBe("symbol", "}");
    p_tree->addChild(token);
    return p_tree;
}

/**
 * Generates a parse tree for a subroutine variable declaration
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileVarDec() {
    return NULL;
}

/**
 * Generates a parse tree for a series of statements
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileStatements() {
    return NULL;
}

/**
 * Generates a parse tree for a let statement
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileLet() {
    return NULL;
}

/**
 * Generates a parse tree for an if statement
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileIf() {
    return NULL;
}

/**
 * Generates a parse tree for a while statement
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileWhile() {
    ParseTree* ptree = new ParseTree("keyword", "while");
    return NULL;
}

/**
 * Generates a parse tree for a do statement
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileDo() {
    return NULL;
}

/**
 * Generates a parse tree for a return statement
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileReturn() {
    return NULL;
}

/**
 * Generates a parse tree for an expression
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileExpression() {
    return NULL;
}

/**
 * Generates a parse tree for an expression term
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileTerm() {
    return NULL;
}

/**
 * Generates a parse tree for an expression list
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileExpressionList() {
    return NULL;
}

/**
 * Advance to the next token
 */
void CompilerParser::next(){
    if(!tokens.empty()){
        tokens.pop_front();
    }
    return;
}

/**
 * Return the current token
 * @return the Token
 */
Token* CompilerParser::current(){
    return tokens.front();
}

/**
 * Check if the current token matches the expected type and value.
 * @return true if a match, false otherwise
 */
bool CompilerParser::have(std::string expectedType, std::string expectedValue){
    Token* token = current();
    if(token->getType() == expectedType && (expectedValue == "" || token->getValue() == expectedValue)) {
        return true;
    }
    return false;
}

/**
 * Check if the current token matches the expected type and value.
 * If so, advance to the next token, returning the current token, otherwise throw a ParseException.
 * @return the current token before advancing
 */
Token* CompilerParser::mustBe(std::string expectedType, std::string expectedValue){
    if(have(expectedType, expectedValue)) {
        Token* curr = current();
        next();
        return curr;
    }
    std::cout << expectedType << " " << expectedValue << "\n";
    throw ParseException();
}

/**
 * Definition of a ParseException
 * You can use this ParseException with `throw ParseException();`
 */
const char* ParseException::what() {
    return "An Exception occurred while parsing!";
}
