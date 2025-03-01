// ✅ เก็บสินค้าในตะกร้า
let cart = [];
let totalPrice = 0;

// ✅ ฟังก์ชันเพิ่มสินค้าลงตะกร้า
function addToCart(id, name, price) {
    let item = cart.find(p => p.id === id);
    if (item) {
        item.quantity += 1;
    } else {
        cart.push({ id, name, price, quantity: 1 });
    }
    updateCart();
}

// ✅ อัปเดตตะกร้าสินค้า
function updateCart() {
    let cartList = document.getElementById("cart-list");
    cartList.innerHTML = "";
    totalPrice = 0;

    cart.forEach(item => {
        totalPrice += item.price * item.quantity;
        let li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        li.innerHTML = `${item.name} x${item.quantity} <span>฿${item.price * item.quantity}</span>`;
        cartList.appendChild(li);
    });

    document.getElementById("total-price").textContent = totalPrice.toFixed(2);
}

// ✅ ฟังก์ชัน Checkout
function checkout() {
    if (cart.length === 0) {
        alert("🛑 ตะกร้าว่าง!");
        return;
    }
    alert("✅ คำสั่งซื้อสำเร็จ!");
    cart = [];
    updateCart();
}
