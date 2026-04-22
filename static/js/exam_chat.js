document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const loadingTemplate = document.getElementById('loading-template');
    const timerElement = document.getElementById('timer-value');
    const turnCounterElement = document.getElementById('turn-value');
    const emergencyEndBtn = document.getElementById('emergency-end-btn');

    let examTimer;
    let remainingTime = 50 * 60; // 50分钟，单位秒
    let currentTurns = 0;
    const maxTurns = 40;

    // 初始化考试计时器
    function initExamTimer() {
        updateTimerDisplay();
        examTimer = setInterval(() => {
            remainingTime--;
            updateTimerDisplay();
            
            if (remainingTime <= 0) {
                endExam('timeout');
            }
        }, 1000);
    }

    // 更新计时器显示
    function updateTimerDisplay() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;
        timerElement.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        // 最后5分钟变红色
        if (remainingTime <= 5 * 60) {
            timerElement.style.color = '#ff6b6b';
        }
    }

    // 更新轮次计数
    function updateTurnCounter() {
        currentTurns++;
        turnCounterElement.textContent = `${currentTurns}/${maxTurns}`;
        
        // 接近上限时变黄色
        if (currentTurns >= maxTurns - 5) {
            turnCounterElement.style.color = '#ffa726';
        }
        
        if (currentTurns >= maxTurns) {
            endExam('turn_limit');
        }
    }

    // 结束考试
    function endExam(reason) {
        clearInterval(examTimer);
        sendBtn.disabled = true;
        userInput.disabled = true;
        userInput.placeholder = '考试已结束';
        
        // 生成考试报告
        generateExamReport(reason).then(report => {
            showExamReportModal(report);
        }).catch(error => {
            console.error('生成考试报告失败:', error);
            showExamReportModal(generateFallbackReport(reason));
        });
    }

    async function generateExamReport(endReason) {
        try {
            const payload = {
                mode: 'exam',
                meta: {
                    end_reason: endReason,
                    total_turns: currentTurns,
                    time_used: 50 * 60 - remainingTime
                }
            };

            const response = await fetch('/api/wai-feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error('生成考试反馈失败');
            }

            const data = await response.json();

            // 如果模型返回了 wai_scores 等规范字段，用它构建 report
            if (data.wai_scores) {
                const report = {
                    end_reason: endReason === 'timeout' ? '时间耗尽' : (endReason === 'manual' ? '手动结束' : endReason),
                    total_turns: currentTurns,
                    time_used: 50 * 60 - remainingTime,
                    skills_assessment: [
                        // 用 item_comments 或 suggestions 构造更可读的能力评估
                        data.item_comments ? `Bond: ${data.item_comments.bond || ''}` : '未能生成能力评估'
                    ],
                    improvement_suggestions: data.suggestions || [],
                    wai_feedback: data
                };
                return report;
            } else {
                // fallback: 如果没有结构化数据，回退到现有的generateFallbackReport
                return generateFallbackReport(endReason);
            }
        } catch (error) {
            console.error('生成考试报告失败:', error);
            throw error;
        }
    }


    // 备用报告生成
    function generateFallbackReport(endReason) {
        const reasonText = endReason === 'timeout' ? '时间耗尽' : '达到最大轮次';
        return {
            end_reason: reasonText,
            total_turns: currentTurns,
            time_used: 50 * 60 - remainingTime,
            skills_assessment: [
                '共情能力：需要更多练习',
                '问题引导：基本掌握',
                '伦理规范：符合要求'
            ],
            improvement_suggestions: [
                '建议增加开放式问题的使用',
                '注意对话节奏的控制',
                '加强情感回应技巧'
            ]
        };
    }

    // 显示考试报告弹窗
    function showExamReportModal(reportData) {
        const modal = document.getElementById('exam-report-modal');
        const basicInfo = document.getElementById('exam-basic-info');
        const skillsAssessment = document.getElementById('exam-skills-assessment');
        const improvementSuggestions = document.getElementById('exam-improvement-suggestions');

        // 填充基本信息
        basicInfo.innerHTML = `
            <p><strong>结束原因:</strong> ${reportData.end_reason}</p>
            <p><strong>完成轮次:</strong> ${reportData.total_turns} 轮</p>
            <p><strong>用时:</strong> ${Math.floor(reportData.time_used / 60)} 分钟</p>
        `;

        // 填充能力评估
        skillsAssessment.innerHTML = '';
        reportData.skills_assessment.forEach(skill => {
            const li = document.createElement('li');
            li.textContent = skill;
            skillsAssessment.appendChild(li);
        });

        // 填充改进建议
        improvementSuggestions.innerHTML = '';
        reportData.improvement_suggestions.forEach(suggestion => {
            const li = document.createElement('li');
            li.textContent = suggestion;
            improvementSuggestions.appendChild(li);
        });

        modal.style.display = 'block';
    }

    // 共用函数（从chat.js复制）
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

    function showLoadingIndicator() {
        const loadingNode = document.importNode(loadingTemplate.content, true);
        const loadingElement = loadingNode.querySelector('.message');
        chatBox.appendChild(loadingElement);
        chatBox.scrollTop = chatBox.scrollHeight;
        return loadingElement;
    }

    function hideLoadingIndicator(loadingElement) {
        if (loadingElement && loadingElement.parentNode) {
            loadingElement.remove();
        }
    }

    // 发送消息函数
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        console.log('开始发送消息:', message); // 调试信息

        // 更新轮次计数
        updateTurnCounter();
        
        // 添加用户消息
        addMessage('user', message);
        userInput.value = '';
        sendBtn.disabled = true;
        
        // 显示加载指示器
        const loadingElement = showLoadingIndicator();
        
        try {
            console.log('发送API请求...'); // 调试信息
            
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Session-Check': 'true'
                },
                body: JSON.stringify({ 
                    message: message,
                    client_id: document.querySelector('.chat-header h2').textContent.split(' ')[0]
                })
            });
            
            console.log('响应状态:', response.status); // 调试信息
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('API错误响应:', errorText); // 调试信息
                throw new Error(`请求失败: ${response.status} ${errorText}`);
            }
            
            const data = await response.json();
            console.log('成功收到响应:', data); // 调试信息
            
            hideLoadingIndicator(loadingElement);
            addMessage('ai', data.response);
            
        } catch (error) {
            console.error('发送消息错误详情:', error); // 调试信息
            hideLoadingIndicator(loadingElement);
            showToast('发送失败: ' + error.message, 'error');
        } finally {
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    // Toast通知函数
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

    // 事件监听
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

    emergencyEndBtn.addEventListener('click', () => {
        if (confirm('确定要提前结束考试吗？这将立即生成评估报告。')) {
            endExam('manual');
        }
    });

    // 弹窗关闭事件
    const modal = document.getElementById('exam-report-modal');
    const closeReportBtn = document.getElementById('close-exam-report-btn');
    const exportReportBtn = document.getElementById('export-exam-report-btn');

    closeReportBtn.addEventListener('click', () => {
        modal.style.display = 'none';
        window.location.href = '/exam';
    });

    exportReportBtn.addEventListener('click', () => {
        // 导出报告功能
        showToast('考试报告导出功能开发中', 'info');
    });

    // 初始化
    initExamTimer();
    userInput.focus();
});