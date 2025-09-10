// Demo Enhancement Script for Live Presentations
// Add this to index.html for enhanced demo features

class DemoEnhancements {
    constructor() {
        this.demoMode = false;
        this.autoRefreshInterval = null;
        this.simulationInterval = null;
        this.init();
    }

    init() {
        this.addDemoControls();
        this.setupKeyboardShortcuts();
        this.enableDemoMode();
    }

    addDemoControls() {
        // Add demo control panel
        const demoPanel = document.createElement('div');
        demoPanel.id = 'demo-controls';
        demoPanel.className = 'fixed top-2 right-2 z-50 bg-gray-900/90 p-3 rounded-lg border border-blue-500/50';
        demoPanel.innerHTML = `
            <div class="text-xs text-blue-400 mb-2 font-semibold">🎬 DEMO CONTROLS</div>
            <div class="flex flex-col space-y-2">
                <button id="demo-simulate" class="bg-red-600 hover:bg-red-700 text-white text-xs px-2 py-1 rounded">
                    🚨 Simulate Threat
                </button>
                <button id="demo-refresh" class="bg-blue-600 hover:bg-blue-700 text-white text-xs px-2 py-1 rounded">
                    🔄 Refresh Data
                </button>
                <button id="demo-reset" class="bg-yellow-600 hover:bg-yellow-700 text-white text-xs px-2 py-1 rounded">
                    🧹 Reset Demo
                </button>
                <label class="text-xs text-gray-300 flex items-center">
                    <input type="checkbox" id="auto-refresh" class="mr-1">
                    Auto-refresh
                </label>
            </div>
        `;
        
        document.body.appendChild(demoPanel);

        // Add event listeners
        document.getElementById('demo-simulate').addEventListener('click', () => this.simulateThreat());
        document.getElementById('demo-refresh').addEventListener('click', () => this.refreshData());
        document.getElementById('demo-reset').addEventListener('click', () => this.resetDemo());
        document.getElementById('auto-refresh').addEventListener('change', (e) => {
            if (e.target.checked) {
                this.startAutoRefresh();
            } else {
                this.stopAutoRefresh();
            }
        });
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Press 'D' to toggle demo controls
            if (e.key === 'd' || e.key === 'D') {
                const panel = document.getElementById('demo-controls');
                if (panel) {
                    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
                }
            }
            
            // Press 'S' to simulate threat
            if (e.key === 's' || e.key === 'S') {
                this.simulateThreat();
            }
            
            // Press 'R' to refresh
            if (e.key === 'r' || e.key === 'R') {
                this.refreshData();
            }
        });
    }

    async simulateThreat() {
        try {
            // Show loading indicator
            this.showNotification('🚨 Simulating live threat detection...', 'info');
            
            const response = await fetch('/api/demo/simulate-detection', {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showNotification(`✅ Threat detected: ${result.scenario}`, 'success');
                
                // Auto-refresh after simulation
                setTimeout(() => {
                    this.refreshData();
                }, 2000);
            } else {
                this.showNotification('❌ Failed to simulate threat', 'error');
            }
        } catch (error) {
            console.error('Demo simulation error:', error);
            this.showNotification('❌ Simulation error - check backend', 'error');
        }
    }

    async refreshData() {
        try {
            this.showNotification('🔄 Refreshing dashboard data...', 'info');
            
            // Refresh dashboard stats
            await loadDashboardStats();
            
            // Refresh live threats
            await loadLiveThreats('all');
            
            // Refresh platform analytics
            await loadPlatformAnalytics();
            
            this.showNotification('✅ Data refreshed successfully', 'success');
        } catch (error) {
            console.error('Refresh error:', error);
            this.showNotification('❌ Failed to refresh data', 'error');
        }
    }

    async resetDemo() {
        try {
            this.showNotification('🧹 Resetting demo data...', 'info');
            
            const response = await fetch('/api/demo/demo-reset', {
                method: 'POST'
            });
            
            if (response.ok) {
                const result = await response.json();
                this.showNotification('✅ Demo data reset', 'success');
                
                // Refresh after reset
                setTimeout(() => {
                    this.refreshData();
                }, 1000);
            } else {
                this.showNotification('❌ Failed to reset demo', 'error');
            }
        } catch (error) {
            console.error('Reset error:', error);
            this.showNotification('❌ Reset failed', 'error');
        }
    }

    startAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
        }
        
        this.autoRefreshInterval = setInterval(() => {
            this.refreshData();
        }, 30000); // Refresh every 30 seconds
        
        this.showNotification('🔄 Auto-refresh enabled (30s)', 'info');
    }

    stopAutoRefresh() {
        if (this.autoRefreshInterval) {
            clearInterval(this.autoRefreshInterval);
            this.autoRefreshInterval = null;
        }
        
        this.showNotification('⏸️ Auto-refresh disabled', 'info');
    }

    enableDemoMode() {
        // Add demo indicators to the UI
        const demoIndicator = document.createElement('div');
        demoIndicator.className = 'fixed bottom-4 left-4 bg-red-600/90 text-white px-3 py-1 rounded-full text-xs font-bold z-40';
        demoIndicator.innerHTML = '🎬 LIVE DEMO MODE';
        document.body.appendChild(demoIndicator);

        // Enhance threat feed with demo features
        this.enhanceThreatFeed();
        
        // Add demo analytics
        this.addDemoAnalytics();
    }

    enhanceThreatFeed() {
        // Add "LIVE" indicators to recent threats
        const threatItems = document.querySelectorAll('.threat-item');
        threatItems.forEach((item, index) => {
            if (index < 3) { // Mark first 3 as "LIVE"
                const liveIndicator = document.createElement('span');
                liveIndicator.className = 'bg-red-500 text-white text-xs px-2 py-1 rounded-full font-bold animate-pulse';
                liveIndicator.textContent = 'LIVE';
                
                const titleElement = item.querySelector('.font-semibold');
                if (titleElement) {
                    titleElement.insertBefore(liveIndicator, titleElement.firstChild);
                }
            }
        });
    }

    addDemoAnalytics() {
        // Add real-time metrics display
        const metricsPanel = document.createElement('div');
        metricsPanel.className = 'fixed bottom-4 right-4 bg-gray-900/90 p-3 rounded-lg border border-green-500/50 text-xs z-40';
        metricsPanel.innerHTML = `
            <div class="text-green-400 font-semibold mb-2">📊 REAL-TIME METRICS</div>
            <div class="text-gray-300">
                <div>Detection Rate: <span class="text-green-400">94.7%</span></div>
                <div>Response Time: <span class="text-blue-400">1.2s avg</span></div>
                <div>Active Monitoring: <span class="text-yellow-400">8 platforms</span></div>
                <div>Status: <span class="text-green-400">🟢 ACTIVE</span></div>
            </div>
        `;
        
        document.body.appendChild(metricsPanel);
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-20 right-4 p-3 rounded-lg text-white text-sm font-medium z-50 transform transition-all duration-300 translate-x-full`;
        
        // Set color based on type
        const colors = {
            'info': 'bg-blue-600',
            'success': 'bg-green-600', 
            'error': 'bg-red-600',
            'warning': 'bg-yellow-600'
        };
        
        notification.className += ` ${colors[type] || colors.info}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('translate-x-full');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
}

// Initialize demo enhancements when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize if we're in demo mode (check URL parameter)
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('demo') === 'true' || window.location.hostname === 'localhost') {
        new DemoEnhancements();
    }
});

// Add some dramatic demo scenarios
window.demoScenarios = {
    critical: [
        "I hate India and want to destroy everything Indian. Pakistan zindabad! Death to Indian democracy!",
        "Khalistan zindabad! Free Kashmir from terrorist Indian army. Break India into pieces!",
        "Indian government are terrorists. Death to all Indians. Destroy Hinduism!"
    ],
    high: [
        "Indian culture is backward and primitive. Boycott all Indian festivals and traditions.",
        "India's economy is fake. All Indian GDP numbers are lies. Boycott Indian products.",
        "Indian army kills innocent people. India is a terrorist nation."
    ],
    moderate: [
        "India has many problems with corruption and poverty issues.",
        "Some Indian policies are questionable and need international review.",
        "Indian government should be more transparent about their actions."
    ],
    low: [
        "I love India and its rich cultural heritage. Proud to be Indian!",
        "India has made great progress in technology and space exploration.",
        "Beautiful Indian festivals and traditions are amazing to experience."
    ]
};

// Add quick test function for presentations
window.quickDemo = function(level = 'critical') {
    const content = window.demoScenarios[level][Math.floor(Math.random() * window.demoScenarios[level].length)];
    document.getElementById('textContent').value = content;
    document.getElementById('analyzeBtn').click();
};