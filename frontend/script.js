const form = document.getElementById("predictForm");
const resultDiv = document.getElementById("result");
const btn = document.getElementById("predictBtn");

form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Visual feedback
    btn.innerText = "CALCULATING...";
    btn.style.opacity = "0.7";
    resultDiv.innerHTML = ""; // Clear previous results

    const formData = new FormData(form);
    const data = Object.fromEntries(formData.entries());

    // Convert numeric fields accurately
    const numericFields = ["runs_left", "balls_left", "wickets", "total_runs_x", "crr", "rrr"];
    numericFields.forEach(key => {
        data[key] = parseFloat(data[key]);
    });

    try {
        const response = await fetch("http://127.0.0.1:8080/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error("Server Error");

        const result = await response.json();

        // Check if we got percentages (the pro way) or just a result (the old way)
        if (result.win_percentage !== undefined) {
            resultDiv.innerHTML = `
                <div style="margin-bottom: 15px; display: flex; justify-content: space-between; font-weight: bold; font-size: 1.1rem;">
                    <span style="color: #2ecc71">${data.batting_team}: ${result.win_percentage}%</span>
                    <span style="color: #e74c3c">${data.bowling_team}: ${result.loss_percentage}%</span>
                </div>
                
                <div style="width: 100%; height: 22px; background: #0d1117; border-radius: 11px; overflow: hidden; display: flex; border: 1px solid #30363d;">
                    <div style="width: ${result.win_percentage}%; background: linear-gradient(90deg, #2ecc71, #27ae60); transition: width 1.5s ease-in-out;"></div>
                    <div style="width: ${result.loss_percentage}%; background: linear-gradient(90deg, #c0392b, #e74c3c); transition: width 1.5s ease-in-out;"></div>
                </div>

                <p style="margin-top: 15px; color: #8b949e; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 1px;">
                    Win Probability for ${data.batting_team}
                </p>
            `;
            resultDiv.style.background = "rgba(255, 255, 255, 0.03)";
            resultDiv.style.padding = "20px";
            resultDiv.style.border = "1px solid #30363d";
            resultDiv.style.borderRadius = "12px";
        } else {
            // Fallback for simple results
            resultDiv.innerHTML = result.result === 1 
                ? `<span style="color: #2ecc71">🏏 Prediction: ${data.batting_team} is likely to Win!</span>`
                : `<span style="color: #e74c3c">🏏 Prediction: ${data.bowling_team} is likely to Win!</span>`;
            resultDiv.style.background = "rgba(255, 255, 255, 0.05)";
        }

    } catch (err) {
        console.error(err);
        resultDiv.innerText = "⚠️ Connection Error: Is the Flask server on Port 8080?";
        resultDiv.style.color = "#f39c12";
        resultDiv.style.background = "transparent";
    } finally {
        btn.innerText = "ANALYZE PROBABILITY";
        btn.style.opacity = "1";
    }
});