#include "CompilerParser.h"
#include <iostream>

/**
 * Constructor for the CompilerParser
 * @param tokens A linked list of tokens to be parsed
 */
CompilerParser::CompilerParser(std::list<Token *> _tokens) {
    tokens = _tokens;
}

/**
 * Generates a parse tree for a single program
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileProgram() {
    ParseTree *p_tree = new ParseTree("class", "");
    p_tree->addChild(mustBe("keyword", "class"));   // "class"
    p_tree->addChild(mustBe("identifier", "Main")); // className (which is Main)
    p_tree->addChild(mustBe("symbol", "{"));        // "{"
    while (have("", "", "classVarDec")) p_tree->addChild(compileClassVarDec()); // classVarDec*
    while (have("", "", "subroutine")) p_tree->addChild(compileSubroutine()); // subroutineDec*
    p_tree->addChild(mustBe("symbol", "}"));   // "}"
    return p_tree;
}

/**
 * Generates a parse tree for a single class
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileClass() {
    ParseTree *p_tree = new ParseTree("class", "");
    p_tree->addChild(mustBe("keyword", "class")); // "class"
    p_tree->addChild(mustBe("identifier", ""));   // className
    p_tree->addChild(mustBe("symbol", "{"));      // "{"
    while (have("", "", "classVarDec")) p_tree->addChild(compileClassVarDec()); // classVarDec*
    while (have("", "", "subroutine")) p_tree->addChild(compileSubroutine()); // subroutineDec*
    p_tree->addChild(mustBe("symbol", "}"));   // "}"
    return p_tree;
}

/**
 * Generates a parse tree for a static variable declaration or field declaration
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileClassVarDec() {
    ParseTree *p_tree = new ParseTree("classVarDec", "");
    p_tree->addChild(mustBe("", "", "classVarDec")); // ("static" | "field")
    p_tree->addChild(mustBe("", "", "type"));        // type
    p_tree->addChild(mustBe("identifier", ""));      // varName
    while (have("symbol", ",")) {
        p_tree->addChild(mustBe("symbol", ","));
        p_tree->addChild(mustBe("identifier", ""));
    }                                                // ("," varName)*
    p_tree->addChild(mustBe("symbol", ";"));         // ";"
    return p_tree;
}

/**
 * Generates a parse tree for a method, function, or constructor
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileSubroutine() {
    ParseTree *p_tree = new ParseTree("subroutine", "");
    p_tree->addChild(mustBe("", "", "subroutine")); // ("constructor" | "function" | "method")
    if (have("keyword", "void") || have("", "", "type")) {
        p_tree->addChild(current());
        next();
    } else throw ParseException();                 // ("void" | "type")
    p_tree->addChild(mustBe("identifier", "")); // subroutineName
    p_tree->addChild(mustBe("symbol", "("));    // "("
    if (have("", "", "type")) p_tree->addChild(compileParameterList()); // parameterList
    p_tree->addChild(mustBe("symbol", ")"));      // ")"
    p_tree->addChild(compileSubroutineBody());    // subroutineBody
    return p_tree;
}

/**
 * Generates a parse tree for a subroutine's parameters
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileParameterList() {
    ParseTree *p_tree = new ParseTree("parameterList", "");
    if (!current()) return p_tree;              // check?
    p_tree->addChild(mustBe("", "", "type"));   // type
    p_tree->addChild(mustBe("identifier", "")); // varName
    while (current() && have("symbol", ",")) {
        p_tree->addChild(mustBe("symbol", ","));
        p_tree->addChild(mustBe("", "", "type"));
        p_tree->addChild(mustBe("identifier", ""));
    }                                           // ("," type varName)*
    return p_tree;
}

/**
 * Generates a parse tree for a subroutine's body
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileSubroutineBody() {
    ParseTree *p_tree = new ParseTree("subroutineBody", "");
    p_tree->addChild( mustBe("symbol", "{")); // "{"
    while (have("", "", "varDec")) p_tree->addChild(compileVarDec()); // varDec*
    p_tree->addChild(compileStatements()); // statements
    p_tree->addChild(mustBe("symbol", "}")); // "}"
    return p_tree;
}

/**
 * Generates a parse tree for a subroutine variable declaration
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileVarDec() {
    ParseTree *p_tree = new ParseTree("varDec", "");
    p_tree->addChild(mustBe("keyword", "var")); // "var"
    p_tree->addChild(mustBe("", "", "type")); // type
    p_tree->addChild(mustBe("identifier", "")); // varName
    while (have("symbol", ",")) {
        p_tree->addChild(mustBe("symbol", ","));
        p_tree->addChild(mustBe("identifier", ""));
    } // ("," varName)*
    p_tree->addChild(mustBe("symbol", ";")); // ";"
    return p_tree;
}

/**
 * Generates a parse tree for a series of statements
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileStatements() {
    ParseTree *p_tree = new ParseTree("statements", "");
    while(current() && have("","","statements")) {
        if(have("keyword","let")) p_tree->addChild(this->compileLet());
        else if(have("keyword","if")) p_tree->addChild(this->compileIf());
        else if(have("keyword","while")) p_tree->addChild(this->compileWhile());
        else if(have("keyword","do")) p_tree->addChild(this->compileDo());
        else if(have("keyword","return")) p_tree->addChild(this->compileReturn());
    }
    return p_tree;
}

/**
 * Generates a parse tree for a let statement
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileLet() {
    ParseTree *p_tree = new ParseTree("letStatement", "");
    p_tree->addChild(mustBe("keyword", "let"));
    p_tree->addChild(mustBe("identifier", ""));
    if(have("symbol", "[")) {
        p_tree->addChild(mustBe("symbol", "["));
        p_tree->addChild(this->compileExpression());
        p_tree->addChild(mustBe("symbol", "]"));
    }
    p_tree->addChild(mustBe("symbol", "="));
    p_tree->addChild(this->compileExpression());
    p_tree->addChild(mustBe("symbol", ";"));
    return p_tree;
}

/**
 * Generates a parse tree for an if statement
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileIf() {
    ParseTree *p_tree = new ParseTree("ifStatement", "");
    p_tree->addChild(mustBe("keyword", "if"));
    p_tree->addChild(mustBe("symbol", "("));
    p_tree->addChild(this->compileExpression());
    p_tree->addChild(mustBe("symbol", ")"));
    p_tree->addChild(mustBe("symbol", "{"));
    p_tree->addChild(this->compileStatements());
    p_tree->addChild(mustBe("symbol", "}"));
    if(have("keyword", "else")) {
        p_tree->addChild(mustBe("keyword", "else"));
        p_tree->addChild(mustBe("symbol", "{"));
        p_tree->addChild(this->compileStatements());
        p_tree->addChild(mustBe("symbol", "}"));
    }
    return p_tree;
}

/**
 * Generates a parse tree for a while statement
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileWhile() {
    ParseTree *p_tree = new ParseTree("whileStatement", "");
    p_tree->addChild(mustBe("keyword", "while"));
    p_tree->addChild(mustBe("symbol", "("));
    p_tree->addChild(this->compileExpression());
    p_tree->addChild(mustBe("symbol", ")"));
    p_tree->addChild(mustBe("symbol", "{"));
    p_tree->addChild(this->compileStatements());
    p_tree->addChild(mustBe("symbol", "}"));
    return p_tree;
}

/**
 * Generates a parse tree for a do statement
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileDo() {
    ParseTree *p_tree = new ParseTree("doStatement", "");
    p_tree->addChild(mustBe("keyword", "do"));
    p_tree->addChild(this->compileExpression());
    p_tree->addChild(mustBe("symbol", ";"));
    return p_tree;
}

/**
 * Generates a parse tree for a return statement
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileReturn() {
    ParseTree *p_tree = new ParseTree("returnStatement", "");
    p_tree->addChild(mustBe("keyword", "return"));
    if(!have("symbol", ";")) p_tree->addChild(this->compileExpression());
    p_tree->addChild(mustBe("symbol", ";"));
    return p_tree;
}

/**
 * Generates a parse tree for an expression
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileExpression() {
    ParseTree *p_tree = new ParseTree("expression", "");
    if(have("keyword","skip")) {
        p_tree->addChild(mustBe("keyword","skip"));
        return p_tree;
    }
    return p_tree;
}

/**
 * Generates a parse tree for an expression term
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileTerm() {
    return NULL;
}

/**
 * Generates a parse tree for an expression list
 * @return a ParseTree
 */
ParseTree *CompilerParser::compileExpressionList() {
    return NULL;
}

/**
 * Advance to the next token
 */
void CompilerParser::next() {
    if (!tokens.empty()) tokens.pop_front();
    return;
}

/**
 * Return the current token
 * @return the Token
 */
Token *CompilerParser::current() {
    return tokens.front();
}

/**
 * Check if the current token matches the expected type and value.
 * @return true if a match, false otherwise
 */
bool CompilerParser::have(std::string expectedType, std::string expectedValue, std::string checkType) {
    Token *token = current();
    if (checkType == "") return (token->getType() == expectedType && (expectedValue == "" || token->getValue() == expectedValue));
    if (checkType == "type") return (have("identifier", "") || have("keyword", "int") || have("keyword", "char") || have("keyword", "boolean"));
    if (checkType == "classVarDec") return (have("keyword", "static") || have("keyword", "field"));
    if (checkType == "subroutine") return (have("keyword", "function") || have("keyword", "constructor") || have("keyword", "method"));
    if (checkType == "varDec") return (have("keyword", "var"));
    if (checkType == "statements") return (have("keyword", "let") || have("keyword", "if") || have("keyword", "while") || have("keyword", "do") || have("keyword", "return"));
    return false;
}

/**
 * Check if the current token matches the expected type and value.
 * If so, advance to the next token, returning the current token, otherwise throw a ParseException.
 * @return the current token before advancing
 */
Token *CompilerParser::mustBe(std::string expectedType, std::string expectedValue, std::string checkType) {
    if (have(expectedType, expectedValue, checkType)) {
        Token *curr = current();
        next();
        return curr;
    }
    std::cout << current()->getType() << " " << current()->getValue() << " " << expectedType << " " << expectedValue << " " << checkType << "\n";
    throw ParseException();
}

/**
 * Definition of a ParseException
 * You can use this ParseException with `throw ParseException();`
 */
const char *ParseException::what() {
    return "An Exception occurred while parsing!";
}
