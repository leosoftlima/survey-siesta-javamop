
import os
import math
import re
import pandas as pd

JAVA_MOP_RESERVED_WORDS = set([
    'abstract', 'assert', 'boolean', 'break', 'byte', 'case', 'catch', 'char',
    'class', 'const', 'continue', 'default', 'do', 'double', 'else', 'enum',
    'extends', 'final', 'finally', 'float', 'for', 'goto', 'if', 'implements',
    'import', 'instanceof', 'int', 'interface', 'long', 'native', 'new', 'null',
    'package', 'private', 'protected', 'public', 'return', 'short', 'static',
    'strictfp', 'super', 'switch', 'synchronized', 'this', 'throw', 'throws',
    'transient', 'try', 'void', 'volatile', 'while', 'true', 'false'
])

JAVA_MOP_OPERATORS = [
    '++', '--', '==', '!=', '<=', '>=', '<<=', '>>=', '&&', '||', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=',
    '+', '-', '*', '/', '%', '=', '<', '>', '!', '~', '&', '|', '^', '<<', '>>', '?', ':', '.', ',', ';', '->',
    '(', ')', '{', '}', '[', ']'
]

class HalsteadMetrics:
    def __init__(self):
        self.operators = set()
        self.operands = set()
        self.total_operators = 0
        self.total_operands = 0
        self.operators_list = []
        self.operands_list = []

    def analyze(self, code):
        code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
        code = re.sub(r'//.*', '', code)
        code = re.sub(r'"[^"]*"', '', code)
        tokens = re.findall(r'[\w]+|[^\s\w]', code)
        for token in tokens:
            if token in JAVA_MOP_OPERATORS or token in JAVA_MOP_RESERVED_WORDS:
                self.operators.add(token)
                self.total_operators += 1
                self.operators_list.append(token)
            elif re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', token):
                self.operands.add(token)
                self.total_operands += 1
                self.operands_list.append(token)

    def compute(self):
        n1 = len(self.operators)
        n2 = len(self.operands)
        N1 = self.total_operators
        N2 = self.total_operands
        n = n1 + n2
        N = N1 + N2
        V = N * math.log2(n) if n > 0 else 0
        D = (n1 / 2) * (N2 / n2) if n2 > 0 else 0
        E = D * V
        return {
            'n1': n1, 'n2': n2, 'N1': N1, 'N2': N2,
            'Vocabulary': n, 'Length': N, 'Volume': V,
            'Difficulty': D, 'Effort': E
        }

    def get_log_detail(self, filename, method, line):
        return {
            'file': filename, 'method': method, 'line': line,
            'n1': len(self.operators), 'n1_operators': sorted(self.operators),
            'n2': len(self.operands), 'n2_operands': sorted(self.operands),
            'N1': self.total_operators, 'N1_operators': self.operators_list,
            'N2': self.total_operands, 'N2_operands': self.operands_list
        }

def extract_methods_from_java(code):
    pattern = re.compile(r'(public|private|protected)?\s+[\w<>\[\]]+\s+(\w+)\s*\([^)]*\)\s*\{')
    methods = []
    for match in pattern.finditer(code):
        start = match.start()
        method_name = match.group(2)
        brace_count = 1
        i = match.end()
        while i < len(code) and brace_count > 0:
            if code[i] == '{': brace_count += 1
            elif code[i] == '}': brace_count -= 1
            i += 1
        method_code = code[start:i]
        method_line = code[:start].count('\n') + 1
        method_size = method_code.count('\n') + 1
        methods.append((method_name, method_code, method_line, method_size))
    return methods

def analyze_file_by_method(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    filename = os.path.basename(filepath)
    blocks = extract_methods_from_java(code)
    result_rows = []
    log_rows = []
    for method_name, method_code, line, size in blocks:
        metrics = HalsteadMetrics()
        metrics.analyze(method_code)
        result = metrics.compute()
        result.update({'file': filename, 'method': method_name, 'line': line, 'methodLOC': size})
        result_rows.append(result)
        log_rows.append(metrics.get_log_detail(filename, method_name, line))
    return result_rows, log_rows

def analyze_directory(directory, extensions=['.java']):
    results = []
    logs = []
    print(f"📁 Analisando arquivos MSL na pasta: {directory}")
    for root, _, files in os.walk(directory):
        for fname in files:
            if any(fname.endswith(ext) for ext in extensions):
                path = os.path.join(root, fname)
                print(f"🔍 {fname}")
                try:
                    res, log = analyze_file_by_method(path)
                    results.extend(res)
                    logs.extend(log)
                except Exception as e:
                    print(f"❌ Erro ao processar {fname}: {e}")
    return pd.DataFrame(results), pd.DataFrame(logs)

if __name__ == '__main__':
    pasta = r'C:\Users\leona\Downloads\expermentSurvey\RQ4\code11'
    df_result, df_log = analyze_directory(pasta)
    df_result.to_csv(os.path.join(pasta, 'halstead_summaryMSL.csv'), index=False)
    df_log.to_csv(os.path.join(pasta, 'logOperationsMSL.csv'), index=False)
    print("[✓] Arquivos MSL gerados com sucesso.")
