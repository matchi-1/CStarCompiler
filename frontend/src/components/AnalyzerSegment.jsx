import React from 'react';
import '../styles/AnalyzerSegment.css';

const AnalyzerSegment = (props) => {
  const tokens = props.tokens;  // Ensure tokens is not undefined

  return (
    <div className="analyzer-segment">
      <div className="analyzer-tab-containers">
        <div className="analyzer-tab-item">
            <p>Lexer</p>
        </div>
        <div className="analyzer-tab-filler"></div>
      </div>
      <div className="analyzer-container">
        <h3>TOKENS</h3>
        <div className="analyzer-table-container">
          <div className="analyzer-table-wrapper">
            <table>
              <thead>
                <tr>
                  <th>Lexeme</th>
                  <th>Token</th>
                </tr>
              </thead>
              <tbody>
                {tokens.map((tokenObj, index) => (
                  <tr key={index}>
                    <td>{tokenObj.tokenName}</td>
                    <td>{tokenObj.tokenType}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyzerSegment;
