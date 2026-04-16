setInterval(async () => {
    try {
        let res = await fetch("/alert");
        let allData = await res.json();
        const grid = document.getElementById("nodesGrid");
        
        // Use object keys dynamically so 1, 2, or N cameras work!
        if (Object.keys(allData).length > 0) {
            grid.innerHTML = ""; // Clear loader
            
            for (const camId in allData) {
                const data = allData[camId];
                
                let tlHtml = "";
                (data.timeline || []).forEach(e => { tlHtml += `<p>${e}</p>`; });
                
                let riskColor = data.risk_score >= 8 ? "#ff3333" : (data.risk_score >= 5 ? "#eab308" : "transparent");
                
                let card = document.createElement("div");
                card.className = "camera-node";
                card.innerHTML = `
                    <div class="alert-banner ${data.alert_level}">
                        <span>[${data.alert_level}] Node ${camId}: ${data.message}</span>
                        <span style="font-size:12px;">📍 ${data.location}</span>
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <h4>Population</h4>
                            <div class="val">${data.people_count}</div>
                        </div>
                        <div class="metric-card" style="border-color:${riskColor};">
                            <h4>Risk Score</h4>
                            <div class="val" style="color:white;">${data.risk_score}</div>
                        </div>
                        <div class="metric-card">
                            <h4>AI Prediction</h4>
                            <div class="val" style="font-size:1rem; color:#facc15;">${data.prediction}</div>
                        </div>
                    </div>
                    
                    <div class="video-container">
                        <div class="recording-dot"></div>
                        <span style="color:#4b5563;">[PIPELINE EXECUTING LOCALLY]</span>
                        <div style="position: absolute; bottom: 10px; right: 10px; color: lime; font-family: monospace; font-size: 12px;">FPS: ${data.fps} | Sync: ${data.timestamp}</div>
                    </div>
                    
                    <div class="timeline-box">
                        ${tlHtml || "<p>No recent events.</p>"}
                    </div>
                `;
                
                grid.appendChild(card);
            }
        }
    } catch (err) {
        console.error("API Error: ", err);
    }
}, 1000);