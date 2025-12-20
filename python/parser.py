import re
import json
import sys

# -------------------------
# Semantic Keywords Mapping
# -------------------------
SELECT_KEYWORDS = ['select', 'show', 'list', 'get', 'display', 'give', 'retrieve', 'fetch', 'provide', 'tell', 'help me show', 'help me get']
WHERE_KEYWORDS = ['where', 'with', 'having', 'that', 'whose', 'filter', 'condition']
COUNT_KEYWORDS = ['count', 'how many', 'total', 'number of']
SUM_KEYWORDS = ['sum', 'total', 'add up']
ORDER_KEYWORDS = ['order', 'sort', 'arrange', 'by']
LIMIT_KEYWORDS = ['limit', 'top', 'first', 'last']
JOIN_KEYWORDS = ['join', 'combine', 'merge', 'with']

COMPARISON_OPS = {
    'greater': '>', 'greater than': '>', 'more than': '>', 'above': '>',
    'less': '<', 'less than': '<', 'below': '<', 'under': '<',
    'equal': '=', 'equals': '=', 'is': '=', 'same as': '=',
    'not equal': '!=', 'different': '!='
}

# -------------------------
# 1. Normalize & Expand Text
# -------------------------
def expand_contractions(text):
    """Expand contractions like 'user\'s' -> 'user'"""
    text = re.sub(r"'s\s+", " ", text)  # user's information -> user information
    text = re.sub(r"'s$", "", text)      # user's -> user
    return text

def normalize_operators(text):
    t = text.lower()
    for key, val in COMPARISON_OPS.items():
        t = t.replace(key, val)
    return t

def extract_column_names(text, table):
    """Extract column names from natural language"""
    keywords_to_remove = ['information', 'data', 'details', 'record', 'row', 'entry', 'field']
    
    for keyword in keywords_to_remove:
        text = text.replace(keyword, '')
    
    # Simple extraction: words after "of", "from", etc
    parts = re.split(r'\b(of|from|in|with)\b', text)
    if len(parts) > 2:
        potential_cols = parts[2].strip().split()
        return ' '.join(potential_cols[:3])  # Max 3 words
    return '*'

def english_to_dsl(text):
    """Convert English to SQL DSL with semantic understanding"""
    text = expand_contractions(text)
    original_text = text
    text = normalize_operators(text)
    text = text.lower()
    
    # ==================== SEMANTIC RULES ====================
    
    # Rule: "Help me show X" / "Help me get X"
    m = re.match(r"help me (show|get|display|provide|tell)\s+(.+?)(?:\s+from|\s+of)?\s+(\w+)?", text, re.IGNORECASE)
    if m:
        action = m.group(1)
        what = m.group(2).strip()
        table = m.group(3) or 'users'
        
        # Extract columns
        if what.lower() in ['all', 'everything', 'both', 'information', 'details', 'data']:
            cols = '*'
        else:
            cols = extract_column_names(what, table)
        
        return f"SELECT {cols} FROM {table}"

    # Rule: "Show me X information"
    m = re.match(r"show me\s+(.+?)\s+(?:information|data|details)?", text, re.IGNORECASE)
    if m:
        what = m.group(1).strip()
        if what.lower() in ['all', 'user', 'product', 'order', 'customer']:
            return f"SELECT * FROM {what}s"  # pluralize
        return f"SELECT * FROM {what}s"

    # Rule: "Give me all X"
    m = re.match(r"(?:give|show|display|provide|tell)\s+me\s+(?:all\s+)?(.+?)(?:\s+where\s+(.+))?$", text, re.IGNORECASE)
    if m:
        what = m.group(1).strip()
        where_clause = m.group(2)
        
        # Singularize to find table
        table = what.rstrip('s') if what.endswith('s') else what
        
        if where_clause:
            return f"SELECT * FROM {table} WHERE {where_clause}"
        return f"SELECT * FROM {table}"

    # Rule: "Find all X with Y = Z"
    m = re.match(r"find\s+(?:all\s+)?(\w+)(?:\s+(?:with|where)\s+(\w+)\s*(=|>|<)\s*(.+))?", text, re.IGNORECASE)
    if m:
        table = m.group(1)
        col = m.group(2)
        op = m.group(3) or '='
        val = m.group(4)
        
        query = f"SELECT * FROM {table}"
        if col:
            query += f" WHERE {col} {op} {val}"
        return query

    # ==================== STANDARD RULES ====================
    
    # Rule 1: SELECT all from table with optional WHERE
    m = re.match(
    r"(select|show|list) all(?: (\w+))? (?:of|from) (\w+)(?:\s+where\s+(\w+)\s*(=|>|<)\s*(\d+))?",
    text,
    flags=re.IGNORECASE
    )
    if m:
       col = m.group(2)
       table = m.group(3)
       where_col = m.group(4)
       operator = m.group(5)
       where_val = m.group(6)
       if col:
        query = f"SELECT {col} FROM {table}"
       else:
        query = f"SELECT * FROM {table}"
       if where_col:
        query += f" WHERE {where_col} {operator} {where_val}"
       return query

    # Rule 2: SELECT with condition
    m = re.match(r"(select|show|list) (?:all\s+)? (\w+) from (\w+) where (\w+) (>|<|=) (\d+)", text)
    if m:
       column = m.group(2)
       table = m.group(3)
       cond_col = m.group(4)
       op = m.group(5)
       val = m.group(6)
       return f"SELECT {column} FROM {table} WHERE {cond_col} {op} {val}"

    # Rule 3: COUNT
    m = re.match(
    r"(count|how many)\s+(\w+)(?:\s+from\s+(\w+))?(?:\s+where\s+(\w+)\s*(=|>|<)\s*(\d+))?",
    text,
    flags=re.IGNORECASE
    )
    if m:
       col = m.group(2)
       table = m.group(3)
       where_col = m.group(4)
       op = m.group(5)
       val = m.group(6)

       if table is None:
        table = col
        col = None

       query = (
        f"SELECT COUNT({col}) FROM {table}"
        if col else
        f"SELECT COUNT(*) FROM {table}"
        )
       if where_col:
        query += f" WHERE {where_col} {op} {val}"

       return query

    # Rule 4: SUM
    m = re.match(
    r"(sum|total)(?: (\w+))? from (\w+)(?: where (\w+)\s*=\s*(\w+))?",
    text,
    flags=re.IGNORECASE
    )
    if m:
       col = m.group(2)
       table = m.group(3)
       where_col = m.group(4)
       where_val = m.group(5)

       if col:
        query = f"SELECT SUM({col}) FROM {table}"
       else:
        query = f"SELECT SUM(*) FROM {table}"

       if where_col:
        query += f" WHERE {where_col} = {where_val}"

       return query

    # Rule 5: ORDER BY
    m = re.match(
    r"(select|show) all (\w+) where (\w+) (>=|<=|>|<|=) (\w+) order by(?: (\w+))?(?: (asc|desc))?",
    text
    )
    if m:
       table = m.group(2)
       cond_col, op, val = m.group(3), m.group(4), m.group(5)
       order_col = m.group(6) if m.group(6) else "id"
       order = m.group(7).upper() if m.group(7) else ""
       return f"SELECT * FROM {table} WHERE {cond_col} {op} {val} ORDER BY {order_col} {order}".strip()

    m = re.match(
    r"(select|show) all (\w+) order by(?: (\w+))?(?: (asc|desc))?",
    text
    )
    if m:
       table = m.group(2)
       order_col = m.group(3) if m.group(3) else "id"
       order = m.group(4).upper() if m.group(4) else ""
       return f"SELECT * FROM {table} ORDER BY {order_col} {order}".strip()

    # Rule 6: GROUP BY
    m = re.match(
    r"(select|show) (\w+(?:, \w+)*) from (\w+) group by (\w+)",
    text,
    flags=re.IGNORECASE
    )
    if m:
       cols = m.group(2)
       table = m.group(3)
       group_col = m.group(4)
       cols = ", ".join([c.strip() for c in cols.split(",")])
       return f"SELECT {cols} FROM {table} GROUP BY {group_col}"

    # Rule 7: Multiple conditions (AND/OR)
    m = re.match(
    r"(select|show|display)(?:\s+(all))?(?:\s+([\w, ]+))?(?:\s+from)?\s+(\w+)\s+where\s+(\w+)\s*(>|<|=)\s*(\d+)\s+(and|or)\s+(\w+)\s*(>|<|=)\s*(\d+)",
    text,
    re.IGNORECASE
    )
    if m:
       all_kw, columns, table, col1, op1, val1, logic, col2, op2, val2 = m.groups()
       if all_kw or not columns:
        select_part = "SELECT *"
       else:
        cols = ",".join([c.strip() for c in columns.split(",")])
        select_part = f"SELECT {cols}"
       query = (
        f"{select_part} FROM {table} "
        f"WHERE {col1} {op1} {val1} {logic.upper()} {col2} {op2} {val2}"
       )
       return query

    # Rule 8: INSERT
    m = re.match(r"(insert into|add new row into)\s+(\w+)\s+values\s+(.+)", text, re.IGNORECASE)
    if m:
      _, table, values = m.groups()
      return f"INSERT INTO {table} VALUES ({values})"

    # Rule 9: UPDATE
    m = re.match(r"(update|change)\s+(\w+)\s+set\s+(\w+)\s*=\s*([\w' ]+)\s+where\s+(\w+)\s*=\s*([\w' ]+)", text, re.IGNORECASE)
    if m:
       _, table, col_set, val_set, col_where, val_where = m.groups()
       return f"UPDATE {table} SET {col_set} = {val_set} WHERE {col_where} = {val_where}"
    
    # Rule 10: DELETE
    m = re.match(r"(delete from|remove from)\s+(\w+)\s+where\s+(\w+)\s*(=|>|<)\s*([\w' ]+)", text, re.IGNORECASE)
    if m:
       _, table, col, op, val = m.groups()
       return f"DELETE FROM {table} WHERE {col} {op} {val}"

    # Rule 11: DROP COLUMN
    m = re.match(r"(delete|remove)\s+(column|columns|col)\s+([\w, ]+)\s+from\s+(\w+)", text, re.IGNORECASE)
    if m:
      _, _, cols, table = m.groups()
      col_list = [c.strip() for c in cols.split(",")]
      drop_parts = ", ".join([f"DROP COLUMN {c}" for c in col_list])
      return f"ALTER TABLE {table} {drop_parts}"

    # Rule 12: LIKE
    m = re.match(r"(find|search)\s+(\w+)\s+where\s+(\w+)\s+(contains|like)\s+'(.+)'", text, re.IGNORECASE)
    if m:
      _, table, col, _, val = m.groups()
      return f"SELECT * FROM {table} WHERE {col} LIKE '%{val}%'"

    # Rule 13: BETWEEN
    m = re.match(r"select\s+(\w+)\s+where\s+(\w+)\s+between\s+(\d+)\s+and\s+(\d+)", text, re.IGNORECASE)
    if m:
       table, col, v1, v2 = m.groups()
       return f"SELECT * FROM {table} WHERE {col} BETWEEN {v1} AND {v2}"

    # Rule 14: IN
    m = re.match(r"select\s+(\w+)\s+where\s+(\w+)\s+in\s+(.+)", text, re.IGNORECASE)
    if m:
      table, col, vals = m.groups()
      val_list = ",".join(v.strip() for v in vals.split(","))
      return f"SELECT * FROM {table} WHERE {col} IN ({val_list})"
    
    # Rule 15: DISTINCT
    m = re.match(r"select\s+(distinct|unique)\s+(\w+)\s+from\s+(\w+)", text, re.IGNORECASE)
    if m:
      _, col, table = m.groups()
      return f"SELECT DISTINCT {col} FROM {table}"

    return "No matching rule found"

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "No input provided"}))
        return
    
    text = sys.argv[1]
    sql = english_to_dsl(text)
    
    print(json.dumps({
        "sql": sql,
        "explanation": f"Converted: {text}"
    }))

if __name__ == "__main__":
    main()
