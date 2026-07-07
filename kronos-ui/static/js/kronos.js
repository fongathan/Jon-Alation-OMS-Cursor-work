/* Kronos UI — client-side helpers */

function filterTable(query) {
  const table = document.getElementById("inventoryTable");
  if (!table) return;
  const rows = table.querySelectorAll("tbody tr");
  const q = query.toLowerCase();
  rows.forEach((row) => {
    const text = row.textContent.toLowerCase();
    row.style.display = text.includes(q) ? "" : "none";
  });
}

function sortTable(colIdx) {
  const table = document.getElementById("inventoryTable");
  if (!table) return;
  const tbody = table.querySelector("tbody");
  const rows = Array.from(tbody.querySelectorAll("tr"));
  const dir = table.dataset.sortDir === "asc" ? "desc" : "asc";
  table.dataset.sortDir = dir;

  rows.sort((a, b) => {
    const aText = (a.cells[colIdx]?.textContent || "").trim().toLowerCase();
    const bText = (b.cells[colIdx]?.textContent || "").trim().toLowerCase();
    if (dir === "asc") return aText.localeCompare(bText);
    return bText.localeCompare(aText);
  });

  rows.forEach((row) => tbody.appendChild(row));
}

document.addEventListener("keydown", (e) => {
  if ((e.metaKey || e.ctrlKey) && e.key === "k") {
    e.preventDefault();
    const searchInput = document.querySelector('input[name="q"]');
    if (searchInput) searchInput.focus();
  }
});
