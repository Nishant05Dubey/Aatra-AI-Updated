document.addEventListener('DOMContentLoaded', function() {
    // --- MOCK DATA ---
    const threatsData = [
        { id: 1, title: 'Fabricated Stories About Indian Achievements', region: 'Mumbai', confidence: 79, type: 'high', time: '6:34:12 PM', platform: 'Twitter', description: 'Coordinated network spreading false information about Indian technological achievements and space missions.' },
        { id: 2, title: 'Separatist Content Distribution Network', region: 'Chennai', confidence: 92, type: 'critical', time: '6:34:15 PM', platform: 'Facebook', description: 'Large-scale distribution of separatist content targeting specific regions with inflammatory messaging.' },
        { id: 3, title: 'Coordinated Inauthentic Behavior', region: 'Punjab', confidence: 88, type: 'high', time: '6:32:05 PM', platform: 'WhatsApp', description: 'Bot network detected spreading coordinated messaging across multiple groups simultaneously.' },
        { id: 4, title: 'Deepfake Media Shared', region: 'Bangalore', confidence: 91, type: 'critical', time: '6:31:55 PM', platform: 'Instagram', description: 'AI-generated deepfake videos of political figures spreading false statements and inflammatory content.' },
        { id: 5, title: 'Anti-National Propaganda Botnet', region: 'Kolkata', confidence: 85, type: 'high', time: '6:30:15 PM', platform: 'Twitter', description: 'Automated bot network pushing anti-national propaganda with sophisticated coordination patterns.' },
        { id: 6, title: 'Provocative Memes Circulation', region: 'Online', confidence: 72, type: 'low', time: '6:29:40 PM', platform: 'Reddit', description: 'Circulation of provocative memes designed to incite communal tensions and spread disinformation.' },
    ];

    // --- ELEMENT SELECTORS ---
    const threatList = document.getElementById('threat-list');
    const tabBtns = document.querySelectorAll('.tab-btn');
    const navLinks = document.querySelectorAll('.nav-link');
    const pageSections = document.querySelectorAll('.page-section');
    const analyzeBtn = document.getElementById('analyzeBtn');
    const textContent = document.getElementById('textContent');
    const analysisResult = document.getElementById('analysisResult');
    const summarizeBtn = document.getElementById('summarizeBtn');
    const summaryResult = document.getElementById('summaryResult');
    
    // Modal elements
    const reportModal = document.getElementById('reportModal');
    const closeModal = document.getElementById('closeModal');
    const cancelReport = document.getElementById('cancelReport');
    const submitReport = document.getElementById('submitReport');
    const selectedThreatInfo = document.getElementById('selectedThreatInfo');
    const additionalDetails = document.getElementById('additionalDetails');
    const reporterContact = document.getElementById('reporterContact');
    const urgentReport = document.getElementById('urgentReport');
    
    let currentSelectedThreat = null;

    // --- GEMINI API INTEGRATION ---
    const apiKey = "AIzaSyB3Dmh8MGD8VmHuz1nikFAhjVmgpOzNeds"; // This will be handled by the execution environment. Do not add a key here.
    const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key=${apiKey}`;

    async function callGeminiAPI(payload, maxRetries = 3) {
        let attempt = 0;
        while (attempt < maxRetries) {
            try {
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                
                const result = await response.json();
                const candidate = result.candidates?.[0];
                if (candidate && candidate.content?.parts?.[0]?.text) {
                    return candidate.content.parts[0].text;
                } else {
                    throw new Error("Invalid response structure from API");
                }
            } catch (error) {
                attempt++;
                if (attempt >= maxRetries) {
                     console.error("Gemini API call failed after multiple retries:", error);
                     return "Error: Could not get a response from the AI. Please try again later.";
                }
                const delay = Math.pow(2, attempt) * 1000;
                await new Promise(res => setTimeout(res, delay));
            }
        }
    }
    
    async function analyzeContentWithGemini(content) {
        analysisResult.innerHTML = '<div class="flex flex-col items-center gap-2"><span class="loader"></span><p>AI is analyzing...</p></div>';
        
        const systemPrompt = `You are a cybersecurity analyst for "Astra AI," specializing in detecting online threats to India's national security. Analyze the provided text for anti-India sentiment, disinformation, hate speech, or propaganda.
        
        Your response must be a JSON object with the following structure:
        {
          "riskLevel": "...", // e.g., "Low Risk", "Moderate Risk", "High Risk", "Critical Risk"
          "confidence": ..., // A number between 0 and 100
          "summary": "...", // A one-paragraph summary of your findings.
          "indicators": ["...", "...", "..."], // A list of 3-4 key detected indicators.
          "recommendedAction": "..." // A concise recommended action.
        }`;

        const payload = {
            contents: [{ parts: [{ text: content }] }],
            systemInstruction: { parts: [{ text: systemPrompt }] },
            generationConfig: {
                responseMimeType: "application/json",
            }
        };

        const responseText = await callGeminiAPI(payload);
        
        try {
            const data = JSON.parse(responseText);
            
            let borderColor, textColor, shieldSVG;
            switch(data.riskLevel.toLowerCase()){
                case 'critical risk':
                    borderColor = 'border-red-500/50'; textColor = 'text-red-400';
                    shieldSVG = `<svg class="w-6 h-6 mr-2 ${textColor}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>`;
                    break;
                case 'high risk':
                    borderColor = 'border-yellow-500/50'; textColor = 'text-yellow-400';
                     shieldSVG = `<svg class="w-6 h-6 mr-2 ${textColor}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path></svg>`;
                    break;
                case 'moderate risk':
                     borderColor = 'border-blue-500/50'; textColor = 'text-blue-400';
                     shieldSVG = `<svg class="w-6 h-6 mr-2 ${textColor}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>`;
                    break;
                default: // Low Risk
                    borderColor = 'border-green-500/50'; textColor = 'text-green-400';
                     shieldSVG = `<svg class="w-6 h-6 mr-2 ${textColor}" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>`;
                    break;
            }
            
            const indicatorsHtml = data.indicators.map(indicator => `
                <div class="bg-gray-800/60 p-2.5 rounded-md text-sm flex items-center">
                   <span class="text-blue-400 mr-2">●</span> ${indicator}
                </div>
            `).join('');

            const resultHtml = `
                <div class="space-y-4 text-left w-full">
                    <div class="p-4 rounded-lg bg-gray-800/50 border ${borderColor}">
                        <div class="flex items-center">
                            ${shieldSVG}
                            <div>
                                <h4 class="font-bold ${textColor}">${data.riskLevel} Content</h4>
                                <p class="text-xs text-gray-400">Confidence: ${data.confidence}%</p>
                            </div>
                        </div>
                        <div class="w-full bg-gray-700 rounded-full h-1.5 my-2"><div class="${textColor.replace('text','bg')} h-1.5 rounded-full" style="width: ${data.confidence}%"></div></div>
                        <p class="text-sm text-gray-300">${data.summary}</p>
                    </div>
                    
                    <div>
                        <h5 class="text-gray-400 text-sm font-semibold mb-2">Detected Indicators</h5>
                        <div class="space-y-2">${indicatorsHtml}</div>
                    </div>

                    <div>
                        <h5 class="text-gray-400 text-sm font-semibold mb-2">Recommended Action</h5>
                        <div class="bg-red-900/40 border border-red-500/30 p-3 rounded-md">
                            <p class="text-sm text-red-300">${data.recommendedAction}</p>
                        </div>
                    </div>
                    
                    <div class="flex justify-between items-center text-xs text-gray-500 pt-2">
                        <span>Analysis Time: ${new Date().toLocaleTimeString()}</span>
                        <span>Model Version: v2.4.1</span>
                    </div>
                </div>`;
            analysisResult.innerHTML = resultHtml;

        } catch (error) {
            console.error("Failed to parse Gemini response:", error);
            analysisResult.innerHTML = `<p class="text-red-400">Error: The AI returned an invalid response. Please check the console for details.</p>`;
        }
    }

    async function summarizeAlertsWithGemini() {
        summaryResult.classList.remove('hidden');
        summaryResult.innerHTML = '<div class="flex items-center gap-2"><span class="loader" style="width:24px; height:24px; border-width: 3px;"></span><p>AI is generating a summary...</p></div>';

        const threatTitles = threatsData.map(t => t.title).join(', ');
        const userQuery = `Summarize the current threat landscape based on these active alert titles: ${threatTitles}. Provide a concise, one-paragraph summary.`;

        const payload = {
            contents: [{ parts: [{ text: userQuery }] }]
        };

        const summaryText = await callGeminiAPI(payload);
        summaryResult.innerHTML = summaryText;
    }

    // --- REPORTING FUNCTIONS ---
    function openReportModal(threat) {
        currentSelectedThreat = threat;
        
        // Populate threat information
        selectedThreatInfo.innerHTML = `
            <div class="space-y-2">
                <h4 class="font-bold text-white">${threat.title}</h4>
                <div class="grid grid-cols-2 gap-4 text-sm">
                    <p><span class="text-gray-400">Platform:</span> ${threat.platform}</p>
                    <p><span class="text-gray-400">Region:</span> ${threat.region}</p>
                    <p><span class="text-gray-400">Confidence:</span> ${threat.confidence}%</p>
                    <p><span class="text-gray-400">Detected:</span> ${threat.time}</p>
                </div>
                <p class="text-sm text-gray-300 mt-2">${threat.description}</p>
            </div>
        `;
        
        reportModal.classList.remove('hidden');
    }

    function closeReportModal() {
        reportModal.classList.add('hidden');
        currentSelectedThreat = null;
        additionalDetails.value = '';
        reporterContact.value = '';
        urgentReport.checked = false;
    }

    function submitThreatReport() {
        if (!currentSelectedThreat) return;

        const reportData = {
            threat: currentSelectedThreat,
            additionalDetails: additionalDetails.value,
            reporterContact: reporterContact.value,
            urgent: urgentReport.checked,
            timestamp: new Date().toISOString(),
            source: 'Astra AI - AICMS'
        };

        // Create report content
        const reportContent = `
CYBERCRIME REPORT - Astra AI AICMS
=====================================

THREAT DETAILS:
Title: ${reportData.threat.title}
Platform: ${reportData.threat.platform}
Region: ${reportData.threat.region}
Confidence Level: ${reportData.threat.confidence}%
Detection Time: ${reportData.threat.time}
Threat Type: ${reportData.threat.type.toUpperCase()}

DESCRIPTION:
${reportData.threat.description}

ADDITIONAL DETAILS:
${reportData.additionalDetails || 'None provided'}

PRIORITY: ${reportData.urgent ? 'URGENT' : 'Normal'}
REPORTED BY: ${reportData.reporterContact || 'Anonymous'}
REPORT TIME: ${new Date().toLocaleString()}
SOURCE SYSTEM: Astra AI - Anti-India Campaign Monitoring System (AICMS)

Note: This report was automatically generated by Astra AI's cybersecurity monitoring system. 
Please investigate the above-mentioned threat and take appropriate action.
        `.trim();

        // Open cybercrime.gov.in in a new tab with pre-filled data
        const cybercrimeUrl = 'https://cybercrime.gov.in/Webform/report_abuse_social_media.aspx';
        const newWindow = window.open(cybercrimeUrl, '_blank');
        
        // Copy report to clipboard for easy pasting
        navigator.clipboard.writeText(reportContent).then(() => {
            console.log('Report content copied to clipboard');
        });

        // Show success message
        selectedThreatInfo.innerHTML = `
            <div class="bg-green-900/40 border border-green-500/30 p-4 rounded-lg">
                <div class="flex items-center mb-2">
                    <svg class="w-5 h-5 text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                    <h4 class="font-bold text-green-400">Report Prepared</h4>
                </div>
                <p class="text-sm text-green-300">
                    • Cybercrime portal opened in new tab<br>
                    • Report details copied to clipboard<br>
                    • Please paste the report content when filing your complaint
                </p>
            </div>
        `;

        // Update button to show completion
        submitReport.innerHTML = '✅ Redirected to Cybercrime Portal';
        submitReport.disabled = true;
        submitReport.classList.add('bg-green-600');

        // Auto-close modal after 3 seconds
        setTimeout(() => {
            closeReportModal();
            submitReport.innerHTML = `
                <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"></path>
                </svg>
                Report to Cybercrime.gov.in
            `;
            submitReport.disabled = false;
            submitReport.classList.remove('bg-green-600');
        }, 3000);
    }

    // --- UI LOGIC ---
    function renderThreats(filter = 'all') {
        threatList.innerHTML = '';
        const filteredThreats = threatsData.filter(threat => filter === 'all' || threat.type === filter);
        
        if (filteredThreats.length === 0) {
            threatList.innerHTML = '<p class="text-gray-500 text-center">No threats match this category.</p>';
            return;
        }

        filteredThreats.forEach(threat => {
            let typeColorClass, typeBgColorClass;
            switch (threat.type) {
                case 'critical':
                    typeColorClass = 'text-red-400';
                    typeBgColorClass = 'bg-red-500/10';
                    break;
                case 'high':
                    typeColorClass = 'text-yellow-400';
                    typeBgColorClass = 'bg-yellow-500/10';
                    break;
                case 'low':
                    typeColorClass = 'text-green-400';
                    typeBgColorClass = 'bg-green-500/10';
                    break;
                default:
                    typeColorClass = 'text-gray-400';
                    typeBgColorClass = 'bg-gray-500/10';
            }

            const threatElement = document.createElement('div');
            threatElement.className = `threat-item flex items-center justify-between p-3 rounded-lg ${typeBgColorClass} cursor-pointer animate-fade-in`;
            threatElement.innerHTML = `
                <div class="flex-1">
                    <p class="font-semibold text-white">${threat.title}</p>
                    <p class="text-sm text-gray-400">${threat.platform} • ${threat.region} • ${threat.time}</p>
                </div>
                <div class="flex items-center space-x-3">
                    <div class="text-right">
                        <span class="font-bold ${typeColorClass}">${threat.type.toUpperCase()}</span>
                        <p class="text-xs text-gray-500">Confidence: ${threat.confidence}%</p>
                    </div>
                    <button class="report-btn bg-red-600 hover:bg-red-700 text-white text-xs font-bold py-1 px-3 rounded transition duration-300" data-threat-id="${threat.id}">
                        Report
                    </button>
                </div>
            `;
            
            // Add click event for reporting
            const reportBtn = threatElement.querySelector('.report-btn');
            reportBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                openReportModal(threat);
            });
            
            threatList.appendChild(threatElement);
        });
    }

    function updateTime() {
        const now = new Date();
        const timeString = now.toLocaleString('en-US', { timeStyle: 'medium' });
        document.getElementById('currentTime').innerHTML = `${timeString}<br>THREAT LEVEL: <span class="text-yellow-400 font-bold">ELEVATED</span>`;
        document.getElementById('lastUpdate').textContent = `Last update: ${now.toLocaleTimeString()}`;
    }

    // --- EVENT LISTENERS ---
    
    // Modal event listeners
    closeModal.addEventListener('click', closeReportModal);
    cancelReport.addEventListener('click', closeReportModal);
    submitReport.addEventListener('click', submitThreatReport);
    
    // Close modal when clicking backdrop
    reportModal.addEventListener('click', (e) => {
        if (e.target === reportModal) {
            closeReportModal();
        }
    });

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active-tab'));
            btn.classList.add('active-tab');
            renderThreats(btn.dataset.filter);
        });
    });

    navLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);

            navLinks.forEach(l => l.classList.remove('active-link'));
            link.classList.add('active-link');

            pageSections.forEach(section => {
                if (section.id === targetId) {
                    section.classList.remove('hidden');
                } else {
                    section.classList.add('hidden');
                }
            });
        });
    });

    analyzeBtn.addEventListener('click', () => {
        if (textContent.value.trim()) {
            analyzeContentWithGemini(textContent.value.trim());
        } else {
            analysisResult.innerHTML = '<p class="text-yellow-400">Please enter some text to analyze.</p>';
        }
    });

    summarizeBtn.addEventListener('click', summarizeAlertsWithGemini);

    // --- INITIALIZATION ---
    renderThreats('all');
    updateTime();
    setInterval(updateTime, 1000);
});
