# 🔐 SQL Anonymizer / Desanonymizer

This project aims to **protect sensitive data** within SQL queries before sharing them with third parties (e.g., ChatGPT for debugging or optimization), and then **restore the original query** after processing.

## ✨ Typical Use Case

1. ✅ You have a SQL query containing confidential procedure, table or column names.
2. 🔐 You anonymize it using this script or web interface.
3. 🤖 You send the anonymized version to ChatGPT for debugging or improvements.
4. 🔓 You retrieve the corrected version and **automatically deanonymize it** to run in your own environment.

---

## 📁 Project Structure

* `anonymisation.py`: Script to anonymize a SQL query.
* `desanonymisation.py`: Script to restore original names using the mapping.
* `app.py`: Streamlit web app to interactively anonymize/deanonymize SQL queries.
* `input.sql`: Example SQL input (original query).
* `output.sql`: Anonymized or deanonymized SQL query, depending on the script.
* `mapping.txt`: Mapping file linking original and anonymized names.

---

## 🚀 Usage (CLI mode)

### 1. Anonymization

```bash
python anonymisation.py
```

This will generate:

* `output.sql`: anonymized SQL query
* `mapping.txt`: mapping of original names to anonymized tokens

👉 At this point, you can share `output.sql` with ChatGPT.

### 2. Deanonymization (after ChatGPT processing)

Place the corrected version from ChatGPT into `output.sql`, then run:

```bash
python desanonymisation.py
```

This will generate:

* `restored.sql`: corrected SQL query with original names restored

---

## 🚪 Usage (Streamlit App)

To use the web interface, run:

```bash
streamlit run app.py
```

The app allows you to:

* Paste or upload a SQL query.
* Anonymize it with a single click.
* View and download the anonymized version.
* View the mapping file.
* Paste or upload a corrected SQL to deanonymize it.
* Download the final restored version.

The app includes two main modes:

* **Manual input** (side-by-side text areas + buttons)
* **File upload** with download buttons.

---

## 🔄 Simple Example

#### `input.sql` (original)

```sql
CREATE PROCEDURE [dbo].[GetUserData]
AS
BEGIN
    SELECT u.name, u.email
    FROM users u
    WHERE u.status = 'active'
END
```

#### `output.sql` (after anonymization)

```sql
CREATE PROCEDURE [schema1].[proc1]
AS
BEGIN
    SELECT alias1.col1, alias1.col2
    FROM table1 alias1
    WHERE alias1.col3 = 'active'
END
```

#### `restored.sql` (after deanonymization)

Back to the corrected version with real table and column names.

---

## ⚠️ Limitations

* Does not yet support advanced SQL features like dynamic SQL or very complex naming schemes.
* The mapping is purely text-based: avoid editing `mapping.txt` manually.

---

## 🧠 Roadmap (Ideas)

* Support for more SQL dialects.
* Smart restoration using ChatGPT output analysis.
* Save project session/history.
* Deploy the Streamlit app to the web (Streamlit Cloud or custom server).

---

## 🛠️ Dependencies

Minimal:

```txt
streamlit
```

Install with:

```bash
pip install -r requirements.txt
```

---

## 👤 Author

Project created to help secure SQL exchanges with LLMs (ChatGPT, Claude, etc.) in sensitive professional contexts.

---

