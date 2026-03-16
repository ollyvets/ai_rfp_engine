use pyo3::prelude::*;

/// Cleans the input text by removing excessive whitespace, tabs, and newlines.
/// This significantly reduces the token count before sending data to the LLM.
#[pyfunction]
fn clean_text(text: &str) -> PyResult<String> {
    // split_whitespace() automatically handles multiple spaces, tabs, and newlines.
    // We then join the words back together with a single space.
    // This is incredibly fast in Rust and uses minimal memory overhead.
    let cleaned_text: String = text.split_whitespace().collect::<Vec<&str>>().join(" ");
    
    Ok(cleaned_text)
}

/// Calculates a relevance score by counting how many times specific keywords appear in the text.
/// This acts as a pre-filter to understand the document's context quickly.
#[pyfunction]
fn calculate_match_score(text: &str, keywords: Vec<String>) -> PyResult<usize> {
    let text_lower = text.to_lowercase();
    let mut total_score = 0;

    for keyword in keywords {
        let kw_lower = keyword.to_lowercase();
        // matches() finds all non-overlapping occurrences of the substring
        total_score += text_lower.matches(&kw_lower).count();
    }

    Ok(total_score)
}

/// The main Python module implemented in Rust.
/// The name of the function MUST match the name in Cargo.toml [lib] section.
#[pymodule]
fn rust_core(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(clean_text, m)?)?;
    m.add_function(wrap_pyfunction!(calculate_match_score, m)?)?;
    Ok(())
}