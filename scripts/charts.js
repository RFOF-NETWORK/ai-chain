// scripts/charts.js
//
// charts.js übernimmt NUR die Visualisierung.
// ui.js liefert die Daten, charts.js zeichnet die Diagramme.
//
// Anforderungen:
// - Keine externen Frameworks nötig (aber kompatibel mit Chart.js, falls später gewünscht)
// - Muss deterministisch funktionieren
// - Muss von ui.js über window.updatePortfolioChart() aufrufbar sein

let portfolioChart = null;

// -----------------------------------------------------------------------------
// Portfolio-Token-Chart
// -----------------------------------------------------------------------------

function updatePortfolioChart(tokenData) {
    // tokenData = { AI: x, COIN: y, AIC_LP: z }

    const ctx = document.getElementById("portfolio_chart");
    if (!ctx) {
        console.warn("portfolio_chart Canvas nicht gefunden.");
        return;
    }

    const labels = Object.keys(tokenData);
    const values = Object.values(tokenData);

    // Falls bereits ein Chart existiert → zerstören
    if (portfolioChart) {
        portfolioChart.destroy();
    }

    // Minimalistische Chart.js‑Konfiguration
    portfolioChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [
                {
                    label: "Token‑Verteilung",
                    data: values,
                    backgroundColor: [
                        "rgba(54, 162, 235, 0.7)",   // AI
                        "rgba(255, 206, 86, 0.7)",   // COIN
                        "rgba(153, 102, 255, 0.7)"   // AIC_LP
                    ],
                    borderColor: [
                        "rgba(54, 162, 235, 1)",
                        "rgba(255, 206, 86, 1)",
                        "rgba(153, 102, 255, 1)"
                    ],
                    borderWidth: 1
                }
            ]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: "bottom"
                },
                title: {
                    display: true,
                    text: "Portfolio‑Token‑Verteilung"
                }
            }
        }
    });
}

// -----------------------------------------------------------------------------
// Export für ui.js
// -----------------------------------------------------------------------------

window.updatePortfolioChart = updatePortfolioChart;

