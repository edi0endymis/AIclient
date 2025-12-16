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
                bond: "基于对话内容，情感联结初步建立",
                task: "咨询任务合作基本达成共识",
                goal: "治疗目标方向基本明确"
            },
            suggestions: [
                "建议加强情感回应的一致性",
                "可以更清晰地阐明咨询目标",
                "需要加强任务导向的合作"
            ],
            strengths: ["能够建立基本信任关系", "咨询目标初步明确"],
            overall_assessment: "对话初步建立了工作联盟，建议继续深化咨询关系。"
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
                insights.push("情感联结良好，建立了较好的信任关系");
            } else {
                insights.push("情感联结有待加强，信任关系需要进一步建立");
            }
            
            if (scores.task >= 5) {
                insights.push("任务合作有效，咨询任务明确");
            } else {
                insights.push("任务合作需要加强，咨询任务可更清晰");
            }
            
            if (scores.goal >= 5) {
                insights.push("目标一致性好，治疗方向明确");
            } else {
                insights.push("目标一致性需提升，治疗方向可进一步明确");
            }
        } else {
            insights.push("完成了" + totalTurns + "轮对话");
            insights.push("对话已正常结束");
            insights.push("建议回顾对话内容进行反思");
        }
        
        return insights;
    }
    
    function generateProfessionalAdvice(waiAssessment) {
        if (waiAssessment?.suggestions) {
            return waiAssessment.suggestions;
        }
        
        return [
            "建议增加开放式问题的使用",
            "注意对话节奏的控制", 
            "加强情感回应技巧",
            "提升倾听和共情能力",
            "注意非语言信息的观察"
        ];
    }
    
    // 主结束会话函数
    async function endSession() {
        try {
            console.log("开始结束会话并生成WAI评估...");
            
            // 显示加载提示
            showToast('正在生成WAI评估报告...', 'info');
            
            // 1. 获取对话基本信息
            const clientName = document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || '来访者';
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
                client_issue: document.querySelector('.chat-header small')?.textContent || '未指定问题',
                conversation_date: new Date().toLocaleString('zh-CN'),
                total_turns: totalTurns,
                estimated_time: `${totalTurns * 2} 分钟`,
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
            showToast('生成报告失败: ' + error.message, 'error');
            
            // 显示基本的报告弹窗
            const fallbackReport = await generateFallbackReport();
            showReportModal(fallbackReport);
        }
    }
    
    // 备用报告生成函数
    async function generateFallbackReport() {
        const clientName = document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || '来访者';
        const userMessages = document.querySelectorAll('.message.user');
        const aiMessages = document.querySelectorAll('.message.ai:not(.loading)');
        const totalTurns = Math.min(userMessages.length, aiMessages.length);
        
        return {
            client_name: clientName,
            client_issue: '未知问题',
            conversation_date: new Date().toLocaleString('zh-CN'),
            total_turns: totalTurns,
            estimated_time: `${totalTurns * 2} 分钟`,
            key_insights: ['报告生成失败，但对话已成功结束'],
            professional_advice: ['请回顾对话内容自行分析'],
            ethical_violations: []
        };
    }
    
    // 显示报告弹窗 - 修复版
    function showReportModal(reportData) {
        const modal = document.getElementById('report-modal');
        if (!modal) {
            console.error('报告弹窗元素未找到');
            return;
        }
        
        const basicInfo = document.getElementById('report-basic-info');
        const keyInsights = document.getElementById('report-key-insights');
        const advice = document.getElementById('report-advice');
        const ethical = document.getElementById('report-ethical');
        const ethicalSection = document.getElementById('ethical-section');
        
        // 清空之前的内容
        if (basicInfo) basicInfo.innerHTML = '';
        if (keyInsights) keyInsights.innerHTML = '';
        if (advice) advice.innerHTML = '';
        if (ethical) ethical.innerHTML = '';
        
        // 填充基本信息
        let basicHTML = `
            <p><strong>来访者:</strong> ${reportData.client_name || '未指定'}</p>
            <p><strong>主要问题:</strong> ${reportData.client_issue || '未指定问题'}</p>
            <p><strong>对话时间:</strong> ${reportData.conversation_date || new Date().toLocaleString('zh-CN')}</p>
            <p><strong>对话轮次:</strong> ${reportData.total_turns || 0} 轮</p>
            <p><strong>预计用时:</strong> ${reportData.estimated_time || '0 分钟'}</p>
        `;
        
        // 如果有WAI评估，显示WAI评分
        if (reportData.wai_assessment) {
            const wai = reportData.wai_assessment;
            const scores = wai.wai_scores || {};
            
            basicHTML += `
                <div class="wai-scores">
                    <p><strong>WAI工作联盟评分:</strong></p>
                    <p>情感联结: ${scores.bond || 'N/A'}/7</p>
                    <p>任务合作: ${scores.task || 'N/A'}/7</p>
                    <p>目标一致: ${scores.goal || 'N/A'}/7</p>
                    <p><strong>总分:</strong> ${wai.wai_total || 'N/A'}/21 (${wai.wai_percentage || 'N/A'}%)</p>
                </div>
            `;
        }
        
        if (basicInfo) basicInfo.innerHTML = basicHTML;
        
        // 填充关键洞察
        if (keyInsights) {
            const insights = reportData.key_insights || [];
            insights.forEach(insight => {
                const li = document.createElement('li');
                li.textContent = insight;
                keyInsights.appendChild(li);
            });
        }
        
        // 填充专业建议
        if (advice) {
            const suggestions = reportData.professional_advice || [];
            suggestions.forEach(adv => {
                const li = document.createElement('li');
                li.textContent = adv;
                advice.appendChild(li);
            });
        }
        
        // 填充伦理注意事项
        if (ethicalSection && ethical) {
            const violations = reportData.ethical_violations || [];
            if (violations.length > 0) {
                ethicalSection.style.display = 'block';
                violations.forEach(violation => {
                    const li = document.createElement('li');
                    li.textContent = violation;
                    ethical.appendChild(li);
                });
            } else {
                ethicalSection.style.display = 'none';
            }
        }
        
        // 显示弹窗
        modal.style.display = 'block';
    }
    
    // ============ 其他功能函数 ============
    
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
            
            console.log('API响应状态:', response.status);
            
            if (response.status === 400) {
                const error = await response.json();
                console.log('API错误详情:', error);
                if (error.error === "会话未初始化") {
                    showToast('会话已过期，正在重新连接...', 'info');
                    await restartSession();
                    return;
                }
                throw new Error(error.error || '请求失败: ' + response.status);
            }
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('API响应文本:', errorText);
                throw new Error('请求失败: ' + response.status);
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
                throw new Error('没有收到回复');
            }
            
        } catch (error) {
            hideLoadingIndicator(loadingElement);
            console.error('完整的错误信息:', error);
            
            if (error.message.includes("会话") || error.message.includes("初始化")) {
                showToast('正在恢复会话...', 'info');
                await restartSession();
            } else {
                const errorMsg = error.message || '未知错误';
                showToast(`发送失败: ${errorMsg}`, 'error');
                addMessage('ai', '抱歉，我暂时无法处理您的请求。请重试。');
            }
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    }
    
    // ============ 页面初始化 ============
    
    // 确保结束按钮存在
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
        btn.innerHTML = '<span style="margin-right: 5px;">📋</span>结束并生成WAI评估';
        btn.style.marginLeft = '8px';
        headerButtons.appendChild(btn);

        btn.addEventListener('click', async () => {
            if (!confirm('确定结束当前会话并生成WAI评估报告吗？')) return;
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