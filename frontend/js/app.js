const API_BASE = "http://127.0.0.1:8000/api";
let productsData = [];

function toggleAuthView(view) {
    if (view === 'signup') {
        document.getElementById('signin-card').classList.add('hidden');
        document.getElementById('signup-card').classList.remove('hidden');
    } else {
        document.getElementById('signup-card').classList.add('hidden');
        document.getElementById('signin-card').classList.remove('hidden');
    }
}

function handleStandardLogin() {
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const btn = document.querySelector('.btn-login-dark');
    const errorMsg = document.getElementById('login-error');

    errorMsg.classList.add('hidden');

    if (!email || !password) {
        errorMsg.innerText = "Please enter both email and password.";
        errorMsg.classList.remove('hidden');
        return;
    }

    btn.innerText = "Authenticating...";
    btn.style.opacity = "0.7";
    btn.disabled = true;

    setTimeout(async () => {
        const storedUsers = JSON.parse(localStorage.getItem('procureiq_users')) || [];
        
        const validUser = storedUsers.find(u => u.email === email && u.password === password);

        if (email === "admin@procureiq.com" && password === "admin123") {
            await loginSuccess("System Admin", "fa-user-shield");
        } else if (validUser) {
            await loginSuccess(validUser.name, "fa-user-check");
        } else {
            errorMsg.innerText = "Invalid credentials. Access denied.";
            errorMsg.classList.remove('hidden');
        }

        btn.innerText = "Sign In";
        btn.style.opacity = "1";
        btn.disabled = false;
        document.getElementById('login-password').value = '';
    }, 800);
}

function handleSignUp() {
    const name = document.getElementById('signup-name').value;
    const email = document.getElementById('signup-email').value;
    const password = document.getElementById('signup-password').value;
    const btn = document.getElementById('btn-signup');
    const errorMsg = document.getElementById('signup-error');

    errorMsg.classList.add('hidden');

    if (!name || !email || !password) {
        errorMsg.innerText = "Please fill out all fields.";
        errorMsg.classList.remove('hidden');
        return;
    }

    const storedUsers = JSON.parse(localStorage.getItem('procureiq_users')) || [];
    if (storedUsers.some(u => u.email === email)) {
        errorMsg.innerText = "This email is already registered.";
        errorMsg.classList.remove('hidden');
        return;
    }

    btn.innerText = "Creating Account...";
    btn.style.opacity = "0.7";
    btn.disabled = true;

    setTimeout(async () => {
        storedUsers.push({ name: name, email: email, password: password });
        localStorage.setItem('procureiq_users', JSON.stringify(storedUsers));
        
        await loginSuccess(name, "fa-user-check");

        btn.innerText = "Create Account";
        btn.style.opacity = "1";
        btn.disabled = false;
        document.getElementById('signup-name').value = '';
        document.getElementById('signup-email').value = '';
        document.getElementById('signup-password').value = '';
        toggleAuthView('signin'); 
        
    }, 1000);
}

async function loginSuccess(displayName, iconClass) {
    document.getElementById('login-screen').classList.add('hidden');
    
    const logoutBtn = document.getElementById('logout-btn');
    logoutBtn.classList.remove('hidden');
    logoutBtn.innerHTML = `<i class="fas ${iconClass}" style="margin-right:8px;"></i> ${displayName}`;
    
    document.getElementById('app-content').classList.remove('hidden');
    await fetchAllData();
}

async function handleGoogleLogin(response) {
    const jwtToken = response.credential;
    const userPayload = decodeJwt(jwtToken);
    
    document.getElementById('login-screen').classList.add('hidden');
    
    const logoutBtn = document.getElementById('logout-btn');
    logoutBtn.classList.remove('hidden');
    logoutBtn.innerHTML = `<img src="${userPayload.picture}" style="width:20px; border-radius:50%; margin-right:8px;"> Sign Out`;
    
    document.getElementById('app-content').classList.remove('hidden');
    await fetchAllData();
}

function decodeJwt(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(window.atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    return JSON.parse(jsonPayload);
}

function logout() {
    location.reload(); 
}

async function fetchAllData() {
    try {
        const vendorRes = await fetch(`${API_BASE}/vendors/`);
        const vendors = await vendorRes.json();
        
        const vendorSelect = document.getElementById('vendor-select');
        const vendorTable = document.getElementById('vendors-table-body');
        if (vendorSelect) vendorSelect.innerHTML = '<option value="">-- Choose a Vendor --</option>'; 
        if (vendorTable) vendorTable.innerHTML = '';
        
        vendors.forEach(v => {
            if (vendorSelect) vendorSelect.innerHTML += `<option value="${v.id}">${v.name}</option>`;
            let stars = '⭐'.repeat(v.rating);
            if (vendorTable) vendorTable.innerHTML += `<tr><td><strong>${v.name}</strong></td><td>${v.email}</td><td>${v.contact}</td><td>${stars}</td></tr>`;
        });

        const productRes = await fetch(`${API_BASE}/products/`);
        productsData = await productRes.json(); 
        
        const productTable = document.getElementById('products-table-body');
        if (productTable) productTable.innerHTML = '';
        productsData.forEach(p => {
            if (productTable) productTable.innerHTML += `<tr>
                <td><span class="badge bg-secondary">${p.sku}</span></td>
                <td><strong>${p.name}</strong></td>
                <td>${p.category}</td>
                <td>$${p.current_unit_price.toFixed(2)}</td>
                <td>${p.stock_level} units</td>
            </tr>`;
        });

        const ordersRes = await fetch(`${API_BASE}/orders/`);
        const orders = await ordersRes.json();
        
        const poTable = document.getElementById('po-table-body');
        if (poTable) poTable.innerHTML = '';
        let totalSpend = 0;

        orders.forEach(o => {
            totalSpend += o.grand_total;
            let statusBadge = o.status === 'Draft' ? 'bg-secondary' : 'bg-success';
            if (poTable) poTable.innerHTML += `<tr>
                <td><strong>${o.reference_no}</strong></td>
                <td>${o.vendor.name}</td>
                <td>$${o.grand_total.toFixed(2)}</td>
                <td><span class="badge ${statusBadge}">${o.status}</span></td>
            </tr>`;
        });

        if (document.getElementById('kpi-total-pos')) document.getElementById('kpi-total-pos').innerText = orders.length;
        if (document.getElementById('kpi-total-spend')) document.getElementById('kpi-total-spend').innerText = `$${totalSpend.toFixed(2)}`;

    } catch (error) {
        console.error("Data load error:", error);
    }
}
function toggleView(viewId, element = null) {
    document.getElementById('dashboard-view').classList.add('hidden');
    document.getElementById('create-po-view').classList.add('hidden');
    document.getElementById('vendors-view').classList.add('hidden');
    document.getElementById('products-view').classList.add('hidden');
    
    document.getElementById(viewId).classList.remove('hidden');

    document.querySelectorAll('.nav-link').forEach(link => link.classList.remove('active'));

    if (element) {
        element.classList.add('active');
    } else {
        const targetLink = Array.from(document.querySelectorAll('.nav-link'))
                                .find(link => link.getAttribute('onclick') && link.getAttribute('onclick').includes(viewId));
        if (targetLink) targetLink.classList.add('active');
    }
}

function addTableRow() {
    const tbody = document.getElementById('po-items-body');
    const rowId = Date.now(); 
    
    let productOptions = '<option value="">Select...</option>';
    productsData.forEach(p => {
        productOptions += `<option value="${p.id}" data-price="${p.current_unit_price}" data-name="${p.name}" data-category="${p.category}">${p.name}</option>`;
    });

    const tr = document.createElement('tr');
    tr.id = `row-${rowId}`;
    tr.innerHTML = `
        <td><select class="form-select product-select" onchange="handleProductChange(${rowId})" id="prod-${rowId}">${productOptions}</select></td>
        <td><input type="number" class="form-control price-input" id="price-${rowId}" readonly></td>
        <td><input type="number" class="form-control qty-input" id="qty-${rowId}" value="1" min="1" oninput="calculateTotals()"></td>
        <td class="align-middle fw-bold line-total" id="total-${rowId}">$0.00</td>
        <td>
            <button class="btn btn-ai btn-sm" onclick="triggerAI(${rowId})">✨ Auto-Describe</button>
            <button class="btn btn-sm ms-1" style="background-color: #8A1538; color: white; border: none;" onclick="removeRow(${rowId})">X</button>
        </td>
    `;
    tbody.appendChild(tr);
}

function removeRow(rowId) {
    document.getElementById(`row-${rowId}`).remove();
    calculateTotals();
}

function handleProductChange(rowId) {
    const selectElem = document.getElementById(`prod-${rowId}`);
    const selectedOption = selectElem.options[selectElem.selectedIndex];
    const priceInput = document.getElementById(`price-${rowId}`);
    
    priceInput.value = selectedOption.value ? selectedOption.getAttribute('data-price') : '';
    calculateTotals();
}

function calculateTotals() {
    let subtotal = 0;
    document.querySelectorAll('#po-items-body tr').forEach(row => {
        const rowId = row.id.split('-')[1];
        const price = parseFloat(document.getElementById(`price-${rowId}`).value) || 0;
        const qty = parseInt(document.getElementById(`qty-${rowId}`).value) || 0;
        const lineTotal = price * qty;
        document.getElementById(`total-${rowId}`).innerText = `$${lineTotal.toFixed(2)}`;
        subtotal += lineTotal;
    });

    const tax = subtotal * 0.05; 
    document.getElementById('display-subtotal').innerText = `$${subtotal.toFixed(2)}`;
    document.getElementById('display-tax').innerText = `$${tax.toFixed(2)}`;
    document.getElementById('display-grand-total').innerText = `$${(subtotal + tax).toFixed(2)}`;
}

async function submitPurchaseOrder() {
    const vendorId = document.getElementById('vendor-select').value;
    if (!vendorId) return alert("Please select a vendor.");

    const items = [];
    document.querySelectorAll('#po-items-body tr').forEach(row => {
        const rowId = row.id.split('-')[1];
        const productId = document.getElementById(`prod-${rowId}`).value;
        const qty = document.getElementById(`qty-${rowId}`).value;
        const price = document.getElementById(`price-${rowId}`).value;
        
        if (productId && qty > 0) items.push({ product_id: parseInt(productId), quantity: parseInt(qty), unit_price: parseFloat(price) });
    });

    if (items.length === 0) return alert("Add at least one product.");

    try {
        const res = await fetch(`${API_BASE}/orders/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ vendor_id: parseInt(vendorId), items: items })
        });
        
        if (res.ok) {
            alert("Purchase Order submitted!");
            document.getElementById('po-items-body').innerHTML = ''; 
            calculateTotals(); 
            await fetchAllData();
            toggleView('dashboard-view', document.querySelector('.nav-link'));
        }
    } catch (error) {
        console.error("Error submitting PO:", error);
    }
}

async function triggerAI(rowId) {
    const selectElem = document.getElementById(`prod-${rowId}`);
    const selectedOption = selectElem.options[selectElem.selectedIndex];
    
    if (!selectedOption.value) return alert("Please select a product first.");

    const prodName = selectedOption.getAttribute('data-name');
    const prodCategory = selectedOption.getAttribute('data-category');

    const aiModal = new bootstrap.Modal(document.getElementById('aiModal'));
    document.getElementById('ai-response-text').innerText = "Querying Gemini...";
    aiModal.show();

    try {
        const res = await fetch(`${API_BASE}/ai/generate-description`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: prodName, category: prodCategory })
        });
        
        const data = await res.json();
        document.getElementById('ai-response-text').innerHTML = `<strong>${prodName}:</strong> ${data.description || data.detail}`;
    } catch (error) {
        document.getElementById('ai-response-text').innerText = "Failed to connect to backend.";
    }
}