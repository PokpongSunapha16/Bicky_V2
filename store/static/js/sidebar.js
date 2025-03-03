document.addEventListener('DOMContentLoaded', function() {
    // ปุ่มเปิด/ปิดไซด์บาร์
    const openBtn = document.getElementById('openSettings');
    const closeBtn = document.getElementById('closeSettings');
    const sidebar = document.querySelector('.settings-sidebar');
    const overlay = document.querySelector('.sidebar-overlay');
    
    // เปิดไซด์บาร์
    openBtn.addEventListener('click', function() {
        sidebar.classList.add('active');
        overlay.classList.add('active');
        document.body.style.overflow = 'hidden'; // ป้องกันการเลื่อนพื้นหลัง
    });
    
    // ปิดไซด์บาร์
    function closeSidebar() {
        sidebar.classList.remove('active');
        overlay.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    closeBtn.addEventListener('click', closeSidebar);
    overlay.addEventListener('click', closeSidebar);
});