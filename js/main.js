// --- 原生JavaScript功能 ---
 
// 功能一：切换夜间模式
// 1. 获取需要操作的元素
const darkModeButton = document.getElementById('toggle-dark-mode');
const bodyElement = document.body;
// 2. 监听按钮的点击事件
darkModeButton.addEventListener('click', function() {
    // 3. 执行切换操作：检查body是否有一个叫'dark-mode'的class
    //    如果有，就移除它；如果没有，就添加它。
    bodyElement.classList.toggle('dark-mode');
});
