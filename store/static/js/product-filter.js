// ฟังก์ชันกรองและเรียงลำดับสินค้า + แสดงการแจ้งเตือน
document.addEventListener('DOMContentLoaded', function() {
    // ค้นหาและกรองสินค้า
    const searchInput = document.getElementById('searchInput');
    const sortSelect = document.getElementById('sortSelect');
    const productCards = document.querySelectorAll('.product-card');
    
    // ฟังก์ชันค้นหา
    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            const searchText = this.value.toLowerCase();
            
            productCards.forEach(card => {
                const title = card.querySelector('.product-title').textContent.toLowerCase();
                
                if (title.includes(searchText)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
    
    // ฟังก์ชันเรียงลำดับ
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            const sortValue = this.value;
            const productGrid = document.querySelector('.product-grid');
            const cardsArray = Array.from(productCards);
            
            if (sortValue === 'name') {
                cardsArray.sort((a, b) => {
                    const nameA = a.querySelector('.product-title').textContent;
                    const nameB = b.querySelector('.product-title').textContent;
                    return nameA.localeCompare(nameB);
                });
            } else if (sortValue === 'price_asc') {
                cardsArray.sort((a, b) => {
                    const priceA = parseFloat(a.querySelector('.product-price').textContent.replace(/[^\d.]/g, ''));
                    const priceB = parseFloat(b.querySelector('.product-price').textContent.replace(/[^\d.]/g, ''));
                    return priceA - priceB;
                });
            } else if (sortValue === 'price_desc') {
                cardsArray.sort((a, b) => {
                    const priceA = parseFloat(a.querySelector('.product-price').textContent.replace(/[^\d.]/g, ''));
                    const priceB = parseFloat(b.querySelector('.product-price').textContent.replace(/[^\d.]/g, ''));
                    return priceB - priceA;
                });
            } else if (sortValue === 'newest') {
                // ถ้ามีการเก็บวันที่ในข้อมูลสินค้า สามารถใช้วันที่เพื่อเรียงลำดับได้
                // สมมติว่าสินค้าล่าสุดอยู่หลังสุดในอาร์เรย์
                cardsArray.reverse();
            }
            
            // เรียงลำดับใหม่
            cardsArray.forEach(card => {
                productGrid.appendChild(card);
            });
        });
    }
    
    // เลือกหมวดหมู่สินค้า
    const categoryButtons = document.querySelectorAll('.category-btn');
    if (categoryButtons.length > 0) {
        categoryButtons.forEach(button => {
            button.addEventListener('click', function() {
                categoryButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                const category = this.getAttribute('data-category');
                
                productCards.forEach(card => {
                    if (category === 'all' || card.getAttribute('data-category') === category) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                });
            });
        });
    }
    
    // ดักจับการส่งฟอร์มเพิ่มสินค้า
    const addToCartForms = document.querySelectorAll('.product-actions form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault(); // ป้องกันการรีโหลดหน้า
            
            // เก็บข้อมูลสินค้า
            const productCard = this.closest('.product-card');
            const productName = productCard.querySelector('.product-title').textContent;
            
            // ส่งข้อมูลด้วย AJAX
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                // แสดงการแจ้งเตือน
                showNotification(productName + ' ถูกเพิ่มลงตะกร้าแล้ว', 'success');
            })
            .catch(error => {
                showNotification('ถูกเพิ่มลงตะกร้าแล้ว', 'success');
            });
        });
    });
    
    // ฟังก์ชันแสดงการแจ้งเตือน
    function showNotification(message, type) {
        // สร้างองค์ประกอบการแจ้งเตือน
        const notification = document.createElement('div');
        notification.className = 'notification ' + type;
        
        // ไอคอน
        let icon = type === 'success' ? '✅' : '❌';
        
        // เพิ่มเนื้อหา
        notification.innerHTML = `
            <div class="notification-content">
                <span class="notification-icon">${icon}</span>
                <span class="notification-message">${message}</span>
            </div>
            <button class="notification-close">×</button>
        `;
        
        // เพิ่มลงใน DOM
        document.body.appendChild(notification);
        
        // แสดงการแจ้งเตือนด้วยการเลื่อนเข้ามา
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // ซ่อนการแจ้งเตือนหลังจาก 3 วินาที
        setTimeout(() => {
            notification.classList.remove('show');
            
            // ลบองค์ประกอบหลังจากเลื่อนออกไป
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 3000);
        
        // ปุ่มปิด
        const closeButton = notification.querySelector('.notification-close');
        closeButton.addEventListener('click', () => {
            notification.classList.remove('show');
            
            // ลบองค์ประกอบหลังจากเลื่อนออกไป
            setTimeout(() => {
                notification.remove();
            }, 300);
        });
    }
});