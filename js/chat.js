document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const loadingTemplate = document.getElementById('loading-template');
    const exportBtn = document.getElementById('export-btn'); // 获取现有的导出按钮
    
    // Show message function
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}`;
        messageDiv.innerHTML = `
            <div class="avatar">${role === 'ai' ? 'AI' : '你'}</div>
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
    async function generateReport() {
        try {
            const response = await fetch('/api/generate-report', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true'
                },
                timeout: 30000  // 30秒超时
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || '生成报告失败');
            }
            
            return await response.json();
        } catch (error) {
            console.error('生成报告错误:', error);
            // 返回一个默认的报告结构，避免前端崩溃
            return {
                client_name: document.querySelector('.chat-header h2').textContent.split(' ')[0],
                client_issue: '未知问题',
                conversation_date: new Date().toLocaleString('zh-CN'),
                total_turns: document.querySelectorAll('.message').length / 2,
                estimated_time: '未知',
                key_insights: ['报告生成失败，请稍后重试'],
                professional_advice: ['系统暂时无法生成专业建议'],
                ethical_violations: []
            };
        }
    }   

    async function endSession() {
        try {
            const response = await fetch('/end-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true'
                }
            });
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.error || '结束会话失败');
            }
            
            const data = await response.json();
            showReportModal(data.report);
            
        } catch (error) {
            console.error('结束会话错误:', error);
            // 即使报告生成失败，也显示一个基本的报告弹窗
            try {
                const fallbackReport = await generateFallbackReport();
                showReportModal(fallbackReport);
            } catch (fallbackError) {
                showToast(`结束会话失败: ${error.message}`, 'error');
            }
        }
    }
    // 将训练模式的报告生成替换为调用 /api/wai-feedback
    async function generateTrainFeedback() {
        try {
            const payload = { mode: 'train', meta: {} };
            const response = await fetch('/api/wai-feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!response.ok) throw new Error('生成训练反馈失败');
            const data = await response.json();
            return data;
        } catch (err) {
            console.error('生成训练反馈错误', err);
            return null;
        }
    }

    // 假设你已有一个“结束”按钮 id 为 end-session-btn；如果没有，下面的代码会动态添加一个
    (function ensureEndButton() {
        const headerButtons = document.querySelector('.header-buttons');
        if (!headerButtons) return;
        if (!document.getElementById('end-session-btn')) {
            const btn = document.createElement('button');
            btn.id = 'end-session-btn';
            btn.className = 'btn btn-danger';
            btn.textContent = '结束并查看反馈';
            btn.style.marginLeft = '8px';
            headerButtons.prepend(btn);

            btn.addEventListener('click', async () => {
                if (!confirm('确定结束会话并生成WAI反馈吗？')) return;
                // 先调用后端 end-session，保存并清理会话
                try {
                    const res = await fetch('/end-session', { method: 'POST', headers: {'Content-Type':'application/json'} });
                    if (!res.ok) {
                        const err = await res.json();
                        throw new Error(err.error || '结束会话失败');
                    }
                    // 再调用 WAI 评分
                    const wai = await generateTrainFeedback();
                    if (wai) {
                        // 构造一个兼容 showReportModal 的 reportData
                        const reportData = {
                            client_name: document.querySelector('.chat-header h2')?.textContent || '未知',
                            client_issue: '',
                            conversation_date: new Date().toLocaleString(),
                            total_turns: wai.meta?.total_turns || 0,
                            estimated_time: `${Math.floor((wai.meta?.time_used || 0) / 60)} 分钟`,
                            key_insights: wai.item_comments ? Object.values(wai.item_comments) : [],
                            professional_advice: wai.suggestions || [],
                            ethical_violations: wai.ethical_violations || []
                        };
                        // showReportModal 从 chat.js 中已存在，直接调用
                        showReportModal(reportData);
                        // 存储当前反馈供导出使用
                        window.currentFeedback = wai;
                    } else {
                        showToast('无法生成WAI反馈', 'error');
                    }
                } catch (error) {
                    showToast(error.message || '结束失败', 'error');
                }
            });
        }
    })();

    // 添加备用报告生成函数
    async function generateFallbackReport() {
        const clientName = document.querySelector('.chat-header h2').textContent.split(' ')[0];
        const messages = document.querySelectorAll('.message');
        const totalTurns = Math.floor(messages.length / 2);
        
        return {
            client_name: clientName,
            client_issue: '未知问题',
            conversation_date: new Date().toLocaleString('zh-CN'),
            total_turns: totalTurns,
            estimated_time: `${totalTurns * 2} 分钟`,
            key_insights: ['报告生成失败，但对话已成功结束'],
            professional_advice: ['系统暂时无法生成专业建议，建议回顾对话内容自行分析'],
            ethical_violations: []
        };
    }

    // 显示报告弹窗
    function showReportModal(reportData) {
        const modal = document.getElementById('report-modal');
        const basicInfo = document.getElementById('report-basic-info');
        const keyInsights = document.getElementById('report-key-insights');
        const advice = document.getElementById('report-advice');
        const ethical = document.getElementById('report-ethical');
        const ethicalSection = document.getElementById('ethical-section');
    
    // 填充基本信息
        basicInfo.innerHTML = `
        <p><strong>来访者:</strong> ${reportData.client_name}</p>
        <p><strong>主要问题:</strong> ${reportData.client_issue}</p>
        <p><strong>对话时间:</strong> ${reportData.conversation_date}</p>
        <p><strong>对话轮次:</strong> ${reportData.total_turns} 轮</p>
        <p><strong>预计用时:</strong> ${reportData.estimated_time}</p>
        `;
    
    // 填充关键洞察
        keyInsights.innerHTML = '';
        reportData.key_insights.forEach(insight => {
            const li = document.createElement('li');
            li.textContent = insight;
            keyInsights.appendChild(li);
        });
    
    // 填充专业建议
        advice.innerHTML = '';
        reportData.professional_advice.forEach(adv => {
            const li = document.createElement('li');
            li.textContent = adv;
            advice.appendChild(li);
        });
    
        // 填充伦理注意事项（如果有）
        if (reportData.ethical_violations && reportData.ethical_violations.length > 0) {
            ethicalSection.style.display = 'block';
            ethical.innerHTML = '';
            reportData.ethical_violations.forEach(violation => {
                const li = document.createElement('li');
                li.textContent = violation;
                ethical.appendChild(li);
            });
        } else {
            ethicalSection.style.display = 'none';
        }
    
    // 显示弹窗
        modal.style.display = 'block';
    }

// 导出报告功能
    async function exportReport() {
        try {
            const response = await fetch('/api/export-report');
            if (!response.ok) {
                throw new Error('导出报告失败');
            }
        
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `咨询报告_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
        
            showToast('报告导出成功！', 'success');
        } catch (error) {
            showToast(`导出失败: ${error.message}`, 'error');
            console.error('导出报告错误:', error);
        }
    }

    // 导出对话功能
    function exportConversation() {
        try {
            const messages = chatBox.querySelectorAll('.message');
            let conversationText = `心理咨询对话记录\n`;
            conversationText += `来访者: ${document.querySelector('.chat-header h2').textContent}\n`;
            conversationText += `导出时间: ${new Date().toLocaleString('zh-CN')}\n`;
            conversationText += '='.repeat(50) + '\n\n';
            
            messages.forEach((message, index) => {
                const role = message.classList.contains('ai') ? 'AI来访者' : '咨询师';
                const content = message.querySelector('.content').textContent;
                conversationText += `${index + 1}. [${role}]: ${content}\n\n`;
            });
            
            // 创建下载链接
            const blob = new Blob([conversationText], { type: 'text/plain;charset=utf-8' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            const clientName = document.querySelector('.chat-header h2').textContent.split(' ')[0];
            const timestamp = new Date().toISOString().slice(0, 10).replace(/-/g, '');
            a.href = url;
            a.download = `${clientName}_对话记录_${timestamp}.txt`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
            
            showToast('对话导出成功！', 'success');
        } catch (error) {
            console.error('导出对话失败:', error);
            showToast('导出失败，请重试', 'error');
        }
    }

    // 显示报告弹窗
    function showReportModal(reportData) {
        const modal = document.getElementById('report-modal');
        const basicInfo = document.getElementById('report-basic-info');
        const keyInsights = document.getElementById('report-key-insights');
        const advice = document.getElementById('report-advice');
        const ethical = document.getElementById('report-ethical');
        const ethicalSection = document.getElementById('ethical-section');
    
    // 填充基本信息
        basicInfo.innerHTML = `
            <p><strong>来访者:</strong> ${reportData.client_name}</p>
            <p><strong>主要问题:</strong> ${reportData.client_issue}</p>
            <p><strong>对话时间:</strong> ${reportData.conversation_date}</p>
            <p><strong>对话轮次:</strong> ${reportData.total_turns} 轮</p>
            <p><strong>预计用时:</strong> ${reportData.estimated_time}</p>
        `;
    
    // 填充关键洞察
        keyInsights.innerHTML = '';
        reportData.key_insights.forEach(insight => {
            const li = document.createElement('li');
            li.textContent = insight;
            keyInsights.appendChild(li);
        });
    
    // 填充专业建议
        advice.innerHTML = '';
        reportData.professional_advice.forEach(adv => {
            const li = document.createElement('li');
            li.textContent = adv;
            advice.appendChild(li);
        });
    
    // 填充伦理注意事项（如果有）
        if (reportData.ethical_violations && reportData.ethical_violations.length > 0) {
            ethicalSection.style.display = 'block';
            ethical.innerHTML = '';
            reportData.ethical_violations.forEach(violation => {
                const li = document.createElement('li');
                li.textContent = violation;
                ethical.appendChild(li);
            });
        } else {
            ethicalSection.style.display = 'none';
        }
    
    // 显示弹窗
        modal.style.display = 'block';
    }

// 导出报告功能
    async function exportReport() {
        try {
            const response = await fetch('/api/export-report');
            if (!response.ok) {
                throw new Error('导出报告失败');
            }
        
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `咨询报告_${new Date().toISOString().slice(0, 10)}.pdf`;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);

            showToast('报告导出成功！', 'success');
        } catch (error) {
            showToast(`导出失败: ${error.message}`, 'error');
            console.error('导出报告错误:', error);
        }
    }

    // Restart session function
    async function restartSession() {
        try {
            const clientId = document.querySelector('.chat-header h2').textContent.split(' ')[0];
            const response = await fetch(`/start-session/${clientId}?_=${Date.now()}`);
            if (!response.ok) throw new Error('会话重置失败');
            location.reload();
        } catch (error) {
            showToast(`会话错误: ${error.message}`, 'error');
        }
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
                    showToast('已达到考试最大对话轮次，无法继续发送消息', 'error');
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
        
        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
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
            
            console.log('API响应状态:', response.status); // 调试信息
            
            if (response.status === 400) {
                const error = await response.json();
                console.log('API错误详情:', error); // 调试信息
                if (error.error === "会话未初始化") {
                    showToast('会话已过期，正在重新连接...', 'info');
                    await restartSession();
                    return;
                }
                throw new Error(error.error || '请求失败: ' + response.status);
            }
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('API响应文本:', errorText); // 调试信息
                throw new Error('请求失败: ' + response.status);
            }
            
            const data = await response.json();
            console.log('API响应数据:', data); // 调试信息
            
            hideLoadingIndicator(loadingElement);
            
            if (data.error) {
                throw new Error(data.error);
            }
            
            if (data.reply) {
                addMessage('ai', data.reply);
            } else {
                throw new Error('没有收到回复');
            }
            
        } catch (error) {
            hideLoadingIndicator(loadingElement);
            console.error('完整的错误信息:', error); // 调试信息
            
            if (error.message.includes("会话") || error.message.includes("初始化")) {
                showToast('正在恢复会话...', 'info');
                await restartSession();
            } else {
                // 添加更详细的错误信息
                const errorMsg = error.message || '未知错误';
                showToast(`发送失败: ${errorMsg}`, 'error');
                // 添加一个默认回复，确保对话可以继续
                addMessage('ai', '抱歉，我暂时无法处理您的请求。请重试。');
            }
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    }
    // 阻抗触发条件检测函数
    function checkImpedanceTriggers(message) {
        const impedanceTriggers = [
            // 多重问题
            /\?.*\?/, // 包含多个问号
            /(首先|然后|接着|最后).*(其次|然后|接着)/, // 多重指令
        
            // 过于直接的问题
            /(为什么|原因|究竟|到底)/,
            /(分析一下|解释一下|告诉我)/,
            
            // 可能触发防御的话题
            /(母亲|爸爸|父亲|家庭|童年|创伤)/,
            /(自杀|死亡|伤害)/,
            
            // 技术性语言
            /(移情|反移情|防御机制|认知扭曲)/,
        
            // 建议性语言
            /(你应该|我认为你必须|为什么不|一定是你有地方做错了)/
        ];
    
    return impedanceTriggers.some(pattern => pattern.test(message));
}

    async function endSession() {
        try {
            const response = await fetch('/end-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true'
                }
            });
            
            if (!response.ok) {
                throw new Error('结束会话失败');
            }
        
            const data = await response.json();
            showReportModal(data.report);
        
        } catch (error) {
            showToast(`结束会话失败: ${error.message}`, 'error');
            console.error('结束会话错误:', error);
        }
    }

    // Event listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });
    
    // 添加导出按钮事件监听
    exportBtn.addEventListener('click', exportConversation);

    // Visibility change handler
    document.addEventListener('visibilitychange', () => {
        if (document.visibilityState === 'visible') {
            fetch('/api/health').catch(() => location.reload());
        }
    });

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
    
    // Auto-focus input
    userInput.focus();
    
        const endSessionBtn = document.getElementById('end-session-btn');
    if (endSessionBtn) {
        endSessionBtn.addEventListener('click', endSession);
    }
    
    // 添加报告弹窗事件监听
    const modal = document.getElementById('report-modal');
    const closeBtn = document.querySelector('.close');
    const closeReportBtn = document.getElementById('close-report-btn');
    const exportReportBtn = document.getElementById('export-report-btn');
    
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }
    
    if (closeReportBtn) {
        closeReportBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }
    
    if (exportReportBtn) {
        exportReportBtn.addEventListener('click', exportReport);
    }
    
    // 点击弹窗外部关闭
    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Embedded styles
    const style = document.createElement('style');
    style.textContent = `
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

        /* 导出按钮样式 - 导出对话按钮 */
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
    `;
    document.head.appendChild(style);
});

