import React from 'react';

const darkBlue = "#080e2e";

// Sample Data
const tokens = [
  { lexeme: 'let', token: 'Keyword' },
  { lexeme: 'x', token: 'Identifier' },
  { lexeme: '=', token: 'Operator' },
  { lexeme: '10', token: 'Literal' },
];

const errors = [
  { lexeme: 'x', error: 'Unexpected token x' },
  { lexeme: '=', error: 'Assignment without declaration' },
];

const RightSegment = () => {
  return (
    <div
      className="right-segment"
      style={{
        position: 'fixed',
        top: '0',
        right: '0',
        bottom: '0',
        width: '300px',
        backgroundColor: darkBlue, 
        color: 'white',
        padding: '20px',
        overflowY: 'auto',
        transition: 'transform 0.3s ease',
      }}
    >
      <h3>Tokens</h3>
      <table
        style={{
          width: '100%',
          borderCollapse: 'collapse',
          marginBottom: '50px',
        }}
      >
        <thead>
          <tr>
            <th style={{ padding: '8px', borderBottom: '1px solid #444' }}>Lexeme</th>
            <th style={{ padding: '8px', borderBottom: '1px solid #444' }}>Token</th>
          </tr>
        </thead>
        <tbody>
          {tokens.map((token, index) => (
            <tr key={index}>
              <td style={{ padding: '8px', borderBottom: '1px solid #444' }}>{token.lexeme}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #444' }}>{token.token}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h3>Errors</h3>
      <table
        style={{
          width: '100%',
          borderCollapse: 'collapse',
        }}
      >
        <thead>
          <tr>
            <th style={{ padding: '8px', borderBottom: '1px solid #444' }}>Lexeme</th>
            <th style={{ padding: '8px', borderBottom: '1px solid #444' }}>Error Message</th>
          </tr>
        </thead>
        <tbody>
          {errors.map((error, index) => (
            <tr key={index}>
              <td style={{ padding: '8px', borderBottom: '1px solid #444' }}>{error.lexeme}</td>
              <td style={{ padding: '8px', borderBottom: '1px solid #444' }}>{error.error}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RightSegment;
