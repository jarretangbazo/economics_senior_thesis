# Figures and Tables Guide
**Reference sheet for inserting figures and tables in LaTeX.**  
This file lives in `thesis/` but is **not** `\input`'d into `main.tex` — it is a reference document to consult while writing.

---

## Part 1: Figures

### File format and location
Save all figures to `thesis/figures/`. Use `.pdf` for vector graphics (plots from matplotlib) and `.png` for raster images. PDF is preferred because it scales perfectly at any zoom level in the compiled PDF.

### Basic figure

```latex
\begin{figure}[H]                          % [H] = "place HERE exactly"
    \centering
    \includegraphics[width=0.85\textwidth]{figures/my_figure.pdf}
    \caption{A descriptive caption explaining what the figure shows.}
    \label{fig:my_figure}                  % Used for \ref{fig:my_figure}
\end{figure}
```

**Width options:**

| Option | Effect |
|---|---|
| `width=0.85\textwidth` | 85% of text width — most common |
| `width=0.5\textwidth` | Half-width |
| `width=\textwidth` | Full text width |
| `height=3in` | Fixed height, aspect ratio preserved |

### Two figures side by side

```latex
\begin{figure}[H]
    \centering
    \begin{subfigure}[b]{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{figures/fig_left.pdf}
        \caption{Left panel caption.}
        \label{fig:left}
    \end{subfigure}
    \hfill
    \begin{subfigure}[b]{0.48\textwidth}
        \centering
        \includegraphics[width=\textwidth]{figures/fig_right.pdf}
        \caption{Right panel caption.}
        \label{fig:right}
    \end{subfigure}
    \caption{Overall figure caption (shown below both panels).}
    \label{fig:both}
\end{figure}
```

### Saving figures from Python

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(x, y)
ax.set_xlabel("X axis")
ax.set_ylabel("Y axis")
plt.tight_layout()

# Save as PDF (preferred — vector, no quality loss)
plt.savefig("thesis/figures/my_figure.pdf", dpi=300, bbox_inches="tight")

# OR save as high-res PNG
plt.savefig("thesis/figures/my_figure.png", dpi=300, bbox_inches="tight")
```

---

## Part 2: Tables

### Basic table (booktabs / econometrics style)

`booktabs` gives you `\toprule`, `\midrule`, `\bottomrule`. **Never use `\hline` in economics tables** — always use booktabs rules.

```latex
\begin{table}[H]
    \centering
    \caption{Table title goes here (above the table in economics style).}
    \label{tab:basic}
    \begin{tabular}{lcc}        % l = left, c = center, r = right
        \toprule
        Variable & Column 1 & Column 2 \\
        \midrule
        Row 1    & 0.123    & 0.456    \\
        Row 2    & 0.789$^{**}$ & 0.012$^{*}$ \\
                 & (0.034)  & (0.007)  \\
        \midrule
        N        & 1,000    & 1,000    \\
        R$^2$    & 0.45     & 0.52     \\
        \bottomrule
    \end{tabular}
\end{table}
```

**Significance stars convention** (standard in economics — report in table notes, not column headers):

| Star | Threshold |
|---|---|
| `*` | p < 0.10 |
| `**` | p < 0.05 |
| `***` | p < 0.01 |

### Table with notes (`threeparttable`)

Use `threeparttable` whenever you need footnotes below the table. This is standard for regression tables.

```latex
\begin{table}[H]
    \centering
    \caption{Regression Results with Notes}
    \label{tab:with_notes}
    \begin{threeparttable}
        \begin{tabular}{lcc}
            \toprule
            & (1) OLS & (2) OLS + FE \\
            \midrule
            Violence (early childhood) & $-$0.022$^{***}$ & 0.010 \\
                                       & (0.007)          & (0.010) \\[0.3em]
            Controls & Yes & Yes \\
            LGA FE   & No  & Yes \\
            \midrule
            N        & 56,878 & 56,878 \\
            R$^2$    & 0.43   & 0.52   \\
            \bottomrule
        \end{tabular}
        \begin{tablenotes}
            \small
            \item \textit{Notes:} Robust standard errors in parentheses.
            $^{*}p < 0.10$, $^{**}p < 0.05$, $^{***}p < 0.01$.
        \end{tablenotes}
    \end{threeparttable}
\end{table}
```

### Decimal-aligned columns (`siunitx`)

Use the `S` column type to align numbers at the decimal point. Requires `\usepackage{siunitx}` in the preamble (already included in `main.tex`). Wrap header text in `{}` to prevent formatting.

```latex
\begin{table}[H]
    \centering
    \caption{Decimal-Aligned Table}
    \label{tab:siunitx}
    \begin{tabular}{l S[table-format=1.3] S[table-format=1.3]}
        \toprule
        Variable & {Column 1} & {Column 2} \\
        \midrule
        Coef 1   & 0.123  & -0.456 \\
        Coef 2   & 1.789  &  0.012 \\
        \bottomrule
    \end{tabular}
\end{table}
```

### Wide table in landscape (`pdflscape`)

For tables too wide to fit in portrait orientation. Requires `\usepackage{pdflscape}` in the preamble (already included in `main.tex`).

```latex
\begin{landscape}
\begin{table}[H]
    \centering
    \caption{Wide Table in Landscape}
    \label{tab:landscape}
    \begin{tabular}{lcccccc}
        \toprule
        Variable & Col1 & Col2 & Col3 & Col4 & Col5 & Col6 \\
        \midrule
        Row 1    & & & & & & \\
        \bottomrule
    \end{tabular}
\end{table}
\end{landscape}
```

### Multi-page table (`longtable`)

For variable definition tables or long appendix tables that need to break across pages. The header row repeats automatically on each new page.

```latex
\begin{longtable}{p{0.25\textwidth}p{0.65\textwidth}}
    \caption{Long Table with Page Breaks} \label{tab:long} \\
    \toprule
    Variable & Definition \\
    \midrule
    \endfirsthead
    % Everything below repeats as the header on continuation pages:
    \multicolumn{2}{c}{\tablename~\thetable{} (continued)} \\
    \toprule
    Variable & Definition \\
    \midrule
    \endhead
    \midrule
    \multicolumn{2}{r}{\textit{Continued on next page}} \\
    \endfoot
    \bottomrule
    \endlastfoot
    % Table content:
    var1 & Definition of variable 1. \\
    var2 & Definition of variable 2. \\
\end{longtable}
```

### Generating LaTeX tables from Python

**Option A — `stargazer` (recommended for regression tables)**

```python
pip install stargazer

from stargazer.stargazer import Stargazer
import statsmodels.formula.api as smf

model = smf.ols("attend ~ viol_ech + age + male", data=df).fit()
s = Stargazer([model])
print(s.render_latex())   # paste output into your .tex file
```

**Option B — `pandas` `.to_latex()` (for summary stat tables)**

```python
df.to_latex("thesis/tables/summary_stats.tex", index=False)
# Then in your chapter file: \input{tables/summary_stats.tex}
```

**Option C — `modelsummary` (if using R)**

```r
library(modelsummary)
modelsummary(model, output = "thesis/tables/results.tex")
```

---

## Part 3: Cross-Referencing

Always use `~` (non-breaking space) between the label word and the number to prevent line breaks. Use `\eqref` for equations (adds parentheses automatically).

```latex
See Figure~\ref{fig:my_figure}.
See Table~\ref{tab:basic}.
See Section~\ref{sec:methodology}.
See Equation~\eqref{eq:attend}.
```

---

## Part 4: End-to-End Workflow

### Figures

1. Write your Python script and save the figure to `thesis/figures/my_fig.pdf`
2. In your `.tex` chapter file, insert:
    ```latex
    \begin{figure}[H]
        \centering
        \includegraphics[width=0.85\textwidth]{figures/my_fig.pdf}
        \caption{Caption here.}
        \label{fig:my_fig}
    \end{figure}
    ```
3. Reference it in the text: `...as shown in Figure~\ref{fig:my_fig}.`
4. Compile — Overleaf does this automatically on save.

### Tables from Python

1. Export a `.tex` snippet using `stargazer` or `.to_latex()`
2. Save to `thesis/tables/table_name.tex`
3. In your chapter file: `\input{tables/table_name.tex}` — or paste the `tabular` environment directly into the chapter
