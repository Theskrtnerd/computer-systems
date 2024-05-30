#include <iostream>
#include <list>

#include "CompilerParser.h"
#include "Token.h"

using namespace std;

int main(int argc, char *argv[]) {
    /* Tokens for:
     *     class MyClass {
     *
     *     }
     */
    list<Token*> tokens;
    // Main . myFunc ( 1 , Hello )  
    tokens.push_back(new Token("identifier", "Main"));
    tokens.push_back(new Token("symbol", "."));
    tokens.push_back(new Token("identifier", "myFunc"));
    tokens.push_back(new Token("symbol", "("));
    tokens.push_back(new Token("integerConstant", "1"));
    tokens.push_back(new Token("symbol", ","));
    tokens.push_back(new Token("stringConstant", "Hello"));
    tokens.push_back(new Token("symbol", ")"));


    try {
        CompilerParser parser(tokens);
        ParseTree* result = parser.compileExpression();
        if (result != NULL){
            cout << result->tostring() << endl;
        }
    } catch (ParseException e) {
        cout << "Error Parsing!" << endl;
    }
}