// 🦞 OpenClaw 像素办公室 - 交互逻辑

// 初始化
document.addEventListener('DOMContentLoaded', () => {
  initSkills();
  initStatusBoard();
  initScreenDisplay();
  initFileCabinet();
});

// 初始化技能展示
function initSkills() {
  const otherSkillsContainer = document.getElementById('other-skills');
  
  // 渲染其他技能（排除 v2.0 的 4 个）
  const v2Skills = ['travel-planner', 'habit-tracker', 'goal-manager', 'expense-tracker'];
  
  Object.entries(SKILLS).forEach(([key, skill]) => {
    if (!v2Skills.includes(key)) {
      const skillEl = createSkillElement(key, skill);
      otherSkillsContainer.appendChild(skillEl);
    }
  });
  
  // 为 v2.0 技能添加点击事件
  document.querySelectorAll('.skill-shelf.v2 .skill-item').forEach(item => {
    item.addEventListener('click', () => {
      const skillKey = item.dataset.skill;
      if (SKILLS[skillKey]) {
        openModal(skillKey, SKILLS[skillKey]);
      }
    });
  });
}

// 创建技能元素
function createSkillElement(key, skill) {
  const div = document.createElement('div');
  div.className = 'skill-item';
  div.dataset.skill = key;
  
  div.innerHTML = `
    <div class="skill-icon">${skill.icon}</div>
    <div class="skill-name">${skill.name}</div>
    <div class="skill-version ${skill.version === 'v2.0' ? 'v2' : ''}">${skill.version}</div>
  `;
  
  div.addEventListener('click', () => openModal(key, skill));
  
  return div;
}

// 初始化状态看板
function initStatusBoard() {
  // 模拟数据更新
  updateStatusBoard();
  
  // 每 5 秒更新一次（模拟实时数据）
  setInterval(updateStatusBoard, 5000);
}

function updateStatusBoard() {
  // 从本地存储读取真实数据（如果有）
  const checkins = localStorage.getItem('todayCheckins') || MOCK_DATA.todayCheckins;
  const goalProgress = localStorage.getItem('goalProgress') || MOCK_DATA.goalProgress;
  const monthExpense = localStorage.getItem('monthExpense') || MOCK_DATA.monthExpense;
  
  // 动画更新
  animateValue('today-checkins', 0, parseInt(checkins), 1000);
  animateValue('goal-percent', 0, parseInt(goalProgress), 1000, '%');
  animateValue('month-expense', 0, parseInt(monthExpense), 1000, '', '¥');
  
  // 更新进度条
  document.getElementById('goal-progress').style.width = goalProgress + '%';
  
  // 更新技能总数
  document.getElementById('total-skills').textContent = MOCK_DATA.totalSkills;
}

// 数值动画
function animateValue(id, start, end, duration, suffix = '', prefix = '') {
  const obj = document.getElementById(id);
  const range = end - start;
  const startTime = performance.now();
  
  function update(currentTime) {
    const elapsed = currentTime - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // 缓动函数
    const easeOut = 1 - Math.pow(1 - progress, 3);
    const current = Math.floor(start + range * easeOut);
    
    obj.textContent = prefix + current + suffix;
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}

// 初始化屏幕显示
function initScreenDisplay() {
  const screen = document.getElementById('screen-display');
  const messages = [
    "🦞 像素龙虾工作中...",
    "📊 加载技能数据...",
    "✨ v2.0 技能已优化",
    "🎯 今天也要加油哦!",
    "💡 点击技能查看详情"
  ];
  
  let index = 0;
  
  setInterval(() => {
    screen.innerHTML = `<span class="typing">${messages[index]}</span><span class="blink">_</span>`;
    index = (index + 1) % messages.length;
  }, 3000);
}

// 初始化文件柜
function initFileCabinet() {
  document.querySelectorAll('.cabinet-drawer').forEach(drawer => {
    drawer.addEventListener('click', () => {
      const category = drawer.dataset.category;
      filterSkillsByCategory(category);
    });
  });
}

// 按分类过滤技能
function filterSkillsByCategory(category) {
  const categoryMap = {
    'life': '生活',
    'work': '工作',
    'learn': '学习',
    'health': '健康'
  };
  
  const categoryName = categoryMap[category];
  const skillKeys = CATEGORIES[categoryName] || [];
  
  // 创建临时展示
  const modalContent = {
    name: `${categoryName}技能`,
    icon: drawerIconMap[category],
    version: '',
    description: `共 ${skillKeys.length} 个技能`,
    features: skillKeys.map(key => {
      const skill = SKILLS[key];
      return skill ? `${skill.icon} ${skill.name} (${skill.version})` : key;
    })
  };
  
  openModal('category-' + category, {
    name: `${categoryName}技能`,
    icon: drawerIconMap[category],
    version: '',
    description: `共 ${skillKeys.length} 个技能`,
    features: skillKeys.map(key => {
      const skill = SKILLS[key];
      return skill ? `${skill.icon} ${skill.name} (${skill.version}) - ${skill.description}` : key;
    })
  });
}

const drawerIconMap = {
  'life': '🗂️',
  'work': '💼',
  'learn': '📖',
  'health': '💪'
};

// 打开详情弹窗
function openModal(key, skill) {
  const modal = document.getElementById('skill-modal');
  
  document.getElementById('modal-icon').textContent = skill.icon;
  document.getElementById('modal-title').textContent = skill.name;
  document.getElementById('modal-version').textContent = skill.version;
  document.getElementById('modal-version').style.display = skill.version ? 'inline-block' : 'none';
  
  // 生成详情内容
  let bodyHtml = `
    <p><strong>📝 描述:</strong> ${skill.description}</p>
    <p><strong>💾 代码量:</strong> ${skill.codeSize || '未知'}</p>
    <p><strong>📂 分类:</strong> ${skill.category || '未分类'}</p>
  `;
  
  if (skill.features && skill.features.length > 0) {
    bodyHtml += `
      <p><strong>✨ 功能特性:</strong></p>
      <ul>
        ${skill.features.map(f => `<li>${f}</li>`).join('')}
      </ul>
    `;
  }
  
  if (skill.commands && skill.commands.length > 0) {
    bodyHtml += `
      <p><strong>💬 使用示例:</strong></p>
      <ul>
        ${skill.commands.map(c => `<li>"${c}"</li>`).join('')}
      </ul>
    `;
  }
  
  document.getElementById('modal-body').innerHTML = bodyHtml;
  
  modal.classList.add('active');
}

// 关闭弹窗
function closeModal() {
  document.getElementById('skill-modal').classList.remove('active');
}

// 点击弹窗外部关闭
document.getElementById('skill-modal')?.addEventListener('click', (e) => {
  if (e.target.id === 'skill-modal') {
    closeModal();
  }
});

// 键盘 ESC 关闭
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    closeModal();
  }
});

// 龙虾动画增强
function animateLobster() {
  const lobster = document.querySelector('.pixel-lobster');
  if (!lobster) return;
  
  // 随机眨眼
  setInterval(() => {
    lobster.style.transform = 'scaleY(0.9)';
    setTimeout(() => {
      lobster.style.transform = 'scaleY(1)';
    }, 200);
  }, 4000);
}

// 添加键盘快捷键
document.addEventListener('keydown', (e) => {
  // 数字键 1-4 快速查看 v2.0 技能
  const v2Keys = ['travel-planner', 'habit-tracker', 'goal-manager', 'expense-tracker'];
  if (e.key >= '1' && e.key <= '4') {
    const index = parseInt(e.key) - 1;
    const skill = SKILLS[v2Keys[index]];
    if (skill) {
      openModal(v2Keys[index], skill);
    }
  }
  
  // Q 键关闭弹窗
  if (e.key === 'q' || e.key === 'Q') {
    closeModal();
  }
});

// 启动龙虾动画
setTimeout(animateLobster, 1000);

// 控制台彩蛋
console.log(`
🦞 欢迎来到 OpenClaw 像素办公室!

按 1-4 快速查看 v2.0 技能
按 Q 或 ESC 关闭弹窗
点击技能卡片查看详情

技能总数：${MOCK_DATA.totalSkills}
v2.0 优化：4 个

`);
