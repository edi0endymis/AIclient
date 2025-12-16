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
            console.log("开始结束会话...");
            
            const response = await fetch('/end-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            console.log("结束会话响应状态:", response.status);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error("结束会话错误详情:", errorData);
                throw new Error(errorData.error || '结束会话失败: ' + response.status);
            }
            
            const data = await response.json();
            console.log("结束会话成功:", data);
            
            if (data.report) {
                showReportModal(data.report);
            } else {
                throw new Error('没有收到报告数据');
            }
            
        } catch (error) {
            console.error('结束会话错误详情:', error);
            
            // 即使报告生成失败，也显示一个基本的报告弹窗
            try {
                const fallbackReport = await generateFallbackReport();
                showReportModal(fallbackReport);
            } catch (fallbackError) {
                showToast(`会话已结束，但报告生成失败: ${error.message}`, 'error');
                // 创建一个最简单的报告弹窗
                const simpleReport = {
                    client_name: document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || '来访者',
                    client_issue: '未知问题',
                    conversation_date: new Date().toLocaleString('zh-CN'),
                    total_turns: document.querySelectorAll('.message.user').length,
                    estimated_time: `${document.querySelectorAll('.message.user').length * 2} 分钟`,
                    key_insights: ['对话已成功结束'],
                    professional_advice: ['请回顾对话内容进行反思'],
                    ethical_violations: []
                };
                showReportModal(simpleReport);
            }
        }
    }

    // 在 chat.js 的 endSession 函数后，添加以下代码：

    // WAI评估函数
    async function generateWAIAssessment() {
        try {
            const response = await fetch('/api/wai-comprehensive', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true'
                }
            });
            
            if (!response.ok) {
                throw new Error('WAI评估失败');
            }
            
            const data = await response.json();
            return data.assessment || data;
            
        } catch (error) {
            console.error('WAI评估错误:', error);
            
            // 返回默认评估
            return {
                wai_dimension_scores: {
                    bond: { score: 4, items: [] },
                    task: { score: 4, items: [] },
                    goal: { score: 4, items: [] }
                },
                wai_total: 12,
                wai_percentage: 57.1,
                dimension_analysis: {
                    bond: "评估失败，无法获取详细分析",
                    task: "评估失败，无法获取详细分析",
                    goal: "评估失败，无法获取详细分析"
                },
                strengths: ["对话正常进行"],
                improvement_suggestions: ["请确保网络连接正常", "对话内容需更丰富"],
                overall_assessment: "WAI评估暂时不可用"
            };
        }
    }

    // 修改结束会话函数，集成WAI评估
    async function endSessionWithWAI() {
        try {
            console.log("开始结束会话并生成WAI评估...");
            
            // 显示加载提示
            const loadingToast = showToast('正在生成WAI评估报告...', 'info');
            
            // 1. 生成WAI评估
            const waiAssessment = await generateWAIAssessment();
            
            // 2. 结束会话获取基本信息
            const response = await fetch('/end-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            let reportData = {};
            if (response.ok) {
                const endData = await response.json();
                reportData = endData.report || {};
            } else {
                // 如果结束会话失败，创建基本报告
                const clientName = document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || '来访者';
                reportData = {
                    client_name: clientName,
                    client_issue: '未知问题',
                    conversation_date: new Date().toLocaleString('zh-CN'),
                    total_turns: document.querySelectorAll('.message.user').length,
                    estimated_time: `${document.querySelectorAll('.message.user').length * 2} 分钟`
                };
            }
            
            // 3. 合并WAI评估到报告
            reportData.wai_assessment = waiAssessment;
            
            // 4. 保存到session
            try {
                await fetch('/api/save-feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ wai_assessment: waiAssessment })
                });
            } catch (e) {
                console.log('保存评估失败:', e);
            }
            
            // 5. 显示综合报告
            showWAIReportModal(reportData);
            
        } catch (error) {
            console.error('结束会话错误:', error);
            showToast('评估失败: ' + error.message, 'error');
        }
    }

    // 显示WAI评估报告弹窗
    function showWAIReportModal(reportData) {
        const modal = document.getElementById('report-modal');
        const basicInfo = document.getElementById('report-basic-info');
        const keyInsights = document.getElementById('report-key-insights');
        const advice = document.getElementById('report-advice');
        
        // 填充基本信息
        basicInfo.innerHTML = `
            <p><strong>来访者:</strong> ${reportData.client_name}</p>
            <p><strong>主要问题:</strong> ${reportData.client_issue}</p>
            <p><strong>对话时间:</strong> ${reportData.conversation_date}</p>
            <p><strong>对话轮次:</strong> ${reportData.total_turns} 轮</p>
            <p><strong>预计用时:</strong> ${reportData.estimated_time}</p>
        `;
        
        // 如果有WAI评估，显示WAI评分
        if (reportData.wai_assessment) {
            const wai = reportData.wai_assessment;
            basicInfo.innerHTML += `
                <div class="wai-scores">
                    <p><strong>WAI工作联盟评分:</strong></p>
                    <p>情感联结: ${wai.wai_dimension_scores?.bond?.score || 'N/A'}/7</p>
                    <p>任务合作: ${wai.wai_dimension_scores?.task?.score || 'N/A'}/7</p>
                    <p>目标一致: ${wai.wai_dimension_scores?.goal?.score || 'N/A'}/7</p>
                    <p><strong>总分:</strong> ${wai.wai_total || 'N/A'}/21 (${wai.wai_percentage || 'N/A'}%)</p>
                </div>
            `;
        }
        
        // 填充关键洞察
        keyInsights.innerHTML = '';
        if (reportData.wai_assessment?.dimension_analysis) {
            const analysis = reportData.wai_assessment.dimension_analysis;
            const insights = [
                `情感联结: ${analysis.bond || '未评估'}`,
                `任务合作: ${analysis.task || '未评估'}`,
                `目标一致: ${analysis.goal || '未评估'}`
            ];
            
            insights.forEach(insight => {
                const li = document.createElement('li');
                li.textContent = insight;
                keyInsights.appendChild(li);
            });
        }
        
        // 填充专业建议
        advice.innerHTML = '';
        const suggestions = reportData.wai_assessment?.improvement_suggestions || 
                        reportData.professional_advice || 
                        ['请回顾对话进行反思'];
        
        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            advice.appendChild(li);
        });
        
        // 如果有优势分析，添加到报告
        if (reportData.wai_assessment?.strengths) {
            const strengthsSection = document.createElement('div');
            strengthsSection.className = 'report-section';
            strengthsSection.innerHTML = '<h4>咨询优势</h4><ul id="report-strengths"></ul>';
            
            const strengthsList = strengthsSection.querySelector('#report-strengths');
            reportData.wai_assessment.strengths.forEach(strength => {
                const li = document.createElement('li');
                li.textContent = strength;
                strengthsList.appendChild(li);
            });
            
            // 插入到专业建议之后
            advice.parentNode.insertBefore(strengthsSection, advice.nextSibling);
        }
        
        // 显示弹窗
        modal.style.display = 'block';
    }

    // 修改现有的事件监听器，使用新的WAI评估
    (function ensureEndButton() {
        const headerButtons = document.querySelector('.header-buttons');
        if (!headerButtons) return;
        
        if (!document.getElementById('end-session-btn')) {
            const btn = document.createElement('button');
            btn.id = 'end-session-btn';
            btn.className = 'btn btn-primary';
            btn.innerHTML = '<span style="margin-right: 5px;">📋</span>结束并生成WAI评估';
            btn.style.marginLeft = '8px';
            headerButtons.appendChild(btn);

            btn.addEventListener('click', async () => {
                if (!confirm('确定结束当前会话并生成WAI评估报告吗？')) return;
                await endSessionWithWAI();
            });
        }
    })();

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

    (function ensureEndButton() {
        const headerButtons = document.querySelector('.header-buttons');
        if (!headerButtons) return;
        
        if (!document.getElementById('end-session-btn')) {
            const btn = document.createElement('button');
            btn.id = 'end-session-btn';
            btn.className = 'btn btn-primary';
            btn.innerHTML = '<span style="margin-right: 5px;">📋</span>结束并生成WAI评估';
            btn.style.marginLeft = '8px';
            headerButtons.appendChild(btn);

            btn.addEventListener('click', async () => {
                if (!confirm('确定结束当前会话并生成WAI评估报告吗？')) return;
                
                // 显示加载
                const loadingToast = showToast('正在分析对话并生成评估...', 'info');
                
                try {
                    // 1. 先调用WAI评估
                    const waiResponse = await fetch('/api/wai-feedback', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({ mode: 'train' })
                    });
                    
                    if (!waiResponse.ok) {
                        const err = await waiResponse.json();
                        throw new Error(err.error || 'WAI评估失败');
                    }
                    
                    const waiData = await waiResponse.json();
                    
                    // 2. 再结束会话获取基本信息
                    const endResponse = await fetch('/end-session', { 
                        method: 'POST',
                        headers: {'Content-Type':'application/json'} 
                    });
                    
                    let reportData = {};
                    if (endResponse.ok) {
                        const endData = await endResponse.json();
                        reportData = endData.report || {};
                    }
                    
                    // 3. 合并数据
                    reportData.wai_feedback = waiData;
                    
                    // 4. 保存到session（用于PDF导出）
                    try {
                        await fetch('/api/save-feedback', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify({ wai_feedback: waiData })
                        });
                    } catch (e) {
                        console.log('保存反馈失败，但不影响显示:', e);
                    }
                    
                    // 5. 显示报告
                    showReportModal(reportData);
                    
                } catch (error) {
                    showToast('评估失败: ' + error.message, 'error');
                    console.error('WAI评估错误:', error);
                }
            });
        }
    })();

    // 添加备用报告生成函数
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
            // 或者明确指定GET方法：
            // const response = await fetch('/api/export-report', {
            //     method: 'GET'
            // });
            
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
            // 或者明确指定GET方法：
            // const response = await fetch('/api/export-report', {
            //     method: 'GET'
            // });
            
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
            console.log("开始结束会话...");
            
            const response = await fetch('/end-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            console.log("结束会话响应状态:", response.status);
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                console.error("结束会话错误详情:", errorData);
                throw new Error(errorData.error || '结束会话失败: ' + response.status);
            }
            
            const data = await response.json();
            console.log("结束会话成功:", data);
            
            if (data.report) {
                showReportModal(data.report);
            } else {
                throw new Error('没有收到报告数据');
            }
            
        } catch (error) {
            console.error('结束会话错误详情:', error);
            
            // 即使报告生成失败，也显示一个基本的报告弹窗
            try {
                const fallbackReport = await generateFallbackReport();
                showReportModal(fallbackReport);
            } catch (fallbackError) {
                showToast(`会话已结束，但报告生成失败: ${error.message}`, 'error');
                // 创建一个最简单的报告弹窗
                const simpleReport = {
                    client_name: document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || '来访者',
                    client_issue: '未知问题',
                    conversation_date: new Date().toLocaleString('zh-CN'),
                    total_turns: document.querySelectorAll('.message.user').length,
                    estimated_time: `${document.querySelectorAll('.message.user').length * 2} 分钟`,
                    key_insights: ['对话已成功结束'],
                    professional_advice: ['请回顾对话内容进行反思'],
                    ethical_violations: []
                };
                showReportModal(simpleReport);
            }
        }
    }

// 在 chat.js 的 endSession 函数后，添加以下代码：

    // WAI评估函数
    async function generateWAIAssessment() {
        try {
            const response = await fetch('/api/wai-comprehensive', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true'
                }
            });
            
            if (!response.ok) {
                throw new Error('WAI评估失败');
            }
            
            const data = await response.json();
            return data.assessment || data;
            
        } catch (error) {
            console.error('WAI评估错误:', error);
            
            // 返回默认评估
            return {
                wai_dimension_scores: {
                    bond: { score: 4, items: [] },
                    task: { score: 4, items: [] },
                    goal: { score: 4, items: [] }
                },
                wai_total: 12,
                wai_percentage: 57.1,
                dimension_analysis: {
                    bond: "评估失败，无法获取详细分析",
                    task: "评估失败，无法获取详细分析",
                    goal: "评估失败，无法获取详细分析"
                },
                strengths: ["对话正常进行"],
                improvement_suggestions: ["请确保网络连接正常", "对话内容需更丰富"],
                overall_assessment: "WAI评估暂时不可用"
            };
        }
    }

    // 修改结束会话函数，集成WAI评估
    async function endSessionWithWAI() {
        try {
            console.log("开始结束会话并生成WAI评估...");
            
            // 显示加载提示
            const loadingToast = showToast('正在生成WAI评估报告...', 'info');
            
            // 1. 生成WAI评估
            const waiAssessment = await generateWAIAssessment();
            
            // 2. 结束会话获取基本信息
            const response = await fetch('/end-session', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            let reportData = {};
            if (response.ok) {
                const endData = await response.json();
                reportData = endData.report || {};
            } else {
                // 如果结束会话失败，创建基本报告
                const clientName = document.querySelector('.chat-header h2')?.textContent.split(' ')[0] || '来访者';
                reportData = {
                    client_name: clientName,
                    client_issue: '未知问题',
                    conversation_date: new Date().toLocaleString('zh-CN'),
                    total_turns: document.querySelectorAll('.message.user').length,
                    estimated_time: `${document.querySelectorAll('.message.user').length * 2} 分钟`
                };
            }
            
            // 3. 合并WAI评估到报告
            reportData.wai_assessment = waiAssessment;
            
            // 4. 保存到session
            try {
                await fetch('/api/save-feedback', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ wai_assessment: waiAssessment })
                });
            } catch (e) {
                console.log('保存评估失败:', e);
            }
            
            // 5. 显示综合报告
            showWAIReportModal(reportData);
            
        } catch (error) {
            console.error('结束会话错误:', error);
            showToast('评估失败: ' + error.message, 'error');
        }
    }

    // 显示WAI评估报告弹窗
    function showWAIReportModal(reportData) {
        const modal = document.getElementById('report-modal');
        const basicInfo = document.getElementById('report-basic-info');
        const keyInsights = document.getElementById('report-key-insights');
        const advice = document.getElementById('report-advice');
        
        // 填充基本信息
        basicInfo.innerHTML = `
            <p><strong>来访者:</strong> ${reportData.client_name}</p>
            <p><strong>主要问题:</strong> ${reportData.client_issue}</p>
            <p><strong>对话时间:</strong> ${reportData.conversation_date}</p>
            <p><strong>对话轮次:</strong> ${reportData.total_turns} 轮</p>
            <p><strong>预计用时:</strong> ${reportData.estimated_time}</p>
        `;
        
        // 如果有WAI评估，显示WAI评分
        if (reportData.wai_assessment) {
            const wai = reportData.wai_assessment;
            basicInfo.innerHTML += `
                <div class="wai-scores">
                    <p><strong>WAI工作联盟评分:</strong></p>
                    <p>情感联结: ${wai.wai_dimension_scores?.bond?.score || 'N/A'}/7</p>
                    <p>任务合作: ${wai.wai_dimension_scores?.task?.score || 'N/A'}/7</p>
                    <p>目标一致: ${wai.wai_dimension_scores?.goal?.score || 'N/A'}/7</p>
                    <p><strong>总分:</strong> ${wai.wai_total || 'N/A'}/21 (${wai.wai_percentage || 'N/A'}%)</p>
                </div>
            `;
        }
        
        // 填充关键洞察
        keyInsights.innerHTML = '';
        if (reportData.wai_assessment?.dimension_analysis) {
            const analysis = reportData.wai_assessment.dimension_analysis;
            const insights = [
                `情感联结: ${analysis.bond || '未评估'}`,
                `任务合作: ${analysis.task || '未评估'}`,
                `目标一致: ${analysis.goal || '未评估'}`
            ];
            
            insights.forEach(insight => {
                const li = document.createElement('li');
                li.textContent = insight;
                keyInsights.appendChild(li);
            });
        }
        
        // 填充专业建议
        advice.innerHTML = '';
        const suggestions = reportData.wai_assessment?.improvement_suggestions || 
                        reportData.professional_advice || 
                        ['请回顾对话进行反思'];
        
        suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            advice.appendChild(li);
        });
        
        // 如果有优势分析，添加到报告
        if (reportData.wai_assessment?.strengths) {
            const strengthsSection = document.createElement('div');
            strengthsSection.className = 'report-section';
            strengthsSection.innerHTML = '<h4>咨询优势</h4><ul id="report-strengths"></ul>';
            
            const strengthsList = strengthsSection.querySelector('#report-strengths');
            reportData.wai_assessment.strengths.forEach(strength => {
                const li = document.createElement('li');
                li.textContent = strength;
                strengthsList.appendChild(li);
            });
            
            // 插入到专业建议之后
            advice.parentNode.insertBefore(strengthsSection, advice.nextSibling);
        }
        
        // 显示弹窗
        modal.style.display = 'block';
    }

    // 修改现有的事件监听器，使用新的WAI评估
    (function ensureEndButton() {
        const headerButtons = document.querySelector('.header-buttons');
        if (!headerButtons) return;
        
        if (!document.getElementById('end-session-btn')) {
            const btn = document.createElement('button');
            btn.id = 'end-session-btn';
            btn.className = 'btn btn-primary';
            btn.innerHTML = '<span style="margin-right: 5px;">📋</span>结束并生成WAI评估';
            btn.style.marginLeft = '8px';
            headerButtons.appendChild(btn);

            btn.addEventListener('click', async () => {
                if (!confirm('确定结束当前会话并生成WAI评估报告吗？')) return;
                await endSessionWithWAI();
            });
        }
    })();

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

