document.addEventListener('DOMContentLoaded', function() {
    var modal = document.getElementById('menu-modal');
    modal.style.display = 'none'; // 初期表示でモーダルを非表示に設定
});

document.getElementById('menu-toggle').addEventListener('click', function(event) {
    event.stopPropagation(); // メニュー以外のクリックで閉じるためにバブルを止める
    var modal = document.getElementById('menu-modal');
    modal.style.display = 'flex';
});

document.getElementById('close-menu').addEventListener('click', function() {
    var modal = document.getElementById('menu-modal');
    modal.style.display = 'none';
});

// メニュー以外の部分をクリックするとメニューを閉じる
window.addEventListener('click', function(event) {
    var modal = document.getElementById('menu-modal');
    if (modal.style.display === 'flex' && !modal.children[0].contains(event.target)) {
        modal.style.display = 'none';
    }
});

// 検索ボタンをクリックした場合にモーダルを閉じる
document.getElementById('search-form').addEventListener('submit', function() {
    var modal = document.getElementById('menu-modal');
    modal.style.display = 'none';
});