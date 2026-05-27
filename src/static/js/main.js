/* -------------------------------------------------------------
 * AeroDash Dashboard Console Logic
 * ------------------------------------------------------------- */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const btnRefreshInfo = document.getElementById('btn-refresh-info');
    const btnTriggerHealth = document.getElementById('btn-trigger-health');
    const btnShowAbout = document.getElementById('btn-show-about');
    const systemInfoContainer = document.getElementById('system-info-container');
    const consoleLogs = document.getElementById('console-logs');
    
    // Expansion Features DOM Elements
    const btnRefreshStocks = document.getElementById('btn-refresh-stocks');
    const stockTickerContainer = document.getElementById('stock-ticker-container');
    const companyNameVal = document.getElementById('company-name-val');
    const companyDeptVal = document.getElementById('company-dept-val');
    const shiftTimeVal = document.getElementById('shift-time-val');
    const shiftLocationVal = document.getElementById('shift-location-val');
    const timelineContainer = document.getElementById('timeline-container');

    // Modal Elements
    const aboutModal = document.getElementById('about-modal');
    const modalCloseBtn = document.getElementById('modal-close-btn');
    const modalOkBtn = document.getElementById('modal-ok-btn');

    // Metrics Elements
    const statusVal = document.getElementById('status-val');
    const uptimeVal = document.getElementById('uptime-val');
    const memoryVal = document.getElementById('memory-val');
    const cpuVal = document.getElementById('cpu-val');

    // Helper: Add logs to the mock console
    function addConsoleLog(message, type = 'info') {
        const time = new Date().toLocaleTimeString();
        const logLine = document.createElement('div');
        logLine.className = `log-line text-${type}`;
        logLine.textContent = `[${time}] ${message}`;
        consoleLogs.appendChild(logLine);
        
        // Auto-scroll to bottom
        consoleLogs.scrollTop = consoleLogs.scrollHeight;
    }

    // Function: Fetch System Info and populate specs card
    async function fetchSystemInfo() {
        if (btnRefreshInfo) {
            btnRefreshInfo.classList.add('icon-spin');
        }
        
        try {
            const response = await fetch('/api/info');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            
            const data = await response.json();
            
            // Build key-value specs
            let htmlContent = `
                <div class="info-row">
                    <span class="info-label">應用程式名稱</span>
                    <span class="info-value">${data.app_name}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">系統版本</span>
                    <span class="info-value">${data.version}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">運作 Port</span>
                    <span class="info-value">${data.port}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">作業系統平台</span>
                    <span class="info-value" style="font-size: 0.8rem;">${data.platform}</span>
                </div>
                <div class="info-row">
                    <span class="info-label">Python 版本</span>
                    <span class="info-value" style="font-size: 0.8rem;">${data.python_version.split(' ')[0]}</span>
                </div>
            `;
            
            systemInfoContainer.innerHTML = htmlContent;
            addConsoleLog('[system] 成功取得主機環境資訊與 Python 版本。', 'success');
        } catch (error) {
            systemInfoContainer.innerHTML = `
                <div class="info-row" style="color: var(--accent-rose); border-color: rgba(244, 63, 94, 0.25);">
                    <span>讀取系統資訊失敗: ${error.message}</span>
                </div>
            `;
            addConsoleLog(`[error] 讀取系統資訊失敗: ${error.message}`, 'error');
        } finally {
            if (btnRefreshInfo) {
                setTimeout(() => {
                    btnRefreshInfo.classList.remove('icon-spin');
                }, 800);
            }
        }
    }

    // Function: Fetch Health Metrics
    async function fetchHealthStats(logOutput = false) {
        try {
            const response = await fetch('/api/health');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();

            // Populate dashboard metrics cards
            statusVal.textContent = data.status.toUpperCase();
            statusVal.style.color = 'var(--accent-emerald)';
            uptimeVal.textContent = data.uptime;
            memoryVal.textContent = data.memory_usage;
            cpuVal.textContent = data.cpu_load;

            if (logOutput) {
                addConsoleLog(`[api-call] Health status: ${data.status} | DB: ${data.database} | Load: ${data.cpu_load}`, 'success');
            }
        } catch (error) {
            statusVal.textContent = 'ERROR';
            statusVal.style.color = 'var(--accent-rose)';
            if (logOutput) {
                addConsoleLog(`[error] 健康狀態 API 連線失敗: ${error.message}`, 'error');
            }
        }
    }

    // Function: Fetch Specified Stocks Watchlist
    async function fetchStocks() {
        if (btnRefreshStocks) {
            btnRefreshStocks.classList.add('icon-spin');
        }
        try {
            const response = await fetch('/api/stocks');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();

            let htmlContent = '';
            data.forEach(stock => {
                const isUp = stock.direction === 'up';
                const cardClass = isUp ? 'card-up' : 'card-down';
                const arrow = isUp ? '▲' : '▼';
                
                htmlContent += `
                    <div class="stock-card ${cardClass}">
                        <div class="stock-info">
                            <div class="stock-name-grp">
                                <span class="stock-symbol">${stock.symbol}</span>
                                <span class="stock-name">${stock.name}</span>
                            </div>
                            <span class="stock-volume-grp">${stock.volume} 股</span>
                        </div>
                        <div class="stock-price-grp">
                            <span class="stock-price">$${stock.price.toFixed(2)}</span>
                            <span class="stock-change">${arrow} ${stock.change_percent}</span>
                        </div>
                    </div>
                `;
            });
            stockTickerContainer.innerHTML = htmlContent;
            addConsoleLog('[stocks] 股市指定標的行情載入完成。', 'success');
        } catch (error) {
            stockTickerContainer.innerHTML = `
                <div class="info-row" style="color: var(--accent-rose); border-color: rgba(244, 63, 94, 0.25); width: 100%;">
                    <span>讀取股票報價失敗: ${error.message}</span>
                </div>
            `;
            addConsoleLog(`[error] 讀取股市行情失敗: ${error.message}`, 'error');
        } finally {
            if (btnRefreshStocks) {
                setTimeout(() => {
                    btnRefreshStocks.classList.remove('icon-spin');
                }, 800);
            }
        }
    }

    // Function: Fetch Afternoon Schedule details
    async function fetchSchedule() {
        try {
            const response = await fetch('/api/schedule');
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const data = await response.json();

            // Populate profile
            companyNameVal.textContent = data.company;
            companyDeptVal.textContent = data.department;
            shiftTimeVal.textContent = data.time_window;
            shiftLocationVal.textContent = data.location;

            // Populate timeline
            let htmlContent = '';
            data.timeline.forEach(item => {
                let statusClass = 'pending';
                let statusText = '未開始';
                if (item.status === 'completed') {
                    statusClass = 'completed';
                    statusText = '已完成';
                } else if (item.status === 'in_progress') {
                    statusClass = 'in_progress';
                    statusText = '進行中';
                }
                
                const tagClass = `status-tag-${statusClass === 'in_progress' ? 'progress' : statusClass}`;

                htmlContent += `
                    <div class="timeline-item ${statusClass}">
                        <div class="timeline-badge"></div>
                        <div class="timeline-content">
                            <div class="timeline-text">
                                <span class="timeline-time">${item.time}</span>
                                <span class="timeline-task">${item.task}</span>
                            </div>
                            <span class="timeline-status-badge ${tagClass}">${statusText}</span>
                        </div>
                    </div>
                `;
            });
            
            timelineContainer.innerHTML = htmlContent;
            addConsoleLog(`[schedule] 已載入下午公司行程：${data.company.split(' ')[0]}。`, 'info');
        } catch (error) {
            addConsoleLog(`[error] 載入排程與上班公司資訊失敗: ${error.message}`, 'error');
        }
    }

    // Modal Control Functions
    function openModal() {
        aboutModal.classList.add('active');
        addConsoleLog('[ui] 開啟關於對話視窗。', 'info');
    }

    function closeModal() {
        aboutModal.classList.remove('active');
        addConsoleLog('[ui] 關閉關於對話視窗。', 'info');
    }

    // Event Listeners
    if (btnRefreshInfo) {
        btnRefreshInfo.addEventListener('click', fetchSystemInfo);
    }

    if (btnRefreshStocks) {
        btnRefreshStocks.addEventListener('click', () => {
            addConsoleLog('[ui] 重新載入指定股票報價。', 'info');
            fetchStocks();
        });
    }

    if (btnTriggerHealth) {
        btnTriggerHealth.addEventListener('click', () => {
            addConsoleLog('[api-call] 正在呼叫健康度 API `/api/health` ...', 'info');
            fetchHealthStats(true);
        });
    }

    if (btnShowAbout) {
        btnShowAbout.addEventListener('click', openModal);
    }

    if (modalCloseBtn) {
        modalCloseBtn.addEventListener('click', closeModal);
    }

    if (modalOkBtn) {
        modalOkBtn.addEventListener('click', closeModal);
    }

    // Close modal when clicking on overlay
    if (aboutModal) {
        aboutModal.addEventListener('click', (e) => {
            if (e.target === aboutModal) {
                closeModal();
            }
        });
    }

    // Initial load calls
    fetchSystemInfo();
    fetchHealthStats();
    fetchStocks();
    fetchSchedule();
});
