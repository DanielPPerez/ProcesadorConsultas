package lexer

import (
	"unicode"
)

// TokenType representa el tipo de token
type TokenType int

const (
	TOKEN_IDENTIFIER TokenType = iota
	TOKEN_DOT
	TOKEN_NUMBER
	TOKEN_EOF
	TOKEN_ERROR
)

// Token representa un token léxico
type Token struct {
	Type    TokenType
	Literal string
	Line    int
	Column  int
}

// Lexer representa el analizador léxico
type Lexer struct {
	input        string
	position     int
	readPosition int
	ch           byte
	line         int
	column       int
}

// NewLexer crea un nuevo analizador léxico
func NewLexer(input string) *Lexer {
	l := &Lexer{
		input:  input,
		line:   1,
		column: 1,
	}
	l.readChar()
	return l
}

// readChar lee el siguiente carácter
func (l *Lexer) readChar() {
	if l.readPosition >= len(l.input) {
		l.ch = 0 // EOF
	} else {
		l.ch = l.input[l.readPosition]
	}
	l.position = l.readPosition
	l.readPosition++
	l.column++
}

// peekChar mira el siguiente carácter sin avanzar
func (l *Lexer) peekChar() byte {
	if l.readPosition >= len(l.input) {
		return 0
	}
	return l.input[l.readPosition]
}

// skipWhitespace salta espacios en blanco
func (l *Lexer) skipWhitespace() {
	for l.ch == ' ' || l.ch == '\t' || l.ch == '\n' || l.ch == '\r' {
		if l.ch == '\n' {
			l.line++
			l.column = 0
		}
		l.readChar()
	}
}

// readIdentifier lee un identificador
func (l *Lexer) readIdentifier() string {
	position := l.position
	for isLetter(l.ch) || isDigit(l.ch) || l.ch == '_' {
		l.readChar()
	}
	return l.input[position:l.position]
}

// readNumber lee un número
func (l *Lexer) readNumber() string {
	position := l.position
	for isDigit(l.ch) {
		l.readChar()
	}
	return l.input[position:l.position]
}

// isLetter verifica si el carácter es una letra
func isLetter(ch byte) bool {
	return unicode.IsLetter(rune(ch)) || ch == '_'
}

// isDigit verifica si el carácter es un dígito
func isDigit(ch byte) bool {
	return unicode.IsDigit(rune(ch))
}

// NextToken retorna el siguiente token
func (l *Lexer) NextToken() Token {
	var tok Token

	l.skipWhitespace()

	switch l.ch {
	case '.':
		tok = Token{Type: TOKEN_DOT, Literal: string(l.ch), Line: l.line, Column: l.column}
	case 0:
		tok.Literal = ""
		tok.Type = TOKEN_EOF
	default:
		if isLetter(l.ch) {
			tok.Literal = l.readIdentifier()
			tok.Type = TOKEN_IDENTIFIER
			tok.Line = l.line
			tok.Column = l.column
			return tok
		} else if isDigit(l.ch) {
			tok.Literal = l.readNumber()
			tok.Type = TOKEN_NUMBER
			tok.Line = l.line
			tok.Column = l.column
			return tok
		} else {
			tok = Token{Type: TOKEN_ERROR, Literal: string(l.ch), Line: l.line, Column: l.column}
		}
	}

	l.readChar()
	return tok
}

// Tokenize tokeniza toda la entrada
func (l *Lexer) Tokenize() []Token {
	var tokens []Token

	for {
		tok := l.NextToken()
		tokens = append(tokens, tok)
		if tok.Type == TOKEN_EOF {
			break
		}
	}

	return tokens
}
