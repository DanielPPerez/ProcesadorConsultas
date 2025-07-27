package parser

import (
	"fmt"
	"procesador-consultas/lexer"
)

// Parser representa el analizador sintáctico
type Parser struct {
	l         *lexer.Lexer
	curToken  lexer.Token
	peekToken lexer.Token
	errors    []string
}

// NewParser crea un nuevo analizador sintáctico
func NewParser(l *lexer.Lexer) *Parser {
	p := &Parser{
		l:      l,
		errors: []string{},
	}

	// Leer dos tokens para inicializar curToken y peekToken
	p.nextToken()
	p.nextToken()

	return p
}

// nextToken avanza al siguiente token
func (p *Parser) nextToken() {
	p.curToken = p.peekToken
	p.peekToken = p.l.NextToken()
}

// curTokenIs verifica si el token actual es del tipo especificado
func (p *Parser) curTokenIs(t lexer.TokenType) bool {
	return p.curToken.Type == t
}

// peekTokenIs verifica si el siguiente token es del tipo especificado
func (p *Parser) peekTokenIs(t lexer.TokenType) bool {
	return p.peekToken.Type == t
}

// expectPeek verifica que el siguiente token sea del tipo esperado
func (p *Parser) expectPeek(t lexer.TokenType) bool {
	if p.peekTokenIs(t) {
		p.nextToken()
		return true
	} else {
		p.peekError(t)
		return false
	}
}

// peekError agrega un error de parsing
func (p *Parser) peekError(t lexer.TokenType) {
	msg := fmt.Sprintf("se esperaba el siguiente token %v, se obtuvo %v en línea %d, columna %d",
		t, p.peekToken.Type, p.peekToken.Line, p.peekToken.Column)
	p.errors = append(p.errors, msg)
}

// Errors retorna los errores de parsing
func (p *Parser) Errors() []string {
	return p.errors
}

// ParseQuery parsea una consulta y retorna una lista de claves
func (p *Parser) ParseQuery() ([]string, error) {
	var keys []string

	// La consulta debe empezar con un identificador
	if !p.curTokenIs(lexer.TOKEN_IDENTIFIER) {
		return nil, fmt.Errorf("se esperaba un identificador, se obtuvo %v", p.curToken.Type)
	}

	// Agregar el primer identificador
	keys = append(keys, p.curToken.Literal)

	// Continuar mientras haya puntos seguidos de identificadores o números
	for p.peekTokenIs(lexer.TOKEN_DOT) {
		// Consumir el punto
		p.nextToken()

		// Verificar que después del punto haya un identificador o número
		if !p.peekTokenIs(lexer.TOKEN_IDENTIFIER) && !p.peekTokenIs(lexer.TOKEN_NUMBER) {
			return nil, fmt.Errorf("se esperaba un identificador o número después del punto")
		}

		// Consumir el identificador o número
		p.nextToken()

		// Agregar el identificador o número
		keys = append(keys, p.curToken.Literal)
	}

	// Verificar que terminamos con EOF
	if !p.peekTokenIs(lexer.TOKEN_EOF) {
		return nil, fmt.Errorf("caracteres inesperados al final de la consulta")
	}

	return keys, nil
}

// ParseQueryString parsea una cadena de consulta directamente
func ParseQueryString(query string) ([]string, error) {
	l := lexer.NewLexer(query)
	p := NewParser(l)

	keys, err := p.ParseQuery()
	if err != nil {
		return nil, err
	}

	if len(p.errors) > 0 {
		return nil, fmt.Errorf("errores de parsing: %v", p.errors)
	}

	return keys, nil
}
