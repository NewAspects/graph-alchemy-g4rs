const JSON_URL = "leaderboard.json";

function render(rows) {
    const tbody = document.querySelector("#tbl tbody");
    tbody.innerHTML = "";
    for (const r of rows) {
        const tr = document.createElement("tr");
        ["rank", "score"].forEach(k => {
            const td = document.createElement("td");
            td.textContent = r[k] || "";
            tr.appendChild(td);
        });
        tbody.appendChild(tr);
    }
}

(async function main() {
    const allRows = await fetch(JSON_URL, { cache: "no-store" }).then(r => r.json());
    render(allRows);
})();
