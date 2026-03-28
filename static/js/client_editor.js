document.getElementById('edit-client-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = new FormData(e.target);
    const eventNames = formData.getAll('event_name[]');
    const eventContents = formData.getAll('event_content[]');
    
    // 构建关键事件数据
    const key_events = [];
    for (let i = 0; i < eventNames.length; i++) {
        if (eventNames[i] && eventContents[i]) {
            key_events.push({
                事件名称: eventNames[i],
                事件内容: eventContents[i]
            });
        }
    }
    
    const data = {
        name: formData.get('name'),
        age: parseInt(formData.get('age')),
        gender: formData.get('gender'),
        core_beliefs: formData.get('core_beliefs'),
        key_events: key_events
    };
    
    try {
        const clientId = formData.get('client_id');
        const response = await fetch(`/edit-client/${clientId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Save failed');
        }
        
        showToast('Client information updated!', 'success');
        setTimeout(() => {
            window.location.href = '/select-client';
        }, 1500);
    } catch (error) {
        showToast('Save failed: ' + (error.error || 'Unknown error'), 'error');
        console.error('Error:', error);
    }
});

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

// 添加Toast样式
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
`;
document.head.appendChild(style);