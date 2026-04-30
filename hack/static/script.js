setInterval(async () => {
    try {
        let res = await fetch("/alert");
        let allData = await res.json();
        const grid = document.getElementById("nodesGrid");
        
        // Use object keys dynamically so 1, 2, or N cameras work!
        if (Object.keys(allData).length > 0) {
            grid.innerHTML = ""; // Clear loader
            
            const camIds = Object.keys(allData).filter(id => id !== "error");
            if (camIds.length > 0) {
                const firstCam = allData[camIds[0]];
                if (firstCam && document.getElementById('globalUniqueCount')) {
                    document.getElementById('globalUniqueCount').innerText = firstCam.global_unique_count || 0;
                }
            } else {
                return; // Nothing to show
            }

            camIds.forEach(camId => {
                const data = allData[camId];
                
                let tlHtml = "";
                (data.timeline || []).forEach(e => { tlHtml += `<p>${e}</p>`; });
                
                let predClass = (data.prediction || "").toUpperCase().includes("STABLE") ? "prediction-stable" : "";
                
                let card = document.createElement("div");
                card.className = "camera-node";
                card.innerHTML = `
                    <div class="alert-banner ${data.alert_level}">
                        <span>[${data.alert_level}] Node ${camId}: ${data.message}</span>
                        <span style="font-size:0.9rem; color: var(--subtext); font-weight: normal;">📍 ${data.location}</span>
                    </div>

                    <div class="metrics-grid">
                        <div class="metric-card">
                            <h4>POPULATION</h4>
                            <div class="val">${data.people_count}<span>/ ${data.max_capacity}</span></div>
                        </div>
                        <div class="metric-card">
                            <h4>RISK SCORE</h4>
                            <div class="val">${Math.round(data.risk_score)}</div>
                        </div>
                        <div class="metric-card">
                            <h4>AI PREDICTION</h4>
                            <div class="val ${predClass}" style="font-weight: 700;">${(data.prediction || "UNKNOWN").toUpperCase()}</div>
                        </div>
                    </div>
                    
                    <div class="video-container">
                        <img src="/video_feed/${camId}" style="width:100%; height:100%; object-fit:cover;" onerror="this.style.display='none';">
                        <div class="recording-dot"></div>
                        <div style="position: absolute; bottom: 15px; right: 20px; color: #00ff00; font-family: monospace; font-size: 12px; background: rgba(0,0,0,0.7); padding: 5px 10px; border-radius: 4px; letter-spacing: 1px;">
                            RES: ${data.resolution} | FPS: ${data.fps} | Sync: ${data.timestamp}
                        </div>
                    </div>
                    
                    <div class="timeline-box">
                        ${tlHtml || "<p>No recent events.</p>"}
                    </div>
                `;
                
                grid.appendChild(card);
            });
        }
    } catch (err) {
        console.error("API Error: ", err);
    }
}, 1000);