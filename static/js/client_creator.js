/**
 * 来访者创建表单提交处理
 * 创建成功后自动跳转到训练会话
 */

document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('client-form');
    
    if (!form) return;

    // 显示Toast通知
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

    // 表单提交处理
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const submitBtn = form.querySelector('button[type="submit"]');
        const originalBtnText = submitBtn.textContent;
        
        try {
            // Disable submit button to prevent duplicate submissions
            submitBtn.disabled = true;
            submitBtn.textContent = 'Creating...';
            
            // Collect form data
            const formData = new FormData(form);
            const data = {
                name: formData.get('name'),
                age: parseInt(formData.get('age')),
                gender: formData.get('gender'),
                main_issue: formData.get('main_issue'),
                background: formData.get('background'),
                style: formData.get('style'),
                initial_stage: formData.get('initial_stage')|| 'defensive' 
            };

            // Validate required fields
            if (!data.name || !data.main_issue || !data.background) {
                throw new Error('Please fill in all required fields');
            }

            // Send creation request
            const response = await fetch('/create-client', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || 'Creation failed, please try again later');
            }

            // Display success notification
            if (result.success) {
                showToast('Client created successfully!', 'success');
                setTimeout(() => {
                    window.location.href = `/start-session/${result.client_id}`;
                }, 1000);
            } else {
                showToast('Creation failed: ' + (result.error || 'Unknown error'), 'error');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Create and Start Training';
            }

        } catch (error) {
            console.error('Error creating visitor:', error);
            showToast(error.message, 'error');
            
            // Re-enable submit button
            submitBtn.disabled = false;
            submitBtn.textContent = originalBtnText;
        }
    });

    // Add validation status to all input fields
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', () => {
            if (input.checkValidity()) {
                input.classList.remove('invalid');
            } else {
                input.classList.add('invalid');
            }
        });
    });
});

// 添加全局样式
const style = document.createElement('style');
style.textContent = `
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
    
    .toast.success {
        background:rgb(156, 200, 254);
    }
    
    .toast.error {
        background:rgb(210, 162, 248);
    }
    
    .toast.info {
        background:rgb(199, 228, 255);
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
    
    .invalid {
        border-color:rgb(189, 197, 255) !important;
    }
`;
document.head.appendChild(style);