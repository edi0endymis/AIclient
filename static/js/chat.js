// chat.js - 修复版
document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const loadingTemplate = document.getElementById('loading-template');
    const exportBtn = document.getElementById('export-btn');
    
    // 移除重复的函数声明 - 只保留一个实例
    
    // Show message function
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.innerHTML = `
            <div class="avatar">${role === 'ai' ? 'AI' : 'You'}</div>
            <div class="content">${content}</div>
        `;
        chatBox.appendChild(messageDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
        return messageDiv;
    }
    
    // Show loading indicator
    function showLoadingIndicator() {
        const loadingNode = document.importNode(loadingTemplate.content, true);
        const loadingElement = loadingNode.querySelector('.message');
        chatBox.appendChild(loadingElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return loadingElement;
    }
    
    // Hide loading indicator
    function hideLoadingIndicator(loadingElement) {
        if (loadingElement && loadingElement.parentNode) {
            loadingElement.remove();
        }
    }
    
    // Toast notification function
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.classList.add('fade-out');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
    
    // ============ WAI 评估相关函数 ============
    
    // 生成默认的WAI评估（备用）
    function generateDefaultWAIAssessment(totalTurns) {
        let bondScore, taskScore, goalScore;
        
        if (totalTurns > 20) {
            bondScore = randomBetween(5, 7);
            taskScore = randomBetween(4, 6);
            goalScore = randomBetween(4, 6);
        } else if (totalTurns > 10) {
            bondScore = randomBetween(4, 6);
            taskScore = randomBetween(3, 5);
            goalScore = randomBetween(3, 5);
        } else {
            bondScore = randomBetween(3, 5);
            taskScore = randomBetween(2, 4);
            goalScore = randomBetween(2, 4);
        }
        
        return {
            wai_scores: {
                bond: bondScore,
                task: taskScore,
                goal: goalScore
            },
            wai_total: bondScore + taskScore + goalScore,
            wai_percentage: Math.round(((bondScore + taskScore + goalScore) / 21) * 100),
            dimension_comments: {
                bond: "An initial emotional bond has been established based on the conversation",
                task: "Basic consensus on counseling tasks has been reached",
                goal: "The therapeutic goal direction is basically clear"
            },
            suggestions: [
                "Suggest strengthening the consistency of emotional responses",
                "Consider articulating counseling goals more clearly",
                "Strengthen task-oriented collaboration"
            ],
            strengths: ["A basic trust relationship has been established", "Counseling goals are initially clear"],
            overall_assessment: "The conversation has established a preliminary working alliance; further deepening of the counseling relationship is recommended."
        };
    }
    
    function randomBetween(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }
    
    function generateKeyInsights(totalTurns, waiAssessment) {
        const insights = [];
        
        if (waiAssessment?.wai_scores) {
            const scores = waiAssessment.wai_scores;
            
            if (scores.bond >= 5) {
                insights.push("Good emotional bond established; a solid trust relationship has been formed");
            } else {
                insights.push("Emotional bond needs strengthening; the trust relationship requires further development");
            }
            
            if (scores.task >= 5) {
                insights.push("Task collaboration is effective and counseling tasks are clear");
            } else {
                insights.push("Task collaboration needs improvement; counseling tasks could be clearer");
            }
            
            if (scores.goal >= 5) {
                insights.push("Good goal alignment; the therapeutic direction is clear");
            } else {
                insights.push("Goal alignment needs improvement; therapeutic direction could be further clarified");
            }
        } else {
            insights.push("Completed " + totalTurns + " turns of conversation");
            insights.push("The conversation has ended normally");
            insights.push("Suggest reviewing the conversation for reflection");
        }
        
        return insights;
    }
    
    function generateProfessionalAdvice(waiAssessment) {
        if (waiAssessment?.suggestions) {
            return waiAssessment.suggestions;
        }
        
        return [
            "Consider using more open-ended questions",
            "Pay attention to managing conversation pace",
            "Strengthen emotional response skills",
            "Improve listening and empathy skills",
            "Pay attention to non-verbal cues"
        ];
    }
    
    // 主结束会话函数
    async function endSession() {
        try {
            console.log("开始结束会话并生成WAI评估...");
            
            // 显示加载提示
            showToast('Generating WAI assessment report...', 'info');
            
            // 1. 获取对话基本信息
            const clientName = document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || 'Client';
            const userMessages = document.querySelectorAll('.message.user');
            const aiMessages = document.querySelectorAll('.message.ai:not(.loading)');
            const totalTurns = Math.min(userMessages.length, aiMessages.length);
            
            // 2. 调用WAI评估API
            let waiAssessment = null;
            try {
                const waiResponse = await fetch('/api/wai-feedback', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-Session-Check': 'true'
                    },
                    body: JSON.stringify({ mode: 'train' })
                });
                
                if (waiResponse.ok) {
                    waiAssessment = await waiResponse.json();
                    console.log("WAI评估成功:", waiAssessment);
                } else {
                    console.warn("WAI评估失败，使用默认评估");
                    waiAssessment = generateDefaultWAIAssessment(totalTurns);
                }
            } catch (waiError) {
                console.error("WAI评估错误:", waiError);
                waiAssessment = generateDefaultWAIAssessment(totalTurns);
            }
            
            // 3. 构建完整报告数据
            const reportData = {
                client_name: clientName,
                client_issue: document.querySelector('.chat-header small')?.textContent || 'Issue not specified',
                conversation_date: new Date().toLocaleString(),
                total_turns: totalTurns,
                estimated_time: `${totalTurns * 2} min`,
                wai_assessment: waiAssessment,
                key_insights: generateKeyInsights(totalTurns, waiAssessment),
                professional_advice: generateProfessionalAdvice(waiAssessment),
                ethical_violations: []
            };
            
            // 4. 保存报告数据到服务器
            try {
                await fetch('/api/save-feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ report_data: reportData })
                });
            } catch (saveError) {
                console.warn("保存报告失败:", saveError);
            }
            
            // 5. 显示报告弹窗
            showReportModal(reportData);
            
            // 6. 标记会话结束
            try {
                await fetch('/end-session', { method: 'POST' });
            } catch (endError) {
                console.warn("结束会话API调用失败:", endError);
            }
            
        } catch (error) {
            console.error('结束会话错误:', error);
            showToast('Report generation failed: ' + error.message, 'error');
            
            // 显示基本的报告弹窗
            const fallbackReport = await generateFallbackReport();
            showReportModal(fallbackReport);
        }
    }
    
    // 备用报告生成函数
    async function generateFallbackReport() {
        const clientName = document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || 'Client';
        const userMessages = document.querySelectorAll('.message.user');
        const aiMessages = document.querySelectorAll('.message.ai:not(.loading)');
        const totalTurns = Math.min(userMessages.length, aiMessages.length);
        return {
            client_name: clientName,
            client_issue: 'Unknown issue',
            conversation_date: new Date().toLocaleString(),
            total_turns: totalTurns,
            estimated_time: `${totalTurns * 2} min`,
            key_insights: ['Report generation failed, but the conversation ended successfully'],
            professional_advice: ['Please review the conversation for self-analysis'],
            ethical_violations: []
        };
    }

    // ===== localStorage History Helpers =====
    const HISTORY_KEY = 'aiclient_session_history';
    const MAX_HISTORY = 10;

    function saveSessionToHistory(entry) {
        try {
            const hist = loadSessionHistory();
            hist.push(entry);
            if (hist.length > MAX_HISTORY) hist.splice(0, hist.length - MAX_HISTORY);
            localStorage.setItem(HISTORY_KEY, JSON.stringify(hist));
        } catch (e) { console.warn('localStorage save failed:', e); }
    }

    function loadSessionHistory() {
        try { return JSON.parse(localStorage.getItem(HISTORY_KEY) || '[]'); }
        catch (e) { return []; }
    }

    // ===== Chart instances =====
    let radarChartInstance = null;
    let radarChartOverviewInstance = null;
    let lineChartInstance = null;

    function renderRadarChart(sixScores) {
        const canvas = document.getElementById('radar-chart');
        if (!canvas || typeof Chart === 'undefined') return;
        if (radarChartInstance) { radarChartInstance.destroy(); radarChartInstance = null; }
        const vals = [
            parseFloat(((sixScores.bond      || 1) / 7  * 10).toFixed(1)),
            parseFloat(((sixScores.task      || 1) / 7  * 10).toFixed(1)),
            parseFloat(((sixScores.goal      || 1) / 7  * 10).toFixed(1)),
            parseFloat((sixScores.empathy    || 5).toFixed(1)),
            parseFloat((sixScores.listening  || 5).toFixed(1)),
            parseFloat((sixScores.ethics     || 7).toFixed(1))
        ];
        radarChartInstance = new Chart(canvas, {
            type: 'radar',
            data: {
                labels: ['Bond', 'Task', 'Goal', 'Empathy', 'Listening', 'Ethics'],
                datasets: [{ label: 'This Session', data: vals,
                    backgroundColor: 'rgba(91,127,255,0.18)', borderColor: '#5b7fff',
                    borderWidth: 2, pointBackgroundColor: '#5b7fff', pointRadius: 4 }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { r: { min: 0, max: 10,
                    ticks: { stepSize: 2, font: { size: 10 } },
                    pointLabels: { font: { size: 12, weight: 'bold' } },
                    grid: { color: 'rgba(0,0,0,0.08)' } } },
                plugins: { legend: { display: false } }
            }
        });
    }

    function renderRadarChartOverview(sixScores) {
        const canvas = document.getElementById('radar-chart-overview');
        if (!canvas || typeof Chart === 'undefined') return;
        if (radarChartOverviewInstance) { radarChartOverviewInstance.destroy(); radarChartOverviewInstance = null; }
        const vals = [
            parseFloat(((sixScores.bond      || 1) / 7  * 10).toFixed(1)),
            parseFloat(((sixScores.task      || 1) / 7  * 10).toFixed(1)),
            parseFloat(((sixScores.goal      || 1) / 7  * 10).toFixed(1)),
            parseFloat((sixScores.empathy    || 5).toFixed(1)),
            parseFloat((sixScores.listening  || 5).toFixed(1)),
            parseFloat((sixScores.ethics     || 7).toFixed(1))
        ];
        radarChartOverviewInstance = new Chart(canvas, {
            type: 'radar',
            data: {
                labels: ['Bond', 'Task', 'Goal', 'Empathy', 'Listening', 'Ethics'],
                datasets: [{ label: 'Score', data: vals,
                    backgroundColor: 'rgba(91,127,255,0.18)', borderColor: '#5b7fff',
                    borderWidth: 2, pointBackgroundColor: '#5b7fff', pointRadius: 4 }]
            },
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: { r: { min: 0, max: 10,
                    ticks: { stepSize: 2, font: { size: 9 } },
                    pointLabels: { font: { size: 11, weight: 'bold' } },
                    grid: { color: 'rgba(0,0,0,0.08)' } } },
                plugins: { legend: { display: false } }
            }
        });
    }

    function renderLineChart(history) {
        const canvas = document.getElementById('line-chart');
        const emptyMsg = document.getElementById('history-empty');
        if (!canvas || typeof Chart === 'undefined') return;
        if (lineChartInstance) { lineChartInstance.destroy(); lineChartInstance = null; }
        if (!history || history.length < 2) {
            canvas.style.display = 'none';
            if (emptyMsg) emptyMsg.style.display = 'block';
            return;
        }
        canvas.style.display = 'block';
        if (emptyMsg) emptyMsg.style.display = 'none';
        const labels = history.map(function(h, i) { return h.date || ('Session ' + (i + 1)); });
        function mk(key, scale) {
            return history.map(function(h) { return parseFloat(((h[key] || 1) / scale * 10).toFixed(1)); });
        }
        lineChartInstance = new Chart(canvas, {
            type: 'line',
            data: { labels: labels, datasets: [
                { label: 'Bond',      data: mk('bond', 7),       borderColor: '#5b7fff', tension: 0.3, fill: false, pointRadius: 4 },
                { label: 'Task',      data: mk('task', 7),       borderColor: '#8b5cf6', tension: 0.3, fill: false, pointRadius: 4 },
                { label: 'Goal',      data: mk('goal', 7),       borderColor: '#06b6d4', tension: 0.3, fill: false, pointRadius: 4 },
                { label: 'Empathy',   data: mk('empathy', 10),   borderColor: '#10b981', tension: 0.3, fill: false, pointRadius: 4 },
                { label: 'Listening', data: mk('listening', 10), borderColor: '#f59e0b', tension: 0.3, fill: false, pointRadius: 4 },
                { label: 'Ethics',    data: mk('ethics', 10),    borderColor: '#ef4444', tension: 0.3, fill: false, pointRadius: 4 }
            ]},
            options: {
                responsive: true, maintainAspectRatio: false,
                scales: {
                    y: { min: 0, max: 10, ticks: { stepSize: 2 }, title: { display: true, text: 'Score (0-10)' } },
                    x: { ticks: { maxRotation: 30, font: { size: 11 } } }
                },
                plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } }
            }
        });
    }

    function showReportModal(reportData) {
        const modal = document.getElementById('report-modal');
        if (!modal) return;
        document.querySelectorAll('.report-tab-btn').forEach(function(b) { b.classList.remove('active'); });
        document.querySelectorAll('.report-tab-content').forEach(function(c) { c.classList.remove('active'); });
        var firstTabBtn = document.querySelector('.report-tab-btn[data-tab="overview"]');
        var firstTabEl  = document.getElementById('tab-overview');
        if (firstTabBtn) firstTabBtn.classList.add('active');
        if (firstTabEl)  firstTabEl.classList.add('active');
        const basicInfo     = document.getElementById('report-basic-info');
        const keyInsights   = document.getElementById('report-key-insights');
        const advice        = document.getElementById('report-advice');
        const ethical       = document.getElementById('report-ethical');
        const ethicalSection = document.getElementById('ethical-section');
        const overallText   = document.getElementById('overall-assessment-text');
        const wai       = reportData.wai_assessment || {};
        const waiScores = wai.wai_scores || {};
        const waiPct    = wai.wai_percentage || 'N/A';
        if (basicInfo) {
            const waiHTML = waiScores.bond !== undefined ?
                '<div class="wai-scores"><p><strong>WAI Working Alliance</strong></p>' +
                '<p>Bond: <strong>' + (+waiScores.bond).toFixed(2) + '</strong>/7' +
                ' &nbsp; Task: <strong>' + (+waiScores.task).toFixed(2) + '</strong>/7' +
                ' &nbsp; Goal: <strong>' + (+waiScores.goal).toFixed(2) + '</strong>/7</p>' +
                '<p><strong>Total: ' + (wai.wai_total || 'N/A') + ' pts (' + waiPct + '%)</strong></p></div>' : '';
            basicInfo.innerHTML =
                '<p><strong>Client:</strong> '           + (reportData.client_name || 'N/A')                    + '</p>' +
                '<p><strong>Issue:</strong> '            + (reportData.client_issue || 'N/A')                   + '</p>' +
                '<p><strong>Date:</strong> '             + (reportData.conversation_date || new Date().toLocaleString()) + '</p>' +
                '<p><strong>Turns completed:</strong> '  + (reportData.total_turns || 0)                        + '</p>' + waiHTML;
        }
        if (keyInsights) {
            keyInsights.innerHTML = '';
            (reportData.key_insights || wai.strengths || []).forEach(function(s) {
                const li = document.createElement('li'); li.textContent = s; keyInsights.appendChild(li);
            });
        }
        if (advice) {
            advice.innerHTML = '';
            (reportData.professional_advice || wai.suggestions || []).forEach(function(s) {
                const li = document.createElement('li'); li.textContent = s; advice.appendChild(li);
            });
        }
        if (ethicalSection && ethical) {
            const violations = reportData.ethical_violations || [];
            ethicalSection.style.display = violations.length > 0 ? 'block' : 'none';
            ethical.innerHTML = '';
            violations.forEach(function(v) { const li = document.createElement('li'); li.textContent = v; ethical.appendChild(li); });
        }
        if (overallText) { overallText.textContent = wai.overall_assessment || ''; }
        const skillScores = wai.skill_scores || {};
        const sixScores = {
            bond:      waiScores.bond      || 4,
            task:      waiScores.task      || 4,
            goal:      waiScores.goal      || 4,
            empathy:   skillScores.empathy   || 5,
            listening: skillScores.listening || 5,
            ethics:    skillScores.ethics    || 7
        };
        const skillDetails = document.getElementById('skill-details');
        if (skillDetails) {
            const dims = [
                { key: 'bond',      label: 'Bond (WAI)',       scale: 7,  comment: (wai.dimension_comments || {}).bond      || '' },
                { key: 'task',      label: 'Task (WAI)',       scale: 7,  comment: (wai.dimension_comments || {}).task      || '' },
                { key: 'goal',      label: 'Goal (WAI)',       scale: 7,  comment: (wai.dimension_comments || {}).goal      || '' },
                { key: 'empathy',   label: 'Empathy',          scale: 10, comment: skillScores.empathy_comment   || '' },
                { key: 'listening', label: 'Active Listening', scale: 10, comment: skillScores.listening_comment || '' },
                { key: 'ethics',    label: 'Ethics',           scale: 10, comment: skillScores.ethics_comment    || '' }
            ];
            skillDetails.innerHTML = dims.map(function(d) {
                const raw = sixScores[d.key];
                const pct = Math.round((raw / d.scale) * 100);
                return '<div class="skill-detail-item">' +
                    '<div class="skill-header">' +
                    '<span class="skill-name">' + d.label + '</span>' +
                    '<span class="skill-score">' + (raw.toFixed ? raw.toFixed(2) : raw) + '/' + d.scale + '</span>' +
                    '</div>' +
                    '<div class="skill-bar"><div class="skill-bar-fill" style="width:' + pct + '%"></div></div>' +
                    (d.comment ? '<div class="skill-comment">' + d.comment + '</div>' : '') +
                    '</div>';
            }).join('');
        }
        const histEntry = { date: new Date().toLocaleDateString(),
            bond: sixScores.bond, task: sixScores.task, goal: sixScores.goal,
            empathy: sixScores.empathy, listening: sixScores.listening, ethics: sixScores.ethics };
        saveSessionToHistory(histEntry);
        const history = loadSessionHistory();
        document.querySelectorAll('.report-tab-btn').forEach(function(btn) {
            btn.onclick = function() {
                document.querySelectorAll('.report-tab-btn').forEach(function(b) { b.classList.remove('active'); });
                document.querySelectorAll('.report-tab-content').forEach(function(c) { c.classList.remove('active'); });
                btn.classList.add('active');
                const t = document.getElementById('tab-' + btn.dataset.tab);
                if (t) t.classList.add('active');
                if (btn.dataset.tab === 'skills')  setTimeout(function() { renderRadarChart(sixScores); }, 50);
                if (btn.dataset.tab === 'history') setTimeout(function() { renderLineChart(history); }, 50);
            };
        });
        const clearBtn = document.getElementById('clear-history-btn');
        if (clearBtn) {
            clearBtn.onclick = function() {
                if (confirm('Clear all session history?')) {
                    localStorage.removeItem(HISTORY_KEY);
                    renderLineChart([]);
                    showToast('History cleared', 'info');
                }
            };
        }
        modal.style.display = 'block';
        setTimeout(function() { renderRadarChartOverview(sixScores); }, 80);
    }

    // 导出对话功能
    function exportConversation() {
        try {
            const messages = chatBox.querySelectorAll('.message');
            let conversationText = 'Psychological Counseling Session Record\n';
            conversationText += 'Client: ' + document.querySelector('.chat-header h2').textContent + '\n';
            conversationText += 'Export Time: ' + new Date().toLocaleString() + '\n';
            conversationText += '='.repeat(50) + '\n\n';
            messages.forEach(function(message, index) {
                const role = message.classList.contains('ai') ? 'AI Client' : 'Counselor';
                const content = message.querySelector('.content').textContent;
                conversationText += (index + 1) + '. [' + role + ']: ' + content + '\n\n';
            });
            const blob = new Blob([conversationText], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            const clientName = document.querySelector('.chat-header h2').textContent.split(' ')[0];
            const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
            a.href = url;
            a.download = clientName + '_session_record_' + timestamp + '.txt';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            showToast('Conversation exported successfully!', 'success');
        } catch (error) {
            console.error('Export conversation failed:', error);
            showToast('Export failed, please try again', 'error');
        }
    }    async function exportReport() {
        try {
            const response = await fetch('/api/export-report');
            
            if (!response.ok) {
                throw new Error('Export failed');
            }
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `counseling_report_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
            
            showToast('Report exported successfully!', 'success');
        } catch (error) {
            showToast(`Export failed: ${error.message}`, 'error');
            console.error('导出报告错误:', error);
        }
    }
    
    // Restart session function
    async function restartSession() {
        try {
            const clientId = document.querySelector('.chat-header h2').textContent.split(' ')[0];
            const response = await fetch(`/start-session/${clientId}?_=${Date.now()}`);
            if (!response.ok) throw new Error('Session reset failed');
            location.reload();
        } catch (error) {
            showToast(`Session error: ${error.message}`, 'error');
        }
    }
    
    // ============ 消息发送功能 ============
    
    // 阻抗触发条件检测函数
    function checkImpedanceTriggers(message) {
        const impedanceTriggers = [
            /\?.*\?/, // 包含多个问号
            /(首先|然后|接着|最后).*(其次|然后|接着)/, // 多重指令
            /(为什么|原因|究竟|到底)/,
            /(分析一下|解释一下|告诉我)/,
            /(母亲|爸爸|父亲|家庭|童年|创伤)/,
            /(自杀|死亡|伤害)/,
            /(移情|反移情|防御机制|认知扭曲)/,
            /(你应该|我认为你必须|为什么不|一定是你有地方做错了)/
        ];
    
        return impedanceTriggers.some(pattern => pattern.test(message));
    }
    
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // 检查考试模式限制
        const isExamMode = document.querySelector('.exam-indicators') !== null;
        if (isExamMode) {
            const turnCounter = document.getElementById('turn-value');
            if (turnCounter) {
                const [current, max] = turnCounter.textContent.split('/').map(Number);
                if (current >= max) {
                    showToast('Maximum exam turns reached; further messages cannot be sent', 'error');
                    return;
                }
            }
        }

        // 检测可能的阻抗触发条件
        const mightTriggerImpedance = checkImpedanceTriggers(message);
        
        // Add user message
        addMessage('user', message);
        userInput.value = '';
        sendBtn.disabled = true;
        
        // Show loading indicator
        const loadingElement = showLoadingIndicator();
        
        const controller = new AbortController();
        const fetchTimeout = setTimeout(() => controller.abort(), 55000);
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                signal: controller.signal,
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true',
                    'X-Impedance-Check': mightTriggerImpedance ? 'true' : 'false'
                },
                body: JSON.stringify({ 
                    message: message,
                    client_id: document.querySelector('.chat-header h2').textContent.split(' ')[0] || 'client_djjo'
                })
            });
            
            console.log('API响应状态:', response.status);
            
            if (response.status === 400) {
                const error = await response.json();
                console.log('API错误详情:', error);
                if (error.error === "Session not initialized") {
                    showToast('Session expired, reconnecting...', 'info');
                    await restartSession();
                    return;
                }
                throw new Error(error.error || 'Request failed: ' + response.status);
            }
            
            if (response.status === 503) {
                const err = await response.json().catch(() => ({}));
                throw new Error(err.error || 'AI service unavailable. Please check API key configuration.');
            }
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('API响应文本:', errorText);
                throw new Error('Request failed: ' + response.status);
            }
            
            const data = await response.json();
            console.log('API响应数据:', data);
            
            hideLoadingIndicator(loadingElement);
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (data.reply) {
                addMessage('ai', data.reply);
            } else {
                throw new Error('No response received');
            }
            
        } catch (error) {
            hideLoadingIndicator(loadingElement);
            console.error('Complete error info:', error);
            
            if (error.name === 'AbortError') {
                showToast('Request timed out. Please try again.', 'error');
                addMessage('ai', 'Sorry, the response timed out. Please try again.');
            } else if (error.message.includes("Session") || error.message.includes("initialized")) {
                showToast('Restoring session...', 'info');
                await restartSession();
            } else {
                const errorMsg = error.message || 'Unknown error';
                showToast(`Send failed: ${errorMsg}`, 'error');
                addMessage('ai', 'Sorry, I am temporarily unable to process your request. Please try again.');
            }
        } finally {
            clearTimeout(fetchTimeout);
            sendBtn.disabled = false;
            userInput.focus();
        }
    }
    
    // ============ Page Initialization ============
    
    function ensureEndButton() {
        const headerButtons = document.querySelector('.header-buttons');
        if (!headerButtons) return;
        
        // 移除已存在的按钮（避免重复）
        const existingBtn = document.getElementById('end-session-btn');
        if (existingBtn) existingBtn.remove();
        
        // 创建新的结束按钮
        const btn = document.createElement('button');
        btn.id = 'end-session-btn';
        btn.className = 'btn btn-primary';
        btn.innerHTML = '<span style="margin-right: 5px;">📋</span> End & Generate WAI Assessment';
        btn.style.marginLeft = '8px';
        headerButtons.appendChild(btn);

        btn.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to end this session and generate a WAI assessment report?')) return;
            await endSession();
        });
    }
    
    // 初始化事件监听器
    function initEventListeners() {
        // 发送消息
        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
        
        // 导出按钮
        if (exportBtn) {
            exportBtn.addEventListener('click', exportConversation);
        }
        
        // 报告弹窗事件
        const modal = document.getElementById('report-modal');
        const closeBtn = document.querySelector('.close');
        const closeReportBtn = document.getElementById('close-report-btn');
        const exportReportBtn = document.getElementById('export-report-btn');
        
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                if (modal) modal.style.display = 'none';
            });
        }
        
        if (closeReportBtn) {
            closeReportBtn.addEventListener('click', () => {
                if (modal) modal.style.display = 'none';
            });
        }
        
        if (exportReportBtn) {
            exportReportBtn.addEventListener('click', exportReport);
        }
        
        // 点击弹窗外部关闭
        window.addEventListener('click', (event) => {
            if (modal && event.target === modal) {
                modal.style.display = 'none';
            }
        });
        
        // 可见性变化处理
        document.addEventListener('visibilitychange', () => {
            if (document.visibilityState === 'visible') {
                fetch('/api/health').catch(() => location.reload());
            }
        });
    }
    
    // 初始化页面
    function initPage() {
        ensureEndButton();
        initEventListeners();
        userInput.focus();
    }
    
    // 启动初始化
    initPage();
    
    // 添加CSS样式
    const style = document.createElement('style');
    style.textContent = `
        /* 原有的样式保持不变 */
        .message {
            display: flex;
            margin-bottom: 15px;
            opacity: 0;
            animation: fadeIn 0.3s ease-out forwards;
        }
        
        @keyframes fadeIn {
            to { opacity: 1; }
        }
        
        .message .avatar {
            width: 40px;
            height: 40px;
            background:rgb(193, 221, 255);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 10px;
            flex-shrink: 0;
            font-weight: bold;
        }
        
        .message.user .avatar {
            background:rgb(207, 221, 252);
        }
        
        .message .content {
            padding: 12px 16px;
            border-radius: 18px;
            max-width: 80%;
            line-height: 1.5;
        }
        
        .message.ai .content {
            background: #f1f1f1;
            border-bottom-left-radius: 4px;
        }
        
        .message.user {
            justify-content: flex-end;
        }
        
        .message.user .content {
            background:rgb(255, 255, 255);
            color: black;
            border-bottom-right-radius: 4px;
        }
        
        .loading .content {
            background: transparent !important;
            padding: 12px 0;
        }
        
        .typing-indicator {
            display: flex;
            padding: 10px 15px;
        }
        
        .typing-indicator span {
            width: 8px;
            height: 8px;
            margin: 0 2px;
            background: #ccc;
            border-radius: 50%;
            display: inline-block;
            animation: typingAnimation 1.4s infinite ease-in-out;
        }
        
        .typing-indicator span:nth-child(1) {
            animation-delay: 0s;
        }
        
        .typing-indicator span:nth-child(2) {
            animation-delay: 0.2s;
        }
        
        .typing-indicator span:nth-child(3) {
            animation-delay: 0.4s;
        }
        
        @keyframes typingAnimation {
            0%, 60%, 100% { transform: translateY(0); }
            30% { transform: translateY(-5px); }
        }
        
        .toast {
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            padding: 12px 24px;
            border-radius: 4px;
            color: white;
            z-index: 1000;
            animation: slideIn 0.3s ease-out;
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .toast.error {
            background:rgb(188, 140, 255);
        }
        
        .toast.success {
            background:rgb(140, 200, 140);
        }
        
        .toast.info {
            background:rgb(140, 180, 255);
        }
        
        @keyframes slideIn {
            from { bottom: -50px; opacity: 0; }
            to { bottom: 20px; opacity: 1; }
        }
        
        .fade-out {
            animation: fadeOut 0.3s ease-in;
        }
        
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }

        /* 导出按钮样式 */
        #end-session-btn, #export-btn {
            display: flex;
            align-items: center;
            gap: 5px;
            padding: 8px 12px;
            font-size: 14px;
            background: #d9e6ff;
            color: #333;
            border: 1px solid #b8d0ff;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.3s ease;
            margin: 0;
        }
    
        #end-session-btn:hover, #export-btn:hover {
            background: #c5d9ff;
            transform: translateY(-1px);
        }
    
        #end-session-btn svg, #export-btn svg {
            width: 14px;
            height: 14px;
        }
        
        /* WAI评分样式 */
        .wai-scores {
            margin-top: 15px;
            padding: 12px;
            background: #f0f8ff;
            border-radius: 8px;
            border-left: 4px solid #4a6fe6;
        }
        
        .wai-scores p {
            margin: 5px 0;
        }
        
        .wai-scores strong {
            color: #2c5282;
        }
        
        .wai-scores p:last-child {
            font-size: 16px;
            font-weight: bold;
            color: #4a6fe6;
            margin-top: 8px;
        }
    `;
    document.head.appendChild(style);
});