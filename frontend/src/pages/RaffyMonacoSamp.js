import { useEffect, useRef, useState } from "react";
import axios from "axios";
import * as monaco from "monaco-editor";

const language = "lexio";
const theme = ${language}-theme;

function Editor({ program, setProgram }) {
  const monacoRef = useRef(null);
  const [codeEditor, setCodeEditor] = useState(null);
  const [hasError, setHasError] = useState(false);
  const keywords = [
    "for",
    "return",
    "function",
    "while",
    "let",
    "const",
    "none",
    "whole",
    "spell",
    "deci",
    "fact",
    "next",
    "halt",
    "match",
    "if",
    "else",
    "object",
    "to",
    "by",
    "and",
    "or",
    "not",
    "show",
    "batch",
    "true",
    "false",
  ];
  useEffect(() => {
    if (monacoRef.current) {
      if (codeEditor) {
        codeEditor.dispose();
      }

      monaco.languages.register({ id: language });

      monaco.languages.setMonarchTokensProvider(language, {
        keywords,
        tokenizer: {
          root: [
            [
              /@?[a-zA-Z][\w$]*/,
              {
                cases: {
                  whole: "type",
                  deci: "type",
                  spell: "type",
                  fact: "type",
                  object: "type",
                  if: "control",
                  else: "control",
                  return: "control",
                  for: "control",
                  to: "control",
                  by: "control",
                  while: "control",
                  halt: "control",
                  next: "control",
                  do: "control",
                  match: "control",
                  and: "control",
                  or: "control",
                  not: "control",
                  other: "control",
                  show: "io",
                  get: "io",
                  "@keywords": "keyword",
                  "@default": "variable",
                },
              },
            ],
            [/"/, "string", "@stringBody"],
            [/\/{2}/, "comment", "@comment"],
            [/\d+/, "number"],
          ],
          stringBody: [
            [/[^\\"]+/, "string"],
            [/\\./, "string.escape"],
            [/"/, "string", "@pop"],
            [/.$/, "string"],
          ],
          comment: [
            [/[^\/]+/, "comment"], // Capture all characters until the next "/"
            [/\/\//, "comment", "@pop"], // End comment on closing pair
            [/\/$/, "comment"], // Allow a single trailing "/" before the end of the comment
            [/\/[^\/]*/, "comment"],
          ],
        },
      });

      monaco.languages.setLanguageConfiguration(language, {
        brackets: [
          ["{", "}"],
          ["[", "]"],
          ["(", ")"],
          ['"', '"'],
        ],
        comments: {
          blockComment: ["//", "//"],
        },
      });

      monaco.languages.registerCompletionItemProvider(language, {
        provideCompletionItems: (model, position) => {
          const textUntilPosition = model.getValueInRange({
            startLineNumber: position.lineNumber,
            startColumn: 1,
            endLineNumber: position.lineNumber,
            endColumn: position.column,
          });

          const keywords = [
            "for",
            "return",
            "function",
            "while",
            "let",
            "const",
            "none",
            "whole",
            "spell",
            "deci",
            "fact",
            "next",
            "halt",
            "match",
            "if",
            "else",
            "object",
            "to",
            "by",
            "and",
            "or",
            "not",
            "show",
            "batch",
            "true",
            "false",
          ];
          keywords.forEach((keyword) => {
            suggestions.set(keyword, {
              label: keyword,
              kind: monaco.languages.CompletionItemKind.Keyword,
              insertText: keyword,
            });
          });

          return { suggestions: Array.from(suggestions.values()) };
        },
      });

      monaco.editor.defineTheme(theme, {
        base: "vs-dark",
        rules: [
          { token: "type", foreground: "#44c9b0" },
          { token: "control", foreground: "#d8a0df" },
          { token: "io", foreground: "#dcdcaa" },
          { token: "keyword", foreground: "#449cd6" },
          { token: "number", foreground: "#94cea8" },
          { token: "string", foreground: "#ce916a" },
          { token: "string.escape", foreground: "#ffd672" },
          { token: "comment", foreground: "#008000" },
        ],
        colors: {
          "editor.foreground": "#FFFFFF",
          "editor.background": "#1E1E1E",
        },
      });

      const newEditor = monaco.editor.create(monacoRef.current, {
        language: language,
        fontSize: 20,
        theme: theme,
        fontFamily: "monospace",
        automaticLayout: true,
        value: program,
        minimap: {
          enabled: false,
        },
      });

      newEditor.onDidChangeModelContent(() => {
        const code = newEditor.getValue();
        setProgram(code);
        axios
          .post(${process.env.REACT_APP_URL}, { code })
          .then((res) => {
            const markers = [];
            const errors = res.data.errors;
            errors.forEach((e) => {
              console.log(errors);
              const {
                lexeme,
                type,
                start_line,
                end_line,
                start_col,
                end_col,
                attribute,
                error,
              } = e;
              markers.push({
                startLineNumber: start_line,
                endLineNumber: end_line,
                startColumn: start_col,
                endColumn: end_col,
                message: error,
                severity: monaco.MarkerSeverity.Error,
              });
            });
            monaco.editor.setModelMarkers(
              newEditor.getModel(),
              "owner",
              markers
            );
          });

       });

      setCodeEditor(newEditor);

      return () => {
        if (newEditor) {
          newEditor.dispose();
        }
      };
    }
  }, [monacoRef]);

  useEffect(() => {
    if (codeEditor && program !== codeEditor.getValue()) {
      codeEditor.setValue(program);
    }
  }, [program, codeEditor]);

  return (
    <div class="flex flex-col">
      <div class="w-[75vw] h-[95vh]" ref={monacoRef}></div>
    </div>
  );
}

export default Editor;