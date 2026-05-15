// ====================================
// FINANCEPRO - MAIN JAVASCRIPT
// ====================================

// Configuração da API
const API_URL = "https://financepro-api.onrender.com/api";

// ====================================
// HELPERS
// ====================================

// Função para formatar moeda
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Função para formatar data
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR').format(date);
}

// Função para obter token
function getToken() {
    return localStorage.getItem('token');
}

// Função para obter usuário
function getUser() {
    const user = localStorage.getItem('user');
    return user ? JSON.parse(user) : null;
}

// Função para verificar autenticação
function checkAuth() {
    const token = getToken();
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Função para fazer logout
function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    window.location.href = 'login.html';
}

// ====================================
// TOAST NOTIFICATIONS
// ====================================

function showToast(type, title, message) {
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icons = {
        success: '✅',
        error: '❌',
        warning: '⚠️',
        info: 'ℹ️'
    };
    
    toast.innerHTML = `
        <div class="toast-icon">${icons[type] || icons.info}</div>
        <div class="toast-content">
            <div class="toast-title">${title}</div>
            <div class="toast-message">${message}</div>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Remover após 5 segundos
    setTimeout(() => {
        toast.style.animation = 'slideInRight 0.3s reverse';
        setTimeout(() => toast.remove(), 300);
    }, 5000);
}

// ====================================
// API REQUESTS
// ====================================

async function apiRequest(endpoint, options = {}) {
    const token = getToken();
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };
    
    try {
        const response = await fetch(`${API_URL}${endpoint}`, {
            ...defaultOptions,
            ...options,
            headers: {
                ...defaultOptions.headers,
                ...options.headers
            }
        });
        
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Erro na requisição');
        }
        
        return data;
    } catch (error) {
        console.error('Erro na API:', error);
        throw error;
    }
}

// ====================================
// LOADING
// ====================================

function showLoading() {
    const loading = document.getElementById('loadingScreen');
    if (loading) {
        loading.classList.remove('hidden');
    }
}

function hideLoading() {
    const loading = document.getElementById('loadingScreen');
    if (loading) {
        loading.classList.add('hidden');
    }
}

// Esconder loading ao carregar página
window.addEventListener('load', () => {
    setTimeout(hideLoading, 1000);
});

// ====================================
// SIDEBAR TOGGLE (Mobile)
// ====================================

function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('open');
    }
}

// ====================================
// MODAL
// ====================================

function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Fechar modal ao clicar fora
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal-overlay')) {
        e.target.classList.add('hidden');
    }
});

// ====================================
// TRANSACTIONS
// ====================================

async function loadTransactions() {
    try {
        const data = await apiRequest('/transactions');
        return data;
    } catch (error) {
        showToast('error', 'Erro', 'Erro ao carregar transações');
        return [];
    }
}

async function createTransaction(transaction) {
    try {
        const data = await apiRequest('/transactions', {
            method: 'POST',
            body: JSON.stringify(transaction)
        });
        showToast('success', 'Sucesso', 'Transação criada com sucesso');
        return data;
    } catch (error) {
        showToast('error', 'Erro', error.message);
        throw error;
    }
}

async function updateTransaction(id, transaction) {
    try {
        const data = await apiRequest(`/transactions/${id}`, {
            method: 'PUT',
            body: JSON.stringify(transaction)
        });
        showToast('success', 'Sucesso', 'Transação atualizada');
        return data;
    } catch (error) {
        showToast('error', 'Erro', error.message);
        throw error;
    }
}

async function deleteTransaction(id) {
    try {
        const data = await apiRequest(`/transactions/${id}`, {
            method: 'DELETE'
        });
        showToast('success', 'Sucesso', 'Transação excluída');
        return data;
    } catch (error) {
        showToast('error', 'Erro', error.message);
        throw error;
    }
}

// ====================================
// CATEGORIES
// ====================================

async function loadCategories(type = null) {
    try {
        const endpoint = type ? `/categories?type=${type}` : '/categories';
        const data = await apiRequest(endpoint);
        return data;
    } catch (error) {
        showToast('error', 'Erro', 'Erro ao carregar categorias');
        return [];
    }
}

// ====================================
// GOALS
// ====================================

async function loadGoals() {
    try {
        const data = await apiRequest('/goals');
        return data;
    } catch (error) {
        showToast('error', 'Erro', 'Erro ao carregar metas');
        return [];
    }
}

async function createGoal(goal) {
    try {
        const data = await apiRequest('/goals', {
            method: 'POST',
            body: JSON.stringify(goal)
        });
        showToast('success', 'Sucesso', 'Meta criada com sucesso');
        return data;
    } catch (error) {
        showToast('error', 'Erro', error.message);
        throw error;
    }
}

async function updateGoal(id, goal) {
    try {
        const data = await apiRequest(`/goals/${id}`, {
            method: 'PUT',
            body: JSON.stringify(goal)
        });
        showToast('success', 'Sucesso', 'Meta atualizada');
        return data;
    } catch (error) {
        showToast('error', 'Erro', error.message);
        throw error;
    }
}

async function deleteGoal(id) {
    try {
        const data = await apiRequest(`/goals/${id}`, {
            method: 'DELETE'
        });
        showToast('success', 'Sucesso', 'Meta excluída');
        return data;
    } catch (error) {
        showToast('error', 'Erro', error.message);
        throw error;
    }
}

// ====================================
// SUMMARY
// ====================================

async function loadSummary() {
    try {
        const data = await apiRequest('/transactions/summary');
        return data;
    } catch (error) {
        showToast('error', 'Erro', 'Erro ao carregar resumo');
        return null;
    }
}

async function loadMonthlySummary(year, month) {
    try {
        const data = await apiRequest(`/transactions/monthly?year=${year}&month=${month}`);
        return data;
    } catch (error) {
        showToast('error', 'Erro', 'Erro ao carregar resumo mensal');
        return [];
    }
}

async function loadByCategory() {
    try {
        const data = await apiRequest('/transactions/by-category');
        return data;
    } catch (error) {
        showToast('error', 'Erro', 'Erro ao carregar gastos por categoria');
        return [];
    }
}

async function loadRecentTransactions(limit = 5) {
    try {
        const data = await apiRequest(`/transactions/recent?limit=${limit}`);
        return data;
    } catch (error) {
        showToast('error', 'Erro', 'Erro ao carregar transações recentes');
        return [];
    }
}

// ====================================
// PROFILE
// ====================================

async function updateProfile(name, email) {
    try {
        const data = await apiRequest('/profile', {
            method: 'PUT',
            body: JSON.stringify({ name, email })
        });
        showToast('success', 'Sucesso', 'Perfil atualizado');
        
        // Atualizar dados no localStorage
        const user = getUser();
        user.name = name;
        user.email = email;
        localStorage.setItem('user', JSON.stringify(user));
        
        return data;
    } catch (error) {
        showToast('error', 'Erro', error.message);
        throw error;
    }
}

// ====================================
// CHARTS
// ====================================

// Função para criar gráfico de pizza (usando canvas)
function createPieChart(canvasId, data) {
    const canvas = document.getElementById(canvasId);
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;
    const radius = Math.min(centerX, centerY) - 20;
    
    let total = data.reduce((sum, item) => sum + item.value, 0);
    let currentAngle = -Math.PI / 2;
    
    // Limpar canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Desenhar fatias
    data.forEach((item, index) => {
        const sliceAngle = (item.value / total) * 2 * Math.PI;
        
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, currentAngle, currentAngle + sliceAngle);
        ctx.lineTo(centerX, centerY);
        ctx.fillStyle = item.color;
        ctx.fill();
        
        currentAngle += sliceAngle;
    });
    
    // Desenhar centro branco (donut)
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius * 0.6, 0, 2 * Math.PI);
    ctx.fillStyle = '#1C1F26';
    ctx.fill();
}

// ====================================
// UTILITY FUNCTIONS
// ====================================

// Debounce para search
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Copiar para clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showToast('success', 'Copiado', 'Texto copiado para a área de transferência');
    });
}

// ====================================
// EXPORT
// ====================================

// Exportar para CSV
function exportToCSV(data, filename) {
    const csv = data.map(row => Object.values(row).join(',')).join('\n');
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
    window.URL.revokeObjectURL(url);
}

// ====================================
// INIT
// ====================================

console.log('🚀 FinancePro carregado com sucesso!');