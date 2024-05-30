#include "CompilerParser.h"
#include <iostream>


/**
 * Constructor for the CompilerParser
 * @param tokens A linked list of tokens to be parsed
 */
CompilerParser::CompilerParser(std::list<Token*> tokens) {
    this->tokens = tokens;
}

/**
 * Generates a parse tree for a single program
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileProgram() {
    ParseTree* p_tree = new ParseTree("class", "class");
    Token* token = this->mustBe("keyword", "class");
    p_tree->addChild(token);
    token = this->mustBe("identifier", "Main");
    p_tree->addChild(token);
    token = this->mustBe("symbol", "{");
    p_tree->addChild(token);
    token = this->mustBe("symbol", "}");
    p_tree->addChild(token);
    return p_tree;
}

/**
 * Generates a parse tree for a single class
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileClass() {
    /*
    ParseTree* p_tree = new ParseTree("class", "class");
    Token* token = this->mustBe("keyword", "class");
    p_tree->addChild(token);
    token = this->mustBe("identifier", "Main");
    p_tree->addChild(token);
    token = this->mustBe("symbol", "{");
    p_tree->addChild(token);
    // ParseTree* classVarDec = this->compileClassVarDec();
    // p_tree->addChild(classVarDec);
    token = this->mustBe("symbol", "}");
    p_tree->addChild(token);
    return p_tree;
    */
    return NULL;
}

/**
 * Generates a parse tree for a static variable declaration or field declaration
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileClassVarDec() {
    ParseTree* p_tree = new ParseTree("classVarDec", "classVarDec");
    Token* token = this->mustBe("keyword", "static");
    p_tree->addChild(token);
    token = this->mustBe("keyword", "int");
    p_tree->addChild(token);
    if(this->current()->getType() != "identifier") throw ParseException();
    p_tree->addChild(this->current());
    this->next();
    token = this->mustBe("symbol", ";");
    p_tree->addChild(token);
    return p_tree;
}

/**
 * Generates a parse tree for a method, function, or constructor
 * @return a ParseTree
 */
ParseTree* CompilerParser::compileSubroutine() {
    return NULL;
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
    return NULL;
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
    if(!this->tokens.empty()){
        this->tokens.pop_front();
    }
    return;
}

/**
 * Return the current token
 * @return the Token
 */
Token* CompilerParser::current(){
    return this->tokens.front();
}

/**
 * Check if the current token matches the expected type and value.
 * @return true if a match, false otherwise
 */
bool CompilerParser::have(std::string expectedType, std::string expectedValue){
    Token* token = this->current();
    if(token->getType() == expectedType && token->getValue() == expectedValue) {
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
    if(this->have(expectedType, expectedValue)) {
        Token* curr = this->current();
        this->next();
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
